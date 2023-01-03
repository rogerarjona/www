# Python
from datetime import datetime

# Third Party Apps
from ckeditor_uploader.fields import RichTextUploadingField
# from stdimage.models import StdImageField
from pictures.models import PictureField
from meta.models import ModelMeta
# Django
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

# Apps

User = get_user_model()


def image_path(instance, filename):
    today = datetime.today()
    return F'uploads/{today.year}/{today.month}/{today.day}/{filename}'


class Category(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=80,
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        kwargs = {
            "category_slug": self.slug
        }
        return reverse("category_list", kwargs=kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=50,
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
    )

    def get_absolute_url(self):
        kwargs = {
            "category_slug": self.slug
        }
        return reverse("category_list", kwargs=kwargs)

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().select_related('category')\
            .filter(to_post=True).defer("content")


class Post(ModelMeta, models.Model):

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_("News URL"),
        help_text=_("URLs for SEO. It is completed automatically."),
        max_length=200,
        unique=True
    )
    description = models.CharField(
        verbose_name=_("Description"),
        max_length=255,
        blank=True
    )
    preview_image = PictureField(
        verbose_name=_("Cover Image"),
        upload_to=image_path,
        blank=True,
        # variations={
        #     'cover_story': {"width": 735, "height": 557, "crop": True},
        #     'cover_story_2': {"width": 361, "height": 272, "crop": True},
        #     'list_v1': {"width": 370, "height": 260, "crop": True},
        #     'list_v2': {"width": 142, "height": 129, "crop": True},
        #     'trending': {"width": 1170, "height": 519, "crop": True},
        # },
    )
    content = RichTextUploadingField(
        verbose_name=_("Post Content")
    )
    to_post = models.BooleanField(
        verbose_name=_("To Post?"),
        default=False,
    )
    visits = models.IntegerField(
        default=0
    )
    publish_on = models.DateTimeField(
        verbose_name=_("Publication Date"),
        blank=True,
        null=True,
    )
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    # FK
    author = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        "Category",
        verbose_name=_("Categoria"),
        related_name="post_categories",
        on_delete=models.SET_NULL,
        null=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("Tags"),
        blank=True
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = _("Posts")
        verbose_name_plural = verbose_name
        ordering = ['-created_on']

    _metadata = {
        'title': 'title',
        'description': 'description',
        'keywords': ['a,b,c,d'],
        # "image": settings.DEFAULT_IMAGE,
        # FB
        "use_og": False,
        "og_title": 'title',
        "og_description": 'description',
        # "title": False,
        # SCHEMA
        "use_schemaorg": True,
        "schemaorg_title": 'title',
        "schemaorg_description": 'description',
        # Twitter
        "twitter_title": 'title',
        "twitter_description": 'description',

        # "image_object": None,
        # "image_width": False,
        # "image_height": False,
        "object_type": "Article",
        "og_type": "Article",
        # "og_app_id": settings.FB_APPID,
        # "og_profile_id": settings.FB_PROFILE_ID,
        # "og_publisher": settings.FB_PUBLISHER,
        # "og_author_url": settings.FB_AUTHOR_URL,
        # "fb_pages": settings.FB_PAGES,
        # "twitter_type": settings.TWITTER_TYPE,
        # "twitter_site": settings.TWITTER_SITE,
        # "twitter_author": settings.TWITTER_AUTHOR,
        # "schemaorg_type": settings.SCHEMAORG_TYPE,
        "published_time": '',
        "modified_time": False,
        "expiration_time": False,
        "tag": False,
        "url": False,
        "locale": settings.TIME_ZONE,
    }

    def get_published_time(self):
        pass

    def get_modified_time(self):
        pass

    def get_absolute_url(self):
        kwargs = {
            'category_slug': self.category.slug,
            'slug': self.slug,
        }
        return reverse('post_detail', kwargs=kwargs)

    # def get_meta_image(self):
    #     if self.preview_image:
    #         return self.preview_image

    def __str__(self):
        return self.title
