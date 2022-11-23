from app import celery

from celery import shared_task
from celery import utils

from django.core.management import call_command

@shared_task
def delete_expired_links_task():
    call_command("delete_expired_links",)
