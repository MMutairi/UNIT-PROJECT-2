
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

class Vision2030Tests(SimpleTestCase):

    def test_vision2030_page(self):
        response = self.client.get(
            reverse("core:vision2030")
        )

        self.assertEqual(response.status_code, 200)

    def test_vision2030_template(self):
        response = self.client.get(
            reverse("core:vision2030")
        )

        self.assertTemplateUsed(
            response,
            "core/vision2030.html"
        )

        self.assertIn("vision", response.context)

    def test_hero_and_overview(self):
        response = self.client.get(
            reverse("core:vision2030")
        )

        vision = response.context["vision"]

        self.assertTrue(vision["hero"]["title"])
        self.assertTrue(vision["overview"]["description"])

        self.assertContains(
            response,
            "Vision 2030"
        )

        self.assertContains(
            response,
            "Building a More Diverse Industrial Economy"
        )

    def test_three_vision_pillars(self):
        vision = load_json("vision2030.json")

        pillars = vision["pillars"]

        self.assertEqual(len(pillars), 3)

        pillar_names = {
            pillar["name"]
            for pillar in pillars
        }

        self.assertEqual(
            pillar_names,
            {
                "A Vibrant Society",
                "A Thriving Economy",
                "An Ambitious Nation"
            }
        )

    def test_three_targets(self):
        vision = load_json("vision2030.json")

        targets = vision["targets"]

        self.assertEqual(len(targets), 3)

        values = {
            target["value"]
            for target in targets
        }

        self.assertEqual(
            values,
            {"50%", "65%", "4,000"}
        )

    def test_target_statuses_are_distinct(self):
        vision = load_json("vision2030.json")

        targets = {
            target["value"]: target
            for target in vision["targets"]
        }

        self.assertEqual(
            targets["50%"]["status"],
            "Vision 2030 target"
        )

        self.assertEqual(
            targets["65%"]["status"],
            "Vision 2030 target"
        )

        self.assertEqual(
            targets["4,000"]["status"],
            "Program aim"
        )

        self.assertEqual(
            targets["50%"]["timeframe"],
            "2030"
        )

        self.assertNotEqual(
            targets["4,000"]["timeframe"],
            "2030"
        )

    def test_four_focus_areas(self):
        vision = load_json("vision2030.json")

        areas = vision["focus_areas"]

        self.assertEqual(len(areas), 4)

        for area in areas:
            self.assertTrue(area["title"])
            self.assertTrue(area["description"])

    def test_six_initiatives(self):
        vision = load_json("vision2030.json")

        initiatives = vision["initiatives"]

        self.assertEqual(len(initiatives), 6)

        names = {
            item["name"]
            for item in initiatives
        }

        self.assertIn(
            "National Industrial Strategy",
            names
        )

        self.assertIn(
            "Future Factories Program",
            names
        )

        self.assertIn(
            "Made in Saudi Program",
            names
        )

    def test_unique_content_ids(self):
        vision = load_json("vision2030.json")

        for key in (
            "pillars",
            "targets",
            "focus_areas",
            "initiatives"
        ):
            with self.subTest(section=key):
                ids = [
                    item["id"]
                    for item in vision[key]
                ]

                self.assertEqual(
                    len(ids),
                    len(set(ids))
                )

    def test_official_source_urls(self):
        vision = load_json("vision2030.json")

        urls = [
            vision["overview"]["source_url"]
        ]

        urls.extend(
            item["source_url"]
            for item in vision["targets"]
        )

        urls.extend(
            item["source_url"]
            for item in vision["initiatives"]
        )

        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(
                    url.startswith("https://")
                )

    def test_vision_image_exists(self):
        vision = load_json("vision2030.json")

        image_path = (
            settings.BASE_DIR
            / "static"
            / vision["hero"]["image"]
        )

        self.assertTrue(
            image_path.is_file()
        )

    def test_vision_page_navigation(self):
        response = self.client.get(
            reverse("core:vision2030")
        )

        self.assertContains(
            response,
            reverse("catalog:industries")
        )

        self.assertContains(
            response,
            reverse("catalog:industrial_cities")
        )

        self.assertContains(
            response,
            reverse("catalog:made_in_saudi")
        )

        self.assertContains(
            response,
            reverse("core:technology")
        )

        self.assertContains(
            response,
            "Sources and Information"
        )
