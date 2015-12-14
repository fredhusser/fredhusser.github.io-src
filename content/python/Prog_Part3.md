Title: Part 3A - Semantic Analysis and Text Clustering with Scikit-Learn
Date: 2015-12-12 12:00
Category: Python
Tags: Machine Learning, Scikit-Learn, NLTK
Slug: semantic-analysis
Authors: Frederic Husser
Summary: We build a workflow for classifying news articles based on their semantic content. Our approach for extracting features is combining text vectorization with TF-IDF weighting, topic modeling with Latent Semantic Indexing (LSI), non-negative matrix factorization (NMF) or Latent Dirichlet Allocation (LDA). Once our documents are characterized by topics, classification and clustering tasks are performed using Self-Organizing Maps (SOM), also called Kohonen Networks, a kind of unsupervised neural network, and agglomerative clustering. SOM algorithm was chosen for it allows a topology preserving two-dimensional classification. It is appealing because of its potential regarding browsing and graphical visualization. Agglomerative clustering is run upon the SOM nodes in order to extract a limited number of news articles groups.

In this tutorial, we tackle the first challenge of building a news article automatic classifier based on the documents content. On our last post, [we scraped some articles]({filename}Prog_Part2.md) using Scrapy from [lemonde.fr](http://www.lemonde.fr), that were stored into a MongoDB instance. We want to classify all these articles, finding out groups of similar articles based on their topics. The constraint is that we do not know in advance the main topics coming up throughout te corpus. This should be infered from our analysis. 

Our second constraint, is that we want to be able to classify a large number of articles. Therefore the algorithms used should be scalable, but also in their design tolerate a large variety of topics. In order to ease browsing into the corpus by humans, we want to visualize graphically the result of the classification.

We will define a basic workflow for building such a classifier in Python, using extensively Numpy, Pandas and Scikit-Learn. These packages are part of the Anaconda Python distribution from Continuum Analytics, which [we installed in our virtual machine using Vagrant]({filename}Prog_Part1.md). From a more abstract perspective we will also propose a general template of a workflow chaining algorithms together. Each building block of the whole workflow is an algorithm operated on the dataset and producing an output which can be then in turn operated on by the following block.

All the code featured in this page can be downloaded from [GitHub](https://github.com/fredhusser/collective-intelligence)


## Building blocks of the classifier


Our semantic, graphical and automatic classification algorithm will be built in four steps.
![Photo]({attach}workflow_v1.png)

+ **Vectorization**: The first task is to extract features from the textual content. Vectorization and weighting is performed using the term-frequencies inverse document-frequencies method (TF-IDF): documents are vectorized, each token (a word or group of consecutive words) being a component, and the weights are proportional to the appearance frequency within the document and modulated by their inverse document frequency. This last steps ensures that terms appearing too often and therefore not discriminating enough, like stop words, can be filtered out. Similarly words appearing in too few documents and therefore too specific or rare can also be filtered out.

+ **Semantic indexing**: From the TF-IDF vectorization it is really common to have a documents-term matrix with several thousands different features. This results in a really noisy dataset: several words might be appearing with different stems and homonymy and polysemy is also a recurrent issue. In addition to this, high dimensionality comes with high computing cost at the analysis step. Dimensionality reduction using semantic analysis is our method to overcome these issues. At our disposal several techniques are available using matrix factorization techniques: latent semantic indexing (LSI), non-negative matrix factorization (NMF) and latent Dirichlet allocation (LDA). We will first try out the LSI since this algorithms is faster than the others, although it has some drawbacks. From the agile data analysis perspective, we want at first to build the full analysis pipeline, getting some insights on performance, and, only then, improve the models. In any of the algorithms stated above, groups of features are formed to build a set of representative topics. Each document is then assigned a distance to that topic in a documents-topic matrix.

+ **Classification**: The third task is to build the classifier based on the topics extracted before. This classifier must be unsupervised: no inputs from a samples or user interaction are required for training it. Instead it shall find by itself the main patterns in the training data set, and infer from the internal structure of the corpus a classification scheme. We use the Self-Organizing Maps (SOM) algorithm invented by T. Kohonen. This unsupervised kind of neural networks algorithms builds a mapping from the input features space into a 2D map space (set of adjacent nodes). This mapping preserves the topology of input space, and is therefore very appealing for its potential regarding data visualization. Besides, the nodes are represented by vectors of same dimensionality than the input space, and are trained to be similar to the training dataset vectors they map to.

+ **Clustering**: This property of SOM is used in a fourth step for building clusters of nodes. We use an agglomerative clustering algorithm for finding a limited number of clusters of adjacent and similar nodes. The Ward algorithm is matching the two conditions of adjacency and similarity for grouping two nodes together. However, this step is not applied on the dataset, but on the output of the classification algorithm. Complementary to it, its goal is to improve the readability of results by humans.


## Structure of the master algorithm

In the introduction of this article we have mentioned the structure of the whole workflow. We basically define two abstract levels:

+ The `Model` class assemble an algorithm that operates on some input data and producing an output. Information about the dimensionality of the input and output space are also provided. The model is a standardized interface between algorithms so that they can be easily chained. It also contains a `fit() ` method that starts the training of the algorithms. Creating a model consists in creating a child class of the `Model` class which overrides the `fit()`method as well as the descriptive attributes. The class also has a method for streaming log messages, and other methods which are not displayed here:

```python
class Model(object):
    model_name = "sample_model"
    output_data_name = "output_data"
    mapper_name = "mapper_name"
    model_type = "model"

    def __init__(self, input_data, fit_parameters, output_space_size=0):
        self.input_data = input_data
        self.fit_parameters = fit_parameters
        self.training_set_size = input_data.shape[0]
        self.output_space_size = output_space_size
        self.model_attributes = {}

    def fit(self):
        self.output_data = np.array([])
        self.mapper_data = np.array
        return self
```

+ The `Worklfow` class defines a master workflow that retrieves data from a source (SQL database or MongoDB store), applies to it a series of models and store the output of the classification in Mongo. In addition to that basic functionality this class must feature some helper methods for aggregating the data into Pandas `DataFrame` instances for cleaning, reformatting, indexing, grouping and querying it.

The `SemanticAnalysisWorkflow` is a class with a MongoDB extractor.

```python 
class SemanticAnalysisWorkflow(object):
    MONGO_DBNAME_OUT = "textmining"
    MONGO_COLLECTION_OUT = "semantic"

    def __init__(self, connection, dbname, collection):
        self.attributes = {}
        self.vectorize_ = None
        self.reduce_ = None
        self.classify_ = None
        self.cluster_ = None
        self.connection = connection
        self.read_mongo(dbname,collection)

    def read_mongo(self, dbname, collection):
        collection = self.connection[dbname][collection]
        articles = collection.find(projection={"title": True, "body": True, "_id": False})

        json_articles = []
        for article in articles:
            json_articles.append(article)
        json_data = json.dumps(json_articles, default=json_util.default)
        self.corpus_data = pd.read_json(json_data).drop_duplicates().dropna()
        print self.corpus_data.head()
        return self
```

In the following sections we will cover the details about the four tasks we have stated in the introduction, that is vectorization, semantic analysis, classification and clustering.
 
## Vectorization

For vectorizing the corpus of articles we create a `Model` child class called `ModelTFIDF` which uses the TF-IDF vectorization algorithm from Scikit-Learn. If you are not familiar to the Scikit-Learn interfaces, you should consult the documentation relative to the `TfidfVectorizer`. This vectorizer

```python
class ModelTFIDF(Model):
    model_type = "transformer"
    model_name = "tfidf"
    output_data_name = "tfidfMatrix"
    mapper_name = "words_to_index"

    def fit(self, language=None):
        self._set_tokenizer(language)
        vectorizer = TfidfVectorizer(**self.fit_parameters)

        self.output_data = vectorizer.fit_transform(self.input_data)
        self.output_space_size = self.output_data.shape[1]

        # Give access to the index of a word
        self.mapper_data = vectorizer.vocabulary_

        # Return a reverse mapper for retrieving a word from index
        self.mapper_reverse = np.empty(self.output_space_size, dtype="a30")
        for key, value in self.mapper_data.iteritems():
            self.mapper_reverse[value] = key
        self._log_model_results()
        return self

```

For the `TfIdfVectorizer` from Scikit-Learn we use the following parameters:

```python
PARAMETERS_VECTORIZE = {
    "vocabulary": None,
    "max_df": 0.6,
    "min_df": 0.01,
    "ngram_range": (1, 1),  # unigrams or bigrams
    "encoding": "utf-8",
    "strip_accents": 'ascii',
    "norm": 'l2',
}
```

The TF-IDF vectorizer comprises two main building blocks: the tokenizer that extract the tokens from the text and the analyzer that counts the occurence frequencies. For the tokenizer, and especially when working with other languages than English, it is recommended to use the NLTK (Natural Language Toolkit). We will use a French tokenizer which also applies a stemming algorithm so that words like 'manger' and 'mangé' are not counted as different. Stemming can be highly beneficial in terms of computing time and also for the relevance of the results.

In the following posts we will cover the three other building blocks of our workflow, and present our first results.
