import webapp2
import os
import json
import cgi
import urllib


class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    guestbook_name = self.request.get('guestbook_name')
    ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
    greetings = Greeting.query_book(ancestor_key).fetch(20)

    for greeting in greetings:
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(greeting.content))

    self.response.out.write("""
          <form action="/sign?%s" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
          <hr>
          <form>Guestbook name: <input value="%s" name="guestbook_name">
          <input type="submit" value="switch"></form>
        </body>
      </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                    cgi.escape(guestbook_name)))

class SubmitForm(webapp2.RequestHandler):
  def post(self):
    # We set the parent key on each 'Greeting' to ensure each guestbook's
    # greetings are in the same entity group.
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=ndb.Key("Book", guestbook_name or "*notitle*"),
                        content = self.request.get('content'))
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', SubmitForm)
])