from django.shortcuts import render

from .models import Post


def index(request):
    o = Post.objects.first()
    context = {
        "post": o,
        "meta": o.as_meta(request)
    }
    return render(request, "index.html", context)