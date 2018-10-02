import sqlite3

conn = sqlite3.connect('bot_final.db', check_same_thread=False)
loc_en_dict = {}
domains = open("domains.json", 'r')
loc_en_dict_file = open("localization_en.json")
loc_en_dict = json.load(loc_en_dict_file)
domains_dict = json.load(domains)



en_group_chat_id = -100XXX
seconds_no_activity_en = 600
last_message_time_en = 9999999999
seconds_repeat_post_en = 1740
max_id_en = 10
min_id_en = 1
id_of_post_en = 1


def get_current_time_sec():
    #MEASURED IN SECONDS
    sec = int(round(time.time()))
    return sec

def get_last_message_time_en():
    global last_message_time_en
    return last_message_time_en

def select_time_en(user_id):
    c = conn.cursor()
    c.execute('select time from users_en where user_id = :user_id',  {'user_id' : user_id} )
    conn.commit()
    time = c.fetchone()[0]
    return time

def update_time_en(user_id):
    time = get_current_time_sec()
    conn.execute('update users_en set time = :time \
     where user_id = :user_id', {'user_id' : user_id, 'time' : time})
    conn.commit()


def add_text_post_en(text):
    conn.execute('insert into posts_en(text, file_id, type) \
     values (:text, null, "text")', {'text' : text,} )
    conn.commit()

def add_image_post_en(text, file_id, caption):
    conn.execute('insert into posts_en(text, file_id, type) \
     values (:text, :file_id, "image")', {'text' : caption, 'file_id' : file_id} )
    conn.commit()

def add_gif_post_en(text, file_id, caption):
    conn.execute('insert into posts_en(text, file_id, type) \
     values (:text, :file_id, "gif")', {'text' : caption, 'file_id' : file_id,} )
    conn.commit()

def add_text_info_post_en(text):
    conn.execute('insert into info_posts_en(text, file_id, type) \
     values (:text, null, "text")', {'text' : text,} )
    conn.commit()

def add_image_info_post_en(text, file_id, caption):
    conn.execute('insert into info_posts_en(text, file_id, type) \
     values (:text, :file_id, "image")', {'text' : caption, 'file_id' : file_id} )
    conn.commit()

def add_gif_info_post_en(text, file_id, caption):
    conn.execute('insert into info_posts_en(text, file_id, type) \
     values (:text, :file_id, "gif")', {'text' : caption, 'file_id' : file_id,} )
    conn.commit()


def get_max_id_en():
    c = conn.cursor()
    global max_id_en
    c.execute('select max(id) from info_posts_en;')
    conn.commit()
    max_id_en = c.fetchone()[0]
    return max_id_en

def get_min_id_en():
    c = conn.cursor()
    global min_id_en
    c.execute('select min(id) from info_posts_en;')
    conn.commit()
    min_id_en = c.fetchone()[0]
    return min_id_en

def delete_info_post_en(id):
    conn.execute('delete from info_posts_en where id = :id', {'id' : id,} )
    conn.commit()




def get_post_en(domains_dict):
    global en_group_chat_id
    global domains
    id_of_post = domains_dict['last_used_post_id_en']
    c = conn.cursor()
    c.execute('select * from posts_en where id = :id;',  {'id' : id_of_post} )
    conn.commit()
    row = c.fetchall()
    if row:
        try:
            type = row[0][3]
            if type == 'text':
                send_message(en_group_chat_id , row[0][1])
                #en group id
            if type == 'image':
                send_photo(en_group_chat_id, row[0][2], row[0][1])
            if type == 'gif':
                send_document(en_group_chat_id, row[0][2], row[0][1])
        except Exception:
            pass
        else:
            id_of_post += 1
            send_message(380162692, id_of_post_en)
            domains_dict['last_used_post_id_en'] = id_of_post
            domains = open("domains.json", 'w')
            domains.write(json.dumps(domains_dict))



def get_info_post_en():
    global en_group_chat_id
    global id_of_post_en
    c = conn.cursor()
    c.execute('select * from info_posts_en where id = :id;',  {'id' : id_of_post_en} )
    conn.commit()
    row = c.fetchall()
    if row:
        type = row[0][3]
        if type == 'text':
            send_message(en_group_chat_id, row[0][1])
            #_en group id
        if type == 'image':
            send_photo(en_group_chat_id, row[0][2], row[0][1])
        if type == 'gif':
            send_document(en_group_chat_id, row[0][2], row[0][1])
    else:
        id_of_post_en += 1
        get_info_post_en()


def no_activity_en():
    time.sleep(300)
    global seconds_no_activity_en
    posted_after_seconds_no_activity = False
    hour_post = 3600
    while True:
        if get_current_time_sec() - get_last_message_time_en() >= seconds_no_activity_en: #seconds_no_activity
            if get_current_time_sec() - get_last_message_time_en() >= hour_post: #hour_post
                get_post_en()
                hour_post += 3600
            else:
                if posted_after_seconds_no_activity == False:
                    get_post_en()
                    posted_after_seconds_no_activity = True
        else:
            hour_post = 3600
            posted_after_seconds_no_activity = False
        time.sleep(60)

def activity_en():
    user1_time = 70
    user2_time = 0
    user3_time = 2
    global max_id_en
    global min_id_en
    global id_of_post_en
    id_of_post_en = min_id_en
    c = conn.cursor()
    while True:
        c.execute('select time from users_en order by time desc;')
        conn.commit()
        row = c.fetchall()
        # gets time of two last messages of different users
        if row:
            user1_time = row[0][0]
            user1_time = int(user1_time)
            user2_time = row[1][0]
            user2_time = int(user2_time)
            user3_time = row[2][0]
            user3_time = int(user3_time)
        max_id_en = get_max_id_en()
        min_id_en = get_min_id_en()
        # is activity here
	#send_message(-1001276518306, get_current_time_sec())
        #send_message(-1001276518306, user1_time)
        if get_current_time_sec() - 120 <= user1_time:
            # is activity of 2 users here?
            if user1_time - user3_time <= 120:
                get_info_post_en()
                if id_of_post_en == max_id_en:
                    id_of_post_en = min_id_en
                else:
                        id_of_post_en += 1
                time.sleep(seconds_repeat_post_en)
        time.sleep(30)