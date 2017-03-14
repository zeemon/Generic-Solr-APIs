import urllib2, urllib
import json

class SolrIndex(object):

	SOLR_URL = 'http://localhost:8983/solr/'

	def __init__(self, core):
		self.core = core

	def get_data(self, id):
		endpoint= "/get?id="+str(id)
		req = self.__solr_request_object(endpoint)
		response = urllib2.urlopen(req)
		data= self.__solr_response_data(response)
		if not data: data= {'id': id}
		return data

	def update_data(self,new_data, id):
		data= self.get_data(id)
		for k,v in new_data.items():
			data[k]=v
		data= json.dumps([data])
		return self.__save_to_solr(data)

	def search(self, fl=[], fq={}, rows=10):

		params = {
			'query' : '&q=*:*',
			'fl'	: '&fl='+','.join(fl) if fl else '',
			'rows'  : '&rows='+ str(rows),
			'fq'	: self.__get_fq_params(fq) if fq else ''
		}

		endpoint= "/select?%s&wt=json&indent=true" % ''.join(params.values())

		req = self.__solr_request_object(endpoint)
		response = urllib2.urlopen(req)
		data= json.loads(response.read())
		return data['response']

	def __get_fq_params(self, fq):
		fq_params= ''
		for key, value in fq.items():
			fq_params +='&fq=%s:"%s"' % (key, urllib.quote_plus(value))
		return fq_params

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