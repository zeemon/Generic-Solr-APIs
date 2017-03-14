from solr_index import SolrIndex
import unittest


class Test_SolrIndex(unittest.TestCase):
	def test_SolrUpdateIndex(self):
		solr_obj = SolrIndex('blogs')
		blog_id=419
		new_data= {
			'title': '10 signs that you are the ulimate Bolywood Bride'
		}
		solr_obj.update_data(new_data,blog_id)
		data= solr_obj.get_data(blog_id)
		self.assertEqual(new_data['title'], data['title'])

	def test_SolrSearch(self):
		solr_obj = SolrIndex('blogs')
		blogs = solr_obj.search(
			fl=['id','title','slug'],
			fq={
				'title': '10 signs'
			},
			rows=10
		)
		self.assertTrue(len(blogs)>=1)