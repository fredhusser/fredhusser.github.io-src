#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Frederic Husser'
SITENAME = u'Data Science for collective intelligence'
SITEURL = ''

PATH = 'content'
THEME = './pelican/pure'
# Tell Pelican to add 'extra/custom.css' to the output dir
STATIC_PATHS = ['images', 'static/css/bootstrap.flatly.min.css']
CUSTOM_CSS = 'static/css/bootstrap.spacelab.min.css'
TIMEZONE = 'Europe/Paris'

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['code_include', 'series', 'related_posts',
           'better_codeblock_line_numbering']

from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension

MD_EXTENSIONS = [
    CodeHiliteExtension(css_class='highlight', linenums=False),
    TocExtension(),
    'markdown.extensions.extra',
]

CATEGORIES_SAVE_AS = 'categories.html'
CATEGORY_URL = 'category/{slug}.html'
CATEGORY_SAVE_AS = 'category/{slug}.html'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

PLUGINS += ['summary']
SUMMARY_BEGIN_MARKER = '<!-- PELICAN_BEGIN_SUMMARY -->'
SUMMARY_END_MARKER = '<!-- PELICAN_END_SUMMARY -->'

PLUGINS += ['tag_cloud']
TAG_CLOUD_STEPS = 5
TAG_CLOUD_SORTING = 'size-rev'
DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Home', '/'),
         )
# Social widget
SOCIAL = (('GitHub', 'https://github.com/fredhusser'),
          )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
