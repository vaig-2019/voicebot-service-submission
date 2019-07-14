import sys
from chatbot.script import Script
from flask import jsonify
from chatbot.static import USER_INFO, SESSION_LIVE_TIME, FINISH_CONVERSATION, ERROR_CHOOSE, ERROR_INPUT
import time
from chatbot.user import User
from chatbot.utils import read_json
from chatbot.utils import write_json


class Bot:
    def __init__(self):
        self.list_speaks = []
        self.born_time = time.time()
        self.attributes = {}
        self.stop = False
        self.user = User()
        self.script = Script(self)

    def reset_time(self):
        self.born_time = time.time()

    def check_over_time(self):
        if time.time() - self.born_time > SESSION_LIVE_TIME:
            return True
        return False

    def add_att(self, key, val):
        self.attributes[key] = str(val)

    def save_user(self):
        ans = "NEW"
        user_info = read_json(USER_INFO)
        # print(user_info)
        for idx, user in enumerate(user_info):
            if user["ATT_PHONE"] == self.attributes["ATT_PHONE"]:
                del user_info[idx]
                ans = "EXITS"
                break
        user_info.append(self.attributes)
        write_json(USER_INFO, user_info)
        return ans

    def get_att(self, att):
        if att in self.attributes:
            return self.attributes[att]
        return ""

    def init_att(self, la):
        for x in la:
            # print(x)
            self.add_att(x["name"], x["value"])

    def solved(self, prob, ok):
        pass

    def speak(self, sentence):
        return sentence
        # return jsonify({"answer": sentence})

    def listen(self):
        sentence = sys.stdin.readline()
        sentence = sentence[0:len(sentence) - 1]
        return sentence
        # return jsonify({"answer": sentence})

    def next_sentence(self, input=None):
        script = self.script
        if self.stop:
            return [FINISH_CONVERSATION]
        node = script.get_node()
        if node is None:
            self.stop = True
            self.script.reset()
            return self.next_sentence()
        if not node.type == "speak":
            self.list_speaks = []
        if node.type == "speak":
            ans = self.speak(node.get_speak_sentence())
            script.next_node()
            self.list_speaks.append(ans)
            if script.get_node() is None or not script.get_node().type == "speak":
                return self.list_speaks
            return self.next_sentence()
        elif node.type == "start":
            if input is None:
                input = ""
            sentence = input
            if not node.check_question(sentence):
                ans = self.speak(FINISH_CONVERSATION)
                return [ans]
            else:
                script.next_node()
        elif node.type == "input":
            if input is None:
                return None
            input = input
            if node.check_input(input):
                script.next_node(input)
            else:
                return [self.speak(ERROR_INPUT)]
        elif node.type == "solve":
            answer = node.solve(input)
            # print(answer)
            # self.solved(node.func, answer)
            script.next_node(answer)
        else:
            if input is None:
                return [self.speak(ERROR_CHOOSE)]
            input = node.select_a_choose(input.lower())
            # print(node.type, bot.user_request)
            if input is None:
                return [self.speak(ERROR_CHOOSE)]
            else:
                input = input
                if node.type == "choose_req":
                    self.user.set_request(self.user.request + (input + "::"))
                script.next_node(input)
        return self.next_sentence()
