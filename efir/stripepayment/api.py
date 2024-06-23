import logging
import os
import shutil
import time

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from orders.models import Order

from .auth import get_oauth_token

logger = logging.getLogger(__name__)
from datetime import datetime

import requests
from django.http import HttpResponse, JsonResponse


def track_shipment(request, shipment_number):
    url = "https://api-dev.dhl.com/ecs/ppl/myapi2/shipment"
    token = get_oauth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"Limit": 1, "Offset": 0, "ShipmentNumbers": [shipment_number]}

    try:
        response = requests.get(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError on bad responses
        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_today_date():
    return datetime.now().isoformat()


def order_trigger(request, batch_id, token, order_id):
    logging.info("function to create order is triggered")
    today_date = get_today_date()
    # order_id=331
    order = get_object_or_404(Order, id=order_id)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "orders": [
            {
                "orderType": "TransportOrder",  # Assuming TransportOrder for shipping
                "referenceId": order.etb_id,  # Unique reference ID
                "shipmentCount": "1",  # Number of shipments, assuming 1
                "email": "objednavky@efirthebrand.cz",  # Notification email
                "sendDate": today_date,  # Send date
                "productType": "BUSS",  # Product type: BUSS / IMPO
                "sender": {
                    "Name": "Ing. Valeriya Ageeva",
                    "Name2": "",  # Optional second name
                    "Street": "Příčná 1892/4",
                    "City": "Praha 1 - Nové Město",
                    "ZipCode": "11000",
                    "Country": "CZ",
                    "Contact": "Contact sender",
                    "Phone": "+420 774 363 883",
                    "Email": "objednavky@efirthebrand.cz",
                },
                "recipient": {
                    "Name": f"{order.first_name} {order.last_name}",
                    "Street": order.address,
                    "City": order.city,
                    "ZipCode": order.zipcode,
                    "Country": order.country,
                    "Contact": "Kontakt prijemce",
                    "Phone": order.number,
                    "Email": order.email,
                },
            }
        ]
    }

    order_url = f"{settings.API_BASE_URL}/order/batch"
    response = requests.post(order_url, headers=headers, json=payload)

    print("POST Request:")
    print("URL:", order_url)
    print("Headers:", headers)
    order_batch_url = response.headers.get("Location")
    order_batch_id = order_batch_url.split("/")[-1]

    print("Payload:", payload)
    print("Response status code:", response.status_code)
    print("Response headers:", response.headers)
    print("Response content:", response.content)
    print()
    time.sleep(5)
    # request get

    order_url_get = f"{settings.API_BASE_URL}/order/batch/{order_batch_id}"
    get_response = requests.get(order_url_get, headers=headers, json=payload)
    print("GET Request:")
    print("URL:", order_url_get)
    print("Headers:", headers)
    print("Response status code:", get_response.status_code)
    print("Response headers:", get_response.headers)
    print("Response content:", get_response.content)
    logging.info("order should be successfully created in PPL admin")

    return response


def create_package_label(payload, request, order_id):
    logging.info("function to create package is running")

    token = get_oauth_token()
    print("this is token:", token, "end of token")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    print("this is headers", headers)
    url = f"{settings.API_BASE_URL}/shipment/batch"
    response = requests.post(url, headers=headers, json=payload)

    print("this is response", response)
    print("Response status code:", response.status_code)
    print("Response content:", response.content)  # Log response content for debugging

    print("this is response", response)
    batch_url = response.headers.get("Location")
    print("this is batch url", batch_url)
    batch_id = batch_url.split("/")[-1]
    print(batch_id)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        logging.error(f"Request failed: {response.status_code} {response.text}")
        raise e

    if response.status_code == 201 or 200:
        data = response.json()
        print("this is data", data)
        try:
            shipment_number = data.get("shipmentNumber", [])
            print("this is shimpent number V1:", shipment_number)
        except Exception as e:
            print("exception", e)
        #order_trigger(request, batch_id, token, order_id)
        print("starting download pdf")
        download_pdf(batch_id, token, order_id)
        print("ending download pdf")
        return {"message": "Shipment batch created successfully", "batch_id": batch_id}

    try:
        return response.json()
    except ValueError:
        logging.error("Response content is not valid JSON")
        return {"error": "Response content is not valid JSON"}
    except Exception as e:
        logging.error(f"Unexpected error when parsing response: {str(e)}")
        return {"error": "Unexpected error when parsing response"}


