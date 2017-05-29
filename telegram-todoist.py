import time
import random
import datetime
import telepot
import todoist
from telepot.loop import MessageLoop
import MySQLdb

"""
After **inserting token** in the source code, run it:
```
$ python2.7 diceyclock.py
```
[Here is a tutorial](http://www.instructables.com/id/Set-up-Telegram-Bot-on-Raspberry-Pi/)
teaching you how to setup a bot on Raspberry Pi. This simple bot does nothing
but accepts two commands:
- `/roll` - reply with a random integer between 1 and 6, like rolling a dice.
- `/time` - reply with the current time, like a clock.
"""

def handle(msg):
    chat_id = msg['chat']['id']
    username = msg['from']['first_name']
    uid = msg['from']['id']
    command = msg['text']

    print 'Got command: %s from user %s, uid %s' % (command, username, uid)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command[:3] == '/t ':
        if len(command) >= 5:
            task_name = command [3:]
        else: #task name too short
            bot.sendMessage(chat_id, 'Task name expected. Syntax is /t [Task name]')
            return
        tapi.items.add(content=task_name, project_id=149316138, date_string='today', date_lang='en')
        s = tapi.commit()
        bot.sendMessage(chat_id, 'Task added for today: ' + command [3:])
        print('Task added for today: ' + command [3:])
    elif command[:20] == 'http://www.funda.nl/':
        db = MySQLdb.connect("localhost", "atque2ru_python", "makbet11", "atque2ru_python")
        cursor = db.cursor()
        sql = "INSERT INTO `funda_listings` (`url`, `date_added`, `address`, `price`, `space`, `timetowork`, `type`) VALUES ('%s', CURRENT_TIMESTAMP, '%s', '%d', '%d', '%d', '%s');" % (command, '-', 0, 0, 0, '-')
        cursor.execute(sql)
        db.commit()
        db.close()
        bot.sendMessage(chat_id, 'Funda listing added to database.')


bot = telepot.Bot('334973904:AAG0hVVNf2y6Wb3yyg_aNVozmTTGT7_bWkg')

tapi = todoist.TodoistAPI('0138240ad9cefd0cd28bbd9cbd726fd843bcf0e8')
s = tapi.sync()

MessageLoop(bot, handle).run_as_thread()
print 'I am listening ...'

while 1:
    time.sleep(10)