from __future__ import print_function
import sys
import traceback
import logging
import pyaudio
import _thread
logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logging.INFO)

import grpc
import time

import voicebot_pb2
import voicebot_pb2_grpc

from pydub import AudioSegment
from pydub.playback import play


CHUNK = 4000
CHANNELS = 1
RATE = 16000
CONNECTED = False

def record_block():
    global CONNECTED
    yield voicebot_pb2.VoiceBotRequest(
        voicebot_config=voicebot_pb2.VoiceBotConfig(
            call_center_code='18002222'))
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    while True:
        block = stream.read(CHUNK)
        block_audio = voicebot_pb2.VoiceBotRequest(audio_content=block)
        if CONNECTED:
            yield block_audio


def play_audio(url):
    sys.stdout.write('{}\n'.format(url))
    sys.stdout.flush()
    
    # fname = "C:\\Users\\Asdf\\Documents\\Audio.wav"
    # mysong = AudioSegment.from_wav(fname)
    # play(mysong)
    # p = pyaudio.PyAudio()  
    # stream = p.open(format = pyaudio.paInt16,  
    #                 channels = 1,  
    #                 rate = 16000,  
    #                 output = True)
    # time.sleep(0.1)
    # stream.write(bytes[44:])
    # stream.stop_stream()  
    # stream.close()  
    # p.terminate()  

def run():
    global CONNECTED
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    # with grpc.insecure_channel('123.31.18.120:50051') as channel:
    with grpc.insecure_channel('localhost:50051') as channel:
        voicebot_stub = voicebot_pb2_grpc.VoiceBotStub(channel)

        # list_call_center_response = voicebot_stub.ListCallCenter(voicebot_pb2.ListCallCenterRequest())
        # for call_center in list_call_center_response.call_centers:
        #     print(call_center.code, call_center.name)

        voicebot_response_iterator = voicebot_stub.CallToBot(record_block())
        voicebot_response = next(voicebot_response_iterator)
        if voicebot_response.status.code == 200:
            logging.info("Connected to call center")
            logging.info("Speak something ...")
            CONNECTED = True
            for voicebot_response in voicebot_response_iterator:
                if not voicebot_response.final:
                    sys.stdout.write('\rMe: {}'.format(voicebot_response.text_asr))
                    sys.stdout.flush()
                else:
                    sys.stdout.write('\rMe: {}\n'.format(voicebot_response.text_asr))
                    sys.stdout.write('Bot: {}\n'.format(voicebot_response.text))
                    sys.stdout.flush()
                    if voicebot_response.audio_url is not None:
                        _thread.start_new_thread(play_audio, (voicebot_response.audio_url, ))
        else:
            logging.error("{} - {}".format(voicebot_response.status.code, voicebot_response.status.message))

if __name__ == '__main__':
    run()