from .mapping import *

try:
    __version__ = __import__('pkg_resources').get_distribution('CouchbaseMapping').version
except:
    __version__ = '?'
