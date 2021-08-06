import logging
import track_coin as tc
import send_notification as sends
import csv
from datetime import datetime 
import sys  
sys.path.append('../')  
import bot_data as bot_api

from telegram import Update, ForceReply,InlineKeyboardButton, InlineKeyboardMarkup ,ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

user_data=[]

token=bot_api.token()
updater = Updater(token)
dispatcher = updater.dispatcher



help_message=("💰 Hello You can See the price of cryptocurrency here 💰\n simply Enter their 'Sign' here "
"\n 🔶 BITCOIN is = 'BTC' \n\n  🔶 ETHERIUM is = 'ETH' "
"\n\n Try entering 'BTC' Or 'ETH' "
" "
"\nAnd can Track their price too ...!"
" ")

INR, USD, EURO, POUND, BTC,ETH = range(6)
add_user=True
error_count=1
track_answer="false"
qurery_response=""
track_coin_index=0

def start(update: Update, context: CallbackContext) -> None:
    """ track a coin ."""
    message=update.message.text
    print("")
    print(str(update.effective_user.first_name)+" "+ str(update.effective_user.last_name)+"  "+str(update.effective_user.username))
    user = update.effective_user
    usrname = user.username
    fname = user.first_name
    global add_user 
    add_user = False

    update.message.reply_text("Hello "+str(fname)+" ! \n How are you ? 😄")

    #to call help cammand 
    help_command(update,context)
    #to append the user data into csv file
    # f = open('user_data/start_cmd.csv', 'a')
    # writer=csv.writer(f)
    now=datetime.now()
    with open('user_data/start_cmd.csv', 'a') as appendFile:
        writer=csv.writer(appendFile)
        time=now.strftime("%D:%H:%M:%S")
        list_append=[str(time),str(user.first_name),str(user.last_name),str(user.id),str(user.username),str(user.language_code)]
        writer.writerow(list_append)
    # print(list_a)
    # Send message with text and appended InlineKeyboard
    try :
        with open('user_data/users_currency.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                for row in reader:
                    # print(row)
                    if row==[]:
                        #do nothing here
                        continue
                    else:
                        if str(row[0])==str(user.id):
                            parse_currency=row[2]
                            print(row[0],": already a user")
                            add_user= False
                            break
                        else:
                            print("else is excuting ")
                            add_user=True
        if add_user== True:
            add_currency(update,context)
            print("user_currency should ask here")
            add_user=False
    except:
        print("error in start start ")
    

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(help_message)

    
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    symbol=update.message.text.upper()
    user_id=update.effective_user.id
    currency="usd"
    print(str(update.effective_user.username)+" : "+symbol)
    try:
        with open('user_data/users_currency.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                if row==[]:
                    continue
                if str(row[0])==str(user_id):
                    currency=str(row[2])
                    currency=currency.upper()
                    
    except:
        print("error in row files")

    price=tc.crypto_calculate(symbol,currency)
    coin=str(price)
    new_price=""
    check_coin=coin.upper()
    if check_coin!="NONE" and check_coin!="ERROR":
        reply_markup = keyboard_layouts("track_or_ok")
            
        # update.message.reply_text("Curent "+symbol+" price is : "+str(coin), reply_markup=reply_markup,timeout=60)
        update.message.reply_text("Curent "+symbol+" price is : "+str(price)+" "+currency, reply_markup=reply_markup,timeout=60)
        # update.message.reply_text("Curent "+symbol+" price is : "+coin)
    else: 
        global error_count
        if (error_count%3)==0:
            update.message.reply_text("Tum chutiya ho bc ")
            print(str(update.effective_user.username)+" is Chutiya ")
            error_count=error_count+1
        else:
            error_count=error_count+1
        # update.message.reply_text(update.message.text)
                                  

#checking currency of  user
def check_currency(update,context,cur):
    id=update.effective_user.id
    user=update.effective_user.username
    # Iterate over each row in the csv using reader object
    # csv_writer.writerow([str(id),str(user),str(cur)])
    # csv_writer.writerow(["id","user","currency"])
    lines = list()
    no_user=True
    replace=[str(id),str(user),str(cur)]
    try:
        # for row in csv_reader:
        #     if row==[]:
        #         #do nothing here
        #         continue
        #     else:
        #         if str(row[1])==str(user):
        #             print("user exist")
        #             replace=[str(update.effective_user.id),str(update.effective_user.username),str(cur)]
        #             csv_writer.write(row)
        #             csv_writer.writerow(row,replace)
        #             no_user=False
        

        with open('user_data/users_currency.csv', 'r') as readFile:

            reader = csv.reader(readFile)

            for row in reader:
                if row==[]:
                    continue
                elif str(row[0])==str(id):
                    # print("user exist")
                    lines.append(replace)
                    no_user=False
                else:
                    lines.append(row)
            
            if no_user==True:
                print("new recod inserted")
                # csv_writer.writerow([str(id),str(user),str(cur)])
                temp_row=[str(id),str(user),str(cur)]
                lines.append(temp_row)
                no_user=False

        with open('user_data/users_currency.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
                
    except:
        print("check currency error")
        
    
    # if no_user==True:
    #     print("new recod inserted")
    #     csv_writer.writerow([str(id),str(user),str(cur)])
        
    #     no_user=False
    


def tracking_coin(update: Update, context: CallbackContext) -> None:

    message_of_user=update.message.text
    message_of_user=message_of_user.lower()
    user_id=update.effective_user.id
    user_username=update.effective_user.username
    user_currency=""
    user_is_present=False
    global track_coin_index
    global qurery_response
    with open("user_data/users_currency.csv","r") as readfile:
        read=csv.reader(readfile)
        for row in read:
            if row==[]:
                continue
            else:
                if str(row[0])==str(user_id):
                    user_currency=str(row[2])

    if message_of_user=="/track":
        update.message.reply_text(" you can track Your_coin line this \n\n /track\tYour coin\tAmount \n Eg.\n /track BTC 30000")     
    else:
        try:
            convert_message=message_of_user.split(" ")
            lenth_of_msg=len(convert_message)
            if lenth_of_msg==3:
                user_coin_symbol=str(convert_message[1])
                user_coin_price_str=str(convert_message[2])
                user_coin_price_float=float(user_coin_price_str)
                with open("user_data/track_coin.csv","r+") as readWritefile:
                    read_2=csv.reader(readWritefile)
                    write_2=csv.writer(readWritefile)
                    # print("track_coin we opened the file")
                    for row in read_2:
                        # print("we can read rows at least for now")
                        if row==[]:  
                            # print("track_coin empty row")
                            continue
                        else:
                            if str(row[0])==str(user_id):
                                new_row=row
                                user_is_present=True
                    if user_is_present==True:
                        print("user is already tracking a coin ")
                        msg_coin=str(new_row[2])
                        msg_price=str(new_row[3])
                        msg_currency=str(new_row[4])
                        price=tc.crypto_calculate(msg_coin)
                        reply_markup=keyboard_layouts("delete_ok")
                        update.message.reply_text("🔰 You are already tracking a coin \nDetails :\n"+msg_coin+" "+msg_price+" "+msg_currency,reply_markup=reply_markup)
                        user_is_present=False
                    elif user_is_present==False:
                        if user_currency=="":
                            add_currency(update,context)
                        else:
                            try:
                                crypto_price=float(tc.crypto_calculate(user_coin_symbol,user_currency))
                                print(crypto_price)
                                if crypto_price<user_coin_price_float:
                                    track_coin_index=track_coin_index+1

                                    cmd=[str(user_id),str(user_username),str(user_coin_symbol),user_coin_price_str,str(user_currency),"greater",str(track_coin_index)]
                                    write_2.writerow(cmd)
                                    message="Current "+str(user_coin_symbol)+" Price is :"+str(crypto_price)+"\nAnd your track Price is : "+str(user_coin_price_float)
                                    "\nAre Yor sure you still want to track your cryoto "
                                    reply_markup=keyboard_layouts("ask_yes_no_trading")
                                    update.message.reply_text(message,reply_markup=reply_markup)   
                                    print(str(user_coin_price_float)+" Greater "+str(crypto_price))
                                elif crypto_price>user_coin_price_float:
                                    track_coin_index=track_coin_index+1

                                    print(str(user_coin_price_float)+" Lesser "+str(crypto_price))
                                    cmd=[str(user_id),str(user_username),str(user_coin_symbol),user_coin_price_str,str(user_currency),"smaller",str(track_coin_index)]
                                    write_2.writerow(cmd)
                                    message="Current "+str(user_coin_symbol)+" Price is :"+str(crypto_price)+"\nAnd your track Price is : "+str(user_coin_price_float)
                                    "\nAre Yor sure you still want to track your cryoto "
                                    reply_markup=keyboard_layouts("ask_yes_no_trading")
                                    update.message.reply_text(message,reply_markup=reply_markup)     
                            except :
                                print("error in track coin greater or lesser blcok ")
                                
            else:
                update.message.reply_text("Enter Proper command Bitch ")
        except:
            update.message.reply_text("🔰 Someting went wrong 🔰\n\nYou can track Your_Coin line this \n\n /track\tYour coin\tAmount \n Eg.\n /track BTC 30000")
    

def settings(update:Update,context:CallbackContext):
    setting_message=(" This message will show you if u press setting command ")
    reply_markup=keyboard_layouts("SETTINGS_MENU")
    update.message.reply_text(setting_message,reply_markup=reply_markup)

def add_currency(update:Update,context:CallbackContext):

    user=str(update.effective_user.id)
    selection=""
    try:
        with open('user_data/users_currency.csv', 'r+') as readfile:
            csv_reader=csv.reader(readfile)
            for row in csv_reader:
                # print(row)
                if row==[]:
                    #do nothing here
                    continue
                else:
                    if str(row[0])==str(user):
                        selection=row[2]
                        selection=selection.upper()
                        print("Selection : "+selection)
    except:
        print("add_currency error")
        
    if selection=="":
        reply_markup = keyboard_layouts("new_currency")
    else:
        reply_markup = keyboard_layouts(selection)

    # print(list_a)
    # Send message with text and appended InlineKeyboard
    try:
        update.message.reply_text("please choose your Currency to procede 👀", reply_markup=reply_markup)
    except:
        query=update.callback_query
        query.edit_message_text("please choose your Currency to procede 👀", reply_markup=reply_markup)

def keyboard_layouts(choice=""):
    choice=choice.upper()
    yes_no_keyboard_for_tracking = [
        [
            InlineKeyboardButton(" Yes ", callback_data='yes_track'),
            InlineKeyboardButton(" No ", callback_data='no_track'),
        ],
        # [InlineKeyboardButton(" Cancle ", callback_data='cancle')],
    ]
    new_currency_keyboard = [
        [
            InlineKeyboardButton("Inr ", callback_data="1"),
            InlineKeyboardButton("Usd", callback_data="2"),
            InlineKeyboardButton("Euro", callback_data="3"),
            InlineKeyboardButton("Yen", callback_data="4"),
        ],
        [InlineKeyboardButton("cancle ❌",callback_data="cancle")],
    ]
    inr_select_keyboard = [
        [
            InlineKeyboardButton("🔘 Inr ", callback_data="1"),
            InlineKeyboardButton("Usd", callback_data="2"),
            InlineKeyboardButton("Euro", callback_data="3"),
            InlineKeyboardButton("Yen", callback_data="4"),
        ],
        [InlineKeyboardButton("cancle ❌",callback_data="cancle")],
    ]
    usd_select_keyboard = [
        [
            InlineKeyboardButton("Inr ", callback_data="1"),
            InlineKeyboardButton("🔘 Usd", callback_data="2"),
            InlineKeyboardButton("Euro", callback_data="3"),
            InlineKeyboardButton("Yen", callback_data="4"),
        ],
        [InlineKeyboardButton("cancle ❌",callback_data="cancle")],
    ]
    euro_select_keyboard = [
        [
            InlineKeyboardButton("Inr ", callback_data="1"),
            InlineKeyboardButton("Usd", callback_data="2"),
            InlineKeyboardButton("🔘 Euro", callback_data="3"),
            InlineKeyboardButton("Yen", callback_data="4"),
        ],
        [InlineKeyboardButton("cancle ❌",callback_data="cancle")],
    ]
    yen_select_keyboard = [
        [
            InlineKeyboardButton("Inr ", callback_data="1"),
            InlineKeyboardButton("Usd", callback_data="2"),
            InlineKeyboardButton("Euro", callback_data="3"),
            InlineKeyboardButton("🔘 Yen", callback_data="4"),
        ],
        [InlineKeyboardButton("cancle ❌",callback_data="cancle")],
    ]
    setting_menue_keyboard = [
        [
            InlineKeyboardButton("⚜️ Show track details ⚜️",callback_data="show_track_data"),
        ],
        [
            InlineKeyboardButton(" 💲 Currency  💲",callback_data="setting_currency")
        ],
        [
            InlineKeyboardButton(" Back ⬅️",callback_data="cancle"),
        ]
    ]
    track_or_ok_keyboard =[[
            InlineKeyboardButton("Track 〽️", callback_data="track"),
            InlineKeyboardButton("OK 🆗", callback_data="ok"),
        ]]
    delete_or_ok_keyboard=[
        [
            InlineKeyboardButton("Delete ❌",callback_data="delete_tracking_Data"),
            InlineKeyboardButton("ok 🆗", callback_data="keep_tracking_data"),
        ]
    ]
    if choice=="INR":
        return_reply_markup = InlineKeyboardMarkup(inr_select_keyboard)
        return return_reply_markup
    elif choice=="USD":
        return_reply_markup = InlineKeyboardMarkup(usd_select_keyboard)
        return return_reply_markup
    elif choice=="EURO":
        return_reply_markup = InlineKeyboardMarkup(euro_select_keyboard)
        return return_reply_markup
    elif choice=="YEN":
        return_reply_markup = InlineKeyboardMarkup(yen_select_keyboard)
        return return_reply_markup
    elif choice=="NEW_CURRENCY":
        return_reply_markup = InlineKeyboardMarkup(new_currency_keyboard)
        return return_reply_markup
    elif choice=="ASK_YES_NO_TRADING":
        return_reply_markup = InlineKeyboardMarkup(yes_no_keyboard_for_tracking)
        return return_reply_markup
    elif choice=="SETTINGS_MENU":
        return_reply_markup = InlineKeyboardMarkup(setting_menue_keyboard)
        return return_reply_markup
    elif choice=="TRACK_OR_OK":
        return_reply_markup = InlineKeyboardMarkup(track_or_ok_keyboard)
        return return_reply_markup
    elif choice=="DELETE_OK":
        return_reply_markup= InlineKeyboardMarkup(delete_or_ok_keyboard)
        return return_reply_markup



def button_reply(update: Update, context:CallbackContext )-> None:
    query = update.callback_query
    choice = query.answer
    global qurery_response
    global track_coin_index
    lines = list()
    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data
    #print(query)
    # Now u can define what choice ("callback_data") do what like this:

    if choice=="cancle"or choice=="no_track"or choice=="keep_tracking_data" or choice=="ok":
        update.callback_query.delete_message()
        print(choice)
    if choice=="track":
        query.edit_message_text(text="Pleace use /track command to track your coin ")
        # query.edit_message_text(text=" Testing this new keyboard",reply_markup=reply_markup)
        # print(str(update.effective_user.username)+" Wants to track")
    if choice=="yes_track":
        query.edit_message_text(text="Now you can track you data ")
    
    if choice=="delete_tracking_Data":
        print("should dlte the data here")
        user_id=str(update.effective_user.id)
        print("User Id is : ",user_id)
        with open("user_data/track_coin.csv","r+") as readWritefile:
                    read_2=csv.reader(readWritefile)
                    
                    for row in read_2:
                        if row==[]:
                            continue
                        else:
                            if row[0]==user_id:
                                print("user row is delted")
                            else:
                                lines.append(row)
        
        with open('user_data/track_coin.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        query.edit_message_text(text=" Deleted the data ")
    if choice=="no_track":
        delete_index=str(track_coin_index)
        print("delete index : ",delete_index)
        with open("user_data/track_coin.csv","r+") as readWritefile:
                    read_2=csv.reader(readWritefile)
                    write_2=csv.writer(readWritefile)
                    for row in read_2:
                        if row==[]:
                            continue
                        else:
                            if row[6]==delete_index:
                                print("user row is delted")
                            else:
                                lines.append(row)
        
        with open('user_data/track_coin.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)

    if choice == "1" :
        # update.message.reply_text("you have choose 1")
        print("user choose INR")
        check_currency(update,context,"inr")
        # update.callback_query.delete_message(timeout=0.5)
        query.edit_message_text(text="Now your currency is : INR")
    if choice == "2":
        print("user choose USD")
        check_currency(update,context,"usd")
        # update.callback_query.delete_message(timeout=0.5)
        query.edit_message_text(text="Now your currency is : USD")
    if choice =="3":
        print("user choose EURO")
        check_currency(update,context,"euro")
        query.edit_message_text(text="Now your currency is : Euro")
        # update.callback_query.delete_message(timeout=0.5)
    if choice =="4":
        print("user choose Yen")
        check_currency(update,context,"yen")
        query.edit_message_text(text="Now your currency is : YEN")
        # update.callback_query.delete_message(timeout=0.5)
    if choice=="setting_currency":
        query.edit_message_text("we should show setting here")
        add_currency(update,context)
    
    if choice=="show_track_data":
        query.edit_message_text("Your tracking coin data")

    if choice=="11":
        print("user choose button 1")
        # update.callback_query.delete_message(timeout=0.5)
    if choice=="12":
        print("user choose button 1")
        # update.callback_query.delete_message(timeout=0.5)

def main():
    """Start the bot."""
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # dispatcher.add_handler(CommandHandler("bitcoin", bitcoin))
    dispatcher.add_handler(CommandHandler("track",tracking_coin))
    dispatcher.add_handler(CommandHandler("settings",settings))
    dispatcher.add_handler(CommandHandler("currency",add_currency))
    dispatcher.add_handler(CallbackQueryHandler(button_reply))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()