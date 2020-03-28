import json
import os
import logging
import traceback
import re

from config import TOKEN, DIR, USER_ID
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from emoji import emojize

CHATWARS_ID = 265204902
CHATWARS_USERNAME = 'ChatWarsBot'
black_small_square = emojize(':black_small_square:', use_aliases=True)

# service functions
def checkString(s):
    return re.search(r'/ga_(atk|def)(\s|_)([a-zA-Z0-9]){6}', s)

def isForward(update):
    return update.message.forward_from != None and update.message.forward_from.id == CHATWARS_ID and update.message.forward_from.username == CHATWARS_USERNAME

def updateLocation(LOCATIONS):
    with open(DIR + 'LOCATIONS.json', 'w') as fl:
        json.dump(LOCATIONS, fl, indent=2)

def loadLocations():
    with open(DIR + 'LOCATIONS.json', 'r') as fl:
        LOCATIONS = json.load(fl)
    return LOCATIONS

LOCATIONS = loadLocations()

def saveLocation(update, context):
    chat_id = update.effective_chat.id
    message = update.message.text
    #print(message + ' - saveLocation in action.')
    context.bot.send_message(chat_id, message + ' - processing with saveLocation.')
    try:
        if isForward(update) and 'You found hidden location' in message: 
            # some actions
	    pass
        else:
            listLocations(update, context)
    except Exception:
        logging.error(traceback.format_exc())

def removeLocation(update, context):
    chat_id = update.effective_chat.id
    message = update.message.text
    user_id = update.message.from_user.id
    #print(message + ' - removeLocation in action.')
    context.bot.send_message(chat_id, message + ' - processing with removeLocation.')
    if not user_id in USER_ID:
        return
    elif message[0:3] == '/rm' and len(re.findall(r'^/rm (.*)', message)) != 1:
        context.bot.send_message(chat_id, 'Bad format. Type /rm [exact name], e.g. /rm Dubious Mine lvl.50.')
    elif len(re.findall(r'^/rm (.*)', message)) == 1:
        location = re.search(r'^/rm (.*)', message).group(1)
        if location in LOCATIONS:
            del LOCATIONS[location]
            updateLocation(LOCATIONS)
            text = 'The <b>' + location + '</b> has been removed.'
            context.bot.send_message(chat_id, text, parse_mode = 'HTML')
        else:
            text = 'The <b>' + location + '</b> not in the database.'
            context.bot.send_message(chat_id, text, parse_mode = 'HTML')
    else:
        pass #listLocations(update, context)

    

def listLocations(update, context):
    chat_id = update.effective_chat.id
    message = update.message.text
    #print(message + ' - listLocations in action.')
    context.bot.send_message(chat_id, message + ' - processing with listLocations.')
    try:
        if message == '/ls':
            # some actions
	    pass
        elif len(re.findall(r'/ls(\s|_)(glory|magic|res|hq)', message)) == 1:
            # some other actions
	    pass
        else:
            removeLocation(update, context)
    except Exception:
        logging.error(traceback.format_exc())



def intoLink(update, context):
    chat_id = update.effective_chat.id
    message = update.message.text
    #print(message + ' - intoLink in action.')
    context.bot.send_message(chat_id, message + ' - processing with intoLink.')
    if checkString(message) != None:
	# some actions
	pass
    else:
        saveLocation(update, context)



updater = Updater(token=TOKEN, use_context = True)
dispatcher = updater.dispatcher

intoLink_handler = MessageHandler(Filters.command | Filters.text, intoLink)
dispatcher.add_handler(intoLink_handler)

saveLocation_handler = MessageHandler(Filters.text, saveLocation)
dispatcher.add_handler(saveLocation_handler)

listLocations_handler = CommandHandler('ls', listLocations)
dispatcher.add_handler(listLocations_handler)

removeLocation_handler = CommandHandler('rm', listLocations)
dispatcher.add_handler(removeLocation_handler)

def main():
	updater.start_polling()
    #updater.idle()

if __name__ == '__main__':
    main()

