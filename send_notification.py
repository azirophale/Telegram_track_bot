from telethon import TelegramClient, events, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = "<Api_id>"
api_hash = '<Your API hash>'


def notify_member(user_id,message): 

   
    
    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    try :
        # client.send_message(user_id, message)
        client.send_message(user,message)
        #client.send_file('username', '/home/myself/Pictures/holidays.jpg') #to send jpg files
        return ("message sent to ",user)
    except:
        print("Error accured")
    

