import urllib2
import json

class SolrIndex(object):

	SOLR_URL = 'http://localhost:8983/solr/'

	def __init__(self, core, id):
		self.core = core
		self.id = id

	def get_data(self):
		endpoint= "/get?id="+str(self.id)
		req = self.__solr_request_object(endpoint)
		response = urllib2.urlopen(req)
		data= self.__solr_response_data(response)
		if not data: data= {'id': self.id}
		return data

	def update_data(self,new_data):
		data= self.get_data()
		for k,v in new_data.items():
			data[k]=v
		data= json.dumps([data])
		return self.__save_to_solr(data)

	def __solr_request_object(self, endpoint):
		full_url= self.SOLR_URL+self.core+endpoint
		req = urllib2.Request(full_url)
		req.add_header('Content-type', 'application/json')
		return req

	def __solr_response_data(self, response):
		return json.loads(response.read())['doc']

	def __save_to_solr(self, data):
		endpoint = '/update/json?commit=true&wt=json'
		req = self.__solr_request_object(endpoint)
		urllib2.urlopen(req, data)