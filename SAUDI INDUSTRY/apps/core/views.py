from django.http import Http404
from django.shortcuts import render

from apps.catalog.content_loader import load_json


def home(request):
    home_data = load_json("home.json")
    industries_data = load_json("industries.json")

    industry_map = {
        industry["slug"]: industry
        for industry in industries_data["industries"]
    }

    featured_industries = [
        industry_map[slug]
        for slug in home_data["featured_industries"]
        if slug in industry_map
    ]

    context = {
        "home": home_data,
        "featured_industries": featured_industries,
    }

    return render(request, "core/home.html", context)


def load_technologies():
    technology_data = load_json("technology.json")
    industries_data = load_json("industries.json")

    industry_lookup = {
        industry["slug"]: industry
        for industry in industries_data["industries"]
    }

    return [
        {
            **item,
            "industries": [
                industry_lookup[slug]
                for slug in item["industry_slugs"]
                if slug in industry_lookup
            ]
        }
        for item in technology_data["technologies"]
    ]


def technology(request):
    page = load_json("technology.json")["page"]
    all_technologies = load_technologies()

    search_query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()
    selected_industry = request.GET.get("industry", "").strip()

    categories = sorted({
        item["category"]
        for item in all_technologies
    })

    industry_options = sorted(
        {
            industry["slug"]: industry
            for item in all_technologies
            for industry in item["industries"]
        }.values(),
        key=lambda industry: industry["name"]
    )

    filtered_technologies = all_technologies

    if search_query:
        query = search_query.casefold()

        filtered_technologies = [
            item
            for item in filtered_technologies
            if query in " ".join([
                item["name"],
                item["category"],
                item["description"],
                item["overview"],
                " ".join(item["applications"]),
                " ".join(
                    industry["name"]
                    for industry in item["industries"]
                ),
            ]).casefold()
        ]

    if selected_category:
        filtered_technologies = [
            item
            for item in filtered_technologies
            if item["category"] == selected_category
        ]

    if selected_industry:
        filtered_technologies = [
            item
            for item in filtered_technologies
            if selected_industry in item["industry_slugs"]
        ]

    context = {
        "page": page,
        "technologies": filtered_technologies,
        "categories": categories,
        "industry_options": industry_options,
        "search_query": search_query,
        "selected_category": selected_category,
        "selected_industry": selected_industry,
        "total_technologies": len(all_technologies),
    }

    return render(
        request,
        "core/technology.html",
        context
    )


def technology_detail(request, slug):
    all_technologies = load_technologies()

    item = next(
        (
            technology
            for technology in all_technologies
            if technology["slug"] == slug
        ),
        None
    )

    if item is None:
        raise Http404("Technology not found")

    return render(
        request,
        "core/technology_detail.html",
        {"technology": item}
    )


def vision2030(request):
    vision_data = load_json("vision2030.json")
    return render(
        request,
        "core/vision2030.html",
        {"vision": vision_data}
    )


def gallery(request):
    return render(request, "core/gallery.html")


def about(request):
    return render(request, "core/about.html")
