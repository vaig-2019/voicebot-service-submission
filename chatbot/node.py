import chatbot.utils
import random


class Node:
    def __init__(self, nodej, chat_bot):
        self.nodej = nodej
        self.type = nodej["type"]
        self.id = nodej["id"]
        self.next = None
        self.type = nodej["type"]
        self.chat_bot = chat_bot
        self.id_next = -1
        self.content = nodej["content"]
        self.input_last = None

    def set_next(self, id_next):
        self.id_next = id_next

    def set_input(self, att=None):
        self.input_last = att

    def get_next(self):
        return self.id_next


class SpeakSentence(Node):
    def __init__(self, nodej, chat_bot):
        super().__init__(nodej=nodej, chat_bot=chat_bot)
        self.set_next(nodej["next_id"])

    def get_speak_sentence(self):
        rd = random.randrange(len(self.nodej["speak"]))
        # print(rd)
        speak = self.nodej["speak"][rd]["text"]
        check = False
        tmp = ""
        ans = ""
        for c in speak:
            if c == "<":
                check = True
            elif c == ">":
                ans += self.chat_bot.get_att(tmp)
                tmp = ""
                check = False
            else:
                if check:
                    tmp += c
                else:
                    ans += c

        return ans


class ChooseSentence(Node):
    def __init__(self, nodej, chat_bot):
        super().__init__(nodej=nodej, chat_bot=chat_bot)
        self.list_chooses = []
        self.attribute = nodej["att_name"]
        lchooses = self.nodej["list_choose"]
        for choose in lchooses:
            self.list_chooses.append((choose["content"], choose["regex"], choose["next_id"]))

    def select_a_choose(self, input):
        for choose in self.list_chooses:
            if chatbot.utils.check_choose(input, choose[1]):
                if self.attribute != "":
                    ct = choose[0]
                    self.chat_bot.add_att(self.attribute, ct)
                self.set_next(choose[2])
                return input
        return None


class InputSentence(Node):
    def __init__(self, nodej, chat_bot):
        super().__init__(nodej=nodej, chat_bot=chat_bot)
        self.data_type = nodej["data_type"]
        self.attribute = nodej["att_name"]

    def check_input(self, input):
        input = chatbot.utils.extract_data(input, self.data_type)
        check = chatbot.utils.check_input_type(input, self.data_type)
        if check:
            self.chat_bot.add_att(self.attribute, input)
            self.set_next(self.nodej["next_id"])
        else:
            inext = self.nodej["except"]
            if inext != 0:
                self.set_next(inext)
                check = True
        return check


class MainQuestion(Node):
    def __init__(self, nodej, chat_bot):
        super().__init__(nodej=nodej, chat_bot=chat_bot)
        self.question = nodej["regex"]
        self.set_next(nodej["next_id"])

    def check_question(self, input):
        if self.question is None:
            return False
        return chatbot.utils.check_start_question(input, self.question)


class SolveCase(Node):
    def __init__(self, nodej, chat_bot):
        super().__init__(nodej, chat_bot=chat_bot)
        self.action = self.nodej["solve"]
        self.list_answers = []
        self.attribute = self.nodej["attribute"]
        self.data_type = self.nodej["data_type"]
        jans = nodej["list_resp"]
        for a in jans:
            self.list_answers.append((a["text"], a["next_id"]))

    def save(self,name_att, input, data_type):
        print(name_att, input, data_type)
        data = chatbot.utils.extract_data(input, data_type)
        self.chat_bot.add_att(name_att, data)
        ans = self.chat_bot.save_user()
        if ans == "NEW":
            self.set_next(self.list_answers[1][1])
        else:
            self.set_next(self.list_answers[0][1])
        return ans

    def qa(self, input):
        ans = chatbot.utils.try_answer(input)
        if ans == "NEW":
            self.set_next(self.list_answers[1][1])
            return "NEW"
        else:
            self.chat_bot.add_att("TRALOI", ans)
            self.set_next(self.list_answers[0][1])
            return "EXITS"

    def solve(self, input=None):
        if input is None:
            input = self.input_last
        print("action: " , self.action)
        if self.action == "save":
            return self.save(self.attribute, input, self.data_type)
        if self.action == "qa":
            return self.qa(input)
        # self.
        # if self.func == "SAVE_NUMBER_PHONE":
        #     return self.save_number_phone()
        # elif self.func == "SAVE_ADDRESS":
        #     return self.save_address()
        # elif self.func == "CHECK_INFO":
        #     return self.check_info()
        # elif self.func == "SHOW_REQUEST":
        #     return self.show_request()
        # elif self.func == "SAVE_DATE":
        #     return self.save_date()
        # elif self.func == "SAVE_TIME":
        #     return self.save_time()
        # elif self.func == "SHOW_MEET_TIME":
        #     return self.show_meet_time()
        # else:
        #     pass
