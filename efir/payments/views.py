import json
import logging

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)

import json

import requests
from django.http import JsonResponse


def get_token():
    url = "https://secure.payu.com/pl/standard/user/oauth/authorize"
    payload = {
        "grant_type": "client_credentials",
        "client_id": "4298008",
        "client_secret": "3715856bea104d102ec1a4e954f30c5c",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Efirthebrand",
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        return data.get("access_token")

    except requests.exceptions.RequestException as req_err:
        # Handle request exceptions
        raise Exception(f"Request Exception: {req_err}")

    except ValueError as json_err:
        # Handle JSON decoding errors
        raise Exception(f"JSON Decode Error: {json_err}")


import requests
from django.http import JsonResponse


def payment_process(request):
    return render(request, "payments/canceled.html")


def payment_process3(request):
    url = "https://secure.snd.payu.com/api/v2_1/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer d9a4536e-62ba-4f60-8017-6053211d3f47",
    }

    data = {
        "notifyUrl": "https://your.eshop.com/notify",
        "customerIp": "127.0.0.1",
        "merchantPosId": "300746",
        "description": "RTV market",
        "currencyCode": "PLN",
        "totalAmount": "21000",
        "buyer": {
            "email": "john.doe@example.com",
            "phone": "654111654",
            "firstName": "John",
            "lastName": "Doe",
            "language": "pl",
        },
        "products": [
            {
                "name": "Wireless Mouse for Laptop",
                "unitPrice": "15000",
                "quantity": "1",
            },
            {
                "name": "HDMI cable",
                "unitPrice": "6000",
                "quantity": "1",
            },
        ],
    }

    response = requests.post(url, json=data, headers=headers)
    response_content = response.content.decode("utf-8")

    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)

    if response.status_code == 302:
        # Handle the redirect case
        redirect_url = response.headers["Location"]
        return redirect(redirect_url)

    try:
        response_data = response.json()
        # ... handle the JSON response ...
    except json.JSONDecodeError as e:
        print("Error decoding JSON ##### response:", e)
        soup = BeautifulSoup(response_content, "html.parser")

        # Extract the relevant information from the HTML and create a dictionary
        entire_html = str(soup)

        # Create a dictionary with the extracted data
        parsed_data = {
            "html_content": entire_html,
            # Add more fields as needed based on the extracted data
        }

        # Create a JSON response using JsonResponse
        json_response = json.dumps(parsed_data)
        filename = "reponse.html"
        # Write the HTML content to a file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(entire_html)

        return json_response
        # ... handle the JSON decoding error ...

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Handle the response data as needed
        response_data = response.json()
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.content)

        return JsonResponse(response_data)
    else:
        # Handle the error case if needed
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.content)

        return JsonResponse({"error": "Failed to create PayU order."}, status=500)


import json

# views.py
from django.http import HttpResponse


def payment_notification(request):
    if request.method == "POST":
        # Get the notification data from the request
        try:
            notification_data = json.loads(request.body)
            # Extract necessary data from notification_data
            notification_data.get("orderId")
            notification_data.get("status")
            # Update the order status in your database based on the received data
            # Example: Update the order status for orderId in your database

            # ... your code to update the order status in the database goes here ...

            return HttpResponse(status=200)  # Return success status to PayU
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return HttpResponse(status=400, content=f"JSON decoding error: {str(e)}")
        except Exception as e:
            # Handle other exceptions
            return HttpResponse(status=500, content=f"Error occurred: {str(e)}")
    else:
        return HttpResponse(status=405)  # Method not allowed for other request types


def Xpayment_process(request):
    # token = get_token()
    token = "4e6e0f7b-5c2a-4516-b877-1e5030d3a5a8"

    # Define the API endpoint and request data
    api_url = "https://secure.payu.com/api/v2_1/orders"
    # api_url = "https://secure.snd.payu.com/api/v2_1/orders"

    payload = {
        "notifyUrl": "https://www.efirthebrand.com/payments/notify/",
        "customerIp": "127.0.0.1",
        "merchantPosId": 4298008,
        "description": "RTV market",
        "currencyCode": "PLN",
        "totalAmount": 15000,
        "products": [
            {"name": "Wireless Mouse for Laptop", "unitPrice": 15000, "quantity": 1}
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",  # Include the token variable inside the f-string
        "User-Agent": "Efirthebrand",
    }

    # Check if the request was successful (status code 200)

    try:
        # Optional: Print the JSON payload for debugging purposes

        response = requests.post(api_url, headers=headers, data=payload)

        response.raise_for_status()  # Raise an exception if the response has an error status code.

        data = response.json()
        print(data)

        return JsonResponse(data)

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., 4xx, 5xx)
        return JsonResponse(
            {"error": f"HTTP Error: {http_err}"}, status=response.status_code
        )
    except requests.exceptions.RequestException as req_err:
        # Handle other request exceptions
        return JsonResponse({"error": f"Request Exception: {req_err}"}, status=500)
    except ValueError as json_err:
        # Handle JSON decoding errors
        return JsonResponse({"error": f"JSON Decode Error: {json_err}"}, status=500)


def payment_processx(request):
    # order_id = request.session.get(
    #    "order_id", None
    # )  # retrieve the id from the request object
    order_id = 2

    get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        logging.info("request method POST initiated")
        # Get form data from the request
        notify_url = "https://your.efirthebrand.com/notify"
        customer_ip = "127.0.0.1"
        merchant_pos_id = "145227"
        description = "RTV market"
        currency_code = "PLN"
        total_amount = "21000"
        buyer_email = "john.doe@example.com"
        buyer_phone = "654111654"
        buyer_first_name = "John"
        buyer_last_name = "Doe"
        buyer_language = "pl"
        products = [
            {
                "name": "Wireless Mouse for Laptop",
                "unitPrice": "15000",
                "quantity": "1",
            },
            {"name": "HDMI cable", "unitPrice": "6000", "quantity": "1"},
        ]

        # Prepare the request payload
        payload = {
            "notifyUrl": notify_url,
            "customerIp": customer_ip,
            "merchantPosId": merchant_pos_id,
            "description": description,
            "currencyCode": currency_code,
            "totalAmount": total_amount,
            "buyer": {
                "email": buyer_email,
                "phone": buyer_phone,
                "firstName": buyer_first_name,
                "lastName": buyer_last_name,
                "language": buyer_language,
            },
            "products": products,
        }

        # Make the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.PAYU_POS_ID}",  # Replace with your PayU API token
        }
        response = requests.post(
            "https://secure.payu.com/api/v2_1/orders", json=payload, headers=headers
        )

        # Process the response
        if response.status_code == 200:
            order_data = response.json()
            redirect_uri = order_data.get("redirectUri")
            order_id = order_data.get("orderId")
            order_data.get("extOrderId")
            # Do something with the order data, such as storing it in the database
            # Redirect the user to the PayU payment page
            logging.info("response status 200, should redirect to PayU gateway")

            return render(
                request, "payments/payment.html", {"redirect_uri": redirect_uri}
            )
        else:
            # Handle the error case
            logging.info("there is some error, payment canceled")

            return render(request, "payments/canceled.html")

    logging.info("function went through but nothing happened")
    return render(request, "orders/new.html")


def payment_completed(request):
    return render(request, "payments/completed.html")


def payment_canceled(request):
    return render(request, "payments/canceled.html")


def notify(request):
    pass
