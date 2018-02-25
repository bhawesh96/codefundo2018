import os
import cloudconvert, requests
import speech_recognition as sr

def download(audio_url)
    print 'download function'

    r = requests.get(audio_url) # create HTTP response object
 
    with open("my_audio.mp4",'wb') as f:
        f.write(r.content)
    return "downloaded"

def convert():
    print 'convert func'
    api = cloudconvert.Api('***REMOVED***')

    file_name = os.path.join(
        os.path.dirname(__file__),
        'my_audio.mp4')

    process = api.convert({
        "inputformat": "mp4",
        "outputformat": "wav",
        "input": "upload",
        "file": file_name
    })
    process.wait()
    process.download('my_audio.wav')

    print 'download ke baad'
    return "converted to wav"

def fetch():
    r = sr.Recognizer()
    file_name_wav = os.path.join(
        os.path.dirname(__file__),
        'my_audio.wav')

    with sr.WavFile(file_name_wav) as source:              # use "testwav" as the audio source
        r.adjust_for_ambient_noise(source)  # here
        audio = r.record(source)                        # extract audio data from the file

    try:
        text = r.recognize_google(audio)
        print text
        return str(text)
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")

# download('https://cdn.fbsbx.com/v/t59.3654-21/28274865_1733851513303759_2953649520560308224_n.mp4/audioclip-1519532632000-3855.mp4?oh=696c6943805eecc0ea54e69f65ee59f3&oe=5A941FF5')