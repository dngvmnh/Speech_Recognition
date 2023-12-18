import wave

obj = wave.open("Speech_Recognition/basics/output.wav",'rb')

print("Number of channels", obj.getnchannels())
print("Sample width", obj.getsampwidth())
print("Frame rate.", obj.getframerate())
print("Number of frames", obj.getnframes())
print("parameters:", obj.getparams())
frames = obj.readframes(obj.getnframes())
# print(frames)
print(len(frames) / obj.getsampwidth(), frames[0], type(frames[0]))
obj.close()

sample_rate = 16000.0 # Hz
obj_new = wave.open("Speech_Recognition/basics/new_output.wav",'wb')
obj_new.setnchannels(1) 
# obj_new.setnchannels(2)
obj_new.setsampwidth(2)
obj_new.setframerate(sample_rate)
obj_new.writeframes(frames)
obj_new.close()
