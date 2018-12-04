import unittest
from flask import json
from app import create_app
from instance.config import TestingConfig

from app.api.v1.models.incidents import incidents_list


class IncidentTest(unittest.TestCase):
    def setUp(self):
        self.incident = {
            "incidentType": "redflag",
            "comment" : "kskksd jieioe",
            "createdBy" : 8,
            "location" : "nairobi"
        }
        self.app = create_app(config_name=TestingConfig)
        self.client = self.app.test_client()

    def create_test_record(self):
        self.client.post('/api/v1/incidents', data=json.dumps(self.incident), content_type='application/json')

    def test_create_incident_success(self):
        resp = self.client.post('/api/v1/incidents', data=json.dumps(self.incident), content_type='application/json')
        data = json.loads(resp.data)
        # self.assertEqual(resp.status_code, 200)
        self.assertEqual("status", 201)
        self.assertEqual(data['Incident'], resp)


    # def test_incident_id_increments_correctly(self):
    #     self.client.post('/api/v1/incidents', data=json.dumps(self.incident), content_type='application/json')
    #     resp = self.client.post('/api/v1/incidents', data=json.dumps(self.incident), content_type='application/json')
    #     data = json.loads(resp.data)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertEqual(data['Incident'], resp)
    #     self.assertEqual(len(incidents_list), 2)



    def test_can_get_all_incidents(self):
        self.create_test_record()
        resp = self.client.get('/api/v1/incidents')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['Incident'], resp)
        self.assertEqual(len(data['Incidents']), 1)

    def test_can_patch_a_location(self):
        self.create_test_record()
        patch_data = {
            "location": "mombasa"
        }
        resp = self.client.patch('/api/v1/incident/1/location', data=json.dumps(patch_data), content_type='application/json')
        data = json.loads(resp.data)
        self.assertEqual(data['Incident'], resp)
        self.assertEqual(resp.status_code, 202)
        self.assertEqual(data['data']['location'], 'mombasa')


    def test_can_not_if_attribute_not_specified(self):
        self.create_test_record()
        patch_data = {
            "": ""
        }
        resp = self.client.patch('/api/v1/incident/1/incidentType', data=json.dumps(patch_data), content_type='application/json')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)

    def test_can_patch_a_comment(self):
        self.create_test_record()
        patch_data = {
            "comment": "I have just updated this comment"
        }
        resp = self.client.patch('/api/v1/incident/1/comment', data=json.dumps(patch_data), content_type='application/json')
        data = json.loads(resp.data)
        self.assertEqual(data['Incident'], resp)
        self.assertEqual(resp.status_code, 202)
        self.assertEqual(data['data']['comment'], 'I have just updated this comment')


    def test_can_get_incident_by_id(self):
        self.create_test_record()
        resp = self.client.get('/api/v1/incident/1')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(incidents_list), 1)
        self.assertEqual(data['incidentType'], 'redflag')

    # def test_get_non_existent_incident(self):
    #     self.create_test_record()
    #     resp = self.client.get('/api/v1/incident/10')
    #     data = json.loads(resp.data)
    #     # self.assertEqual(resp.status_code, 404)
    #     self.assertEqual(data['message'], 'Record with that ID does not exist.')

    def test_can_delete_incident(self):
        self.create_test_record()
        resp = self.client.get('/api/v1/incident/1')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(len(incidents_list), 0)
        self.assertEqual(data['message'], resp)


    def tearDown(self):
        incidents_list.clear()
