import json
import os
import random

import regex as re

dir_path = os.path.dirname(os.path.realpath(__file__))

END_SIGNAL = "_END_."
USER_BUSY = 1
USER_REJECT = 2


def get_random_item(messages):
    if messages is None or len(messages) == 0:
        return None
    return random.choice(messages)


class TelesaleBot:
    def __init__(self, bot_data=os.path.join(dir_path, 'stories.json')):
        bot_data = json.load(open(bot_data, encoding='utf8'))
        self.user = get_random_item(bot_data["paras"]["users"])
        self.welcome_message = bot_data["welcome_message"]
        self.fail_message = bot_data["fail_message"]
        self.pass_message = bot_data["pass_message"]
        self.busy_message = bot_data["busy_message"]
        self.again_message = bot_data["again_message"]
        self.regex_para = bot_data["regex_para"]
        self.classify_regex = bot_data["classify_regex"]
        self.welcomed = False
        self.ended = False

    def interactive(self, user_message=None):
        if not self.welcomed:
            self.welcomed = True
            return self.fill_message_para(get_random_item(self.welcome_message))
        else:
            if user_message is None or len(user_message) == 0:
                return self.fill_message_para(get_random_item(self.again_message) + END_SIGNAL)
            case = self.classify(user_message)
            if case == USER_REJECT:
                return self.fill_message_para(get_random_item(self.fail_message) + END_SIGNAL)
            elif case == USER_BUSY:
                return self.fill_message_para(get_random_item(self.busy_message) + END_SIGNAL)
            else:
                return self.fill_message_para(get_random_item(self.pass_message) + END_SIGNAL)

    def fill_message_para(self, message):
        paras = re.findall(self.regex_para, message)
        for para in paras:
            message = re.sub(para, self.user.get(para), message)
        return re.sub("\\s+", " ", message).strip()

    def classify(self, user_message):
        for pattern in self.classify_regex["busy"]:
            if re.match(pattern, user_message):
                return USER_BUSY
        for pattern in self.classify_regex["reject"]:
            if re.match(pattern, user_message):
                return USER_REJECT


def interactive():
    bot = TelesaleBot()
    bot_mess = bot.interactive()
    while True:
        print(bot_mess.replace(END_SIGNAL, ""))
        if bot_mess.endswith(END_SIGNAL):
            break
        message = input('> ')
        bot_mess = bot.interactive(user_message=message)


if __name__ == '__main__':
    interactive()
