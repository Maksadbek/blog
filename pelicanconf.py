#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'maksadbek'
SITENAME = 'Maksadbek'

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'en'

PLUGIN_PATHS = ['./plugins']
PLUGINS = ['i18n_subsites', 'render_math']
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'archives', 'search')

ARCHIVES_SAVE_AS = "archives.html"

DISPLAY_CATEGORIES_ON_MENU=False
DISPLAY_PAGES_ON_MENU=True
DISPLAY_TAGS_INLINE=True
DISPLAY_ARTICLE_INFO_ON_INDEX=True

PYGMENTS_STYLE = "emacs"
HIDE_SIDEBAR = True

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = "./theme"
I18N_TEMPLATES_LANG = 'en'

SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

CC_LICENSE="CC-BY"

STATIC_PATHS = [
    'static',
]

EXTRA_PATH_METADATA = {
    'static/favicon.ico': { 'path': 'favicon.ico' },
}

CUSTOM_CSS = 'static/css/custom.css'