import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load('en_core_web_sm')

import math
import re


st.title('Text Summarization')

dataset_name = st.sidebar.selectbox("Select Type",("Nepali","Extraction"))


def summarization(text):
    stopwords = list(STOP_WORDS)
    doc = nlp(text)
    tokens = [token.text for token in doc]
    punctuation = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~\\n"
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords or word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] +=1
    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency

    sentence_tokens = [sent for sent in doc.sents]

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    from heapq import nlargest

    select_length = int(len(sentence_tokens)*0.3)
    summary = nlargest(select_length,sentence_scores, key = sentence_scores.get)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    return summary

def nepali_tfidf(nepali_text): 
    f = open('nepali_stopwords.txt','r')
    nepali_tfidf_sentence = re.split('|',nepali_text)
    words = nepali_text.split()
    def frequency(nepali_tfidf_sentence):
        frequency_matrix = {}
        stopWords = [x.strip() for x in f]
        

def det_dataset(dataset_name):
    if dataset_name == "Nepali":
        nepali_text = st.text_area('Nepali Text')
        nepali_tfidf(nepali_text)
    if dataset_name == "Extraction":
        text = st.text_area('Text')
        if st.button('Summary'):
            summary = summarization(text)
            st.write(summary)

det_dataset(dataset_name)
