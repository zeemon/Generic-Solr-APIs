from solr_index import SolrIndex
import unittest


class Test_SolrIndex(unittest.TestCase):
	def test_SolrUpdateIndex(self):
		solr_obj = SolrIndex('blogs',419)
		new_data= {
			'title': '7 signs that you are the ulimate Bolywood Bride'
		}
		solr_obj.update_data(new_data)
		data= solr_obj.get_data()
		self.assertEqual(new_data['title'], data['title'])
