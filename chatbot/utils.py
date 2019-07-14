import re
import datetime
import json
from chatbot.static import QA_FILE, QA_KEYWORD, MEDICINE_NAME
from wit import Wit
import random
import traceback

access_token = "IMR2QK2LRAF4KEIPWGK72UOYALF366FG"
client = Wit(access_token)


def wit_mess(input):
    try:
        return client.message(input)
    except:
        return {'entities': {}}

def write_json(filename, js):
    with open(filename, 'w',  encoding='utf8') as f:
        json.dump(js, f)


def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


jf_question = read_json(QA_KEYWORD)
jf_medicine = read_json(MEDICINE_NAME)
ljs = read_json(QA_FILE)


def check_start_question(input, questions):
    for q in questions:
        if len(re.findall(q["text"], input)) != 0:
            return True
    return False


def check_choose(input, chooses):
    for choose in chooses:
        rg = choose["text"]
        if rg.startswith("WIT"):
            mch = rg.split("|", 1)[1]
            resp = wit_mess(input)
            entities = resp["entities"]
            if 'intent' in entities:
                intent = entities['intent'][0]['value']
            else:
                continue
            print("intent:", intent, mch)
            if intent == mch:
                return True
        elif len(re.findall(rg, input)) != 0:
            return True
    return False


def check_number_int(x):
    x = str(x)
    if x == "":
        return False
    for c in x:
        if not c.isdecimal():
            return False
    return True


def check_string(input):
    return input is not None and len(input) != 0


def check_date(input):
    try:
        datetime.datetime.strptime(input, '%d-%m-%Y')
    except ValueError:
        try:
            datetime.datetime.strptime(input, '%d/%m/%Y')
        except ValueError:
            try:
                datetime.datetime.strptime(input, '%d,%m,%Y')
            except ValueError:
                try:
                    datetime.datetime.strptime(input, '%Y,%m,%d')
                except ValueError:
                    return False
    return True


def check_time(input):
    return input is not None
    # return len(re.findall("....-..-..T..:..:.......+..:..", input)) != 0
    # return True


def get_time(itime):
    return itime.split("T",1)[1]

def get_date(itime):
    return itime.split("T",1)[0]

def check_input_type(input, input_type):
    if input_type == "NUMBER":
        return check_number_int(input)
    if input_type == "ADDRESS":
        return check_string(input)
    if input_type == "DATE":
        return check_date(input)
    if input_type == "TIME":
        return check_time(input)
    return True


def extract_data(input, input_type):
    if input_type == "NUMBER":
        return input
    if input_type == "ADDRESS":
        resp = wit_mess(input)
        entities = resp["entities"]
        if 'location' not in entities:
            input = None
        return input
    if input_type == "DATE":
        resp = wit_mess(input)
        entities = resp["entities"]
        if 'datetime' not in entities:
            return input
        else:
            if 'to' in entities['datetime'][0]['values'][0]:
                return entities['datetime'][0]['values'][0]['to']['value']
            return entities['datetime'][0]['values'][0]['value']
    if input_type == "TIME":
        ans = wit_mess(input)
        # print("ANS:" , ans)
        ans = get_time_speak(ans)
        # print("ANS:" , ans)
        return ans
    return input



def get_time_speak(wit_respond):
    try:
        responds = []
        entities = wit_respond["entities"]
        if 'datetime' in entities:
            time_value = entities["datetime"][0]["values"][0]["value"]
            # out: 2019-07-12T16:02:51.000+07:00
            time_value = re.sub(r"\.\d+\+.+", "", time_value)
            time_value = datetime.datetime.strptime(time_value, "%Y-%m-%dT%H:%M:%S")
            time = time_value.time()
            date = time_value.date()

            if date == datetime.datetime.now().date():
                responds.append(time.strftime("%H:%M"))
            if date - datetime.timedelta(days=1) == datetime.datetime.now():
                responds.append(time.strftime("%H:%M") + " ngày mai")
            responds.append("{} ngày {}".format(time.strftime("%H:%M"), date.strftime("%d/%m")))
        elif 'duration' in entities:
            duration_second = entities["duration"][0]["normalized"]["value"]
            time_value = (datetime.datetime.now() + datetime.timedelta(seconds=duration_second)).time()
            responds.append(time_value.strftime("%H:%M"))
            responds.append(time_value.strftime("%H:%M") + " hôm nay")
            responds.append(time_value.strftime("%H:%M") + " ngày hôm nay")
            responds.append(
                time_value.strftime("%H:%M") + " ngày {}".format(datetime.datetime.now().date().strftime("%d/%m")))
            if duration_second < 3600:
                responds.append("{} phút nữa".format(duration_second // 60))
                responds.append("{} phút sau".format(duration_second // 60))
            else:
                if duration_second % 3600 == 0:
                    responds.append("{} tiếng nữa".format(duration_second // 3600))
                    responds.append("{} tiếng sau".format(duration_second // 3600))
                    responds.append("{} giờ nữa".format(duration_second // 3600))
                    responds.append("{} giờ sau".format(duration_second // 3600))
                else:
                    responds.append("{}:{} nữa".format(duration_second // 3600, duration_second % 3600 // 60))
        return random.choice(responds)
    except:
        # traceback.print_exc()
        return None

######################################################### QA #########################################################
def extract_medicine_name(input):
    for x in jf_medicine:
        for y in x['text']:
            if y in input:
                return x['medicine_name']
    return ""


def extract_type_question(input):
    for x in jf_question:
        for y in x['text']:
            if y in input:
                return x['type_quetion']
    return ""


def try_answer(input):

    medicine_name = extract_medicine_name(input)
    type_question = extract_type_question(input)

    print(medicine_name, type_question)

    for qa in ljs:
        if qa["medicine_name"] == medicine_name and qa["type_quetion"] == type_question:
            print("QUESTION same : " + qa["question"])
            print("ANSWER: " + qa["answer"])
            return qa["answer"]
    return "NEW"

# print(client.message("mua thuốc tràng phục linh ở đâu ?"))