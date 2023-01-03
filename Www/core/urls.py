"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from ckeditor_uploader import views as views_ckeditor

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    # apps
    path('', include('Www.apps.blog.urls')),

    # Extras
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/upload/', views_ckeditor.upload, name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(views_ckeditor.browse), name='ckeditor_browse'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        # DEBUG TOOLBAR
        path('__debug__/', include(debug_toolbar.urls)),
        # TAILWIND
        path("__reload__/", include("django_browser_reload.urls")),
    ] + urlpatterns
