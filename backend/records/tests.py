from django.test import TestCase
from rest_framework.test import APIClient


BASE = "/api/v1/records/"


class RecordTests(TestCase):

    def setUp(self):

        self.client = APIClient()


    def test_upload_record(self):

        res = self.client.post(

            BASE,

            {
                "source": "SAP"
            },

            format="json"

        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_invalid_source(self):

        res = self.client.post(

            BASE,

            {
                "source": "ABC"
            },

            format="json"

        )

        self.assertEqual(
            res.status_code,
            400
        )


    def test_stats(self):

        res = self.client.get(

            BASE + "stats/"

        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_health(self):

        res = self.client.get(

            BASE + "health/"

        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_pagination(self):

        res = self.client.get(

            BASE + "list/?page=1"

        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_quality(self):

        res = self.client.get(

            BASE + "quality/"

        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_audit_summary(self):

        res = self.client.get(

            BASE + "audit/summary/"

        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_audit_logs(self):

        res = self.client.get(

            BASE + "audit/"

        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_record_history(self):

        self.client.post(

            BASE,

            {
                "source": "TRAVEL"
            },

            format="json"

        )

        res = self.client.get(

            BASE + "1/history/"

        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_reject(self):

        self.client.post(

            BASE,

            {
                "source": "UTILITY"
            },

            format="json"

        )

        res = self.client.post(

            BASE + "1/reject/"

        )

        self.assertEqual(
            res.status_code,
            200
        )