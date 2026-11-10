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

class CompanyTests(SimpleTestCase):

    def test_companies_page(self):
        response = self.client.get(
            reverse("catalog:companies")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/companies.html"
        )
        self.assertEqual(
            len(response.context["companies"]),
            6
        )

    def test_company_search(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {"q": "SABIC"}
        )

        self.assertEqual(response.status_code, 200)

        companies = response.context["companies"]

        self.assertEqual(len(companies), 1)
        self.assertEqual(
            companies[0]["slug"],
            "sabic"
        )

    def test_industry_filter(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {"industry": "automotive"}
        )

        self.assertEqual(response.status_code, 200)

        companies = response.context["companies"]

        self.assertEqual(len(companies), 1)
        self.assertEqual(
            companies[0]["name"],
            "Ceer"
        )

    def test_location_filter(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {"location": "Riyadh"}
        )

        self.assertEqual(response.status_code, 200)

        companies = response.context["companies"]

        self.assertGreater(len(companies), 0)

        for company in companies:
            self.assertEqual(
                company["location"],
                "Riyadh"
            )

    def test_combined_filters(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {
                "q": "alfanar",
                "industry": "energy-technologies",
                "location": "Riyadh"
            }
        )

        self.assertEqual(response.status_code, 200)

        companies = response.context["companies"]

        self.assertEqual(len(companies), 1)
        self.assertEqual(
            companies[0]["slug"],
            "alfanar"
        )

    def test_company_detail(self):
        response = self.client.get(
            reverse(
                "catalog:company_detail",
                args=["ceer"]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/company_detail.html"
        )
        self.assertEqual(
            response.context["company"]["slug"],
            "ceer"
        )
        self.assertContains(
            response,
            "King Abdullah Economic City"
        )
        self.assertContains(
            response,
            "Automotive"
        )

    def test_invalid_company(self):
        response = self.client.get(
            reverse(
                "catalog:company_detail",
                args=["unknown-company"]
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_empty_search_results(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {"q": "nonexistent-company-xyz"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["companies"]),
            0
        )
        self.assertContains(
            response,
            "No Companies Found"
        )

    def test_company_industry_relationships(self):
        from .content_loader import load_json

        companies = load_json("companies.json")["companies"]
        industries = load_json("industries.json")["industries"]

        industry_slugs = {
            industry["slug"]
            for industry in industries
        }

        for company in companies:
            self.assertIn(
                company["industry_slug"],
                industry_slugs
            )
