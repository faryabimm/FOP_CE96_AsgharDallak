import requests
from time import sleep
import re


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, params)
        result_json = response.json()['result']
        return result_json

    def send_message(self, chat_id, message_text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': message_text}
        response = requests.post(self.api_url + method, params)
        return response

    def get_last_update(self):
        updates = self.get_updates()
        if len(updates) > 0:
            last_update = updates[-1]
        else:
            last_update = updates[len(updates)]
        return last_update

    def get_first_update(self):
        updates = self.get_updates()
        if len(updates) > 0:
            first_update = updates[0]
        else:
            first_update = updates[len(updates)]
        return first_update


asghar_bot_token = '473254991:AAGin-zxdn4EZ7--ikuHdbRNJ4_ZiqVXssI'
asghar_bot_handler = BotHandler(asghar_bot_token)
student_list = [
    "96101121",
    "96101913",
    "96105864",
    "96105904",
    "96105915",
    "96106066",
    "96106099",
    "96109588",
    "96109599",
    "96109652",
    "96110272",
    "96110294"]

pattern = re.compile('961\d{5}')


def main():
    try:
        new_offset = None
        while True:
            asghar_bot_handler.get_updates(new_offset)
            last_update = asghar_bot_handler.get_first_update()

            last_update_id = last_update['update_id']
            last_stdid = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_first_name = last_update['message']['chat']['first_name']

            print(last_stdid)



            if last_stdid == '/start':
                message_to_send = "لطفا شماره دانشجوییتو دقیق و با ارقام انگلیسی وارد کن"
            elif not pattern.match(last_stdid):
                message_to_send = "این چیزی که وارد کردی شماره دانشجویی نیست که 😐"
            else:

                if last_stdid in student_list:
                    message_to_send = last_first_name + " عزیز" + "\n" + "شما باید تمرین اضافی اصغر رو انجام بدید!"
                else:
                    message_to_send = last_first_name + "عزیز" + "\n" + \
                                      "شما دارید با سرعت مطمئن حرکت می‌کنید! نیازی به انجام تمرین اضافی اصغر نیست!" + \
                                      "اگه دوست دارید میتونید برای تمرین بیشتر به بررسی اون بپردازید."
            asghar_bot_handler.send_message(last_chat_id, message_to_send)

            new_offset = last_update_id + 1
    except Exception:
        print("Restarting")
        main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
