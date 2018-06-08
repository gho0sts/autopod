"""
Different feeds. In the future use PRAW to get top reddit datascience, machinelearning, python threads
"""
import special_handling as special


LATEST_ISSUES = []
DATA_SCIENCE_WEEKLY = "http://www.datascienceweekly.org/newsletters"
# Add more feeds!

ALL_FEEDS = {"data_science_weekly": DATA_SCIENCE_WEEKLY
             }

for feed, url in ALL_FEEDS.iteritems():
    LATEST_ISSUES.append(special.fetch_latest_issue(feed, url))
