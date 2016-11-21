import json, logging, certifi
# from kafka import KafkaProducer
import time
from  elasticsearch import Elasticsearch

ES_ENDPOINT = ('https://search-tap-fashion-ahlt6conoduuuihoeyjqd7olpq.us-west-2.es.amazonaws.com')

def getObject(id, index, doc_type):
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),) 

	results = es.search(index=index,
		doc_type=doc_type, 
		body={"query":{ "terms": { "_id": [id]}}})

	if results['hits']['total'] == 1:
		return results['hits']['hits'][0]['_source']
	else:
		return None

''' 
Gets the post from ElasticSearch, given a post ID.
Accepts a post ID as a string
Returns a dictionary object containing the data of the post, if found.
Returns None if the post isn't found or if multiple results are returned.
'''
def getPost(post_id):
	return getObject(post_id, "posts", "post")

'''
Gets a comment from ElasticSearch, given a comment ID.
Accepts a comment ID as a string
Returns a dictionary object containing the information of the post.
'''
def getComment(comment_id):
	return getObject(comment_id, "comments", "comment")

'''
Builds the entire post, given a post ID.
Accepts a post ID as a string
Returns a fully formed dictionary object that contains the full post, including
all comments (rather than comment IDs)

Note: Not sure if we need this. What about resolving user IDs to user names?
'''
def buildWholePost(post_id):
	post = getPost(post_id)
	comments = post.pop('comments')
	post['comments'] = []

	for comment in comments:
		print comment
		comment_body = getComment(comment)
		post['comments'].append(comment_body)

	return post

def getAllPosts():
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	results = es.search(index=index,
		doc_type=doc_type, 
		body={"query" : {"match_all" : {}}})

	if results['hits']['total'] > 0:
		return results['hits']['hits']
	else:
		return None

'''
Note: We're grabbing comments one at a time. However, we can dump all the IDs
into ElasticSearch as a list which will be quicker. But we can visit this
later.
'''