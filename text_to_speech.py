import os, pydub
from unicodedata import name
from urllib import response
from google.cloud import texttospeech_v1
from pydub import AudioSegment

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/remysteele/.config/gcloud/plucky-paratext-379015-abf653d0df1f.json'
client = texttospeech_v1.TextToSpeechClient()
combined_sounds = AudioSegment.empty()

char_limit = 45

def convert(s):
 
    # initialization of string to ""
    new = ""
 
    # traverse in the string
    for x in s:
        new += x
 
    # return string
    return new

tospeech = \
''' 

it is seriously crazy how many bitches i have fucked in my lifetime. if i had gotten kicked in the balls every time i fucked a bitch, i'd have half as many kids. now go get your dad a beer, kiddo

'''
characters = list(tospeech)

for i in range(int(len(characters)/char_limit)+1):

        b = convert(characters[(char_limit*i-10*i):(char_limit+char_limit*i-10*i)])
              
        text = "<speak>"+b+"</speak>"

        synthesis_input = texttospeech_v1.SynthesisInput(ssml=text)

        voice = texttospeech_v1.VoiceSelectionParams (
                language_code = 'en-us',
                name = 'en-US-Neural2-G',
                ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech_v1.AudioConfig(
                audio_encoding = texttospeech_v1.AudioEncoding.LINEAR16
        )
        response = client.synthesize_speech (
                input = synthesis_input,
                voice = voice,
                audio_config = audio_config
        )
        with open('audio%.i.wav'%i,'wb',) as output:
                output.write(response.audio_content)

for i in range(int(len(characters)/char_limit)+1):

        sound = (AudioSegment.from_wav('audio%.i.wav'%i))

        combined_sounds = combined_sounds+sound

print('Name output file:')
x = input()
combined_sounds.export("{}.mp3".format(str(x)), format="mp3", bitrate = '320k')

for i in range(int(len(characters)/char_limit)+1):

        os.remove('audio%.i.wav'%i)