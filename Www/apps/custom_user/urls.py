from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (UpdateProfileView)


urlpatterns = [
    # path('profile/update/', login_required(UpdateProfileView.as_view()), name="editar_perfil"),
]
