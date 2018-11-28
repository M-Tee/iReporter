from flask import jsonify
from datetime import date
import uuid

incidents_list = []
class Incident(object):
   """class that deals with incidents data"""

   def __init__(self):
       self.incidents_list = incidents_list

    # Method to create an incident   
   def create(self, incidentType, comment, createdBy, location):
       incident_details = {}
       incident_details['createdBy'] = createdBy
       incident_details['incidentType'] = incidentType
       incident_details['location'] = location
       incident_details['status'] = "pending"
       incident_details['comment'] = comment
       incident_details['CreatedOn'] = date.today()
       incident_details['id'] = len(incidents_list) + 1

       incidents_list.append(incident_details)
       incidents = len(self.incidents_list)
       print(incidents)
       newIncident = self.incidents_list[incidents - 1]
       return jsonify({
           "status": 201,
           "message": "Created succesfully",
           "data": newIncident
       })

    # method to GET all incidents
   def get_all(self):
        return jsonify({
            "incidents" : self.incidents_list
    })
  
   def getById(self,    id):
        for item in incidents_list:
            if item['incidentType'] == 'redflag' and item['id'] == int(id):
                print('ghgh')
                return item
        return "no item found"