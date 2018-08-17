#!/usr/bin/env python

from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from models import Note
import os
import webapp2
import jinja2
import logging
import time
from google.appengine.ext import ndb

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CoordsRequest(ndb.Model):
    lat = ndb.StringProperty(required = True)
    lon = ndb.StringProperty(required = True)
    timestamp = ndb.DateTimeProperty(auto_now_add = True)

class AddressRequest(ndb.Model):
    address = ndb.StringProperty(required = True)
    timestamp = ndb.DateTimeProperty(auto_now_add = True)

class RecordRequestHandler(webapp2.RequestHandler):
    def post(self):
        logging.info(self.request)
        if self.request.get('type') == "coords":
            new_record = CoordsRequest(lat = self.request.get('lat'),
                                       lon = self.request.get('lon'))
            new_record.put()
        elif self.request.get('type') == "address":
            new_address_record = AddressRequest(address = self.request.get('address'))
            new_address_record.put()
        else:
            logging.error("Malformed Request!")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('templates/map.html')
        self.response.write(template.render())

        descr = self.request.get('address')

        if descr == None:
            print("There's nothing in here. ")
            
        if self.request.get('img'):
        	photo = Photo.get_by_id(int(self.request.get('img')))

    def post(self):
        print("Done.")

        note = Note(
                img = self.request.get('img'), 
                describe = self.request.get('desc'),
                )

        note.put()
        
        template = jinja_env.get_template('templates/map.html')
        self.response.out.write(template.render())


class InfoHandler(webapp2.RequestHandler):
    def get(self):

        descr = self.request.get('address')

        if descr == None:
            print("There's nothing in here. ")
            
        if self.request.get('img'):
        	photo = Photo.get_by_id(int(self.request.get('img')))

    def post(self):
        print("Done.")

        note = Note(
                img = self.request.get('img'), 
                describe = self.request.get('desc'),
                )

        note.put()
        
        template = jinja_env.get_template('./templates/map.html')
        self.response.out.write(template.render())

		
class ViewInfo(webapp2.RequestHandler):
	def _render_template(self, template_name, context = None):
		if context is None:
			context = {}
		
	def get(self):
		qry = Note.owner_query()
		context['notes'] = qry.fetch
		template_name = jinja_env.get_template('./view.html')
		return template.render(context)
		

class Note(ndb.Model):
    img = ndb.BlobProperty()
    describe = ndb.StringProperty()
    
    @classmethod
    def owner_query(cls):
        return cls.query().order(
            cls.date_created)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/record_request', RecordRequestHandler)
], debug=True)
