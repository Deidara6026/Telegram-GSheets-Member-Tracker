
import telebot
import schedule
import csv
import pygsheets
import threading
import time
import logging
import datetime, time
import config
from config import getcaption, photourl

logging.basicConfig(
    filename='flow.log', 
    encoding='utf-8', 
    level=logging.DEBUG)
logger=logging.getLogger(__name__)



token = '5555555555:lllllllllllllllllllllllllllllll'
bot = telebot.TeleBot(token)
sheet_id = '1sd23r4t5y6yu7ukliuyhtrt7865rrtghjuytrdssdfghjkjhgf'
admin_id = '100000000' #supreme admin
admin_ids =[100000000, 245555009]
status_col = 'B' # Column that contains the status of the user


def get_sheet():
    client = pygsheets.authorize(
    service_account_file="client.json")
    sheet = client.open_by_key(sheet_id)
    return sheet


def ban_user(group_id, chat_id):
    '''
    Code for removing users from the chat
    chat_id: users chat_id from telegram
    '''
    try:
        bot.ban_chat_member(
            chat_id=group_id,
            user_id=chat_id
        )
        return 0
    except Exception as e:
        logger.error(e)
        return e


def unban_user(group_id, chat_id):
    '''
    Code for removing restrictions on previously removed users
    '''
    try:
        bot.unban_chat_member(
            chat_id=group_id,
            user_id=chat_id,
            only_if_banned=True
        )
        return 0
    except Exception as e:
        logger.error(e)
        return e

def log_user(user):
    wks = get_worksheet('Banned users')
    s=wks.get_all_values(returnas='cell',
        include_tailing_empty=False,
        include_tailing_empty_rows=False)
    s = [x for x in s if x]
    chat_id = user.id
    v = [chat_id, user.username,     
    str(datetime.date.today())]
    wks = wks.insert_rows(
    len(s), number=1, values=v)

def delog_user(user):
    wks = get_worksheet('Banned users')
    f = wks.find(str(user.id))
    if f not in ([], None):
            wks.delete_rows(f[0].row, 1)

 
def get_worksheet(sheet_id):
    '''
    Get the worksheet with the id/name
    '''
    s=get_sheet()
    print(s)
    sheet = s.worksheet(
    'title', sheet_id)
    return sheet

def update_groups(gid, sid): #each group has a sheets keeping track of users
    '''
    Add a new group to the list,
    '''
    f = open('list.csv', 'w')
    w = csv.writer(f, delimiter=',')
    w.writerow([gid, sid])
    f.close()

def remove_group(gid):
    '''
    Remove a group from the csv
    '''
    s = csv_to_list()
    print(gid)
    seen=[]
    with open('list.csv', 'a') as f:
        w = csv.writer(f, delimiter=',')
        for row in s:
            print(row)
            if str(row[0]) != str(gid):
                if row[0] not in seen:
                    w.writerow(
                    [row[0], row[1]]
                    )
                    seen.append(row[0])             
        return

def csv_to_list():
    with open('list.csv', 'r') as f:
        r = csv.reader(f, delimiter=',')
        return [row for row in r]

def csv_to_dict():
    with open('list.csv', 'r') as f:
        r = csv.reader(f, delimiter=',')
        return {row[0]:row[1] for row in r}


def remove_user(gid, user):
    chat_id=user.id
    d = csv_to_dict()
    sheetid=d[str(gid)]
    wks = get_worksheet(sheetid)
    s=wks.get_all_values(returnas='cell',
        include_tailing_empty=False,
        include_tailing_empty_rows=False)
    s = [x for x in s if x]
    c = wks.find(str(user.id), 
    matchEntireCell = True)
    if c != []:
            c3 = status_col+str(c[0].row)
            cell = wks.cell(c3)
            cell.value = 'inactive'
            return
          
def welcome_user(gid, user):
    with open(photourl, 'rb') as photo:
        g = getcaption(user)
        m = bot.send_photo(chat_id=gid,
        photo=photo,
        caption=g, parse_mode='html')
        return m     
            
