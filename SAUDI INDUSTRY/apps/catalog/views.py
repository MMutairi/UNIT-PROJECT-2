from django.http import Http404
from django.shortcuts import render

from .content_loader import load_json


def industries(request):
    data = load_json("industries.json")
    all_industries = data["industries"]

    search_query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()

    categories = sorted({
        industry["category"]
        for industry in all_industries
    })

    filtered_industries = all_industries

    if search_query:
        query = search_query.casefold()

        filtered_industries = [
            industry
            for industry in filtered_industries
            if query in industry["name"].casefold()
            or query in industry["description"].casefold()
            or query in industry["category"].casefold()
        ]

    if selected_category:
        filtered_industries = [
            industry
            for industry in filtered_industries
            if industry["category"] == selected_category
        ]

    context = {
        "industries": filtered_industries,
        "categories": categories,
        "search_query": search_query,
        "selected_category": selected_category,
        "total_industries": len(all_industries),
    }

    return render(request, "catalog/industries.html", context)


def industry_detail(request, slug):
    data = load_json("industries.json")

    industry = next(
        (
            item
            for item in data["industries"]
            if item["slug"] == slug
        ),
        None
    )

    if industry is None:
        raise Http404("Industry not found")

    return render(
        request,
        "catalog/industry_detail.html",
        {"industry": industry}
    )


def companies(request):
    return render(request, "catalog/companies.html")


def company_detail(request, slug):
    return render(
        request,
        "catalog/company_detail.html",
        {"slug": slug}
    )


def industrial_cities(request):
    return render(request, "catalog/industrial_cities.html")


def industrial_city_detail(request, slug):
    return render(
        request,
        "catalog/industrial_city_detail.html",
        {"slug": slug}
    )


def made_in_saudi(request):
    return render(request, "catalog/made_in_saudi.html")
