Title: Part 2 - Crawling a news website in Python with Scrapy and MongoDB
Date: 2015-12-11 12:00
Category: Python
Tags: Scrapy, MongoDB, Python
Slug: web-crawling
Authors: Frederic Husser
Summary: In this second part of our series, we will crawl the news website www.lemonde.fr with Scrapy for collecting a set of news articles, and store them in a MongoDB store. Scrapy is very easy to fire up and has a steep learning curve. We make profit of this to be able to start quickly our text mining activities on real data sets. With real data we mean data from a real use case. There are well known datasets such as the 20newsgroup reuters dataset of labelled documents. In our case, we want to learn to be confronted to unlabelled datasets, in any language.

## Quick start with Scrapy

We will work on our virtual machine as defined in the previous part. The code that we will go through is available in the GitHub repository under the worker_scrapy subdirectory. If the VM is not running just type `vagrant up` and then `vagrant ssh` while being at the root of the project.

Since Scrapy will require some additional packages it is convenient to use a virtual python environment dedicated to our Scrapy worker. For doing this we will simply use the Conda package manager, and type in the terminal:

```bash
$ cd /vagrant/worker_scrapy
$ sudo conda create -n scrapyenv -y scrapy pymongo
```

This will create a python virtual environment named **scrapyenv**, in which we will work with Scrapy and pymongo. For activating the environment just type in the bash:

```bash
$ source activate scrapyenv
```

In your terminal, each line should now start with **(scrapyenv)**. We are now ready to build a crawler with scrapy.

## Project Structure

At the root of our scraper project we create a python package called scraper in which we will pack all the code. The file scrapy.cfg states the location of the scraper settings module:

```
[settings]
default = scraper.settings
```

The scraper package contains:

+ A package containing the code of a **spider**. The spider is crawling into a website, selects web pages from all the internal hyperlinks according to selection rules, and collects items in the html pages according to their css classes or html tags.
+ A module called **items.py** defines the model of the object we want to extract. Defined as Python classes, the `Item` objects are shaped according to the data we want to extract.
+ A module called **pipelines.py** defines the pipeline of actions to be performed once an item was extracted from a web page. In our case it will consist in storing the data into our MongoDB instance.
+ The **settings.py** module defines all the parameters that will be needed in the scraping process. It tells Scrapy which spiders to use, states which pipelines must be followed and also defines the database connection settings.

The file Structure of the projects looks therefore as following:

```
scraper
  spiders
    __init__.py
    webarticles.py
  __init__.py
  items.py
  pipelines.py
  settings.py
scrapy.cfg
```

### Defining the model of the items

The Item class is defined in the Scrapy internals. We will create a child class that will contains the fields we want to extract from each lemonde.fr webpage: the title, the article body and the publication timestamp.

```python
from scrapy.item import Item, Field

class LeMondeArt(Item):
    """Define the model of the articles extracted from the website.
    """
    title = Field()
    timestamp = Field()
    body = Field()
```

This class models the items we want to extract, and this extraction is operated by the spider. 

### Defining the spider for lemonde.fr

There are different spiders base classes defined in Scrapy. We will use the CrawlSpider class as it contains procedures to extract data in the html page and to follow the hyperlinks. Thanks to class inheritance we only need to state the extraction rules, the parsing of the html data. We also create a method parse_article that tells Scrapy backend where to and how to get data in the html tree.

The class is looking like this:

```python
class LeMondeSpider(CrawlSpider):
    name = "lemonde"
    allowed_domains = ["lemonde.fr"]
    start_urls = ["http://www.lemonde.fr/"]
    article_item_fields = {
        'title': './/article/h1/text()',
        'timestamp': './/article/p[@class="bloc_signature"]/time[@itemprop="datePublished"]/@datetime',
        'body': './/article/div[@id="articleBody"]/*',
    }
    rules = (Rule(LinkExtractor(allow=(r"article/\d{4}/\d{2}/\d{2}/.+")), callback="parse_article", follow=True),
    )
```

The dictionary `article_item_fields` links each field of the `LeMondeItem` to a **xpath** selector telling where to get the data in the HTML tree. The `rules` tuple tells how the URLs allowed to be followed look like. It helps for instance restricting the crawler on all the pages referring to articles.

Then we add to this class a method for parsing data from the web page: it features a Selector, a Loader and a Processor object. When the data is extracted this method also define how a new LeMondeItem is created and populated with fields. Explaining in details the internals of Scrapy is out of the scope of this tutorial. However, you can refer to the official documentation.

Add this method to the LeMondeSpider method.

```python
    def parse_article(self, response):
        selector = Selector(response)
        loader = XPathItemLoader(LeMondeArt(), selector=selector)
        self.log('\n\nA response from %s just arrived!' % response.url)

        # define processors
        text_input_processor = MapCompose(unicode.strip)
        loader.default_output_processor = Join()

        # Populate the LeMonde Item with the item loader
        for field, xpath in self.article_item_fields.iteritems():
            try:
                loader.add_xpath(field, xpath, text_input_processor)
            except ValueError:
                self.log("XPath %s not found at url %s" % (xpath, response.url))
        yield loader.load_item()

```

Note that a spider is defined for a given website, as it fits to the HTML tags and CSS classes. However, thanks to the model defined in the `items.py` module our data is generalized so that the same king of fields could be extracted from any other news website. To do that, it is just needed to create another CrawlSpider class, and adapt the fields.

### Defining the data storage pipelines

In the module `pipelines.py` we tell scrapy what to do when an item instance was created from a spider instance. Our pipeline only consists in processing the item fields and store them in a MongoDB. The class `__init__` method creates a connection to the MongoDB service from the connection settings using the `pymongo` driver.

The pipeline is generally defined and operates principally on the item instances. We use the **bleach** package for cleaning the HTML text in the body. If you plan to make another pipeline object, make sure that you declare the `process_item` as it is required by Scrapy.

```python
tags = ['h2', 'p', 'em', 'strong']

class WebArticlesPipeline(object):
    """A pipeline for storing scraped items in the database"""
    MONGODB_COLLECTION = "lemonde"

    def __init__(self, collection_name='lemonde'):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER_HOST'],
            settings['MONGODB_SERVER_PORT']
        )
        db = connection[settings["MONGODB_DB"]]
        self.collection = db[collection_name]

    def process_item(self, item, spider):
        item["timestamp"]=item["timestamp"].split("+")[0]
        item["body"]=bleach.clean(item["body"], tags, strip=True)
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database",
                    level = log.DEBUG, spider=spider)
        return item
```

### Defining the settings

The settings module simply contains all the set of constants required for the crawling process: declare the spider settings, the pipelines to use and the database connection details.

### Fire-up crawling

Once you are all set, from the root of the subdirectory, where the `scrapy.conf` file is located you can start the crawler from the command line. The syntax is as follows:

```bash
scrapy crawl lemonde
```
