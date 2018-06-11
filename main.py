#!/usr/bin/env python

# name: AR Code Locator - main.py
# date: 6-5-2018
# author: Matt Nutsch
# description: This is the web API for the AR Code Locator Android app.
# it is written in Python 2.7 and is intended to run in Google App Engine.

__author__ = 'nutschm@oregonstate.edu'

# imports
from google.appengine.ext import ndb
import webapp2
import json

from datetime import datetime # for datetime

#converts datetime to json
#based on example at: https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable/36142844#36142844
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

class targetMarker(ndb.Model):
    url = ndb.StringProperty(required=True)
    latitude = ndb.StringProperty(required=True)
    longitude = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    createdBy = ndb.StringProperty(required=True)
    
class targetMarkerHandler(webapp2.RequestHandler):
    def post(self, id=None):
        targetMarkerData = json.loads(self.request.body)
        newTargetMarker = targetMarker(url=targetMarkerData['url'])
        newTargetMarker.latitude = targetMarkerData['latitude']
        newTargetMarker.longitude = targetMarkerData['longitude']
        newTargetMarker.name = targetMarkerData['name']
        newTargetMarker.createdBy = targetMarkerData['createdBy']
        newTargetMarker.put()
        targetMarkerDict = newTargetMarker.to_dict()
        targetMarkerDict['self'] = '/target/' + newTargetMarker.key.urlsafe() 
        self.response.status_int = 200
        self.response.write(json.dumps(targetMarkerDict))
        #Dev Note: add code to validate that the user logged in and that the user info was sent

    def get(self, id=None):
        if id:
            try:
              t = ndb.Key(urlsafe=id).get()
              targetMarkerDict = t.to_dict()
              targetMarkerDict['self'] = "/target/" + id
              self.response.status_int = 200
              self.response.write(json.dumps(targetMarkerDict))
            except:
                self.response.status_int = 204
                self.response.write("Record not found.")
        else:
            #get the userID if it is set as a REST parameter
            userID = self.request.get("user_id")
            if userID:
              #query the targetMarkers for just this user
              targetMarkers = ndb.gql("SELECT * FROM targetMarker WHERE createdBy = '" + userID + "'")
              self.response.status_int = 200
              #self.response.write("Get all request received.")
              #iterate through each targetMarker and return it
              JSONOutputString = ""
              JSONOutputString = JSONOutputString + '['
              for p in targetMarkers:
                JSONOutputString = JSONOutputString + '{'
                JSONOutputString = JSONOutputString + '"name":"'
                JSONOutputString = JSONOutputString + str(p.name)
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"key":"'
                JSONOutputString = JSONOutputString + str(p.key.urlsafe())
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"url":"'
                JSONOutputString = JSONOutputString + str(p.url)
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"longitude":"'
                JSONOutputString = JSONOutputString + str(p.longitude)
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"latitude":"'
                JSONOutputString = JSONOutputString + str(p.latitude)
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"createdBy":"'
                JSONOutputString = JSONOutputString + str(p.createdBy)
                JSONOutputString = JSONOutputString + '"'
                
                JSONOutputString = JSONOutputString + '},'
              JSONOutputString = JSONOutputString.rstrip(',')
              JSONOutputString = JSONOutputString + ']'
              self.response.write(JSONOutputString)  
            else:  
              #query the targetMarkers for all
              targetMarkers = ndb.gql("SELECT * FROM targetMarker")
              self.response.status_int = 200
              #self.response.write("Get all request received.")
              #iterate through each targetMarker and return it
              JSONOutputString = ""
              JSONOutputString = JSONOutputString + '['
              for p in targetMarkers:
                JSONOutputString = JSONOutputString + '{'
                JSONOutputString = JSONOutputString + '"name":"'
                JSONOutputString = JSONOutputString + str(p.name)
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"self":"'
                JSONOutputString = JSONOutputString + str(p.key.urlsafe())
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"url":"'
                JSONOutputString = JSONOutputString + str(p.url)
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"longitude":"'
                JSONOutputString = JSONOutputString + str(p.longitude)
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"latitude":"'
                JSONOutputString = JSONOutputString + str(p.latitude)
                JSONOutputString = JSONOutputString + '"'
                JSONOutputString = JSONOutputString + ','
                JSONOutputString = JSONOutputString + '"createdBy":"'
                JSONOutputString = JSONOutputString + str(p.createdBy)
                JSONOutputString = JSONOutputString + '"'
                
                JSONOutputString = JSONOutputString + '},'
              JSONOutputString = JSONOutputString.rstrip(',')
              JSONOutputString = JSONOutputString + ']'
              self.response.write(JSONOutputString)  
            
        #Dev Note: in version 2 add GET functionality for getting nearby latitude and longitude within distance
            
    def delete(self, id=None):
        if id:
            try:
                t = ndb.Key(urlsafe=id).get()
                t.key.delete()
                self.response.status_int = 200
                self.response.write("Record deleted.")
            except:
                self.response.status_int = 204
                self.response.write("Record not found.")                
        else:
            self.response.status_int = 400
            self.response.write("Delete request received, but no ID.")
        #Dev Note: in version 2 add code to validate that this user is authorized to delete this record

    def patch(self, id=None):
        if id:
            #match the record
            t = ndb.Key(urlsafe=id).get()
            targetMarkerData = json.loads(self.request.body)
            ##set the values of the record from the parameters
            t.latitude = targetMarkerData['latitude']
            t.longitude = targetMarkerData['longitude']
            t.name = targetMarkerData['name']
            t.url = targetMarkerData['url']
            
            #update the values in the DB
            t.put()

            #respond to the client
            targetMarkerDict = t.to_dict()
            self.response.status_int = 200
            self.response.write(json.dumps(targetMarkerDict))
        else:
            self.response.status_int = 400
            self.response.write("Patch request received, but no ID.")
        #Dev Note: in version 2 add code to validate that this user is authorized to modify this record


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.status_int = 404
        self.response.write("Incorrect URL")

# Code added to allow PATCH method
# source: https://stackoverflow.com/questions/16280496/patch-method-handler-on-google-appengine-webapp2
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# [START main]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/target', targetMarkerHandler), #post
    ('/target/(.*)', targetMarkerHandler) #get, delete, patch
], debug=True)
# [END main]
