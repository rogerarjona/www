import logging
import uuid

from stdimage import StdImageField

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

logger = logging.getLogger(__name__)
phone_regex = RegexValidator(regex=r'^\d{8,14}((,\d{8,14})?)*$',
                             message="El formato del teléfono debe ser: '9998888777', "
                                     "sin código de país. De 8-14 dígitos permitidos. "
                                     "Puede agregar más telefonos seperados por coma.")


class User(AbstractUser):

    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    TYPE = (
        (ADMIN, ADMIN),
        (EDITOR, EDITOR),
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, MinLengthValidator(5)],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    avatar = StdImageField(
        verbose_name=_("avatar"),
        upload_to='users/%Y/%m/', variations={'perfil': {"width": 240, "height": 240, "crop": True},
                                              'thumbnail': {"width": 45, "height": 45, "crop": True}},
        default="users/avatar.png")
    type = models.CharField(
        verbose_name=_("type of user"),
        choices=TYPE,
        default=ADMIN,
        blank=False,
        max_length=15)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username
