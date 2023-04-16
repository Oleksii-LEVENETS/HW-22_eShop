import json

from orders import tasks

import requests

from shop.models import Product


def api_cart(pk, stock):
    url_base = "http://estorehouse:8001/product"
    headers = {"Content-Type": "application/json"}
    data = {"stock": stock}
    url = f"{url_base}/{pk}/"
    response_old = requests.get(url, headers=headers)
    response_new = requests.patch(url, data=json.dumps(data), headers=headers)
    book = Product.objects.get(pk=pk)
    subject = f"Change book {book}: shop -> storehouse"
    message = f"Was: {response_old.json()}\n" f"Is:  {response_new.json()}"
    tasks.send_mail_temp.delay(subject, message)


def api_order_new(pk, first_name, last_name, email, phone_number, city, created, updated, paid):
    url = "http://estorehouse:8001/order/"
    headers = {"Content-Type": "application/json"}
    data = {
        "id": pk,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "city": city,
        "created": created.strftime("%Y-%m-%d %H:%M:%S"),
        "updated": updated.strftime("%Y-%m-%d %H:%M:%S"),
        "paid": paid,
    }
    requests.post(url, data=json.dumps(data), headers=headers)


def api_order_paid_change(pk, paid):
    url = f"http://estorehouse:8001/order/{pk}/"
    headers = {"Content-Type": "application/json"}
    data = {
        "paid": paid,
    }
    requests.patch(url, data=json.dumps(data), headers=headers)


def api_order_delete(pk):
    url = f"http://estorehouse:8001/order/{pk}/"
    headers = {"Content-Type": "application/json"}
    data = {
        "id": pk,
    }
    requests.delete(url, data=json.dumps(data), headers=headers)


def api_orderitem(pk, order, product, price, quantity):
    url = "http://estorehouse:8001/orderitems/"
    headers = {"Content-Type": "application/json"}
    data = {
        "id": pk,
        "order": order,
        "product": product,
        "price": price,
        "quantity": quantity,
    }
    requests.post(url, data=json.dumps(data, ensure_ascii=False, default=str), headers=headers)


def api_orderitem_delete(pk):
    url = f"http://estorehouse:8001/orderitems/{pk}/"
    headers = {"Content-Type": "application/json"}
    data = {
        "id": pk,
    }
    requests.delete(url, data=json.dumps(data), headers=headers)
