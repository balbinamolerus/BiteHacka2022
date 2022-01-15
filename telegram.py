import time
import telepot
from telepot.loop import MessageLoop


available_spaces = {
    '10': '9A',
    '24': '9A',
    '65': '9B',
    '38': '9B',
    '48': '9B',
    '35': '9B',
    '42': '9B',
    '50': '9B',
    '69': '9B',
    '68': '9B',
    '14': '9C',
    '19': '9C',
    '20': '9C',
    '15': '9C',
    '08': '9C'
}
bot = telepot.Bot('1865773870:AAET2CqaAeUoe_gdTlfyZco887fcskxBdCk')
permissions = [1255224844, ]
sendLast = False
sendLastTo = 0


def msg_me(bot, message):
    bot.sendMessage(1255224844, message)


def msg_all(bot, message):
    global permissions
    for ID in permissions:
        bot.sendMessage(ID, message)
    # bot.sendMessage(1255224844, message)


def handle(msg):
    global serviceAllowed, permissions, systemStart, sendLast, sendLastTo

    if msg['from']['id'] in permissions:
        if '/ping' in msg['text']:
            bot.sendMessage(msg['from']['id'], 'Pong!')
            sendLast = True
            sendLastTo = msg['from']['id']
        elif '/add' in msg['text'] and len(msg['text']) > 5:
            try:
                toadd = int(msg['text'].replace('/add ', ''))
                permissions.append(toadd)
                bot.sendMessage(msg['from']['id'], 'User added!')
            except:
                bot.sendMessage(msg['from']['id'], 'Unknown error while adding user!')
        else:
            msg_all(bot,
                    'Wrong message! If want to respond to last email, type:\nSPACE,BUILDING   (example: 05,9A)\nnone  <- for custom without space&building')
    else:
        bot.sendMessage(msg['from']['id'],
                        'No permisions! Ask admin to add your ID.\nYour ID:\n' + str(msg['from']['id']))


def check_building(messagetocheck, building, textspace):
    lastBuilding = ''
    goodToGo = False
    for i in range(len(messagetocheck)):
        if messagetocheck.startswith('9A', i):
            lastBuilding = '9A'
        if messagetocheck.startswith('9B', i):
            lastBuilding = '9B'
        if messagetocheck.startswith('9C', i):
            lastBuilding = '9C'
        if messagetocheck.startswith('7A', i):
            lastBuilding = '7A'
        if messagetocheck.startswith(textspace, i) and lastBuilding == building:
            goodToGo = True
    return goodToGo


print("done")
MessageLoop(bot, handle).run_as_thread()
# msgs = service_gmail.users().messages().list(userId='me', q=Q).execute()
# last_message_id = msgs['messages'][0]['id']
# serviceAllowed = True
# systemStart = True
msg_all(bot, 'Service starting after system restart!\n To get last message payload type: /last')

while True:
    time.sleep(1)
    # if systemStart:
    #     time.sleep(1)
    #     try:
    #         msgs = service_gmail.users().messages().list(userId='me', q=Q).execute()
    #         if msgs['messages'][0]['id'] != last_message_id:
    #             msg_all(bot, 'WARNING! MESSAGE FROM ATAL FOUND!\nProceeding with autoresponse!')
    #             emailMsg = ''
    #             thread_id = msgs['messages'][0]['id']
    #             message = service_gmail.users().messages().get(userId='me', id=thread_id, format='raw').execute()
    #             message_decode_raw, subject, to, message_id, payload = message_decode(message)
    #             # if len(payload) < 1500:
    #             #     print(len(payload))
    #             #     msg_all(bot, 'msg:\n' + payload.decode("utf-8"))
    #             # else:
    #             #     msg_all(bot, 'Email message too long to attach. check email')
    #             lastBuilding = ''
    #
    #             if len(payload) > 2000:
    #                 while payload:
    #                     part = payload[:2000]
    #                     msg_all(bot, 'Message, parts:\n' + part.decode("utf-8"))
    #                     payload = payload[2000:]
    #             else:
    #                 msg_all(bot, 'Message:\n' + payload.decode("utf-8"))
    #
    #             if serviceAllowed:
    #                 for space in available_spaces.keys():
    #                     textspace = "P" + str(space)
    #                     canContinue = check_building(message_decode_raw, available_spaces[space], textspace)
    #
    #                     if canContinue:
    #                         emailMsg = build_response(available_spaces[space], space)
    #                         msg_all(bot,
    #                                 'FOUND MATCHING PARKING SPACE!\nSpace: ' + space + '\nBuilding: ' +
    #                                 available_spaces[
    #                                     space] + '\nPreparing to send response!')
    #
    #                         raw_string = prepare_raw_string(subject, to, message_id, emailMsg)
    #                         msg_all(bot, 'Message to send:\n' + emailMsg)
    #                         try:
    #                             sentMessage = service_gmail.users().messages().send(userId='me',
    #                                                                                 body={'raw': raw_string,
    #                                                                                       'threadId': thread_id}).execute()
    #                             msg_all(bot,
    #                                     'MESSAGE SENT! Check sent messages!\nMessage metadata:\n' + str(sentMessage))
    #                             msg_all(bot,
    #                                     'JOB DONE, STOPPING MAIN THREAD TO AVOID ERRORS...\n\nCUSTOM RESPONSES AND WARNINGS STILL WORKING!')
    #                             serviceAllowed = False
    #                         except:
    #                             msg_all(bot,
    #                                     'Unexpected error! Respond manually by:\nSPACE,BUILDING   (example: 05,9A)\nnone  <- for custom without space&building')
    #                         break
    #                 if emailMsg == '':
    #                     msg_all(bot,
    #                             'MATCHING GARAGES NOT FOUND! PROCEED MANUALLY BY:\nSPACE,BUILDING   (example: 05,9A)\nnone  <- for custom without space&building')
    #             else:
    #                 msg_all(bot,
    #                         'Service has been stopped before! proceed manually by typing space,building (example: 05,9A)')
    #             # print("sending: ", subject, to, message_id)
    #
    #             last_message_id = thread_id
    #             time.sleep(1)
    #         elif sendLast:
    #             sendLast = False
    #             thread_id = msgs['messages'][0]['id']
    #             message = service_gmail.users().messages().get(userId='me', id=thread_id, format='raw').execute()
    #             message_decode_raw, subject, to, message_id, payload = message_decode(message)
    #             if len(payload) > 2000:
    #                 while payload:
    #                     part = payload[:2000]
    #                     bot.sendMessage(sendLastTo, 'Last message, parts:\n' + part.decode("utf-8"))
    #                     payload = payload[2000:]
    #             else:
    #                 bot.sendMessage(sendLastTo, 'Last message:\n' + payload.decode("utf-8"))
    #
    #     except Exception as e:
    #         print(e)
    #         msg_all(bot,
    #                 'UNEXPECTED ERROR WHILE CHECKING EMAILS!\n SERVICE MAY BE UNSTABLE!')
