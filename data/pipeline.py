"""
Pull and summarize feeds
"""
from bs4 import BeautifulSoup
import re
import requests
import OpenSSL

from feeds import LATEST_ISSUES
import constants

ARTICLES = []
LINKS = []

from bs4.element import Comment
import datetime as dt


def tag_visible(element):
    """Used for cleaning HMTL"""
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def clean_articles(issue):
    """
    Clean the articles in an issue for database

    Args:
        issue (url)

    Returns:
        (list)
    """
    formatted_articles = []
    try:
        text = requests.get(issue).text
        soup = BeautifulSoup(text, "lxml")
    except Exception, msg:
        print msg
        return []

    for link in soup.findAll('a', href=True):
        if ((not any([ext in link.get('href') for ext in constants.UNWANTED]))
            and "http" in link.get('href')):
            LINKS.append(link.get('href'))

    for link in set(LINKS):
        try:
            soup = BeautifulSoup(requests.get(link).text, "lxml")
        except (requests.exceptions.MissingSchema, requests.exceptions.SSLError, OpenSSL.SSL.ZeroReturnError), msg:
            print "Error", msg, "for ", link
            break
        html_text = soup.findAll(text=True)
        visible_text = filter(tag_visible, html_text)
        formatted =  u" ".join(t.strip() for t in visible_text)
        
        formatted_articles.append({'issue': issue,
                                   'title': soup.findAll('h1')[0].text if len(soup.findAll('h1')) > 0 else "",
                                   'link': link,
                                   'body': formatted,
                                   'date_accessed': dt.datetime.utcnow(),
                                   'used_on_podcast': False})

    return formatted_articles
