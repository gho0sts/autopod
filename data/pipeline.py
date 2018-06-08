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

from bs4.element import Comment
import datetime as dt


def tag_visible(element):
    """Used for cleaning HMTL"""
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def create_soup_from_url(url):
    """
    Args:
        url

    Returns:
        bs4 soup or None
    """
    soup = None
    if url:
        try:
            txt = requests.get(url).text
            soup = BeautifulSoup(txt, "lxml")
        except (requests.exceptions.MissingSchema, requests.exceptions.SSLError, OpenSSL.SSL.ZeroReturnError), msg:
            pass # Log the error here, later
    return soup


def retrieve_links(issue):
    """
    Retrieve all links in document
    """
    urls = []
    soup = create_soup_from_url(issue)
    if not soup:
        return []

    for link in soup.findAll('a', href=True):
        if ((not any([ext in link.get('href') for ext in constants.UNWANTED]))
            and "http" in link.get('href')):
            urls.append(link.get('href'))

    return {'issue': issue, 'urls': urls}


def clean_articles(issue):
    """
    Clean the articles in an issue for database

    Args:
        issue (dict) containing issue link and all urls in link

    Returns:
        (list)
    """
    formatted_articles = []


    for url in set(issue.get('urls', [])):
        soup = create_soup_from_url(url)
        if not soup:
            break
        html_text = soup.findAll(text=True)
        visible_text = filter(tag_visible, html_text)
        formatted =  u" ".join(t.strip() for t in visible_text)
        
        formatted_articles.append({'issue': issue['issue'],
                                   'title': soup.findAll('h1')[0].text if len(soup.findAll('h1')) > 0 else "",
                                   'link': url,
                                   'body': formatted,
                                   'date_accessed': dt.datetime.utcnow(),
                                   'used_on_podcast': False})

    return formatted_articles
