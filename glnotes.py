import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


#class Handler(webapp2.RequestHandler):
    #def write(self, *a, **kw):
       #self.response.out.write(*a, **kw)

   # def render_str(self, template, **params):
       # t = jinja_env.get_template(template)
        #return t.render(params)

   # def render(self, template, **kw):
      #  self.write(self.render_str(template, **kw))


#class MainPage(Handler):
   # def get(self):
      #  items = self.request.get_all("name")
       # self.render("home.html", items = items)

class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

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

        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
