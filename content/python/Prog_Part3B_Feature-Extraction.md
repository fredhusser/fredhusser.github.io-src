Title: Part 3B - Text documents feature extraction with Scikit-Learn
Date: 2015-12-15 12:00
Category: Python
Tags: Machine Learning, Scikit-Learn, GENSIM, NLTK, TF-IDF, Vector Space Model, 
Slug: feature_extraction
Authors: Frederic Husser
Summary:In this tutorial, the mechanics of text vectorization and topic modeling will be covered. Text vectorization is a technique transforming documents into vectors of words where the components refer to the weight the words have in a specific document. We will use the interface defined in the [post 3A]({filename}Prog_Part3A_Introduction.md) for building a model producing an output usable in the workflow by the subsequent model instance. The text vectorizer is built on top of the `TfidfVectorizer` from Scikit-Learn, using a tokenizer from the NLTK framework. 

In the [introduction post]({filename}Prog_Part3A_Introduction.md) we have described the workflow we want to create for performing an automatic classification of text documents. These text documents have been crawled on lemonde.fr website.


## Text vectorization 

For vectorizing the corpus of articles we create a `Model` child class called `ModelTFIDF`. It uses the TF-IDF vectorization algorithm from Scikit-Learn. If you are not familiar to the Scikit-Learn interfaces,[the documentation](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) can be consulted relatively to the `TfidfVectorizer`. 

The underlying algorithm is based on a count vectorizer and a tf-idf transformer. 

+ The first tokenizes the text documents and makes a reference of all tokens with their appearance frequency in each document. A count matrix is built with tokens as columns and documents as rows. Since all words are not appearing in all documents the count matrix is very sparse. Especially when working with other languages than English, a very high level implementation of the tokenizer is available in the NLTK (Natural Language Toolkit). In a future step, a French tokenizer will be used. It applies a stemming algorithm, so that words like 'manger' and 'mangé' are not counted as different. Stemming can be highly beneficial in terms of computing time and also improves the relevance of the results.
+ The tf-idf transformer operates a modulation of the in-document term frequencies by the log of the inverse of the document frequency for each feature. In other words, each time that a words appears at least once in a document of the corpus this is 

We first create the class, and override the metadata, namely the name of the output data. This is mainly required for producing consistant logs during the fit process.

```python
class ModelTFIDF(Model):
    model_type = "transformer"
    model_name = "tfidf"
    output_data_name = "tfidfMatrix"
    mapper_name = "words_to_index"
```

Obviously we need to override the `fit` method. In this method we instantiate the vectorizer from Scikit-Learn with all the required parameters. Note that the object attribute `fit_parameters` is set in the standardized `__init__` method. Using the vectorizer from Scikit-Learn, we have to load the input data as a numpy array, which is the type requirement of the object attribute `input_data` as instantiated in the `__init__` method as well.

The vectorizer outputs a sparse documents-features matrix. This will be assigned to our `output_data` attributes. The `mapper_data` attributes takes the vectorizer dictionary which maps the indexes of the features in the documents-features matrix and the string representation of the feature. In the most basic set-up a feature is a word. But it could also be bi-grams (two consecutive words), or more.

```python
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

The `TfIdfVectorizer` fit parameters are stored as Python dictionary in the `MLconfig.py` module. The key-value pairs are then passed to the vectorizer instance in the fit method. The most important parameters at first are the `max_df` and `min_df`: they set the upper and lower thresholds for filtering out features considering their document frequencies. The document frequency is calculated relatively to the occurance in the corpus:

+ Words or features appearing in all documents tend to be non discriminating in terms of documents comparisons. Usually these are what are called the stop-words: these are common to the language and grammar, and do not add much information on the content. In our example, we filter out features with more than 60% document frequency.
+ Words or features appearing in a very small amount of documents tend to so specific that they cannot be used for a proper comparison. In the similarity measure that we will use in the classifier based on a dot product, they will constantly account for a multiplication by zero. Therefore they will be responsible a high computational while bringing low insight. In our example, we filter out features with less than 1% document frequency.


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

Using the workflow class defined in [Part A]({filename}Prog_Part3A_Introduction.md), we add a method for vectorizing the documents inputs. This method return the `self` keyword for easing the chaining of processors in single command lines.

```python
    def vectorizer(self):
        """Representation of the text data into the vector space model.
        """
        self.vectorize_ = ModelTFIDF(self.corpus_data.body, PARAMETERS_VECTORIZE).fit()
        self.attributes["corpus_size"] = self.vectorize_.training_set_size
        self.attributes["n_features"] = self.vectorize_.output_space_size
        return self
``` 

Then a workflow object must be instantiated with the MongoDB connection parameters, and the `vectorizer` method is operated. In a Python shell at the root of the subproject, you can fire-up the vectorization in one single command line. The log displays information about the processed job.
```bash
>>> from textmining.workflows import SemanticAnalysisWorkflow
>>> SemanticAnalysisWorkflow(mongoclient, "scrapy", "lemonde").vectorizer()
tfidf:	Model tfidf of type transformer was trained
tfidf:	Output name:	 tfidfMatrix
tfidf:	Input space:	 (1958,)
tfidf:	Output space:	 (1958, 4777)
tfidf:	Model attributes:
```

In our example, we have a corpus of 1958 text documents. After vectorization, a document matrix of shape 1958 documents by 4777 features. Obviously, the number of features is rather limited for such a high number of documents. However, for testing purposes, with the only goal to set up a full workflow this is more than enough. At the end of the iteration, we will be able to review the full process and make right decisions on rather or not we should filter so many features.

Since the vectorizer returns the object itself, we could store it in a variable in order to reuse it later, with a second model. In the [Github repo](https://github.com/fredhusser/collective-intelligence), a IPython notebook can be used for better understanding the mechanics of the vectorization model.



