from transformers import pipeline

emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')


def detect(sentence):
    emotion_labels = emotion(sentence)
    return emotion_labels[0]['label']
