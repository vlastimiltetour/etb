#!/bin/bash

apiEndpoint="https://www.zasilkovna.cz/api/rest"
apiPassword="1234567890abcdef1234567890abcdef"

# Packet attributes data in JSON format
packetData='{
  "number": "123456",
  "name": "Petr",
  "surname": "Novák",
  "email": "petr@novak.cz",
  "phone": "+420777123456",
  "addressId": 79,
  "cod": 145,
  "value": 145.55,
  "eshop": "muj-eshop.cz"
}'

# Make the CURL request and capture the response
response=$(curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $apiPassword" -d "$packetData" "$apiEndpoint")

# Check for CURL errors
if [ $? -ne 0 ]; then
  echo "CURL Error: $response"
  exit 1
fi

# Check if the response contains "packetId" to confirm successful creation
if [[ "$response" == *"packetId"* ]]; then
  echo "Packet created successfully:"
  echo "$response"
else
  echo "Error creating packet."
fi
