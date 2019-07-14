from concurrent import futures
import os
import uuid
import time
import json
import redis
import requests
from datetime import datetime
import traceback
import logging
logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logging.INFO)

import grpc

from chatbot.bot import Bot
from pizzabot.pizza_bot import PizzaBot

import voicebot_pb2
import voicebot_pb2_grpc
import streaming_voice_pb2
import streaming_voice_pb2_grpc

import config

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
DUOC_CALL_IN = '18001111'
DUOC_CALL_OUT = '18002222'
PIZZA_CALL_IN = '18003333'
PIZZA_CALL_OUT = '18004444'

class VoiceBot(voicebot_pb2_grpc.VoiceBotServicer):
    ERROR = -1
    SUCCESS = 200

    def __init__(self):
        logging.info("VoiceBot service started!")
        self.redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

    def ListCallCenter(self, request, context):
        list_call_center_response = voicebot_pb2.ListCallCenterResponse()
        for code, name, _ in config.CALL_CENTERS:
            call_center = voicebot_pb2.CallCenter(code=code, name=name)
            list_call_center_response.call_centers.append(call_center)
        return list_call_center_response

    def _VoiceBotRequest2VoiceRequest(self, request_iterator):
        try:
            for request in request_iterator:
                yield streaming_voice_pb2.VoiceRequest(byte_buff=request.audio_content)
        except GeneratorExit:
            return
        except:
            logging.error(traceback.format_exc())

    def _SpeechToText(self, client_id, request_iterator):
        with grpc.insecure_channel(config.ASR_URI) as channel:
            metadata = [
                ('channels', '1'), 
                ('rate', '16000'), 
                ('format', 'S16LE'), 
                ('single_sentence', 'False'), 
                ('token', 'voicebot'), 
                ('id', 'test_id')]
            streaming_voice_stub = streaming_voice_pb2_grpc.StreamVoiceStub(channel)
            response_interator = streaming_voice_stub.SendVoice(self._VoiceBotRequest2VoiceRequest(request_iterator), metadata=metadata)
            try:
                status_success = voicebot_pb2.Status(
                    code=VoiceBot.SUCCESS, 
                    message="Voicebot hearing ...")
                for text_reply in response_interator:
                    sentence = text_reply.result.hypotheses[0].transcript
                    if text_reply.result.final:
                        logging.info("{}\t_SpeechToText | Final: {}".format(client_id, sentence))
                        yield status_success, sentence, True
                    else:
                        logging.info("{}\t_SpeechToText: {}".format(client_id, sentence))
                        yield status_success, sentence, False

            except GeneratorExit:
                return
            except:
                status_error = voicebot_pb2.Status(
                    code=VoiceBot.ERROR, 
                    message="ASR Service not working!")
                logging.error(traceback.format_exc())
                yield status_error, "", True

    def _TextToText_Duoc_CallOut(self, client_id, request_iterator):
        try:
            bot_duoc = Bot()
            status_success = voicebot_pb2.Status(
                code=VoiceBot.SUCCESS, 
                message="Voicebot thinking ...")
            text_response = bot_duoc.next_sentence("alo")
            resp = ""
            for token in text_response:
                resp += token + "."
            text_response = resp.replace("..",".")
            logging.info("{}\t_TextToText: {}".format(client_id, text_response))
            yield status_success, "", True, text_response
            for status, text, final in request_iterator:
                if status.code == VoiceBot.ERROR:
                    yield status, ""
                    break
                if not final:
                    yield status_success, text, False, ""
                else:
                    ## BOT HERE ##
                    # text_bot = "ha ha buồn cười quá"
                    text_ask = text
                    text_response = bot_duoc.next_sentence(text_ask)
                    resp = ""
                    for token in text_response:
                        resp += token + "."
                    text_response = resp.replace("..",".")
                    ##############
                    logging.info("{}\t_TextToText: {}".format(client_id, text_response))
                    if 'END' in text_response:
                        return
                    yield status_success, text, True, text_response
        except GeneratorExit:
            return
        except:
            status_error = voicebot_pb2.Status(
                code=VoiceBot.ERROR, 
                message="NLU Service not working!")
            logging.error(traceback.format_exc())
            yield status_error, "", True, ""

    def _TextToText_Pizza_CallIn(self, client_id, request_iterator):
        try:
            pizza_bot = PizzaBot()
            status_success = voicebot_pb2.Status(
                code=VoiceBot.SUCCESS, 
                message="Voicebot thinking ...")
            text_response = pizza_bot.interactive()
            logging.info("{}\t_TextToText: {}".format(client_id, text_response))
            yield status_success, "", True, text_response
            for status, text, final in request_iterator:
                if status.code == VoiceBot.ERROR:
                    yield status, "", True, ""
                    break
                if not final:
                    yield status_success, text, False, ""
                else:
                    ## BOT HERE ##
                    # text_bot = "ha ha buồn cười quá"
                    text_ask = text
                    text_response = pizza_bot.interactive(user_message=text_ask)
                    ##############
                    logging.info("{}\t_TextToText: {}".format(client_id, text_response))
                    if 'END' in text_response:
                        return
                    yield status_success, text, True, text_response
        except GeneratorExit:
            return
        except:
            status_error = voicebot_pb2.Status(
                code=VoiceBot.ERROR, 
                message="NLU Service not working!")
            logging.error(traceback.format_exc())
            yield status_error, "", True, ""

    def _TextToSpeech(self, client_id, request_iterator, timeout=5):
        try:
            for status, text_asr, final, text_bot in request_iterator:
                if status.code == VoiceBot.ERROR:
                    yield voicebot_pb2.VoiceBotResponse(status=status)
                    return
                # If text not final, return asr text only
                if not final:
                    yield voicebot_pb2.VoiceBotResponse(
                        status=status,
                        text_asr=text_asr,
                        final=False)
                # If text final Process audio and response
                else:
                    audio_url = None
                    try:
                        response = requests.post(config.TTS_URL, data={'text': text_bot, 'voice': 'doanngocle_1_unnorm_cpu'}, timeout=config.TTS_TIMEOUT)
                        if response.status_code != 200:
                            logging.warn("{}\t_TextToSpeech | Error {}!".format(client_id, response.status_code))
                        else:
                            result = response.json()
                            if result['success']:
                                audio_url = result['audio_path']
                                logging.info("{}\t_TextToSpeech: {}".format(client_id, audio_url))
                                if 'end2end' not in audio_url:
                                    requests.post(config.TTS_CACHE, data={'text': text_bot})
                                    logging.info("{}\t_TextToSpeech | Request for cache".format(client_id))
                            else:
                                logging.warn("{}\t_TextToSpeech: {}".format(client_id, result.msg))
                    except requests.Timeout:
                        logging.warn("{}\t_TextToSpeech | Timeout".format(client_id))
                    except:
                        logging.warn("{}\t_TextToSpeech | Not working".format(client_id))
                    yield voicebot_pb2.VoiceBotResponse(
                        status=voicebot_pb2.Status(
                            code=VoiceBot.SUCCESS, 
                            message="Voicebot speaking"),
                        text=text_bot,
                        audio_url=audio_url,
                        text_asr=text_asr,
                        final=True)
        except GeneratorExit:
            return
        except:
            status_error = voicebot_pb2.Status(
                code=VoiceBot.ERROR, 
                message="TTS Service not working!")
            logging.error(traceback.format_exc())
            yield voicebot_pb2.VoiceBotResponse(status=status_error)

    def CallToBot(self, request_iterator, context):
        # Get config from first request
        request = next(request_iterator)
        if request.voicebot_config is None:
            yield voicebot_pb2.VoiceBotResponse(
                status=voicebot_pb2.Status(
                    code=VoiceBot.ERROR, 
                    message="First request must contain voicebot_config field!"))
            return
        call_center_code = None
        for code, name, _ in config.CALL_CENTERS:
            if code == request.voicebot_config.call_center_code:
                call_center_code = code
                break
        if call_center_code is None:
            yield voicebot_pb2.VoiceBotResponse(
                status=voicebot_pb2.Status(
                    code=VoiceBot.ERROR, 
                    message="Unknown callcenter code {}".format(request.voicebot_config.call_center_code)))
            return
        # Notify successful connection to client
        client_id = datetime.now().strftime("%Y%m%d%H%M%S") + "-" + str(uuid.uuid4())[:8]
        yield voicebot_pb2.VoiceBotResponse(
            status=voicebot_pb2.Status(
                code=VoiceBot.SUCCESS,
                message="Call center {} connected".format(call_center_code)))
        logging.info("{}\tConnected to call center {}".format(client_id, call_center_code))
        # Pipeline microservice
        asr_response_iterator = self._SpeechToText(client_id, request_iterator)
        if call_center_code == DUOC_CALL_OUT:
            chatbot_response_iterator = self._TextToText_Duoc_CallOut(client_id, asr_response_iterator)
        elif call_center_code == PIZZA_CALL_IN:
            chatbot_response_iterator = self._TextToText_Pizza_CallIn(client_id, asr_response_iterator)
        else:
            chatbot_response_iterator = self._TextToText_Duoc_CallOut(client_id, asr_response_iterator)
        tts_response_iterator = self._TextToSpeech(client_id, chatbot_response_iterator, timeout=config.TTS_TIMEOUT)
        for tts_response in tts_response_iterator:
            yield tts_response
        logging.info("{}\tFinish call!".format(client_id))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), maximum_concurrent_rpcs=10, options=(('grpc.so_reuseport', 1),))
    voicebot_pb2_grpc.add_VoiceBotServicer_to_server(VoiceBot(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
