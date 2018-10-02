import requests


URL = 'https://api.telegram.org/botXXX/'


def send_message(chat_id, text):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text }
    requests.post(url, json=answer)

def delete_message(chat_id, message_id):
    url = URL + 'deleteMessage'
    answer = {'chat_id': chat_id, 'message_id': message_id }
    requests.post(url, json=answer)

def restrict_chat_member(chat_id, user_id, time):
    url = URL + 'restrictChatMember'
    answer = {'chat_id': chat_id, 'user_id': user_id, 'until_date': time , \
     'can_send_messages': False, 'can_send_media_messages': False, 'can_send_other_messages': False, \
      'can_add_web_page_previews': False }
    requests.post(url, json=answer)

def kick_chat_member(chat_id, user_id):
    url = URL + 'kickChatMember'
    answer = {'chat_id': chat_id, 'user_id': user_id, 'until_date': get_current_time_sec() + 1 }
    requests.post(url, json=answer)

def get_chat_member(chat_id, user_id):
    url = URL + 'getChatMember'
    answer = {'chat_id': chat_id, 'user_id': user_id}
    response = requests.post(url, json=answer)
    return response.json()

def send_photo(chat_id, file_id, caption):
    url = URL + 'sendPhoto'
    answer = {'chat_id': chat_id, 'photo': file_id, 'caption' : caption}
    response = requests.post(url, json=answer)

def send_document(chat_id, file_id, caption):
    url = URL + 'sendDocument'
    answer = {'chat_id': chat_id, 'document': file_id, 'caption' : caption}
    response = requests.post(url, json=answer)

def set_webhook():
    url = URL + 'sendDocument'
    answer = {'chat_id': 'https://167.99.124.27:8443', 'certificate': file_id, 'caption' : caption}
    response = requests.post(url, json=answer)