# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import jsonify
import json
import time
import threading
import sys
from flask_sslify import SSLify
import urlmarker
import re
import codecs

import en.posts_en
import en.posts_en

import ch.moderation_ch
import ch.posts_ch

import tgapi

reload(sys)
sys.setdefaultencoding('utf8')


en_group_chat_id = -100XXX
ch_group_chat_id = -100XXX
#-1001213434454
URL = 'https://api.telegram.org/botXXX/'

app = Flask(__name__)
#sslify = SSLify(app)

loc_en_dict_file = {}
loc_ch_dict_file = {}
domains_dict = {}
faq_en = {}
faq_ch = {}

allow_pics_gifs_en = True
allow_pics_gifs_ch = True
allow_links_en = True
allow_links_ch = True


loc_en_dict_file = open("localization_en.json")
loc_ch_dict_file = codecs.open("localization_ch.json",'r', 'utf-8')

#, encoding="utf8")
domains = open("domains.json", 'r')
faq_en_file = open("faq_en.json")
faq_ch_file = codecs.open("faq_ch.json",'r', 'utf-8')#
#, encoding="utf8")
loc_en_dict = json.load(loc_en_dict_file)
loc_ch_dict = json.load(loc_ch_dict_file)
domains_dict = json.load(domains)
faq_en_dict = json.load(faq_en_file)
faq_ch_dict = json.load(faq_ch_file)

seconds_no_activity_en = 600
last_message_time_en = 9999999999
seconds_repeat_post_en = 1740  # add 60 to get the real number(eks di)
max_id_en = 10
min_id_en = 1
id_of_post_en = 1

seconds_no_activity_ch = 600
last_message_time_ch = 9999999999
seconds_repeat_post_ch = 1740  # add 60 to get the real number(eks di)
max_id_ch = 10
min_id_ch = 1
id_of_post_ch = 1



def get_current_time_sec():
    #MEASURED IN SECONDS
    sec = int(round(time.time()))
    return sec


def get_last_message_time_en():
    global last_message_time_en
    return last_message_time_en

def get_last_message_time_ch():
    global last_message_time_ch
    return last_message_time_ch


