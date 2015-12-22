Title: Part 0 - Introduction to Programming Collective in Python
Date: 2015-12-09 12:00
Category: Python
Tags: dev environment, Machine Learning, Agile Data Science
Slug: introduction-collective-intelligence
Authors: Frederic Husser
Summary: Introduction to agile text mining with python: this post starts a series covering a full text mining workflow on information, from the collection of text documents, their classification using machine learning techniques and the presentation in a light weight web application. The workflow features for a large part the workflow well explained in details in the books [*Agile Data Science*] by Russel Jurney.

This blog is also meant to be a recipe for data scientists and physicists who want to be able to present and communicate about their work, so that their algorithms and analysis do not sleep forever deep in their GitHub account.
The series of posts we are starting here is a guide book of [this GitHub repository](https://github.com/fredhusser/collective-intelligence). Programmers having an account on GitHub are mostly welcome to fork it.

## So what are the goals we want to pursue?

We want to build an application that collects a great number of blog posts, news articles or opinions in the web, use a semantic analysis to classify them based on content and allows users to browse faster in the corpus through a simple web application.

In this blog we intend to present some tools for doing data analysis with Python but also we want to propose a way to conduct data analysis projects. The goals are to reduce the frictions in the full process. Frictions stem usually from the difficulty to work together for people with different backgrounds and fields: developers, data scientists, users and consummers. 

The lean data science is based upon the principle that data collection, analysis and visualization should be considered as a loop that must be completed at the fastest possible speed. At each iteration, developers and data scientists can work collaboratively to improve the solution at any level as they can see the full picture. So let's get to work.

## Mission, objectives and roadmap

### Mission

Our mission is to build a intelligent news web application able to classify and cluster articles and opinions. It must offer to users a simple but complete browsing experience, so that they can reach the biggest amount of relevant content in the least amount of time. Documents relevance is assessed using:

+ **semantic analysis**, that is to say extract features from the textual content, 
+ **collaborative filtering** that is to say extract features on documents based on how users interact with them (likes, shares, comments).


### Objectives 

In order to realize this mission we can set up few objectives and constraints. First and foremost, we want to be **open source** and **transparent**. When using machine learning algorithms with the aim of recommending content to users it is immensely necessary to be open to critics so that it acknowledged by users to be fair and not pursuing self-interests. 

Secondly, we do not seek the ultimate model and algorithm that will unequivocally resolve the challenge. Instead, algorithms must be combined, confronted and strongly challenged. There is no debate on whether model-based recommendations are better that collaborative filtering when it comes to recommending content. Instead, it must be recognized that both have strengths and weeknesses and therefore the question is how to make them operate together.

Finally, we want to offer to users the capability to browse quickly in the documents although the corpus is meant to be important. The classification and clustering algorithms must integrate this objective so that documents indexing is perfectly matching the requirements of a smart data visualization.

### Roadmap

In the first iteration we will tackle the issue of semantic analysis for classifying documents based on their content. In order to achieve this goal we will operate in an agile manner so that we complete the following steps the fastest possible.

1. **Environment set-up**

    We will set up a reproducible development environment, with all the basic tools and frameworks we are going to need. For this we will be using Vagrant for taking care of our virtual machine on which to run Python scripts and Docker containers.
    
2. **Data Collection**

    Then some input data will be scraped from the web in order to have a collection of articles on which to perform some analysis. We will use Scrapy, a web scraper in made in Python, to help us crawling articles from [*www.lemonde.fr*](http://www.lemonde.fr).

3. **Data analytics and text mining**

    Here is the hard work! Standing on the shoulder of giants like Numpy, NLTK and Scikit-Learn, we will build a document classification algorithm based on semantic analysis and self-organizing maps. We will rely a lot on the existing algorithms for natural language processing (NLP) such as in Scikit-Learn and NLTK, and we will eventually build our own self-organizing map classifier in Python.

4. **Data visualization and browsing**

    Building a light weight web application with Flask and pymongo, we will make possible to data scientists to communicate on their results, with a step-by-step workflow.
    
    + Present atomic records or chunks of the data; in our case it will be the news articles crawled from lemonde.fr. This step is really important to complete so that you can also evaluate the quality of your raw data. Keep the iteration based mindset.
    + Build data visualizations for presenting the results of your analysis, enabling the user to understand the full scope of it. We want also to make the data scientists able to evaluate the quality of the analysis they performed with an objective point of view.
    + Create reports that convey a message understandable by your audience. These reports are based on the analysis you conducted. For instance, what are the hot topics, the most transversal articles or the most specific ones? The value of your analysis is derived from the insight on the data it can give and the actions that can be taken.


