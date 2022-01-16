import datetime
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import logging
import sys
import cv2
from flask import Flask, Response
import paho.mqtt.client as mqtt


# Global Variables
text_buffer = ''
status = 'Waiting'
speech_timeout = 5
interval = 300 #[ms]
remaining_time = 0
client = None
position_topic = 'position'
# End of global variables


# Camera Feed
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('rtsp://192.168.0.114:8554/unicast')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        try:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            pass
# End of Camera Feed



# Speech recognition
import speech_recognition as sr
def recognize_speech_from_mic():
    global status, speech_timeout
    recognizer_module = sr.Recognizer()
    microphone_module = sr.Microphone()

    with microphone_module as source:
        status = 'Calibrating'
        recognizer_module.adjust_for_ambient_noise(source)
        status = "Listening"
        audio = recognizer_module.listen(source, phrase_time_limit=speech_timeout)
        status = "Translating"
    
    response = {
        "success": True,
        "error": None,
        "transcription": 'Unable to recognize text'
    }
    try:
        response["transcription"] = recognizer_module.recognize_google(audio, language="pl-PL")
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    status = "Waiting"
    return response['transcription']
# End of Speech Recognition


# Main framework functions
def CreateLogger():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

# Speech to text Tab
def SpeechToText():
    return [
    dcc.Interval(
            id = 'update-timer',
            interval = interval,
            n_intervals = 0
        ),
        
    html.Div([
        html.Button('Clear Text', id='clear_button', style={'display':'inline-block'}),
        html.Button('Start recognition', id='speech_button', style={'display':'inline-block',"margin-left": "2px"}),
        html.P(id='status-text-output', children = ['Status:'], style={'whiteSpace': 'pre-line','display':'inline-block',"margin-left": "5px"}),
        html.B(id='status-output', children = ['Waiting'], style={'whiteSpace': 'pre-line','display':'inline-block',"margin-left": "5px", 'color': 'red'})
        ]),
    html.B( children = ['Speech lenght: '], style={'whiteSpace': 'pre-line','display':'inline-block'}),
    dcc.Slider(
        id = 'time-slider',
        min=5,
        max=60,
        step=5,
        value=5,
        dots = True,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Div([
    html.B(children = ['Remaining time:'], style={'whiteSpace': 'pre-line','display':'inline-block'}),
    html.B(id='timer', children = ['0'], style={'whiteSpace': 'pre-line','display':'inline-block'}),
    html.B(children = ['s'], style={'whiteSpace': 'pre-line','display':'inline-block'})
    ]),
    html.Hr(),
    html.Div(id='text-output', children = [''], style={'whiteSpace': 'pre-line'}),
        ]   
# End of Speech to text Tab


# Video feed Tab
def VideoFeed():
    return[
    html.H1("Connected Webcam Feed and Position"),
    html.Div([
    html.Button('Camera Left', id='camera-button-left', style={'display':'inline-block'}),
    html.Button('Camera Right', id='camera-button-right', style={'display':'inline-block'}),
    ]),
    html.Img(src="/video_feed")
    ]
# End of Video feed Tab



def CreateWebPage():
    global interval
    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Tabs(id="tabs", value='tab_1', children=[
        dcc.Tab(label='Speech to Text', value='tab_1'),
        dcc.Tab(label='Video Feed', value='tab_2'),
        ]),
        html.Div(id='tabs_content'),


        # Hidden divs for handling unnecessary inputs/outputs
        html.Div(id='hidden-div', style={'display':'none'}),
        html.Div(id='hidden-div2', style={'display':'none'}),  
        html.Div(id='hidden-div3', style={'display':'none'}),  
        html.Div(id='hidden-div4', style={'display':'none'}),  
    ])


# CALLBACKS
    @app.callback ( Output('tabs_content', 'children'),
                    Input('tabs', 'value'))
    def render_content(tab):
        # Global graphs data
        if tab == 'tab_1':
            return (SpeechToText())

        elif tab == 'tab_2':
            return (VideoFeed())



    @app.callback(
        Output('hidden-div', 'children'),
        Input('speech_button', 'n_clicks'),
        prevent_initial_call=True
    )
    def update_output(n_clicks):
        if dash.callback_context.triggered[0]['value'] != None:
            global text_buffer, speech_timeout, remaining_time
            if remaining_time == 0:
                remaining_time = int(speech_timeout)
                text = recognize_speech_from_mic()
                text_buffer += f'[{(datetime.datetime.today()).strftime("%H:%M:%S")}]: {text}\n'
            return dash.no_update

    @app.callback(
        Output('hidden-div2', 'children'),
        Input('clear_button', 'n_clicks'),
        prevent_initial_call=True
    )
    def clear_output(n_clicks):
        if dash.callback_context.triggered[0]['value'] != None:
            global text_buffer, client
            text_buffer = ''

    @app.callback(
        Output('text-output', 'children'),
        Output('status-output', 'children'),
        Output('status-output', 'style'),
        Output('timer', 'children'),
        Input('update-timer', 'n_intervals'),
        Input('time-slider', 'value')
    )
    def update_text(n_intervals,value):
        global text_buffer, status, speech_timeout, remaining_time, interval
        color = 'red'
        speech_timeout = value
        if remaining_time > 0 and status == "Listening":
            remaining_time = round(remaining_time - (interval/1000),1)
            color = 'green'
        if remaining_time < 0 or status == "Translating":
            remaining_time = 0
        
        return text_buffer, status, {'color': color}, remaining_time


    @app.server.route('/video_feed')
    def video_feed():
        return Response(gen(VideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


    @app.callback(
        Output('hidden-div3', 'children'),
        Input('camera-button-left', 'n_clicks'),
        prevent_initial_call=True
    )
    def send_position_left(n_clicks):
        if dash.callback_context.triggered[0]['value'] != None:
            global client, position_topic
            client.publish(position_topic, -1, qos=0, retain=False)
            return dash.no_update


    @app.callback(
        Output('hidden-div4', 'children'),
        Input('camera-button-right', 'n_clicks'),
        prevent_initial_call=True
    )
    def send_position_right(n_clicks):
        if dash.callback_context.triggered[0]['value'] != None:
            global client, position_topic
            client.publish(position_topic, 1, qos=0, retain=False)
            return dash.no_update


    return app


# Main Function
###############################################################################################################################
def main():
    global received_flag,received_frame, client

    try:
        CreateLogger()

        broker_address = "192.168.0.123"
        client = mqtt.Client()
        client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")

        client.connect(broker_address, 1881)

        app = CreateWebPage()
        # app.run_server(debug=True,host='0.0.0.0')
        app.run_server(host='0.0.0.0')
        # app.config.suppress_callback_exceptions = True

            
# Manually closing server with exception
###############################################################################################################################
    except KeyboardInterrupt:
        print('Keyboard Interrupt, closing program')
        print('Program ended successfully')
        sys.exit(0)


# EXECUTION
############################
if __name__ == '__main__':
    main()
