"""
Everything to do with the voice
"""
from bson import ObjectId

import data.constants as constants
from google.cloud import texttospeech
from builder import Speech

import random
import datetime as dt
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'credentials.json'
client = texttospeech.TextToSpeechClient()

TODAY = dt.datetime.today().strftime('%Y-%m-%d')


def synthesize_ssml_write_mp3(ssml, article):
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    Example: <speak>Hello there.</speak>
    """
    input_text = texttospeech.types.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name="en-US-Wavenet-F",
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=.90,
        pitch=-2
    )

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open(TODAY + '_pod_' + str(article['_id']) + '.mp3', 'wb') as out:
        out.write(response.audio_content)
        print("Audio content written to file 'pod_'" + str(article['_id']) + "'.mp3'")

    return


def article_ssml(article):
    """
    Args:
        article (dictionary): Title and sentences of post
    # <say-as interpret-as="ordinal">10</say-as>
    Returns:
        mp3
    """
    speech = Speech()

    if article.get('title'):
        speech.say('The title of this article is ' + str(article.get('title')) + ".")
        speech.pause("1s")

    for key in range(constants.SENTENCES_COUNT):
        if (article.get('nonsense_words_' + str(key)) < constants.NONSENSE_THRESHOLD):
            if article.get('sentence_' + str(key)):
                speech.say(article['sentence_' + str(key)])
                duration = "500ms" #str(random.randint(300, 1000)) + "ms" 
                speech.pause(duration)
    
    return speech.ssml(False)


def free_form_ssml_to_mp3(text, name):
    """
    """
    speech = Speech()

    for sentence in text:
        speech.say(sentence)
        duration = "500ms" #str(random.randint(300, 1000)) + "ms" #
        speech.pause(duration)

    input_text = texttospeech.types.SynthesisInput(ssml=speech.ssml(False))

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name="en-US-Wavenet-F",
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=.90,
        pitch=0
    )

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open(TODAY + name + '.mp3', 'wb') as out:
        out.write(response.audio_content)

