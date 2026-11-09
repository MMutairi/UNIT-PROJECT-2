from django.shortcuts import render


def industries(request):
    return render(request, "catalog/industries.html")


def industry_detail(request, slug):
    return render(request, "catalog/industry_detail.html", {"slug": slug})


def companies(request):
    return render(request, "catalog/companies.html")


def company_detail(request, slug):
    return render(request, "catalog/company_detail.html", {"slug": slug})


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
