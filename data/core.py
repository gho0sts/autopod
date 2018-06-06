"""
Core of the data pipeline
"""
import pipeline
from database import articles_collection
from feeds import LATEST_ISSUES


if __name__ == '__main__':
    for issue in LATEST_ISSUES:
        print "----------------------------------------"
        print "----------------------------------------"
        print "Working with issue", issue
        print "----------------------------------------"
        print "----------------------------------------"
        formatted = pipeline.clean_articles(issue)
        for article in formatted:
            if articles_collection.find_one({'link': article['link']}):
                print "We already have this article in the DB!", article['link']
            else:
                result = articles_collection.insert_one(article)
                print "Saved", article['title'], article['link'], result.inserted_id
        print "----------------------------------------"
        print "----------------------------------------"
        print "Done with issue", issue
        print "----------------------------------------"
        print "----------------------------------------"
