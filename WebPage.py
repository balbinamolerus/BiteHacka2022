from code import interact
import datetime
from distutils import text_file
from os import stat
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import plotly
import plotly.graph_objs as go
import logging
import sys
import traceback
import pickle


text_buffer = ''
status = 'Waiting'
speech_timeout = 5
interval = 300 #[ms]
remaining_time = 0

# Speech recognition
import speech_recognition as sr
def recognize_speech_from_mic():
    path = ''

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
        response["transcription"] = recognizer_module.recognize_google(audio)
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

def CreateWebPage():
    global interval
    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Interval(
                id = 'update-timer',
                interval = interval,
                n_intervals = 0
            ),


        html.Div([
            html.Button('Clear Text', id='clear_button', style={'display':'inline-block'}),
            html.Button('Start recognition', id='speech_button', style={'display':'inline-block',"margin-left": "2px"}),
            html.P(id='status-text-output', children = ['Status: '], style={'whiteSpace': 'pre-line','display':'inline-block',"margin-left": "5px"}),
            html.B(id='status-output', children = ['Waiting'], style={'whiteSpace': 'pre-line','display':'inline-block',"margin-left": "5px"})
            ]),
        html.B( children = ['Speech lenght: '], style={'whiteSpace': 'pre-line','display':'inline-block'}),
        dcc.Slider(
            id = 'time-slider',
            min=5,
            max=60,
            step=5,
            value=5,
            dots = True,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Div([
        html.B(id='timer', children = ['0'], style={'whiteSpace': 'pre-line','display':'inline-block'}),
        html.B(children = ['s'], style={'whiteSpace': 'pre-line','display':'inline-block'})
        ]),
        html.Hr(),
        html.Div(id='text-output', children = [''], style={'whiteSpace': 'pre-line'}),

        # Hidden divs for handling unnecessary inputs/outputs
        html.Div(id='hidden-div', style={'display':'none'}),
        html.Div(id='hidden-div2', style={'display':'none'}),  
        
    ])


# CALLBACKS

    @app.callback(
        Output('hidden-div', 'children'),
        Input('speech_button', 'n_clicks'),
        prevent_initial_call=True
    )
    def update_output(n_clicks):
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
        global text_buffer
        text_buffer = ''
        return dash.no_update

    @app.callback(
        Output('text-output', 'children'),
        Output('status-output', 'children'),
        Output('timer', 'children'),
        Input('update-timer', 'n_intervals'),
        Input('time-slider', 'value')
    )
    def update_text(n_intervals,value):
        global text_buffer, status, speech_timeout, remaining_time, interval
        speech_timeout = value
        if remaining_time > 0 and status == "Listening":
            remaining_time = round(remaining_time - (interval/1000),1)
        if remaining_time < 0 or status == "Translating":
            remaining_time = 0
        return text_buffer, status, remaining_time

    return app

# Main Function
###############################################################################################################################

def main():
    global received_flag,received_frame

    try:
        CreateLogger()

        app = CreateWebPage()
        app.run_server(debug=True,host='0.0.0.0')
        # app.run_server(host='0.0.0.0')
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
