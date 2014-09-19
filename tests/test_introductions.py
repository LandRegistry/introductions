import json
import unittest
import uuid
from introductions.server import app
from introductions import db


class IntroductionTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        db.create_all()
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_can_hit_url(self):
        with self.app.test_request_context():
            resp = self.client.get("/")
            self.assertEquals(resp.status_code, 200)
            self.assertEquals(resp.data, 'OK')

    def test_start_relationship_and_retrieve_details_is_successful(self):
        with self.app.test_request_context():
            conveyancer_lrid = uuid.uuid4()
            client_lrid = uuid.uuid4();
            jd = json.dumps({"title_number":"test_title", "conveyancer_lrid":str(conveyancer_lrid),
                             "clients":[{"lrid": str(client_lrid)}],
                             "task":"buying", "conveyancer_name":"Bob's realty", "conveyancer_address":"somewhere"})
            response = self.client.post("/relationship",
                             data=jd,
                             headers={'content-type': 'application/json'})

            self.assertEquals(response.status_code, 200)

            get_response = self.client.get("/details/%s" % json.loads(response.data)['token'])
            self.assertEquals(get_response.status_code, 200)
