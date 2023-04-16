from celery import shared_task

from core import settings

from django.core.mail import send_mail
from django.http import BadHeaderError, HttpResponse

import requests

from shop.models import Product


@shared_task
def send_mail_temp(subject, message, user_email=None):
    email_to = [settings.EMAIL_HOST_USER, user_email]
    if user_email is None:
        email_to = [settings.EMAIL_HOST_USER]
    try:
        send_mail(
            subject=f"{subject}",
            message=f"{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_to,
            fail_silently=False,
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")


"""
Import json data from URL to Database
"""


# Helping function: Checking the connection to the site:
def check_connection(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.HTTPError:
        return False
    except Exception:
        return False


@shared_task
def synchro_db(*args, **kwargs):
    """
    Makes a GET request to the API.
    """

    page = 1
    while True:
        # http://localhost:8001/product/?page=1   -- the first page of the site
        IMPORT_URL = f"http://estorehouse:8001/product/?page={page}"  # noqa: N806
        headers = {"Content-Type": "application/json"}
        if not check_connection(IMPORT_URL):  # Helping function: Checking the connection to the site
            return

        response = requests.get(
            url=IMPORT_URL,
            headers=headers,
        )
        data_object = response.json()
        for data in data_object["results"]:
            name = data.get("name")
            price = data.get("price")
            stock = data.get("stock")
            isbn_no = data.get("isbn_no")

            try:
                updated_values = {"name": name, "price": price, "stock": stock}
                product, created = Product.objects.update_or_create(isbn_no=isbn_no, defaults=updated_values)
            except Exception as ex:
                raise ex

        page += 1
