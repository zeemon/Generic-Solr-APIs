# Generic-Solr-APIs

*Easy-to-use generic apis for <a href="http://www.theserverside.com/definition/Apache-Solr">Apache Solr</a> integration with python projects* <br>
<br>

**How to use:**
* Create your solr cores<br>
  example : blogs
  
* Define your solr base url in the class **SolrIndex** <br>
  `SOLR_URL = 'http://localhost:8983/solr/'`
  
* Call the methods of the class SolrIndex for creating/updating/filtering solr data <br><br>

**For creating/updating an item in solr blogs core.**<br>
*If id exists in solr it updates, else creates*

    solr_obj = SolrIndex('blogs')
    data= {
        'id': 431,
        'title': '10 signs that you are the ulimate football star',
        'slug': '10-signs-ultimate-football-star'
    }
    solr_obj.update_data(data, 431)
    
**For getting an existing item from solr** <br>
*item id 431 is being retrieved*

    solr_obj = SolrIndex('blogs')
    solr_obj.get_data(431)

**Fetching data by filtering/ sorting**<br>
*this query will get the id, title and slug of the top 10 records that have titles like "10 signs" sorted by latest id*

    blogs = solr_obj.filter(
        fl=['id','title','slug'],
        fq={
            'title': '10 signs',
        },
        sort='id',
        sort_order= 'desc',
        rows=10
    )


**Fetching data by filtering on multiple fields at once**<br>
*this query will show fetch id and title of all blogs that have the words red or roses in them in the tile or description fields*

    solr_obj.filter(
        fl=['id', 'title'],
        search_term="red roses",
        qf=['title', 'description']
    )



**Boosting results by weight**<br>
*sometimes we want to order results based on priorities, example, show the results having the search term in the title first and the ones in description later in the results. This can be achieved with boosted queries*

    solr_obj.filter(
        fl=['id'],
        search_term="red roses",
        qf=['title^0.8','description^0.2']
    )
    
**Adding custom queries** <br>
*if you know what you're doing and want to add some parameters directly to the solr api endpoint*

    blogs = solr_obj.filter(
        fl=['id','title','slug'],
        custom_query= '&defType=dismax&qf=description'
    )
    
    
### All filter parameters and their meanings:
  * **fq** : *faceted query* : this is used to get results based on particular fields. <br>
    example where title like 'red roses' and country = 'india' <br>
    `fq: { title : 'red roses', country: 'india' }`
   * **rows**: how many results to return | defaults to `10`
   * **sort**: which field to sort by `sort: 'title'`
   * **sort_order**: `asc` or `desc` | defaults to `desc`
   * **fl**: *fields list* : a list of fields that will be returned from solr | defaults to all fields
   * **search_term** : generic search term. this term will be searched in one/more query fields (`qf`) that you specify.<br>
     when using search_term parameter, it is compulsory to specify which all fields to search in. this is done using the `qf` parameter which takes a list of fields.<br>
     following example will search for red roses in title & description fields in solr<br>
      `search_term="red roses",`<br>
      `qf=['title', 'description']`<br>
   * **qf** : which fields query the search_term on. can accept boost values as well. example : `id^0.5` specifies the weight of id field in the search results
   * **custom_query**: any additional query parameters. partial url string to be appended at the end of the request if supplied 
    
