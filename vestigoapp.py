import cgi, csv, StringIO

from google.appengine.ext import db, webapp
from google.appengine.ext.db import polymodel
from google.appengine.api import users, images
from google.appengine.ext.webapp.util import run_wsgi_app

class db_user(db.Model):
    ##key is app code
    user = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)
    zip_code = db.IntegerProperty()

class db_photo(db.Model):
    user = db.StringProperty()
    id = db.StringProperty()
    avatar = db.BlobProperty()
    avatiny = db.BlobProperty()
    primary = db.BooleanProperty()

class db_item(polymodel.PolyModel):
    user = db.StringProperty()
    type = db.StringProperty()
    photo = db.ListProperty(db.Blob)
    text = db.TextProperty()
    title = db.StringProperty()
    model_number = db.StringProperty()
    url = db.StringProperty()
    qty = db.IntegerProperty()
    date_purchase = db.DateTimeProperty()
    date_create = db.DateTimeProperty(auto_now=True)
    date_update = db.DateTimeProperty(auto_now_add=True)

class db_item_music(db_item):
    media = db.StringProperty()
    artist = db.StringProperty()
    year_release = db.IntegerProperty()

class db_item_movie(db_item):
    media = db.StringProperty()
    format = db.StringProperty()
    language = db.StringProperty()
    producer = db.StringProperty()

class db_item_toy(db_item):
    pieces = db.StringProperty()

class db_item_book(db_item):
    author = db.StringProperty()
    publisher = db.StringProperty()

class db_item_boardgame(db_item):
    year_release = db.IntegerProperty()
    edition = db.IntegerProperty()

class db_item_digitalgame(db_item):
    media = db.StringProperty()
    digital_system = db.StringProperty()

class db_item_tool(db_item):
    manufacturer = db.StringProperty()
    year_warranty = db.FloatProperty()

#CD, Vinyl, Reel to Reel, etc
class db_opt_media(db.Model):
    title = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)

#PC, NES, DC, N64 etc
class db_opt_digital_system(db.Model):
    title = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)

#Craftsman, Lego
class db_opt_manufacturer(db.Model):
    title = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)

#Widescreen, Full screen
class db_opt_format(db.Model):
    title = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)

#English, French, Spanish.. etc
class db_opt_language(db.Model):
    title = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)

#Publisher
class db_opt_publisher(db.Model):
    title = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)

class db_opt_producer(db.Model):
    title = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)

#Author of book or story
class db_opt_author(db.Model):
    title = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)

#Performing artist
class db_opt_artist(db.Model):
    title = db.StringProperty()
    date_create = db.DateTimeProperty(auto_now=True)


def db_item_key(db_item_name=None):
  """Constructs a db_App datastore key for a db_item entity with db_item_name."""
  return db.Key.from_path('vestigo', db_item_name or 'default-vestigo-app')

class PageAppAdd(webapp.RequestHandler):
    def get(self, v_type):
        if v_type == 'music':
            self.response.out.write("""

""")
        elif v_type == 'movie':
            self.response.out.write("Movie code here")
        else:
            self.response.out.write("Not a valid item type.")

