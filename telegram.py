import time
import telepot
from telepot.loop import MessageLoop


class Telegram:
    def __init__(self):
        self.bot = telepot.Bot('1865773870:AAET2CqaAeUoe_gdTlfyZco887fcskxBdCk')
        self.permissions = [1255224844, 1990072643]
        MessageLoop(self.bot, self.handle).run_as_thread()

    def msg_me(self, message):
        self.bot.sendMessage(1255224844, message)

    def msg_all(self, message):
        for ID in self.permissions:
            self.bot.sendMessage(ID, message)

    def handle(self, msg):
        if msg['from']['id'] in self.permissions:
            if '/ping' in msg['text']:
                self.bot.sendMessage(msg['from']['id'], 'Pong!')
            elif '/add' in msg['text'] and len(msg['text']) > 5:
                try:
                    toadd = int(msg['text'].replace('/add ', ''))
                    self.permissions.append(toadd)
                    self.bot.sendMessage(msg['from']['id'], 'User added!')
                except:
                    self.bot.sendMessage(msg['from']['id'], 'Unknown error while adding user!')
            else:
                self.msg_all(
                    'Wrong message! If want to respond to last email, type:\nSPACE,BUILDING   (example: 05,9A)\nnone  <- for custom without space&building')
        else:
            self.bot.sendMessage(msg['from']['id'],
                                 'No permisions! Ask admin to add your ID.\nYour ID:\n' + str(msg['from']['id']))
