"""
Grab latest articles and output mp3s into directory
"""
from bson import ObjectId

from tqdm import tqdm

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from nltk.tokenize import word_tokenize

from data.database import articles_collection
from data.constants import LANGUAGE, SENTENCES_COUNT, CHECKER, EPISODE_1_ARTICLES

stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

import speech as sp


def grab_n_articles(n=None):
    """
    Grab n articles from database that have not
    been on podcast previously
    """
    if n:
        return list(articles_collection.find({'used_on_podcast': False,
                                          'mp3_created': {'$exists': False}}).limit(n))
    else:
        return list(articles_collection.find({'used_on_podcast': False,
                                          'mp3_created': {'$exists': False}}))


def clean_article(article):
    """
    """
    cleaned = {'_id': article['_id'],
               'title': article['title'].encode('ascii', errors='ignore') if article['title'] else None,
               'issue': article['issue'],
               'link': article['link']}

    tokens = word_tokenize(article['body'])
    # words = [word for word in tokens if word.isalpha()]
    long_string = ' '.join(tokens)
    parser = PlaintextParser.from_string(long_string, Tokenizer(LANGUAGE))

    for index, sentence in enumerate(summarizer(parser.document, SENTENCES_COUNT)):
        cleaned.update({'sentence_' + str(index): sentence._text.encode('ascii', errors='ignore')})

    for key in range(SENTENCES_COUNT):
        nonsense_words = 0
        if cleaned.get('sentence_' + str(key)):
            for word in cleaned['sentence_' + str(key)].split(): # This .split() is very important
                if not CHECKER.check(word):
                    nonsense_words +=1

            cleaned['nonsense_words' + "_" + str(key)] = nonsense_words
    
    return cleaned


def pipeline(articles_to_process=None):
    """
    articles_to_process (int): If None, process all
    """
    articles = grab_n_articles(articles_to_process)
    with tqdm(total=len(articles)) as pbar:
        for article in articles:
            cleaned = clean_article(article)
            ssml = sp.article_ssml(cleaned)
            sp.synthesize_ssml_write_mp3(ssml, article)
            articles_collection.update_one({'_id': article['_id']},{'$set': {'mp3_created': True}}, upsert=False)
            pbar.update(1)

    return "Success"

if __name__ == '__main__':
    #pipeline()
    # free_form = [
    # 'Hi this is the machine love us podcast.',
    # 'On this show we do a review of the latest articles on machine learning, data science, and python to help keep you aware of the latest conversations in these areas.',
    # 'The show consists of ten articles which we will provide short summaries for.',
    # 'The link for each article is available on this episodes page at www.machineloveus.com',
    # 'Also note that the code we used to build this podcast is available via a series on our website.',
    # 'Enjoy this weeks articles and look out for more projects in data science and software engineering.',
    #             ]
    # sp.free_form_ssml_to_mp3(free_form, 'intro')
    # one = ["Let's dive in with our first article."]
    # sp.free_form_ssml_to_mp3(one, 'one')
    # two = ["And now for the second article."]
    # sp.free_form_ssml_to_mp3(two, 'two')
    # three = ["Remember all the links for these articles are available via machine love us dot com."]
    # sp.free_form_ssml_to_mp3(three, 'three')
    # four = ["I'll just jump in here quick to urge you to sign up for the machine love us dot com newsletter.", 'Sign up on the site, thanks!']
    # sp.free_form_ssml_to_mp3(four, 'four')

    # Update articles in db
    for id in EPISODE_1_ARTICLES:
        articles_collection.update_one({'_id': ObjectId(id)},{'$set': {'used_on_podcast': True}}, upsert=False)

