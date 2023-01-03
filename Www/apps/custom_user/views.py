
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from django.urls import reverse

User = get_user_model()


class UpdateProfileView(UpdateView):
    pass
