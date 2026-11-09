from django.test import SimpleTestCase
from django.urls import reverse


class IndustryTests(SimpleTestCase):

    def test_industries_page(self):
        response = self.client.get(
            reverse("catalog:industries")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["industries"]),
            6
        )

    def test_search(self):
        response = self.client.get(
            reverse("catalog:industries"),
            {"q": "pharma"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["industries"][0]["slug"],
            "pharmaceuticals"
        )
        self.assertEqual(
            len(response.context["industries"]),
            1
        )

    def test_category_filter(self):
        response = self.client.get(
            reverse("catalog:industries"),
            {"category": "Vehicle Manufacturing"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["industries"]),
            1
        )

    def test_industry_detail(self):
        response = self.client.get(
            reverse(
                "catalog:industry_detail",
                args=["petrochemicals"]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Petrochemicals")

    def test_invalid_industry(self):
        response = self.client.get(
            reverse(
                "catalog:industry_detail",
                args=["unknown-industry"]
            )
        )

        self.assertEqual(response.status_code, 404)