def add_user(gid, user):
    chat_id=user.id
    d = csv_to_dict()
    sheetid=d[str(gid)]
    wks = get_worksheet(sheetid)
    s=wks.get_all_values(returnas='cell',
        include_tailing_empty=False,
        include_tailing_empty_rows=False)
    s = [x for x in s if x]
    k = wks.find(str(chat_id))
    if k:
        c = k[0].row
        cell = wks.cell(status_col+str(c))
        cell.value = 'active'
        return
    wks.insert_rows(
        len(s), number=1,
        values= [chat_id,'active',
            user.first_name,
            user.username]
        )
    print(s)
    return
    

def job():
    groups = csv_to_list()
    for group in groups:
        sheet = get_worksheet(group[1])
        for row in sheet:
            if row[1] == 'inactive':
                x = ban_user(group[0],
                row[0])
                try:
                    user = bot.get_chat(row[0])
                    log_user(user)
                except:
                    pass
                print('1')
                if x != 0:
                    bot.send_message(
                    admin_id,
                    f'An error occured: {x}')  
                continue
            elif row[1] == 'active':
                x = unban_user(group[0],
                row[0])
                try:
                    user = bot.get_chat(row[0])
                    delog_user(user)
                except:
                    pass
                print('2')
                if x != 0:
                    bot.send_message(
                    admin_id,
                    f'An error occured: {x}')  
                continue
            else:
                print('3')
                bot.send_message(
                admin_id,
                f'An error occured: Expected column1 = userid, column2 = active/inactive got {row[0]}, {row[1]}. Please check the format of the spreadsheet.' 
                )
 
 
@bot.message_handler(commands=["add", "remove"])
def ahandler(message):
    print('h')
    l = message.text.split(' ')
    if message.chat.type == 'private':
        bot.send_message(message.chat.id,
        'Use in the group to add')
        return
    elif message.from_user.id not in admin_ids:
        bot.send_message(
        message.chat.id,
        'Command reserved for admins',
        reply_to_message_id=message.id)
        return
    elif 'remove' in l[0]:
        remove_group(message.chat.id)
        bot.send_message(
        message.chat.id,
        'Group removed from list')
        return     
    try:
        message.text.split(' ')[1]
    except:
        bot.send_message(message.chat.id,
            'Send /help to the bot to learn how to use this')
        return
    l = message.text.split(' ')
    update_groups(message.chat.id, l[1])
    bot.send_message(message.chat.id,
    f'This chat was successfully added to the service with sheet name {l[1]}')

@bot.message_handler(commands=["start"])
def shandler(message):
    bot.send_message(message.chat.id, config.starttext, parse_mode='html')


@bot.message_handler(commands=["help"])
def hhandler(message):
    bot.send_message(message.chat.id,
    "To add a group, add the bot to the group, give it admin rights and send /add worksheetname in the group.")



@bot.message_handler(content_types=["new_chat_members"])
def thandler(message):
    try:
        if message.new_chat_members not in ([], [ ], None):
            for user in message.new_chat_members:
            
                if user.is_bot==True:
                    continue
                bot.delete_message(
                message.chat.id,
                message.message_id)
                m = welcome_user(
                    message.chat.id,
                    user)
                add_user(message.chat.id, 
                    user)          
                delog_user(user)           
                time.sleep(60)
                bot.delete_message(
                message.chat.id,
                m.message_id)
                return
    except Exception as e:
        logger.error(e)
        return


@bot.message_handler(content_types=['left_chat_member'])
def lhandler(message):
    try:
        user = message.left_chat_member
        log_user(user)
        remove_user(message.chat.id, user)
        bot.delete_message(
        message.chat.id,
        message.message_id)
        return
    except Exception as e:
        logger.error(e)
        return
       

def runBot():
    bot.infinity_polling()
    bot.polling(none_stop=True)

def runSchedulers():
    schedule.every().day.at('18:40').do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    t1 = threading.Thread(target=runBot)
    t2 = threading.Thread(target=runSchedulers)
    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start()  
    