def package_trigger(request):
    """
    this is a debugging help function
    """

    payload = {
        "returnChannel": {"type": "Email", "address": "test@test.cz"},
        "labelSettings": {
            "format": "Pdf",
            "dpi": 300,
            "completeLabelSettings": {
                "isCompleteLabelRequested": True,
                "pageSize": "A4",
                "position": 1,
            },
        },
        "shipments": [
            {
                "referenceId": "Reference03",
                "productType": "CONN",
                "note": "Poznamka",
                "depot": "07",
                "shipmentSet": {"numberOfShipments": 1},
                "sender": {
                    "name": "Name sender",
                    "street": "Street sender 99",
                    "city": "Olomouc",
                    "zipCode": "77200",
                    "country": "CZ",
                    "contact": "Contact sender",
                    "phone": "+420777999888",
                    "email": "test@test.cz",
                },
                "recipient": {
                    "name": "Recipient Pepa",
                    "street": "Novoveská 1262/95",
                    "city": "Ostrava",
                    "zipCode": "70900",
                    "country": "DE",
                    "contact": "Kontakt prijemce",
                    "phone": "+420777888999",
                    "email": "test@test.cz",
                },
            }
        ],
    }

    return create_package_label(payload, request, order_id=382)





def download_pdf(batch_id, token, order_id):
    # order_id = request.session.get("order_id")

    # order_id = 289
    order = get_object_or_404(Order, id=order_id)
    # DHL API endpoint and parameters

    url = f"https://api-dev.dhl.com/ecs/ppl/myapi2/shipment/batch/{batch_id}/label"
    params = {"pageSize": "A4", "position": 1, "limit": 200, "offset": 0}
    headers = {
        "Authorization": f"Bearer {token}",  # Replace with your actual token
    }
    params = {"pageSize": "A4", "position": "1", "limit": "200", "offset": "0"}

    # Send the GET request
    time.sleep(5)

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200 or 201:
        # Save the PDF into the STATIC_ROOT directory
        try:
            data = response.json()
            print(data)

            ##shipment_number = data.get('shipmentNumber', [])
            # print('this is shimpent number V2:', shipment_number)
        except Exception as e:
            print("exception", e)

        file_name = f"ppl_etiketa{batch_id}.pdf"
        file_path = os.path.join(settings.STATIC_ROOT, file_name)
        with open(file_path, "wb") as f:
            f.write(response.content)
        print("PDF saved successfully.")

        # Move the PDF to catalog/ppl_labels directory
        target_directory = os.path.join(settings.MEDIA_ROOT, "catalog/ppl_labels")
        os.makedirs(target_directory, exist_ok=True)  # Ensure target directory exists
        target_path = os.path.join(target_directory, file_name)
        shutil.move(file_path, target_path)
        print("PDF moved to catalog/ppl_labels directory.")
    else:
        # Print detailed error information
        print(f"Error: Failed to download PDF, status code: {response.status_code}")
        print(response.text)

    try:
        order = Order.objects.get(id=order_id)
        order.label = target_path
        order.save()
        print("Order label field updated successfully.")
    except Order.DoesNotExist:
        print(f"Error: Order with id {order_id} does not exist.")

    return



