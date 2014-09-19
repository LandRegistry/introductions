import json
import unittest
import uuid
from introductions.server import app
from introductions import db
from introductions.models import Conveyancer


class IntroductionTestCase(unittest.TestCase):
    conveyancer_lrid = uuid.UUID("214b78b1-20a0-4cdb-a0f3-111b5ba21d48")
    client_lrid = uuid.UUID("f55a02a0-057b-4a3f-9e34-ede5791a5874")
    token = "FKLN"
    title_number = "TEST1410429781566"

    def setUp(self):
        app.config["TESTING"] = True
        db.create_all()
        self.app = app
        self.client = app.test_client()
        self.__add_conveyancer_to_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_can_hit_url(self):
        with self.app.test_request_context():
            resp = self.client.get("/")
            self.assertEquals(resp.status_code, 200)
            self.assertEquals(resp.data, 'OK')

    def test_start_relationship(self):
        with self.app.test_request_context():
            jd = self.__get_relationship_json()

            response = self.client.post("/relationship",
                                        data=jd,
                                        headers={'content-type': 'application/json'})

            self.assertEquals(response.status_code, 200)
            self.assertTrue('token' in response.data)

    def test_confirmation_with_invalid_lrid(self):
        with self.app.test_request_context():
            jd = self.__get_invalid_uuid_confirm_json()

            response = self.client.post("/confirm",
                                        data=jd,
                                        headers={'content-type': 'application/json'})

            self.assertEquals(response.status_code, 400)

    def test_invalid_start_relationship(self):
        with self.app.test_request_context():
            jd = self.__get_invalid_relationship_json()

            response = self.client.post("/relationship",
                                        data=jd,
                                        headers={'content-type': 'application/json'})

            self.assertEquals(response.status_code, 400)

    def test_relationship_with_invalid_conveyancer_lrid(self):
        with self.app.test_request_context():
            jd = self.__get_relationship_json_with_invalid_conveyancer()

            response = self.client.post("/relationship",
                                        data=jd,
                                        headers={'content-type': 'application/json'})

            self.assertEquals(response.status_code, 404)

    def test_start_relationship_and_retrieve_token_details(self):
        with self.app.test_request_context():
            jd = self.__get_relationship_json()

            response = self.client.post("/relationship",
                                        data=jd,
                                        headers={'content-type': 'application/json'})

            self.assertEquals(response.status_code, 200)
            self.assertTrue('token' in response.data)

            token = json.loads(response.data)
            response = self.client.get("/details/%s" %token["token"])

            response_json = json.loads(response.data)
            self.assertEquals(response.status_code, 200)
            self.assertTrue('conveyancer_lrid' in response.data)
            self.assertItemsEqual(response_json['conveyancer_lrid'], str(self.conveyancer_lrid))
            self.assertItemsEqual(response_json['client_lrid'], str(self.client_lrid))
            self.assertItemsEqual(response_json['title_number'], str(self.title_number))

    def test_retrieve_invalid_token_details(self):
        with self.app.test_request_context():
            response = self.client.get("/details/ZZZ")
            self.assertEquals(response.status_code, 400)

    def test_create_and_confirm_relationship(self):
        with self.app.test_request_context():
            jd = self.__get_relationship_json()

            response = self.client.post("/relationship",
                                        data=jd,
                                        headers={'content-type': 'application/json'})

            token = json.loads(response.data)
            confirm_json = self.__get_confirm_json(token['token'])

            response = self.client.post("/confirm",
                                        data=confirm_json,
                                        headers={'content-type': 'application/json'})

            self.assertEquals(response.status_code, 200)
            self.assertTrue('conveyancer_name' in response.data)

    def test_invalid_confirmation_details(self):
        with self.app.test_request_context():
            jd = self.__get_relationship_json()

            response = self.client.post("/relationship",
                                        data=jd,
                                        headers={'content-type': 'application/json'})

            confirm_json = self.__get_invalid_confirm_json()

            response = self.client.post("/confirm",
                                        data=confirm_json,
                                        headers={'content-type': 'application/json'})

            self.assertEquals(response.status_code, 400)

    def __add_conveyancer_to_db(self):
        conveyancer = Conveyancer()
        conveyancer.lrid = self.conveyancer_lrid
        conveyancer.name = "Mr Gustavo Fring"
        conveyancer.address = "Los Pollos Hermanos, Albuquerque, New Mexico"
        db.session.add(conveyancer)
        db.session.commit()

    def __get_relationship_json(self):
        relationship_json = json.dumps({"title_number": self.title_number,
                                        "conveyancer_lrid": str(self.conveyancer_lrid),
                                        "clients": [{"lrid": str(self.client_lrid)}],
                                        "task": "buying", "conveyancer_name": "Enact",
                                        "conveyancer_address": "somewhere"})
        return relationship_json

    def __get_relationship_json_with_invalid_conveyancer(self):
        relationship_json = json.dumps({"title_number": self.title_number,
                                        "conveyancer_lrid": "214b78b1-20a0-4cdb-a0f3-111b5ba21d55",
                                        "clients": [{"lrid": str(self.client_lrid)}],
                                        "task": "buying", "conveyancer_name": "Enact",
                                        "conveyancer_address": "somewhere"})
        return relationship_json

    def __get_invalid_uuid_confirm_json(self):
        confirm_json = json.dumps({"client_lrid": "214b78b1-aaaa-a-a-a-a-",
                                   "token": self.token})
        return confirm_json

    def __get_invalid_relationship_json(self):
        relationship_json = json.dumps({"conveyancer_lrid": str(self.conveyancer_lrid),
                                        "clients": [{"lrid": str(self.client_lrid)}],
                                        "task": "buying", "conveyancer_name": "Enact",
                                        "conveyancer_address": "somewhere"})
        return relationship_json

    def __get_confirm_json(self, token):
        confirm_json = json.dumps({"client_lrid": str(self.client_lrid),
                                   "token": token})
        return confirm_json

    def __get_invalid_confirm_json(self):
        invalid_confirm_json = json.dumps({"client_lrid": str(self.client_lrid),
                                           "token": "ABCD"})
        return invalid_confirm_json
