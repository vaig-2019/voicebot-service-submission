import pyaudio  
import wave  

#define stream chunk   
chunk = 1024  

#open a wav format music  
f = wave.open(r"test.wav","rb")  
#instantiate PyAudio  
p = pyaudio.PyAudio()  
#open stream  
print(p.get_format_from_width(f.getsampwidth()))
stream = p.open(format = pyaudio.paInt16,  
                channels = 1,  
                rate = 16000,  
                output = True)  
#read data  
# data = f.readframes(chunk)  

# print(data)
# #play stream  
# while data:  
#     stream.write(data)  
#     data = f.readframes(chunk)  

stream.write(open(r"test.wav","rb").read()[44:])

#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()  