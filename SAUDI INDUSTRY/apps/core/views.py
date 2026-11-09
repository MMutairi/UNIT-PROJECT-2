from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def technology(request):
    return render(request, "core/technology.html")


def vision2030(request):
    return render(request, "core/vision2030.html")


def gallery(request):
    return render(request, "core/gallery.html")


def about(request):
    return render(request, "core/about.html")