'''download_pdf('9cd03061-9047-4ee6-a41d-d0d08039ff92', 
             'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIxb2FKeG9vbGtDeENrQlZva1VWVE5SZXBrbEdFMEZRNUZfMHBnWXBYU1pZIn0.eyJleHAiOjE3MTg3NDQ5NTUsImlhdCI6MTcxODc0MzE1NSwianRpIjoiMTBiZTVmZmMtMjk1OC00NzBmLTg2ZjItMDRiMzU0MDQ3Nzg1IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLXRlc3QtY3VzdC5wcGwuY3ovYXV0aC9yZWFsbXMvaGZfY3pfbXlhcGkiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNzBlM2ZkNDUtYzczNi00NTI0LTllMmMtZDA2MzYxMTRjYTM1IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiVkE0NTM3MjkzIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm15YXBpLXNlcnZpY2UiLCJkZWZhdWx0LXJvbGVzLWhmX2N6X215YXBpIiwibXlhcGkuY2xpZW50Iiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoibXlhcGkyIiwiY2xpZW50SG9zdCI6IjM1LjIzNC43OC4zMyIsImNsaWVudElkIjoiVkE0NTM3MjkzIiwiZXBzIjp7ImN1c3RvbWVyIjp7ImlkIjoyMDUwOTM3fX0sImNsaWVudEFkZHJlc3MiOiIzNS4yMzQuNzguMzMifQ.SC4gVrVtj1d_KPX_w6w9DPQC2iI58DRjvQUjieLlNsLd9ir15RGYH4abn6avfTOXPNHlh9kEKxvRKAQAZa9NDEFMVGy_V70jXsd0ICZkS1EL_aIawsLnpTHpNZsWqbq3wr-YTsvRsFDP3Wdk4uMS-42jRGRafvQlOa3bBTrPwnvJ4yhRKcF7QBjIUzydFheCJxxkfVwO8EXFbflEsO4-_vwC7ZwATx18md3uO6izQJltA-yQTYFF-sPWe6DVEV2cM8heVv18vGgGoGsjc05chi3AVr1X7rJrDinQmUyEgQmtsldah9jFLhqyBlGfSnboMNJkDZS_3cyAnrSPwNayOA',
             order_id=456)
'''


#print(package_trigger(request=requests))
# print(order_trigger(request=requests, batch_id='22d2ecf2-b2b7-45ef-90ea-fb8ee0082929', token='''eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIxb2FKeG9vbGtDeENrQlZva1VWVE5SZXBrbEdFMEZRNUZfMHBnWXBYU1pZIn0.eyJleHAiOjE3MTcyNDQzMzEsImlhdCI6MTcxNzI0MjUzMSwianRpIjoiOTJhNDc4ZTgtYmY4Yy00ZTNiLTg3MmYtNWI5NGRhOTIxZTMyIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLXRlc3QtY3VzdC5wcGwuY3ovYXV0aC9yZWFsbXMvaGZfY3pfbXlhcGkiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNzBlM2ZkNDUtYzczNi00NTI0LTllMmMtZDA2MzYxMTRjYTM1IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiVkE0NTM3MjkzIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm15YXBpLXNlcnZpY2UiLCJkZWZhdWx0LXJvbGVzLWhmX2N6X215YXBpIiwibXlhcGkuY2xpZW50Iiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoibXlhcGkyIiwiY2xpZW50SG9zdCI6IjEwLjI4LjI0MC4yMCIsImNsaWVudElkIjoiVkE0NTM3MjkzIiwiZXBzIjp7ImN1c3RvbWVyIjp7ImlkIjoyMDUwOTM3fX0sImNsaWVudEFkZHJlc3MiOiIxMC4yOC4yNDAuMjAifQ.KsiLHuyppfIV_33KtfWnAZ7QhhYF0EbhvfKnEyNvaUJCdYMVg-mBP_V9DHLmkQ0P1KZbOYrIMvs9HIQfq1N0lI-rsBSnRH2ZyhyO0LjqFXDv-3Erg7cEO7M7o6wS4cO2CWHe5FhO9oDgs4uqyzdGW_xlFNXwkhiovt8H0xm_Y5BZ9Y9q4gJJN4SA-hbbq2YSyAqPqFpYfIQMO2FzIMSNDLBA8CN0hjc_udByWHWemuAzo-_GD6l9WfaH8EOa3pP7rQr5CLuZwSGNhKAzBGvs4NB1AHd-7mruXZOJS6-nak3p2AU5Ifi-wKs2EeV8HG2p9wcMBWbl6sF_0pzSsTfAmA''', order_id=349))
# print(track_shipment(requests, ["81253538687"]))
