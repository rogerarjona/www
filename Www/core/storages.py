from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class CustomMediaStorage(S3Boto3Storage):
    """
        Basic Class Media Bucket
    """
    location = settings.MEDIAFILES_LOCATION


# class CustomStaticStorage(S3Boto3Storage):
#     """
#         Basic Class Media Bucket
#     """
#     location = settings.AWS_STATIC_LOCATION
