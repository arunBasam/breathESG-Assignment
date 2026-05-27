from django.test import TestCase
from rest_framework.test import APIClient


class RecordTests(TestCase):

    def setUp(self):

        self.client = APIClient()


    def test_upload_record(self):

        res = self.client.post(

            "/api/records/",

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

            "/api/records/",

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
            "/api/records/stats/"
        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_health(self):

        res = self.client.get(
            "/api/records/health/"
        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_pagination(self):

        res = self.client.get(
            "/api/records/list/?page=1"
        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_quality(self):

        res = self.client.get(
            "/api/records/quality/"
        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_audit_summary(self):

        res = self.client.get(
            "/api/records/audit/summary/"
        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_audit_logs(self):

        res = self.client.get(
            "/api/records/audit/"
        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_record_history(self):

        self.client.post(

            "/api/records/",

            {
                "source": "TRAVEL"
            },

            format="json"

        )

        res = self.client.get(
            "/api/records/1/history/"
        )

        self.assertEqual(
            res.status_code,
            200
        )


    def test_reject(self):

        self.client.post(

            "/api/records/",

            {
                "source": "UTILITY"
            },

            format="json"

        )

        res = self.client.post(
            "/api/records/1/reject/"
        )

        self.assertEqual(
            res.status_code,
            200
        )