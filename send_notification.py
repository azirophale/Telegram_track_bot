from telethon import TelegramClient, events, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 3868944
api_hash = 'c4be4bcfa07a908c8d70d8c94cfcd341'


def notify_member(user,message): 
# def notify_member():  
    user_id="489077052"
    message_2="we are just testing this bot "
    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    try :
        # client.send_message('@Bruno_from_mars', 'Missing you')
        # client.send_message('@sanket_mahskar', 'This is test parice')
        # client.send_message(user_id, message_2)
        client.send_message(user,message)
        #client.send_file('username', '/home/myself/Pictures/holidays.jpg') #to send jpg files
        return ("message sent to ",user)
    except:
        print("Error accured")
    
# notify_member()