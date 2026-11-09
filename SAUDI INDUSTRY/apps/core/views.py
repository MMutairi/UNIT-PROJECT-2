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


def technology(request):
    return render(request, "core/technology.html")


def vision2030(request):
    return render(request, "core/vision2030.html")


def gallery(request):
    return render(request, "core/gallery.html")


def about(request):
    return render(request, "core/about.html")
