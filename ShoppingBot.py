
"""

"""
import os
import json
import telebot
from telebot import types


API_TOKEN = os.environ['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}
current_new_item = ""


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.f = open("data_file.json")
        self.json_data = json.load(self.f)
        self.divisions_list = list(self.json_data["מחלקות"])
        self.shopping_list = None
        self.current_divisions_list = {}



# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
שלום!, אני רובוט רשימת הקניות שלך.
בכל עת תוכל לשלוח לי את רשימת הקניות שלך (כל מוצר בשורה חדשה) ואני אסדר לפי מחלקות :)\
\n
שליחת start/ תאפשר מיון של רשימה חדשה\n
שליחת add/ תאפשר הוספת מוצרים חדשים למחלקה קיימת\n

במידה וחסרה מחלקה אנא פנה ליוצר שלי
""")
    # print(msg.text)
    # -> gives Hi there, I am Example bot. What's your name?
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    # try:
    print("usage!")
    chat_id = message.chat.id
    shopping_list = message.text
    shopping_list = shopping_list.splitlines()
    print(shopping_list)
    shopping_list = strip_start_and_end(shopping_list)
    user = User(chat_id)
    user_dict[chat_id] = user
    at_least_1_item_found = False
    for item in shopping_list:
        found, div = find_item(user.json_data, item, user)
        if found:
            if div not in user.current_divisions_list.keys():
                user.current_divisions_list[div] = item
            else:
                user.current_divisions_list[div] = user.current_divisions_list[
                                                  div] + "\n" + item
            at_least_1_item_found = True
        else:
            print("הפריט " + item + " איננו מוכר לי. ")
            bot.send_message(chat_id, "הפריט " + item + " איננו מוכר לי. ")
    if at_least_1_item_found:
        bot.send_message(chat_id, str(pretty_output(user)))
    else:
        bot.send_message(chat_id, " נסה שוב מההתחלה")
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')

def strip_start_and_end(shopping_list):
    for i in range(len(shopping_list)):
        shopping_list[i] = (shopping_list[i].lstrip()).rstrip()
    return shopping_list

def pretty_output(user):
    ordered_output = ""
    for div in user.current_divisions_list:
        ordered_output += "* " + div + " *\n"
        ordered_output += user.current_divisions_list[div] + "\n\n"
    return ordered_output

def find_item(json_data, item,user):
    found, div = (False, None)
    for div in user.json_data["מחלקות"]:
        for product in user.json_data["מחלקות"][div]:
            if item == product:
                found = True
                return found, div
    return found, div

# Handle '/add'
@bot.message_handler(commands=['add'])
def send_add_welcome(message):
    chat_id = message.chat.id
    user = User(chat_id)
    msg = bot.reply_to(message, """\
:אנא הכנס בשורה הראשונה את שם המחלקה המתאימה שברצונך להוסיף אליה מוצרים (מבין המחלקות הבאות) 
ובשורות הבאות פריט בשורה ולאחריו מחיר הפריט לדוגמה:\n
מוצרי חלב וביצים
חלב
7
חמאה
5

לבדיקת שייכות מוצר למחלקה: https://www.shukcity.co.il/categories?level1=79653
""")
    for i in range(len(user.divisions_list)):
        bot.send_message(chat_id, str(user.divisions_list[i])+'\n')
    bot.register_next_step_handler(msg, process_add)

def process_add(message):
    # try:
    chat_id = message.chat.id
    user = User(chat_id)
    lines = message.text.splitlines()
    print("Attempt to add!")
    print(lines)
    lines = strip_start_and_end(lines)
    div = lines[0]
    if div not in user.json_data["מחלקות"]:
        bot.send_message(chat_id, 'נראה שהמחלקה שהזנת לא מתאימה למחלקות הקיימות עליך לנסות שוב מהתחלה על ידי שליחת add\ ')
        return
    for i in range(len(lines)):
        if i==0:
            continue
        else:
            if i%2==1:
                item = lines[i]
                i=i+1
                price = lines[i]
                found, some_div = find_item(user.json_data, item, user)
                if found:
                    bot.send_message(chat_id, 'הפריט '+item+' כבר מופיע במחלקה '+str(div))
                else:
                    user.json_data["מחלקות"][div].append(item)
                    # user.f = open("/home/Eran/pyTelegramBotAPI/examples/data_file.json", 'w')
                    user.f = open("data_file.json", 'w')
                    json.dump(user.json_data, user.f)
                    user.f.close()
                    print("Someone added: "+item+" to "+str(div))
                    bot.send_message(chat_id, 'הפריט '+item+ ' התווסף בהצלחה למחלקת '+str(div)+'. תודה ' )
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')
    return




# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
