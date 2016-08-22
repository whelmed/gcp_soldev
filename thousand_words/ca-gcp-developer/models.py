from google.appengine.ext import ndb
from google.appengine.api import memcache

class SiteMetadata(ndb.Model):
    ''' Used to store any site wide settings.
        Currently, it'll store the initialized flag.

        The intent is to call this via the .get method, and it'll act as
        a singleton.

        initialized determines if we've run the /init code from init.py
    '''
    initialized = ndb.BooleanProperty(default=False)
    created_on = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get(cls):
        return cls.query().get() or SiteMetadata()


class GenericModel(ndb.Model):
    '''A generic ndb model that will hold commom properties and methods. '''
    created_on = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def key_for_url_string(cls, url_string):
        '''Fetch a key base on the URL safe key.'''
        return ndb.Key(urlsafe=url_string)

    @classmethod
    def entity_for_urlsafe_key(cls, url_string):
        return cls.key_for_url_string(url_string).get()


class Category(GenericModel):
    """Models an individual category. A parent of images"""
    name = ndb.StringProperty(indexed=True)

    @classmethod
    def by_name(cls, name):
        '''Query to get a single category by name. eventual consistency.'''
        return cls.query().filter(cls.name==name).get()

    @classmethod
    def names(cls, limit=20):
        '''Get all distinct names. eventual consistency.'''
        return cls.query(projection=[cls.name], distinct=True).fetch(limit)


    @classmethod
    def last_image_for_n_categories(cls):
        ''' Returns a tuple (Category, Image) '''
        def _mapfunc(cat):
            return (cat, Image.last_for_category(cat))

        return cls.query(projection=[cls.name],distinct=True).map(_mapfunc)


class Image(GenericModel):
    '''Models an individual image'''
    url = ndb.StringProperty()
    details = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)

    @classmethod
    def _for_category(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.created_on)

    @classmethod
    def for_category(cls, ancestor_key, limit=20):
        return cls._for_category(ancestor_key).fetch(limit)

    @classmethod
    def count_for_category(cls, ancestor_key):
        return cls._for_category(ancestor_key).count()

    @classmethod
    def last_for_category(cls, ancestor_key):
        if type(ancestor_key) is Category:
            ancestor_key = ancestor_key.key

        return cls._for_category(ancestor_key).get()

    @classmethod
    def _update_image_count_cache(cls):
        icount = cls.query().count()
        memcache.set(key='image_count', value=icount)
        return icount

    @classmethod
    def image_count(cls):
        icount = memcache.get('image_count')

        if icount is None:
            icount = cls._update_image_count_cache()
        return icount


    @classmethod
    def _post_delete_hook(cls, key, future):
        '''Update the total cached count '''
        print future
        memcache.decr('image_count')

    @classmethod
    def _post_put_hook(cls, future):
        '''Update the total cached count '''
        memcache.incr('image_count')


class User(GenericModel):
    user_id = ndb.StringProperty()
