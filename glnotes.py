import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

DEFAULT_GUESTBOOK_NAME = "Public"

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
   return ndb.Key('Guestbook', guestbook_name)


class Author(ndb.Model):
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        max_greetings = 10
        greetings = greetings_query.fetch(max_greetings)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = jinja_env.get_template('home.html')
        self.response.write(template.render(template_values))


class Stage(webapp2.RequestHandler):

  def get(self, stage_number):
        stage_pages = {'0': 'stage0.html',
                       '1': 'stage1.html',
                       '2': 'stage2.html',
                       '3': 'stage3.html',
                       '4': 'stage4.html',
                       '5': 'stage5.html'}

        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        max_greetings = 10
        greetings = greetings_query.fetch(max_greetings)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = jinja_env.get_template(stage_pages[stage_number])
        self.response.write(template.render(template_values))

class Home(webapp2.RequestHandler):

  def get(self):
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        max_greetings = 10
        greetings = greetings_query.fetch(max_greetings)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = jinja_env.get_template('home.html')
        self.response.write(template.render(template_values))


class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()
       
        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/stage(\d+)\.html', Stage),
    ('/home.html', Home),
], debug=True)
