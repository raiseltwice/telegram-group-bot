import sqlite3

conn = sqlite3.connect('bot_final.db', check_same_thread=False)
loc_ch_dict = {}
domains = open("domains.json", 'r')
loc_ch_dict_file = open("localization_ch.json")
loc_ch_dict = json.load(loc_ch_dict_file)
domains_dict = json.load(domains)


ch_group_chat_id = -100XXX
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

def get_last_message_time_ch():
    global last_message_time_ch
    return last_message_time_ch

    
def select_time_ch(user_id):
    c = conn.cursor()
    c.execute('select time from users_ch where user_id = :user_id',  {'user_id' : user_id} )
    conn.commit()
    time = c.fetchone()[0]
    return time

def update_time_ch(user_id):
    time = get_current_time_sec()
    conn.execute('update users_ch set time = :time \
     where user_id = :user_id', {'user_id' : user_id, 'time' : time})
    conn.commit()


def add_text_post_ch(text):
    conn.execute('insert into posts_ch(text, file_id, type) \
     values (:text, null, "text")', {'text' : text,} )
    conn.commit()

def add_image_post_ch(text, file_id, caption):
    conn.execute('insert into posts_ch(text, file_id, type) \
     values (:text, :file_id, "image")', {'text' : caption, 'file_id' : file_id} )
    conn.commit()

def add_gif_post_ch(text, file_id, caption):
    conn.execute('insert into posts_ch(text, file_id, type) \
     values (:text, :file_id, "gif")', {'text' : caption, 'file_id' : file_id,} )
    conn.commit()

def add_text_info_post_ch(text):
    conn.execute('insert into info_posts_ch(text, file_id, type) \
     values (:text, null, "text")', {'text' : text,} )
    conn.commit()

def add_image_info_post_ch(text, file_id, caption):
    conn.execute('insert into info_posts_ch(text, file_id, type) \
     values (:text, :file_id, "image")', {'text' : caption, 'file_id' : file_id} )
    conn.commit()

def add_gif_info_post_ch(text, file_id, caption):
    conn.execute('insert into info_posts_ch(text, file_id, type) \
     values (:text, :file_id, "gif")', {'text' : caption, 'file_id' : file_id,} )
    conn.commit()


def get_max_id_ch():
    c = conn.cursor()
    global max_id_ch
    c.execute('select max(id) from info_posts_ch;')
    conn.commit()
    max_id_ch = c.fetchone()[0]
    return max_id_ch

def get_min_id_ch():
    c = conn.cursor()
    global min_id_ch
    c.execute('select min(id) from info_posts_ch;')
    conn.commit()
    min_id_ch = c.fetchone()[0]
    return min_id_ch

def delete_info_post_ch(id):
    conn.execute('delete from info_posts_ch where id = :id', {'id' : id,} )
    conn.commit()





def get_post_ch(domains_dict):
    global ch_group_chat_id
    global domains
    id_of_post = domains_dict['last_used_post_id_ch']
    c = conn.cursor()
    c.execute('select * from posts_ch where id = :id;',  {'id' : id_of_post} )
    conn.commit()
    row = c.fetchall()
    if row:
        type = row[0][3]
        if type == 'text':
            send_message(ch_group_chat_id, row[0][1])
            #_ch group id
        if type == 'image':
            send_photo(ch_group_chat_id, row[0][2], row[0][1])
        if type == 'gif':
            send_document(ch_group_chat_id, row[0][2], row[0][1])
        id_of_post += 1
        domains_dict['last_used_post_id_ch'] = id_of_post
        domains = open("domains.json", 'w')
        domains.write(json.dumps(domains_dict))



def get_info_post_ch():
    global id_of_post_ch
    global ch_group_chat_id
    c = conn.cursor()
    c.execute('select * from info_posts_ch where id = :id;',  {'id' : id_of_post_ch} )
    conn.commit()
    row = c.fetchall()
    if row:
        type = row[0][3]
        if type == 'text':
            send_message(ch_group_chat_id, row[0][1])
            #_ch group id
        if type == 'image':
            send_photo(ch_group_chat_id, row[0][2], row[0][1])
        if type == 'gif':
            send_document(ch_group_chat_id, row[0][2], row[0][1])
    else:
        id_of_post_ch += 1
        get_info_post_ch()


def no_activity_ch():
    posted_after_seconds_no_activity = False
    hour_post = 3600
    while True:
        if get_current_time_sec() - get_last_message_time_ch() >= seconds_no_activity_ch: #seconds_no_activity
            if get_current_time_sec() - get_last_message_time_ch() >= hour_post: #hour_post
                get_post_ch()
                hour_post += 3600
            else:
                if posted_after_seconds_no_activity == False:
                    get_post_ch()
                    posted_after_seconds_no_activity = True
        else:
            hour_post = 3600
            posted_after_seconds_no_activity = False
        time.sleep((seconds_no_activity_ch / 10) - 5)

def activity_ch():
    user1_time = 70
    user2_time = 0
    global max_id_ch
    global min_id_ch
    global id_of_post_ch
    id_of_post_ch = min_id_ch
    c = conn.cursor()
    while True:
        c.execute('select time from users_ch order by time desc;')
        conn.commit()
        row = c.fetchall()
        # gets time of two last messages of different users
        if row:
            user1_time = row[0][0]
            user1_time = int(user1_time)
            user2_time = row[1][0]
            user2_time = int(user2_time)
        max_id_ch = get_max_id_ch()
        min_id_ch = get_min_id_ch()
        # is activity here
        if get_current_time_sec() - 60 <= user1_time:
            # is activity of 2 users here?
            if user1_time - user2_time <= 60:
                get_info_post_ch()
                if id_of_post_ch == max_id_ch:
                    id_of_post_ch = min_id_ch
                else:
                        id_of_post_ch += 1

                time.sleep(seconds_repeat_post_ch)
        time.sleep(60)
