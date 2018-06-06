"""
Special handling of feeds
"""
from bs4 import BeautifulSoup
import requests


def fetch_latest_issue(feed_name, link):
    """
    Get the latest issue of a feed
    """
    return DISPATCH[feed_name](link)


def data_science_weekly(url):
    """
    """
    latest_issue = None
    text = requests.get(url).text
    soup = BeautifulSoup(text, "lxml")
    links = soup.findAll('a', href=True)
    for link in links:
        if "Data Science Weekly Newsletter - Issue" in link.text:
            latest_issue = link.get('href')
            break

    return "https://www.datascienceweekly.org" + str(latest_issue)


def center_for_data_innovation(url):
    """
    """
    latest_issue = None
    text = requests.get(url).text
    soup = BeautifulSoup(text, "lxml")
    links = soup.findAll('a', href=True)
    for link in links:
        if "10 Bits" in link.text:
            latest_issue = link.get('href')
            break

    return latest_issue


def kdnuggets(url):
    """
    """
    return url


def pythonweekly(url):
    """
    """
    latest_issue = None
    text = requests.get(url, verify=False).text
    soup = BeautifulSoup(text, "lxml")
    links = soup.findAll('a', href=True)
    for link in links:
        if "Issue" in link.text:
            latest_issue = link.get('href')
            break

    return "https://www.pythonweekly.com/archive/" + latest_issue


def importpython(url):
    """
    """
    latest_issue = None
    text = requests.get(url, verify=False).text
    soup = BeautifulSoup(text, "lxml")
    links = soup.findAll('a', href=True)
    for link in links:
        if "newsletter/no/" in link.get('href'):
            latest_issue = link.get('href')
            break

    return "http://importpython.com" + latest_issue


DISPATCH = {
            "data_science_weekly": data_science_weekly,
            "center_for_data_innovation": center_for_data_innovation,
            "kdnuggets": kdnuggets,
            "pythonweekly": pythonweekly,
            "importpython": importpython
            }
