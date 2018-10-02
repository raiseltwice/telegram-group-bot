import sqlite3

conn = sqlite3.connect('bot_final.db', check_same_thread=False)


allow_pics_gifs_ch = True
allow_links_ch = True




def insert_db_ch(user_id):
    time = get_current_time_sec()
    conn.execute('insert or ignore into users_ch(user_id, time, warnings) \
     select :user_id, :time, 0 where not exists \
      (select * from users_ch where user_id = :user_id)', {'user_id' : user_id, 'time': time} )
    conn.commit()

def select_amount_warnings_ch(user_id):
    c = conn.cursor()
    c.execute('select warnings from users_ch where user_id = :user_id',  {'user_id' : user_id} )
    conn.commit()
    amount = c.fetchone()[0]
    return amount

def update_warnings_ch(user_id, warnings):
    conn.execute('update users_ch set warnings = :warnings \
     where user_id = :user_id', {'user_id' : user_id, 'warnings' : warnings})
    conn.commit()


def insert_restriction_ch(from_id, is_voted, for_id):
    conn.execute('insert or ignore into restriction_ch(id, time, is_voted,for_id) \
     values (:id, :time, :is_voted, :for_id);', {'id' : from_id, 'time' : get_current_time_sec(), 'is_voted' : is_voted, 'for_id' : for_id} )
    conn.commit()

def mute_insert_restriction_ch(from_id, is_voted, for_id):
    conn.execute('insert or ignore into mute_restriction_ch(id, time, is_voted,for_id) \
     values (:id, :time, :is_voted, :for_id);', {'id' : from_id, 'time' : get_current_time_sec(), 'is_voted' : is_voted, 'for_id' : for_id} )
    conn.commit()


def is_voted_ch(id,for_id):
    c = conn.cursor()
    c.execute('select is_voted from restriction_ch where id = :id and for_id = :for_id;',{'id': id, 'for_id': for_id})
    conn.commit()
    is_voted = c.fetchone()[0]
    return is_voted

def mute_is_voted_ch(id,for_id):
    c = conn.cursor()
    c.execute('select is_voted from mute_restriction_ch where id = :id and for_id = :for_id;',{'id': id, 'for_id': for_id})
    conn.commit()
    is_voted = c.fetchone()[0]
    return is_voted


def set_voted_ch(id, for_id):
    conn.execute('update restriction_ch \
     set is_voted = 1 where id = :id and for_id = :for_id', {'id': id, 'for_id': for_id} )
    conn.commit()

def mute_set_voted_ch(id, for_id):
    conn.execute('update mute_restriction_ch \
     set is_voted = 1 where id = :id and for_id = :for_id', {'id': id, 'for_id': for_id} )
    conn.commit()


def get_max_time_restriction_ch():
    c = conn.cursor()
    c.execute('select max(time) from restriction_ch;')
    conn.commit()
    time = c.fetchone()[0]
    return time

def mute_get_max_time_restriction_ch():
    c = conn.cursor()
    c.execute('select max(time) from mute_restriction_ch;')
    conn.commit()
    time = c.fetchone()[0]
    return time

def insert_to_ban_ch(id):
    conn.execute('insert into restriction_user_ch(id, amount) \
     values (:id, 1)', {'id' : id} )
    conn.commit()

def update_to_ban_ch(id):
    conn.execute('update restriction_user_ch \
     set amount = ((select amount from restriction_user_ch where id = :id)+1) where id = :id', {'id' : id} )
    conn.commit()


def insert_to_mute_ch(id):
    conn.execute('insert into mute_restriction_user_ch(id, amount) \
     values (:id, 1)', {'id' : id} )
    conn.commit()

def update_to_mute_ch(id):
    conn.execute('update mute_restriction_user_ch \
     set amount = ((select amount from mute_restriction_user_ch where id = :id)+1) where id = :id', {'id' : id} )
    conn.commit()

def get_amount_of_votes_ch(id):
    c = conn.cursor()
    c.execute('select amount from restriction_user_ch where id = :id;',{'id': id})
    conn.commit()
    amount = c.fetchone()[0]
    return amount

def mute_get_amount_of_votes_ch(id):
    c = conn.cursor()
    c.execute('select amount from mute_restriction_user_ch where id = :id;',{'id': id})
    conn.commit()
    amount = c.fetchone()[0]
    return amount


def general_restr_ch(id):
    c = conn.cursor()
    c.execute('select * from restriction_user_ch where id = :id', {'id' : id})
    conn.commit()
    res = c.fetchall()
    if res:
        update_to_ban_ch(id)
    else:
        insert_to_ban_ch(id)

def mute_general_restr_ch(id):
    c = conn.cursor()
    c.execute('select * from mute_restriction_user_ch where id = :id', {'id' : id})
    conn.commit()
    res = c.fetchall()
    if res:
        update_to_mute_ch(id)
    else:
        insert_to_mute_ch(id)


def usage_of_warnings_ch(from_id, chat_id, username, message_id_to_be_deleted):
    if(select_amount_warnings_ch(from_id) == 0):
        delete_message(chat_id, message_id_to_be_deleted)
        text = loc_ch_dict["warning"]
        text = text.replace("xxxx", username)
        send_message(chat_id, text)
        update_warnings_ch(from_id, 1)
    else:
        kick_chat_member(chat_id, from_id)
        delete_message(chat_id, message_id_to_be_deleted)




def usage_of_warnings_ch_mute(from_id, chat_id, username, message_id_to_be_deleted):
    if(select_amount_warnings_ch(from_id) == 0):
        delete_message(chat_id, message_id_to_be_deleted)
        text = loc_ch_dict["warning"]
        text = text.replace("xxxx", username)
        send_message(chat_id, text)
        update_warnings_ch(from_id, 1)
    else:
        restrict_chat_member(chat_id, from_id, get_current_time_sec() + 86400)
        delete_message(chat_id, message_id_to_be_deleted)

