from chatbot.static import *
from chatbot.node import MainQuestion, SpeakSentence, InputSentence, SolveCase, ChooseSentence
from chatbot.utils import read_json


class Script:
    def __init__(self, chat_bot):
        script_json = read_json(SCRIPT_FILE)
        self.list_node = []
        self.chat_bot = chat_bot
        self.chat_bot.init_att(script_json["attribute"])
        # init SCRIPT
        ########################### CHANGE THIS ##################################
        self.id = script_json["id"]
        self.func = script_json["function"]
        self.name = script_json["name"]
        self.lscript = script_json["script"]

        for nodej in self.lscript:
            type = nodej["type"]
            if type == "start":
                node = MainQuestion(nodej, chat_bot=chat_bot)
            elif type == "speak":
                node = SpeakSentence(nodej, chat_bot=chat_bot)
            elif type == "input":
                node = InputSentence(nodej, chat_bot=chat_bot)
            elif type == "solve":
                node = SolveCase(nodej, chat_bot=chat_bot)
            else:
                node = ChooseSentence(nodej, chat_bot=chat_bot)
            self.list_node.append(node)

        ##########################################################################
        self.id_now = 0

    def get_start_node(self):
        if len(self.list_node) == 0:
            return None
        return self.list_node[0]

    def get_node(self):
        if self.id_now == -1:
            return None
        return self.list_node[self.id_now]

    def next_node(self, attribute=None):
        self.id_now = self.list_node[self.id_now].get_next()
        if self.get_node() is not None:
            self.get_node().set_input(attribute)

    def reset(self):
        self.__init__(self.chat_bot)

