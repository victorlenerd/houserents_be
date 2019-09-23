from main import app
import unittest
import json


class MainTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDown(self) -> None:
        pass

    def setUp(self) -> None:
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_predict_status_code(self) -> None:
        result = self.app.post('/predict', data=json.dumps(dict(
                data=dict(
                    locations=list(dict(lat=6.5005, lng=3.3666)),
                    no_bed=1
                ))),
               content_type='application/json')

        self.assertEqual(result.status_code, 200)

    def test_apartments_status_code(self) -> None:
        result = self.app.post('/apartments?offset=0&limit=5', data=json.dumps(dict(
                    location=dict(lat=6.5005, lng=3.3666),
                    specs=dict(no_bed=1))),
               content_type='application/json')

        self.assertEqual(result.status_code, 200)

    def test_data_status_code(self) -> None:
        result = self.app.get('/data/data-1569199789403.json')
        self.assertEqual(result.status_code, 200)
