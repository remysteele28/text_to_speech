import os, pydub
from google.cloud import texttospeech_v1
from pydub import AudioSegment

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='REDACTED'                                                 # Add path to key.json
client = texttospeech_v1.TextToSpeechClient()
combined_sounds = AudioSegment.empty()

char_limit = 4500                                                                                       # Google only allows each request to be 5000 bytes > about 5 minutes of audio

def convert(s):                                                                                         # Function to concatinate a list of characters
 
    # initialization of string to ""
    new = ""
 
    # traverse in the string
    for x in s:
        new += x
 
    # return string
    return new

tospeech = \
''' 

ENTER TEXT HERE

'''
characters = list(tospeech)                                                                             # Split text into a list characters

for i in range(int(len(characters)/char_limit)+2):                                                      # Loop through the first 4500 characters, then the next 4500...

        b = convert(characters[(char_limit*i-10*i):(char_limit+char_limit*i-10*i)])                     # Convert the first 4500 characters in the list back into a string. Then, convert the next 4500 characters,
                                                                                                        # with a small 10 character buffer so that the word is guarenteed to be understood
        text = "<speak>"+b+"</speak>"                                                                   # make the string ssml compatible

        synthesis_input = texttospeech_v1.SynthesisInput(ssml=text)

        voice = texttospeech_v1.VoiceSelectionParams (
                language_code = 'en-us',                                                                # Select accent
                name = 'en-US-Neural2-G',                                                               # Select the voice. The voices can be previewed on the Google text-to-speech API's website
                ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech_v1.AudioConfig(
                audio_encoding = texttospeech_v1.AudioEncoding.LINEAR16                                 # Exports a WAV file to preserve quality
        )
        response = client.synthesize_speech (                                                           # Make Google do things
                input = synthesis_input,
                voice = voice,
                audio_config = audio_config
        )
        with open('text_to_speech_audio%.i.wav'%i,'wb',) as output:                                     # Write the audio files in order as the loop goes round and round
                output.write(response.audio_content)

for i in range(int(len(characters)/char_limit)+2):                                                      # Concatinate the audio files

        sound = (AudioSegment.from_wav('text_to_speech_audio%.i.wav'%i))

        combined_sounds = combined_sounds+sound

print('Name output file:')                                                                              # Input the desired output file name
x = input()
combined_sounds.export("{}.mp3".format(str(x)), format="mp3", bitrate = '320k')                         # Lessen the bitrate to create a smaller filesize. Less than 32k is not the best

for i in range(int(len(characters)/char_limit)+2):                                                      # Delete the split files from harddrive

        os.remove('text_to_speech_audio%.i.wav'%i)