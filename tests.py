from solr_index import SolrIndex
import unittest


class Test_SolrIndex(unittest.TestCase):
	def test_SolrUpdateIndex(self):

		solr_obj = SolrIndex('blogs')
		blog_id=419
		new_data= {
			'title': '10 signs that you are the ulimate Bolywood Bride'
		}

		#update blog id 419 with the above title
		solr_obj.update_data(new_data,blog_id)

		#fetch data of blog id 419
		data= solr_obj.get_data(blog_id)

		#verify that the title has been updated
		self.assertEqual(new_data['title'], data['title'])

	def test_SolrSearch(self):
		solr_obj = SolrIndex('blogs')
		blogs = solr_obj.filter(
			fl=['id','title','slug'],
			fq={
				'title': '10 signs'
			},
			rows=10
		)
		self.assertTrue(len(blogs)>=1)

	def test_SolrSortingAsc(self):

		solr_obj = SolrIndex('blogs')
		blogs = solr_obj.filter(
			fl=['id','title','slug'],
			fq={
				'title': 'perfect'
			},
			rows=10,
			sort="id",
			sort_order="asc"
		)
		blog_ids= [i['id'] for i in blogs['docs']]

		check_sort= [i['id'] for i in blogs['docs']]
		check_sort.sort()

		self.assertEquals(blog_ids, check_sort)


	def test_SolrSortingDesc(self):

		solr_obj = SolrIndex('blogs')
		blogs = solr_obj.filter(
			fl=['id','title','slug'],
			fq={
				'title': 'perfect'
			},
			rows=10,
			sort="id"
		)
		blog_ids= [i['id'] for i in blogs['docs']]

		check_reverse_sort= [i['id'] for i in blogs['docs']]
		check_reverse_sort.sort(reverse=True)

		self.assertEquals(blog_ids, check_reverse_sort)
