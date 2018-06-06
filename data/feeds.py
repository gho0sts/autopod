"""
Different feeds. In the future use PRAW to get top reddit datascience, machinelearning, python threads
"""
import special_handling as special


LATEST_ISSUES = []
DATA_SCIENCE_WEEKLY = "http://www.datascienceweekly.org/newsletters"
CENTER_FOR_DATA_INNOVATION = "http://www.datainnovation.org/category/blog/weekly-news/"
KDNUGGETS = "https://www.kdnuggets.com/news/top-stories.html"
PYTHONWEEKLY = "https://www.pythonweekly.com/archive/"
IMPORTPYTHON = "http://importpython.com/newsletter/archive/"

ALL_FEEDS = {"data_science_weekly": DATA_SCIENCE_WEEKLY,
             "center_for_data_innovation": CENTER_FOR_DATA_INNOVATION,
             "kdnuggets": KDNUGGETS,
             "pythonweekly": PYTHONWEEKLY,
             "importpython": IMPORTPYTHON
             }

for feed, url in ALL_FEEDS.iteritems():
    LATEST_ISSUES.append(special.fetch_latest_issue(feed, url))
