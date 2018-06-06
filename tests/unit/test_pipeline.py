"""
Test the pipeline
"""
import mock
from autopod.data import pipeline

def test__grab_visible():
	pass

@mock.patch('requests.get')
def test__clean_articles(mock_get):
	assert pipeline.clean_articles(None) == []
	mock_response.json.return_value = expected_dict
	mock_get.return_value = mock_response
