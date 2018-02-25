import urllib2
import speech_recognition as sr
import subprocess
import os

file_name = os.path.join(
        os.path.dirname(__file__),
        'my_audio.mp4')

# with open(file_name, "wb") as handle:
#     handle.write(mp4file.read())

cmdline = ['avconv',
           '-i',
           file_name,
           '-vn',
           '-f',
           'wav',
           'my_audio.wav']
subprocess.call(cmdline)
'''
r = sr.Recognizer()
with sr.AudioFile('test.wav') as source:
    audio = r.record(source)

command = r.recognize_google(audio)
print command

os.remove("test.mp4")
os.remove("test.wav")
'''