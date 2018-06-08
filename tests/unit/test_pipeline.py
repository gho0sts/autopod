"""
Test the pipeline
"""
from bs4 import BeautifulSoup
import mock
from autopod.data import pipeline as pipeline
from autopod.tests.mocks.text import text as test_text, url

def test__grab_visible():
    pass


@mock.patch('autopod.data.pipeline.create_soup_from_url')
def test__retrieve_links(mock_pipeline):
    assert pipeline.retrieve_links(None) == {'issue': None, 'urls': []}

    soup = BeautifulSoup(test_text, "lxml")
    mock_pipeline.return_value = soup

    assert pipeline.retrieve_links(url)['issue'] == url    
    assert len(pipeline.retrieve_links(url)['urls']) > 0


@mock.patch('autopod.data.pipeline.create_soup_from_url')
def test__clean_articles(mock_pipeline):
    assert pipeline.clean_articles({}) == []

    soup = BeautifulSoup(test_text, "lxml")
    mock_pipeline.return_value = soup
    issue_dict = pipeline.retrieve_links(url)    

    assert pipeline.clean_articles(issue_dict)
    assert len(pipeline.clean_articles(issue_dict)) > 0
