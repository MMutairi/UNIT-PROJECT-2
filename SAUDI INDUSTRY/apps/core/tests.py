
from django.conf import settings
from django.test import SimpleTestCase
from django.urls import reverse

from apps.catalog.content_loader import load_json


class TechnologyTests(SimpleTestCase):

    def test_technology_page(self):
        response = self.client.get(
            reverse("core:technology")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "core/technology.html"
        )

        self.assertEqual(
            len(response.context["technologies"]),
            6
        )

    def test_search_case_insensitive(self):
        response = self.client.get(
            reverse("core:technology"),
            {"q": "dIgItAl TwInS"}
        )

        self.assertEqual(response.status_code, 200)

        technologies = response.context["technologies"]

        self.assertEqual(len(technologies), 1)
        self.assertEqual(
            technologies[0]["slug"],
            "digital-twins"
        )

    def test_category_filter(self):
        response = self.client.get(
            reverse("core:technology"),
            {"category": "Robotics & Automation"}
        )

        technologies = response.context["technologies"]

        slugs = {
            item["slug"]
            for item in technologies
        }

        self.assertEqual(
            slugs,
            {
                "industrial-robotics",
                "industrial-automation"
            }
        )

    def test_industry_filter(self):
        response = self.client.get(
            reverse("core:technology"),
            {"industry": "mining-metals"}
        )

        technologies = response.context["technologies"]

        slugs = {
            item["slug"]
            for item in technologies
        }

        self.assertEqual(
            slugs,
            {
                "ai-manufacturing",
                "industrial-iot",
                "digital-twins"
            }
        )

    def test_combined_filters(self):
        response = self.client.get(
            reverse("core:technology"),
            {
                "q": "PLC",
                "category": "Robotics & Automation",
                "industry": "petrochemicals"
            }
        )

        technologies = response.context["technologies"]

        self.assertEqual(len(technologies), 1)
        self.assertEqual(
            technologies[0]["slug"],
            "industrial-automation"
        )

    def test_technology_detail(self):
        response = self.client.get(
            reverse(
                "core:technology_detail",
                args=["industrial-robotics"]
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "core/technology_detail.html"
        )

        self.assertEqual(
            response.context["technology"]["slug"],
            "industrial-robotics"
        )

        self.assertContains(response, "How It Works")
        self.assertContains(response, "Industrial Applications")
        self.assertContains(response, "Benefits")
        self.assertContains(
            response,
            "Challenges and Considerations"
        )

    def test_invalid_technology(self):
        response = self.client.get(
            reverse(
                "core:technology_detail",
                args=["unknown-technology"]
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_empty_search_results(self):
        response = self.client.get(
            reverse("core:technology"),
            {"q": "technology-xyz-not-found"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(response.context["technologies"]),
            0
        )

        self.assertContains(
            response,
            "No Technologies Found"
        )

    def test_all_technology_detail_pages(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        for item in technologies:
            with self.subTest(slug=item["slug"]):
                response = self.client.get(
                    reverse(
                        "core:technology_detail",
                        args=[item["slug"]]
                    )
                )

                self.assertEqual(
                    response.status_code,
                    200
                )

                self.assertContains(
                    response,
                    item["name"]
                )

    def test_valid_industry_relationships(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        industries = load_json(
            "industries.json"
        )["industries"]

        industry_slugs = {
            industry["slug"]
            for industry in industries
        }

        for item in technologies:
            for slug in item["industry_slugs"]:
                self.assertIn(
                    slug,
                    industry_slugs
                )

    def test_unique_ids_and_slugs(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        ids = [
            item["id"]
            for item in technologies
        ]

        slugs = [
            item["slug"]
            for item in technologies
        ]

        self.assertEqual(
            len(ids),
            len(set(ids))
        )

        self.assertEqual(
            len(slugs),
            len(set(slugs))
        )

    def test_technology_image_files(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        for item in technologies:
            with self.subTest(slug=item["slug"]):
                image_path = (
                    settings.BASE_DIR
                    / "static"
                    / item["image"]
                )

                self.assertTrue(
                    image_path.is_file()
                )

    def test_required_technology_content(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        for item in technologies:
            with self.subTest(slug=item["slug"]):
                self.assertTrue(item["name"])
                self.assertTrue(item["description"])
                self.assertTrue(item["overview"])
                self.assertTrue(item["how_it_works"])
                self.assertTrue(item["applications"])
                self.assertTrue(item["benefits"])
                self.assertTrue(item["considerations"])
                self.assertTrue(item["industry_slugs"])
                self.assertTrue(
                    item["source_url"].startswith("https://")
                )

    def test_saudi_program_information(self):
        page = load_json("technology.json")["page"]

        self.assertTrue(page["title"])
        self.assertTrue(page["saudi_context"])

        self.assertTrue(
            page["saudi_source_url"].startswith("https://")
        )

        response = self.client.get(
            reverse("core:technology")
        )

        self.assertContains(
            response,
            "Future Factories in Saudi Arabia"
        )