@app.route('/kek', methods=['POST', 'GET'])
def kek():
    #message
    global en_group_chat_id
    global ch_group_chat_id
    global allow_pics_gifs_en
    global allow_pics_gifs_ch
    global allow_links_en
    global allow_links_ch
    if request.method == 'POST':
        r = request.get_json()
        try:
            if 'message' in r:
                admin_en_id = 0
                admin_ch_id = 0
                chat_id = r['message']['chat']['id']
                from_id = r['message']['from']['id']
                response = get_chat_member(en_group_chat_id, from_id)
		#send_message(-1001276518306,response['result']['status'])
		#send_message(-1001276518306,en_group_chat_id)
                admin_en = False
                response2 = get_chat_member(ch_group_chat_id, from_id)
                admin_ch = False
                if response['result']:
                    if response['result']['status'] in ('admin','creator','administrator'):
                        admin_en = True
                        admin_en_id = response['result']['user']['id']
                if response2['result']:
                    if response2['result']['status'] in ('admin','creator', 'administrator'):
                        admin_ch = True
                        admin_ch_id = response['result']['user']['id']
                if chat_id not in (en_group_chat_id, ch_group_chat_id):
                    # let's call it an admin panel
                    if admin_en == True:
                        if "text" in r['message'] != None:
                            message = r['message']['text']
                            # allow_pics_gifs - Allow regular users send pictures and gifs
                            if '/add_text_post_en' in message:
                                message = message.replace("/add_text_post_en", '')
                                add_text_post_en(message)
                                send_message(chat_id,"The post was added to the database")
                            if '/add_text_info_post_en' in message:
                                message = message.replace("/add_text_info_post_en", '')
                                add_text_info_post_en(message)
                                get_max_id_en()
                                string = "The info_post with id = %d was added to the database" % (get_max_id_en(),)
                                send_message(chat_id,string)
                            if '/allow_pics_gifs_stickers_en' in message:
                                allow_pics_gifs_en = True
                                send_message(chat_id,"Users are allowed to send pictures, stickers and gifs")
                            if '/allow_links_en' in message:
                                allow_links_en = True
                                send_message(chat_id,"Users are allowed to links")
                            if '/disallow_links_en' in message:
                                allow_links_en = False
                                send_message(chat_id,"Users are disallowed to send links")
                            if '/disallow_pics_gifs_sticker_en' in message:
                                allow_pics_gifs_en = False
                                send_message(chat_id,"Users are disallowed to send pictures, stickers and gifs")
                            if '/set_time_start_posting_en' in message:
                                message = message.replace("/set_time_start_posting_en", '')
                                global seconds_no_activity_en
                                seconds_no_activity_en = int(message) - 60
                                send_message(chat_id,"The time after which the bot starts public the posts was set")
                            if '/delete_info_post_en' in message:
                                message = message.replace("/delete_info_post_en ", '')
                                message = int(message)
                                delete_info_post_en(message)
                                send_message(chat_id,"The post was deleted from the database")
                            if '/add_mute_word_en' in message:
                                message = message.replace("/add_mute_word_en ", '')
                                loc_en_dict['mute_words'].append(message)
                                loc_en_dict_file = open("localization_en.json", 'w')
                                loc_en_dict_file.write(json.dumps(loc_en_dict))
                                send_message(chat_id, "The mute word was added")


                        if "caption" in r['message']:
                            caption = r['message']['caption']
                            if '/add_image_post_en' in caption:
                                caption = caption.replace("/add_image_post_en", '')
                                add_image_post_en(chat_id, r['message']['photo'][-1]['file_id'], caption)
                                send_message(chat_id,"The post was added to the database")
                            if '/add_gif_post_en' in caption:
                                caption = caption.replace("/add_gif_post_en", '')
                                add_gif_post_en(chat_id, r['message']['document']['file_id'], caption)
                                send_message(chat_id,"The post was added to the database")
                            if '/add_image_info_post_en' in caption:
                                caption = caption.replace("/add_image_info_post_en", '')
                                add_image_info_post_en(chat_id, r['message']['photo'][-1]['file_id'], caption)
                                get_max_id_en()
                                string = "The info_post with id = %d was added to the database" % (get_max_id_en(),)
                                send_message(chat_id,string)
                            if '/add_gif_info_post_en' in caption:
                                caption = caption.replace("/add_gif_info_post_en", '')
                                add_gif_info_post_en(chat_id, r['message']['document']['file_id'], caption)
                                get_max_id_en()
                                string = "The info_post with id = %d was added to the database" % (get_max_id_en(),)
                                send_message(chat_id,string)

                    elif admin_ch == True:
                        if "text" in r['message'] != None:
                            message = r['message']['text']
                            # allow_pics_gifs - Allow regular users send pictures and gifs
                            if '/add_text_post_ch' in message:
                                message = message.replace("/add_text_post_ch", '')
                                add_text_post_ch(message)
                                send_message(chat_id,"The post was added to the database")
                            if '/add_text_info_post_ch' in message:
                                message = message.replace("/add_text_info_post_ch", '')
                                add_text_info_post_ch(message)
                                get_max_id_ch()
                                string = "The info_post with id = %d was added to the database" % (get_max_id_ch(),)
                                send_message(chat_id,string)
                            if '/allow_pics_gifs_sticker_ch' in message:
                                allow_pics_gifs_ch = True
                                send_message(chat_id,"Users are allowed to send pictures, stickers and gifs")
                            if '/allow_links_ch' in message:
                                allow_links_ch = True
                                send_message(chat_id,"Users are allowed to links")
                            if '/disallow_links_ch' in message:
                                allow_links_ch = False
                                send_message(chat_id,"Users are disallowed to send links")
                            if '/disallow_pics_gifs_sticker_ch' in message:
                                allow_pics_gifs_ch = False
                                send_message(chat_id,"Users are disallowed to send pictures, stickers and gifs")
                            if '/set_time_start_posting_ch' in message:
                                message = message.replace("/set_time_start_posting_ch", '')
                                global seconds_no_activity_ch
                                seconds_no_activity_ch = int(message) - 60
                                send_message(chat_id,"The time after which the bot starts public the posts was set")
                            if '/delete_info_post_ch' in message:
                                message = message.replace("/delete_info_post_ch ", '')
                                delete_info_post_ch(message)
                                send_message(chat_id,"The post was deleted from the database")
                            if '/add_mute_word_ch' in message:
                                message = message.replace("/add_mute_word_ch ", '')
                                loc_ch_dict['mute_words'].append(message)
                                loc_ch_dict_file = open("localization_ch.json", 'w')
                                loc_ch_dict_file.write(json.dumps(loc_ch_dict))
                                send_message(chat_id, "The mute word was added")




                        if "caption" in r['message']:
                            caption = r['message']['caption']
                            if '/add_image_post_ch' in caption:
                                caption = caption.replace("/add_image_post_ch", '')
                                add_image_post_ch(chat_id, r['message']['photo'][-1]['file_id'], caption)
                                send_message(chat_id,"The post was added to the database")
                            if '/add_gif_post_ch' in caption:
                                caption = caption.replace("/add_gif_post_ch", '')
                                add_gif_post_ch(chat_id, r['message']['document']['file_id'], caption)
                                send_message(chat_id,"The post was added to the database")
                            if '/add_image_info_post_ch' in caption:
                                caption = caption.replace("/add_image_info_post_ch", '')
                                add_image_info_post_ch(chat_id, r['message']['photo'][-1]['file_id'], caption)
                                get_max_id_ch()
                                string = "The info_post with id = %d was added to the database" % (get_max_id_ch(),)
                                send_message(chat_id,string)
                            if '/add_gif_info_post_ch' in caption:
                                caption = caption.replace("/add_gif_info_post_ch", '')
                                add_gif_info_post_ch(chat_id, r['message']['document']['file_id'], caption)
                                get_max_id_ch()
                                string = "The info_post with id = %d was added to the database" % (get_max_id_ch(),)
                                send_message(chat_id,string)
                    else:
                        send_message(chat_id,"Sorry, you're not an admin")

                else:
                    if chat_id == en_group_chat_id:
                        insert_db_en(from_id)
                        if "new_chat_member" in r['message']:
                            if 'username' in  r['message']["new_chat_member"]:
                                username = r['message']["new_chat_member"]['username']
                            else:
                                username = r['message']["new_chat_member"]['first_name']
                            user_id = r['message']["new_chat_member"]['id']
                            text = loc_en_dict["welcome_new_member"]
                            text = text.replace("xxxx", username)
                            send_message(chat_id,text)
                        # if not new member
                        else:
                            if 'username' in  r['message']['from']:
                                username = r['message']['from']['username']
                            else:
                                username = r['message']['from']['first_name']
                            message_id_to_be_deleted = r['message']['message_id']
                            #that's for avoiding empty telegram messages that may cause error
                            if "text" in r['message'] != None:
                                message = r['message']['text']
                                # if user have been not wrtining anything during 24h sends welcome_back message, 86400sec = 24h
                                if get_current_time_sec() - select_time_en(from_id) >= 86400:
                                    text = loc_en_dict["welcome_old_member"]
                                    text = text.replace("xxxx", username)
                                    send_message(chat_id,text)
                                # mutes a user that used in his message a word from mute_word list twice
                                message = message.lower()
                                if any(word in message for word in loc_en_dict['mute_words']):
                                    usage_of_warnings_en_mute(from_id, chat_id, username, message_id_to_be_deleted)
                                # kicks user whose message contains a word from ban_words list
                                if any(word in message for word in loc_en_dict['ban_words']):
                                    kick_chat_member(chat_id, from_id)
                                    delete_message(chat_id, message_id_to_be_deleted)
                                # collects all urls what appeared in message
                                urls = re.findall(urlmarker.WEB_URL_REGEX,message)
                                # if there is some urls in message
                                if urls:
                                    # delete message which contains urls that is not from allowed list
                                    if not any(url in message for url in domains_dict['domains']):
                                        #allows admin to post any urls
                                        response = get_chat_member(chat_id, from_id)
                                        if response['result']['status'] == 'member':
                                            if allow_links_en == False:
                                                usage_of_warnings_en(from_id, chat_id, username, message_id_to_be_deleted)
                                if message in faq_en_dict:
                                    temp = faq_en_dict[message]
                                    send_message(chat_id, "Hello @" + username + ", " + temp)
                                if 'reply_to_message' in r['message']:
                                    for_id = r['message']['reply_to_message']['from']['id']
                                    if admin_en_id != for_id:
                                        if '/ban' in message:
                                            insert_restriction_en(from_id, 0, for_id)
                                            if is_voted_en(from_id, for_id) == 0:
                                                general_restr_en(for_id)
                                                set_voted_en(from_id, for_id)
                                            else:
                                                send_message(chat_id, "Sorry, you already voted for ban of this user")
                                            if get_amount_of_votes_en(for_id) >= 2:
                                                kick_chat_member(chat_id, for_id)
                                            else:
                                                send_message(chat_id, "%d votes, 2 is required" % (get_amount_of_votes_en(for_id),))
                                        if '/mute' in message:
                                            for_id = r['message']['reply_to_message']['from']['id']
                                            mute_insert_restriction_en(from_id, 0, for_id)
                                            if mute_is_voted_en(from_id, for_id) == 0:
                                                mute_general_restr_en(for_id)
                                                mute_set_voted_en(from_id, for_id)
                                            else:
                                                send_message(chat_id, "Sorry, you have already voted to mute this user")
                                            if mute_get_amount_of_votes_en(for_id) >= 2:
                                                restrict_chat_member(chat_id, for_id, get_current_time_sec() + 86400)
                                            else:
                                                send_message(chat_id, "%d votes, 2 is required" % (mute_get_amount_of_votes_en(for_id),))

                                    else:
                                        send_message(chat_id, "This user is an admin")


                            if any(x in r['message'] for x in ('photo', 'video', 'video_note', 'document', 'voice', 'audio', 'location', 'sticker')):
                                response = get_chat_member(chat_id, from_id)

                                if any(x in r['message'] for x in ('video', 'video_note', 'voice', 'audio', 'location')):
                                    if response['result']['status'] == 'member':
                                        usage_of_warnings_en(from_id, chat_id, username, message_id_to_be_deleted)
                                    else:
                                        delete_message(chat_id, message_id_to_be_deleted)
                                if 'photo' in r['message'] and allow_pics_gifs_en == False:
                                    if response['result']['status'] == 'member':
                                        usage_of_warnings_en(from_id, chat_id, username, message_id_to_be_deleted)
                                if 'sticker' in r['message'] and allow_pics_gifs_en == False:
                                    if response['result']['status'] == 'member':
                                        usage_of_warnings_en(from_id, chat_id, username, message_id_to_be_deleted)
                                if 'document' in r['message']:
                                    # handles gifs
                                    if 'mp4' in r['message']['document']['mime_type']:
                                        if allow_pics_gifs_en == False:
                                            if response['result']['status'] == 'member':
                                                usage_of_warnings_en(from_id, chat_id, username, message_id_to_be_deleted)
                                    else:
                                        usage_of_warnings_en(from_id, chat_id, username, message_id_to_be_deleted)
                                # this time is needed to greet member if he has been not writning anything for 24h
                            update_time_en(from_id)
                            global last_message_time_en
                            last_message_time_en = r['message']['date']


                    if chat_id == ch_group_chat_id:
                        insert_db_ch(from_id)
                        if "new_chat_member" in r['message']:
                            username = r['message']["new_chat_member"]['username']
                            user_id = r['message']["new_chat_member"]['id']
                            text = loc_ch_dict["welcome_new_member"]
                            text = text.replace("xxxx", username)
                            send_message(chat_id,text)
                        # if not new member
                        else:
                            username = r['message']['from']['username']
                            message_id_to_be_deleted = r['message']['message_id']
                            #that's for avoiding empty telegram messages that may cause error
                            if "text" in r['message'] != None:
                                message = r['message']['text']
                                # if user have been not wrtining anything during 24h sends welcome_back message, 86400sec = 24h
                                if get_current_time_sec() - select_time_ch(from_id) >= 86400:
                                    text = loc_ch_dict["welcome_old_member"]
                                    text = text.replace("xxxx", username)
                                    send_message(chat_id,text)
                                # mutes a user that used in his message a word from mute_word list twice
                                message = message.lower()
                                if any(word in message for word in loc_ch_dict['mute_words']):
                                    usage_of_warnings_ch_mute(from_id, chat_id, username, message_id_to_be_deleted)
                                # kicks user whose message contains a word from ban_words list
                                if any(word in message for word in loc_ch_dict['ban_words']):
                                    kick_chat_member(chat_id, from_id)
                                    delete_message(chat_id, message_id_to_be_deleted)
                                # collects all urls what appeared in message
                                urls = re.findall(urlmarker.WEB_URL_REGEX,message)
                                # if there is some urls in message
                                if urls:
                                    # delete message which contains urls that is not from allowed list
                                    if not any(url in message for url in domains_dict['domains']):
                                        #allows admin to post any urls
                                        response = get_chat_member(chat_id, from_id)
                                        if response['result']['status'] == 'member':
                                            if allow_links_ch == False:
                                                usage_of_warnings_ch(from_id, chat_id, username, message_id_to_be_deleted)
                                if message in faq_ch_dict:
                                    temp = faq_ch_dict[message]
                                    send_message(chat_id, "你好 @" + username + ", " + temp)
                                if 'reply_to_message' in r['message']:
                                    for_id = r['message']['reply_to_message']['from']['id']
                                    if admin_ch_id != for_id:
                                        if '/ban' in message:
                                            insert_restriction_ch(from_id, 0, for_id)
                                            if is_voted_ch(from_id, for_id) == 0:
                                                general_restr_ch(for_id)
                                                set_voted_ch(from_id, for_id)
                                            else:
                                                send_message(chat_id, "對不起，您已經投票禁止該用戶")
                                            if get_amount_of_votes_ch(for_id) >= 2:
                                                kick_chat_member(chat_id, for_id)
                                            else:
                                                send_message(chat_id, "%d 票，2是必需的" % (get_amount_of_votes_ch(for_id),))
                                        if '/mute' in message:
                                            for_id = r['message']['reply_to_message']['from']['id']
                                            mute_insert_restriction_ch(from_id, 0, for_id)
                                            if mute_is_voted_ch(from_id, for_id) == 0:
                                                mute_general_restr_ch(for_id)
                                                mute_set_voted_ch(from_id, for_id)
                                            else:
                                                send_message(chat_id, "對不起，您已經投票禁止該用戶")
                                            if mute_get_amount_of_votes_ch(for_id) >= 2:
                                                restrict_chat_member(chat_id, for_id, get_current_time_sec() + 86400)
                                            else:
                                                send_message(chat_id, "%d 票，2是必需的" % (mute_get_amount_of_votes_en(for_id),))

                                    else:
                                        send_message(chat_id, "此用戶是管理員")

                            if any(x in r['message'] for x in ('photo', 'video', 'video_note', 'document', 'voice', 'audio', 'location')):
                                response = get_chat_member(chat_id, from_id)
                                if any(x in r['message'] for x in ('video', 'video_note', 'voice', 'audio', 'location')):
                                    if response['result']['status'] == 'member':
                                        usage_of_warnings_ch(from_id, chat_id, username, message_id_to_be_deleted)
                                    else:
                                        delete_message(chat_id, message_id_to_be_deleted)
                                if 'photo' in r['message'] and allow_pics_gifs_ch == False:
                                    if response['result']['status'] == 'member':
                                        usage_of_warnings_ch(from_id, chat_id, username, message_id_to_be_deleted)
                                if 'document' in r['message']:
                                    # handles gifs
                                    if 'mp4' in r['message']['document']['mime_type']:
                                        if allow_pics_gifs_ch == False:
                                            if response['result']['status'] == 'member':
                                                usage_of_warnings_ch(from_id, chat_id, username, message_id_to_be_deleted)
                                    else:
                                        usage_of_warnings_ch(from_id, chat_id, username, message_id_to_be_deleted)
                            update_time_ch(from_id)
                            global last_message_time_ch
                            last_message_time_ch = r['message']['date']
        except Exception as e:
            e = str(e)
            send_message(my_tg_id, e)
            send_message(my_tg_id, "error")


        return 'ASKD', 200
    return 'DIASD ', 200



#host='0.0.0.0'
#port = 8443
#port = int(port)
if __name__ == "__main__":
   # t1.start()
#t2.start()
#t3.start()
#t4.start()
#t5.start()
    ssl_context=('webhook_cert.pem', 'webhook_pkey.pem')
    t1 = threading.Thread(target = app.run, kwargs ={'host' : '0.0.0.0', 'port' : 8443,'ssl_context' : ssl_context, 'debug' : False, 'use_reloader' : False})
    t2 = threading.Thread(target = no_activity_en, args = ())
    t3 = threading.Thread(target = activity_en, args = ())
    t4 = threading.Thread(target = no_activity_ch, args = ())
    t5 = threading.Thread(target = activity_ch, args = ())
    t1.start()
    t2.start()
    t3.start()
    #t4.start()
    #t5.start()