class APIList(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = self.request.get('item_id', default_value='')

        q = db_item.all().filter('user =', user.user_id())
        if v_item <> '':
            q.filter ('__key__', db.Key.from_path('vestigo', user.user_id(), 'db_item', int(v_item)))

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<items>\n')
        for item in q:
            self.response.out.write('<item>\n')
            self.response.out.write('  <id>%s</id>\n' % item.key().id())
            self.response.out.write('  <type>%s</type>\n' % item.type)
            self.response.out.write('  <title>%s</title>\n' % item.title)
            self.response.out.write('  <text>%s</text>\n' % item.text)
            self.response.out.write('  <model_number>%s</model_number>\n' % item.model_number)
            self.response.out.write('  <url>%s</url>\n' % item.url)
            self.response.out.write('  <qty>%s</qty>\n' % item.qty)
            self.response.out.write('  <date_purchase>%s</date_purchase>\n' % item.date_purchase)
            self.response.out.write('  <date_create>%s</date_create>\n' % item.date_create)
            self.response.out.write('</item>\n')
        self.response.out.write("</items>")

class APIList_music(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        q = db_item_music.all().filter('user =', user.user_id()).order('artist').order('year_release')
        v_item = self.request.get('item_id', default_value='')
        if v_item <> '':
            q.filter ('__key__', db.Key.from_path('vestigo', user.user_id(), 'db_item', int(v_item)))

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<items>')
        for item in q:
            self.response.out.write('<item>\n')
            self.response.out.write('  <id>%s</id>\n' % item.key().id())
            self.response.out.write('  <type>%s</type>\n' % item.type)
            self.response.out.write('  <title>%s</title>\n' % item.title.replace('&','&amp;'))
            self.response.out.write('  <text>%s</text>\n' % item.text.replace('&','&amp;'))
            self.response.out.write('  <model_number>%s</model_number>\n' % item.model_number)
            self.response.out.write('  <url>%s</url>\n' % item.url.replace('&','&amp;'))
            self.response.out.write('  <qty>%s</qty>\n' % item.qty)
            self.response.out.write('  <media>%s</media>\n' % item.media.replace('&','&amp;'))
            self.response.out.write('  <artist>%s</artist>\n' % item.artist.replace('&','&amp;'))
            self.response.out.write('  <year_release>%s</year_release>\n' % item.year_release)
            self.response.out.write('  <date_purchase>%s</date_purchase>\n' % item.date_purchase)
            self.response.out.write('  <date_create>%s</date_create>\n' % item.date_create)
            self.response.out.write('</item>\n')
        self.response.out.write("</items>")

class APIList_movie(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        q = db_item_movie.all().filter('user =', user.user_id())
        v_item = self.request.get('item_id', default_value='')
        if v_item <> '':
            q.filter ('__key__', db.Key.from_path('vestigo', user.user_id(), 'db_item', int(v_item)))

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<items>')
        for item in q:
            self.response.out.write('<item>\n')
            self.response.out.write('  <id>%s</id>\n' % item.key().id())
            self.response.out.write('  <type>%s</type>\n' % item.type)
            self.response.out.write('  <title>%s</title>\n' % item.title.replace('&','&amp;'))
            self.response.out.write('  <text>%s</text>\n' % item.text.replace('&','&amp;'))
            self.response.out.write('  <model_number>%s</model_number>\n' % item.model_number)
            self.response.out.write('  <url>%s</url>\n' % item.url.replace('&','&amp;'))
            self.response.out.write('  <qty>%s</qty>\n' % item.qty)
            self.response.out.write('  <media>%s</media>\n' % item.media)
            self.response.out.write('  <format>%s</format>\n' % item.format)
            self.response.out.write('  <language>%s</language>\n' % item.language)
            self.response.out.write('  <producer>%s</producer>\n' % item.producer)
            self.response.out.write('  <date_purchase>%s</date_purchase>\n' % item.date_purchase)
            self.response.out.write('  <date_create>%s</date_create>\n' % item.date_create)
            self.response.out.write('</item>\n')
        self.response.out.write('</items>')

class APIList_toy(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        q = db_item_toy.all().filter('user =', user.user_id())
        v_item = self.request.get('item_id', default_value='')
        if v_item <> '':
            q.filter ('__key__', db.Key.from_path('vestigo', user.user_id(), 'db_item', int(v_item)))

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<items>')
        for item in q:
            self.response.out.write('<item>\n')
            self.response.out.write('  <id>%s</id>\n' % item.key().id())
            self.response.out.write('  <type>%s</type>\n' % item.type)
            self.response.out.write('  <title>%s</title>\n' % item.title)
            self.response.out.write('  <text>%s</text>\n' % item.text)
            self.response.out.write('  <model_number>%s</model_number>\n' % item.model_number)
            self.response.out.write('  <url>%s</url>\n' % item.url)
            self.response.out.write('  <qty>%s</qty>\n' % item.qty)
            self.response.out.write('  <pieces>%s</pieces>\n' % item.pieces)
            self.response.out.write('  <date_purchase>%s</date_purchase>\n' % item.date_purchase)
            self.response.out.write('  <date_create>%s</date_create>\n' % item.date_create)
            self.response.out.write('</item>\n')
        self.response.out.write('</items>')

class APIList_book(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        q = db_item_book.all().filter('user =', user.user_id())
        v_item = self.request.get('item_id', default_value='')
        if v_item <> '':
            q.filter ('__key__', db.Key.from_path('vestigo', user.user_id(), 'db_item', int(v_item)))

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<items>')
        for item in q:
            self.response.out.write('<item>\n')
            self.response.out.write('  <id>%s</id>\n' % item.key().id())
            self.response.out.write('  <type>%s</type>\n' % item.type)
            self.response.out.write('  <title>%s</title>\n' % item.title)
            self.response.out.write('  <text>%s</text>\n' % item.text)
            self.response.out.write('  <model_number>%s</model_number>\n' % item.model_number)
            self.response.out.write('  <url>%s</url>\n' % item.url)
            self.response.out.write('  <qty>%s</qty>\n' % item.qty)
            self.response.out.write('  <author>%s</author>\n' % item.author)
            self.response.out.write('  <publisher>%s</publisher>\n' % item.publisher)
            self.response.out.write('  <date_purchase>%s</date_purchase>\n' % item.date_purchase)
            self.response.out.write('  <date_create>%s</date_create>\n' % item.date_create)
            self.response.out.write('</item>\n')
        self.response.out.write('</items>')

class APIList_boardgame(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        q = db_item_boardgame.all().filter('user =', user.user_id())
        v_item = self.request.get('item_id', default_value='')
        if v_item <> '':
            q.filter ('__key__', db.Key.from_path('vestigo', user.user_id(), 'db_item', int(v_item)))

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<items>')
        for item in q:
            self.response.out.write('<item>\n')
            self.response.out.write('  <id>%s</id>\n' % item.key().id())
            self.response.out.write('  <type>%s</type>\n' % item.type)
            self.response.out.write('  <title>%s</title>\n' % item.title)
            self.response.out.write('  <text>%s</text>\n' % item.text)
            self.response.out.write('  <model_number>%s</model_number>\n' % item.model_number)
            self.response.out.write('  <url>%s</url>\n' % item.url)
            self.response.out.write('  <qty>%s</qty>\n' % item.qty)
            self.response.out.write('  <year_release>%s</year_release>\n' % item.year_release)
            self.response.out.write('  <edition>%s</edition>\n' % item.edition)
            self.response.out.write('  <date_purchase>%s</date_purchase>\n' % item.date_purchase)
            self.response.out.write('  <date_create>%s</date_create>\n' % item.date_create)
            self.response.out.write('</item>\n')
        self.response.out.write('</items>')

class APIList_digitalgame(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        q = db_item_digitalgame.all().filter('user =', user.user_id())
        v_item = self.request.get('item_id', default_value='')
        if v_item <> '':
            q.filter ('__key__', db.Key.from_path('vestigo', user.user_id(), 'db_item', int(v_item)))

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<items>')
        for item in q:
            self.response.out.write('<item>\n')
            self.response.out.write('  <id>%s</id>\n' % item.key().id())
            self.response.out.write('  <type>%s</type>\n' % item.type)
            self.response.out.write('  <title>%s</title>\n' % item.title)
            self.response.out.write('  <text>%s</text>\n' % item.text)
            self.response.out.write('  <model_number>%s</model_number>\n' % item.model_number)
            self.response.out.write('  <url>%s</url>\n' % item.url)
            self.response.out.write('  <qty>%s</qty>\n' % item.qty)
            self.response.out.write('  <media>%s</media>\n' % item.media)
            self.response.out.write('  <digital_system>%s</digital_system>\n' % item.digital_system)
            self.response.out.write('  <date_purchase>%s</date_purchase>\n' % item.date_purchase)
            self.response.out.write('  <date_create>%s</date_create>\n' % item.date_create)
            self.response.out.write('</item>\n')
        self.response.out.write('</items>')

class APIList_tool(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        q = db_item_tool.all().filter('user =', user.user_id())
        v_item = self.request.get('item_id', default_value='')
        if v_item <> '':
            q.filter ('__key__', db.Key.from_path('vestigo', user.user_id(), 'db_item', int(v_item)))

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<items>')
        for item in q:
            self.response.out.write('<item>\n')
            self.response.out.write('  <id>%s</id>\n' % item.key().id())
            self.response.out.write('  <type>%s</type>\n' % item.type)
            self.response.out.write('  <title>%s</title>\n' % item.title)
            self.response.out.write('  <text>%s</text>\n' % item.text)
            self.response.out.write('  <model_number>%s</model_number>\n' % item.model_number)
            self.response.out.write('  <url>%s</url>\n' % item.url)
            self.response.out.write('  <qty>%s</qty>\n' % item.qty)
            self.response.out.write('  <manufacturer>%s</manufacturer>\n' % item.manufacturer)
            self.response.out.write('  <year_warranty>%s</year_warranty>\n' % item.year_warranty)
            self.response.out.write('  <date_purchase>%s</date_purchase>\n' % item.date_purchase)
            self.response.out.write('  <date_create>%s</date_create>\n' % item.date_create)
            self.response.out.write('</item>\n')
        self.response.out.write('</items>')

class APISave_music(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = self.request.get('item_id', default_value='')
        ##Construct the ID based on input. If nothing was given a new item is created, otherwise this will be an update.
        if v_item == '':
            v_db_item = db_item_music(parent=db_item_key(user.user_id()))
        else:
            v_db_item = db.Key.from_path('vestigo', user.user_id(), 'db_item', v_item)

        v_db_item.user = user.user_id()
        v_db_item.type = 'music'
        v_db_item.title = self.request.get('item_title', default_value='')
        v_db_item.text = self.request.get('item_text', default_value='')
        v_db_item.model_number = self.request.get('item_model_number', default_value='')
        v_db_item.url = self.request.get('item_url', default_value='')
        v_db_item.qty = int(self.request.get('item_qty', default_value=1).replace('','1'))
        v_db_item.year_release = int(self.request.get('item_release', default_value=1900).replace('','1900'))
        v_db_item.date_purchase = self.request.get('item_date_purchase', default_value='')
        v_db_item.media = self.request.get('item_media', default_value='')
        v_db_item.artist = self.request.get('item_artist', default_value='')
        v_db_item.put()

class APISave_movie(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = self.request.get('item_id', default_value='')
        ##Construct the ID based on input. If nothing was given a new item is created, otherwise this will be an update.
        if v_item == '':
            v_db_item = db_item_movie(parent=db_item_key(user.user_id()))
        else:
            v_db_item = db.Key.from_path('vestigo', user.user_id(), 'db_item', v_item)

        v_db_item.user = user.user_id()
        v_db_item.type = 'movie'
        v_db_item.title = self.request.get('item_title', default_value='')
        v_db_item.text = self.request.get('item_text', default_value='')
        v_db_item.model_number = self.request.get('item_model_number', default_value='')
        v_db_item.url = self.request.get('item_url', default_value='')
        v_db_item.qty = int(self.request.get('item_qty', default_value=1).replace('','1'))
        v_db_item.date_purchase = self.request.get('item_date_purchase', default_value='')
        v_db_item.media = self.request.get('item_media', default_value='')
        v_db_item.format = self.request.get('item_format', default_value='')
        v_db_item.language = self.request.get('item_language', default_value='')
        v_db_item.producer = self.request.get('item_producer', default_value='')
        v_db_item.put()

class APISave_toy(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = self.request.get('item_id', default_value='')
        ##Construct the ID based on input. If nothing was given a new item is created, otherwise this will be an update.
        if v_item == '':
            v_db_item = db_item_toy(parent=db_item_key(user.user_id()))
        else:
            v_db_item = db.Key.from_path('vestigo', user.user_id(), 'db_item', v_item)

        v_db_item.user = user.user_id()
        v_db_item.type = 'toy'
        v_db_item.title = self.request.get('item_title', default_value='')
        v_db_item.text = self.request.get('item_text', default_value='')
        v_db_item.model_number = self.request.get('item_model_number', default_value='')
        v_db_item.url = self.request.get('item_url', default_value='')
        v_db_item.qty = int(self.request.get('item_qty', default_value=1).replace('','1'))
        v_db_item.date_purchase = self.request.get('item_date_purchase', default_value='')
        v_db_item.pieces = self.request.get('item_pieces', default_value='')
        v_db_item.put()

class APISave_book(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = self.request.get('item_id', default_value='')
        ##Construct the ID based on input. If nothing was given a new item is created, otherwise this will be an update.
        if v_item == '':
            v_db_item = db_item_book(parent=db_item_key(user.user_id()))
            v_db_item = db_item_book.all()

        else:
            v_db_item = db.Key.from_path('vestigo', user.user_id(), 'db_item', v_item)

        v_db_item.user = user.user_id()
        v_db_item.type = 'book'
        v_db_item.title = self.request.get('item_title', default_value='')
        v_db_item.text = self.request.get('item_text', default_value='')
        v_db_item.model_number = self.request.get('item_model_number', default_value='')
        v_db_item.url = self.request.get('item_url', default_value='')
        v_db_item.qty = int(self.request.get('item_qty', default_value=1).replace('','1'))
        v_db_item.date_purchase = self.request.get('item_date_purchase', default_value='')
        v_db_item.author = self.request.get('item_author', default_value='')
        v_db_item.publisher = self.request.get('item_publisher', default_value='')
        v_db_item.put()

class APISave_boardgame(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = self.request.get('item_id', default_value='')
        ##Construct the ID based on input. If nothing was given a new item is created, otherwise this will be an update.
        if v_item == '':
            v_db_item = db_item_boardgame(parent=db_item_key(user.user_id()))
        else:
            v_db_item = db.Key.from_path('vestigo', user.user_id(), 'db_item', v_item)

        v_db_item.user = user.user_id()
        v_db_item.type = 'boardgame'
        v_db_item.title = self.request.get('item_title', default_value='')
        v_db_item.text = self.request.get('item_text', default_value='')
        v_db_item.model_number = self.request.get('item_model_number', default_value='')
        v_db_item.url = self.request.get('item_url', default_value='')
        v_db_item.qty = int(self.request.get('item_qty', default_value=1).replace('','1'))
        v_db_item.date_purchase = self.request.get('item_date_purchase', default_value='')
        v_db_item.year_release = self.request.get('item_year_release', default_value='')
        v_db_item.edition = self.request.get('item_edition', default_value='')
        v_db_item.put()

class APISave_digitalgame(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = self.request.get('item_id', default_value='')
        ##Construct the ID based on input. If nothing was given a new item is created, otherwise this will be an update.
        if v_item == '':
            v_db_item = db_item_digitalgame(parent=db_item_key(user.user_id()))
        else:
            v_db_item = db.Key.from_path('vestigo', user.user_id(), 'db_item', v_item)

        v_db_item.user = user.user_id()
        v_db_item.type = 'digital_game'
        v_db_item.title = self.request.get('item_title', default_value='')
        v_db_item.text = self.request.get('item_text', default_value='')
        v_db_item.model_number = self.request.get('item_model_number', default_value='')
        v_db_item.url = self.request.get('item_url', default_value='')
        v_db_item.qty = int(self.request.get('item_qty', default_value=1).replace('','1'))
        v_db_item.date_purchase = self.request.get('item_date_purchase', default_value='')
        v_db_item.media = self.request.get('item_media', default_value='')
        v_db_item.digital_system = self.request.get('item_digital_system', default_value='')
        v_db_item.put()

class APISave_tool(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = self.request.get('item_id', default_value='')
        ##Construct the ID based on input. If nothing was given a new item is created, otherwise this will be an update.
        if v_item == '':
            v_db_item = db_item_tool(parent=db_item_key(user.user_id()))
        else:
            v_db_item = db.Key.from_path('vestigo', user.user_id(), 'db_item', v_item)

        v_db_item.user = user.user_id()
        v_db_item.type = 'tool'
        v_db_item.title = self.request.get('item_title', default_value='')
        v_db_item.text = self.request.get('item_text', default_value='')
        v_db_item.model_number = self.request.get('item_model_number', default_value='')
        v_db_item.url = self.request.get('item_url', default_value='')
        v_db_item.qty = int(self.request.get('item_qty', default_value=1).replace('','1'))
        v_db_item.date_purchase = self.request.get('item_date_purchase', default_value='')
        v_db_item.manufacturer = self.request.get('item_manufacturer', default_value='')
        v_db_item.year_warranty = self.request.get('item_year_warranty', default_value='')
        v_db_item.put()

class APIGet_media(webapp.RequestHandler):
    def get(self):
        v_like = self.request.get('node_like', default_value='')

        if v_like <> '':
            q = db_opt_media.all().filter('title >=', v_like).filter('title <=', v_like + "\uFFFD").order('title').limit(10);
        else:
            q = db_opt_media.all().order('title').limit(10);

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<nodes>\n')
        for node in q:
            self.response.out.write('<node>\n')
            self.response.out.write('  <title>%s</title>\n' % node.title)
            self.response.out.write('  <date_create>%s</date_create>\n' % node.date_create)
            self.response.out.write('</node>\n')
        self.response.out.write("</nodes>")

class APIGet_artist(webapp.RequestHandler):
    def get(self):
        v_like = self.request.get('node_like', default_value='')

        if v_like <> '':
            q = db_opt_artist.all().filter('title >=', v_like).filter('title <=', v_like + "\uFFFD").order('title').limit(10);
        else:
            q = db_opt_artist.all().order('title').limit(10);

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<nodes>\n')
        for node in q:
            self.response.out.write('<node>\n')
            self.response.out.write('  <title>%s</title>\n' % node.title)
            self.response.out.write('  <date_create>%s</date_create>\n' % node.date_create)
            self.response.out.write('</node>\n')
        self.response.out.write("</nodes>")

class APIGet_format(webapp.RequestHandler):
    def get(self):
        v_like = self.request.get('node_like', default_value='')

        if v_like <> '':
            q = db_opt_format.all().filter('title >=', v_like).filter('title <=', v_like + "\uFFFD").order('title').limit(10);
        else:
            q = db_opt_format.all().order('title').limit(10);

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<nodes>\n')
        for node in q:
            self.response.out.write('<node>\n')
            self.response.out.write('  <title>%s</title>\n' % node.title)
            self.response.out.write('  <date_create>%s</date_create>\n' % node.date_create)
            self.response.out.write('</node>\n')
        self.response.out.write("</nodes>")

class APIGet_language(webapp.RequestHandler):
    def get(self):
        v_like = self.request.get('node_like', default_value='')

        if v_like <> '':
            q = db_opt_language.all().filter('title >=', v_like).filter('title <=', v_like + "\uFFFD").order('title').limit(10);
        else:
            q = db_opt_language.all().order('title').limit(10);

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<nodes>\n')
        for node in q:
            self.response.out.write('<node>\n')
            self.response.out.write('  <title>%s</title>\n' % node.title)
            self.response.out.write('  <date_create>%s</date_create>\n' % node.date_create)
            self.response.out.write('</node>\n')
        self.response.out.write("</nodes>")

class APIGet_producer(webapp.RequestHandler):
    def get(self):
        v_like = self.request.get('node_like', default_value='')

        if v_like <> '':
            q = db_opt_producer.all().filter('title >=', v_like).filter('title <=', v_like + "\uFFFD").order('title').limit(10);
        else:
            q = db_opt_producer.all().order('title').limit(10);

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<nodes>\n')
        for node in q:
            self.response.out.write('<node>\n')
            self.response.out.write('  <title>%s</title>\n' % node.title)
            self.response.out.write('  <date_create>%s</date_create>\n' % node.date_create)
            self.response.out.write('</node>\n')
        self.response.out.write("</nodes>")

class APIGet_author(webapp.RequestHandler):
    def get(self):
        v_like = self.request.get('node_like', default_value='')

        if v_like <> '':
            q = db_opt_author.all().filter('title >=', v_like).filter('title <=', v_like + "\uFFFD").order('title').limit(10);
        else:
            q = db_opt_author.all().order('title').limit(10);

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<nodes>\n')
        for node in q:
            self.response.out.write('<node>\n')
            self.response.out.write('  <title>%s</title>\n' % node.title)
            self.response.out.write('  <date_create>%s</date_create>\n' % node.date_create)
            self.response.out.write('</node>\n')
        self.response.out.write("</nodes>")

class APIGet_publisher(webapp.RequestHandler):
    def get(self):
        v_like = self.request.get('node_like', default_value='')

        if v_like <> '':
            q = db_opt_publisher.all().filter('title >=', v_like).filter('title <=', v_like + "\uFFFD").order('title').limit(10);
        else:
            q = db_opt_publisher.all().order('title').limit(10);

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<nodes>\n')
        for node in q:
            self.response.out.write('<node>\n')
            self.response.out.write('  <title>%s</title>\n' % node.title)
            self.response.out.write('  <date_create>%s</date_create>\n' % node.date_create)
            self.response.out.write('</node>\n')
        self.response.out.write("</nodes>")

class APIGet_digital_system(webapp.RequestHandler):
    def get(self):
        v_like = self.request.get('node_like', default_value='')

        if v_like <> '':
            q = db_opt_digital_system.all().filter('title >=', v_like).filter('title <=', v_like + "\uFFFD").order('title').limit(10);
        else:
            q = db_opt_digital_system.all().order('title').limit(10);

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<nodes>\n')
        for node in q:
            self.response.out.write('<node>\n')
            self.response.out.write('  <title>%s</title>\n' % node.title)
            self.response.out.write('  <date_create>%s</date_create>\n' % node.date_create)
            self.response.out.write('</node>\n')
        self.response.out.write("</nodes>")

class APIGet_manufacturer(webapp.RequestHandler):
    def get(self):
        v_like = self.request.get('node_like', default_value='')

        if v_like <> '':
            q = db_opt_manufacturer.all().filter('title >=', v_like).filter('title <=', v_like + "\uFFFD").order('title').limit(10);
        else:
            q = db_opt_manufacturer.all().order('title').limit(10);

        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<nodes>\n')
        for node in q:
            self.response.out.write('<node>\n')
            self.response.out.write('  <title>%s</title>\n' % node.title)
            self.response.out.write('  <date_create>%s</date_create>\n' % node.date_create)
            self.response.out.write('</node>\n')
        self.response.out.write("</nodes>")

class APIGet_types(webapp.RequestHandler):
    def get(self):
        self.response.headers.add_header("Content-Type", "text/xml")
        self.response.out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.response.out.write('<item_types>\n')
        self.response.out.write('  <item_type>\n')
        self.response.out.write('    <title>book</title>\n')
        self.response.out.write('  </item_type>\n')
        self.response.out.write('  <item_type>\n')
        self.response.out.write('    <title>boardgame</title>\n')
        self.response.out.write('  </item_type>\n')
        self.response.out.write('  <item_type>\n')
        self.response.out.write('    <title>digitalgame</title>\n')
        self.response.out.write('  </item_type>\n')
        self.response.out.write('  <item_type>\n')
        self.response.out.write('    <title>movie</title>\n')
        self.response.out.write('  </item_type>\n')
        self.response.out.write('  <item_type>\n')
        self.response.out.write('    <title>music</title>\n')          
        self.response.out.write('  </item_type>\n')
        self.response.out.write('  <item_type>\n')
        self.response.out.write('    <title>tool</title>\n')
        self.response.out.write('  </item_type>\n')
        self.response.out.write('  <item_type>\n')
        self.response.out.write('    <title>toy</title>\n')
        self.response.out.write('  </item_type>\n')
        self.response.out.write("</item_types>")

class APISave_photo(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = self.request.get('item_id', default_value = '')
        if (v_item <> ''):
            v_photo = db_photo(parent=db_item_key(user.user_id()))
            v_photo.id = v_item
            v_photo.user = user.user_id()
            v_photo.avatar = images.resize(self.request.get('img'), 800, 600)
            v_photo.primary = false
            v_photo.put()

class APISave_csv(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        self.response.out.write("----Attempting to upload: %s----<br>"%self.request.get('filetype'))
        stringReader = csv.reader(StringIO.StringIO(self.request.get('file')))
        for row in stringReader: 
            v_db_item = db_item_music(parent=db_item_key(user.user_id()))
            v_db_item.user = user.user_id()
            v_db_item.type = 'music'
            v_db_item.title = row[1].replace('"','')
            v_db_item.text = row[3].replace('"','')
            v_db_item.url = row[5].replace('"','')
            v_db_item.qty = int(row[6].replace('','1'))
            v_db_item.year_release = int(row[2])
            v_db_item.media = row[4]
            v_db_item.artist = row[0].replace('"','')
            v_db_item.put()
            self.response.out.write('Row:%s %s Y:%s:<br>'%(row[0],row[1],row[2]))

class APIDelete(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_item = int(self.request.get('item_id', default_value=''))
        v_db_item = db.Key.from_path('vestigo', user.user_id(), 'db_item', v_item)
        db.delete(v_db_item)
        self.response.out.write("Delete request for item %s submitted\n\n" % v_item)

class APITest(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        v_db_item = db_item_movie(parent=db_item_key(user.user_id()))
        v_db_item.user = user.user_id()
        v_db_item.title = 'Tyler'
        v_db_item.text = 'Group1'
        v_db_item.format = 'Smashing Pumpkins'
        v_db_item.type = 'movie'
        v_db_item.put()

application = webapp.WSGIApplication([('/api/list', APIList),
                                      ('/api/list/music', APIList_music),
                                      ('/api/list/movie', APIList_movie),
                                      ('/api/list/toy', APIList_toy),
                                      ('/api/list/book', APIList_book),
                                      ('/api/list/boardgame', APIList_boardgame),
                                      ('/api/list/digitalgame', APIList_digitalgame),
                                      ('/api/list/tool', APIList_tool),
                                      ('/api/save/music', APISave_music),
                                      ('/api/save/movie', APISave_movie),
                                      ('/api/save/toy', APISave_toy),
                                      ('/api/save/book', APISave_book),
                                      ('/api/save/tool', APISave_tool),
                                      ('/api/save/boardgame', APISave_boardgame),
                                      ('/api/save/digitalgame', APISave_digitalgame),
                                      ('/api/save/photo', APISave_photo),
                                      ('/api/save/csv', APISave_csv),
                                      ('/api/get/media', APIGet_media),
                                      ('/api/get/artist', APIGet_artist),
                                      ('/api/get/format', APIGet_format),
                                      ('/api/get/language', APIGet_language),
                                      ('/api/get/producer', APIGet_producer),
                                      ('/api/get/author', APIGet_author),
                                      ('/api/get/publisher', APIGet_publisher),
                                      ('/api/get/digital_system', APIGet_digital_system),
                                      ('/api/get/_types_', APIGet_types),
                                      ('/api/get/manufacturer', APIGet_manufacturer),
                                      ('/api/delete', APIDelete),
                                      (r'/app/add/(.*)', PageAppAdd),
                                      ('/test', APITest)],
                                     debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
