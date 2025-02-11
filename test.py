import requests
import json
import re

BASE_URL="http://127.0.0.1:7676"
RECEIPT_EXAMPLES=[{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "14:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}, {
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}]
EXPECTED_POINTS=[38, 109]

def test_root_url():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    print("✅ Testing root url - Passed")

def test_get_points_with_nonexisting_id():
    id = "non-exist-id"
    response = requests.get(f"{BASE_URL}/receipts/{id}/points")
    assert response.status_code == 404
    assert str(response.json()) == "{'detail': 'No receipt found for that ID.'}"
    print("✅ Testing get points with nonexisting id - Passed")

def test_post_receipt_and_retrive_points():
    for i in range(len(RECEIPT_EXAMPLES)):
        receipt = RECEIPT_EXAMPLES[i]
        exp_points = EXPECTED_POINTS[i]
        response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
        assert response.status_code == 200
        assert re.match(r"^\{\'id\': \'[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\'\}$", str(response.json()))
        id = response.json()["id"]
        # Check if the id is retrievable and the points are correct.
        response = requests.get(f"{BASE_URL}/receipts/{id}/points")
        assert response.status_code == 200
        assert str(response.json()) == "{'points': " + str(exp_points) + "}"
        print(f"✅ Testing post receipt with valid data ({i + 1} of {len(RECEIPT_EXAMPLES)}) - Passed")

def test_post_receipt_with_invalid_retailer():
    receipt = RECEIPT_EXAMPLES[0] | {"retailer": "Target!@#"}
    response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
    assert response.status_code == 400
    assert str(response.json()) == "{'detail': 'The receipt is invalid.'}"
    print(f"✅ Testing post receipt with invalid retailer - Passed")

def test_post_receipt_with_invalid_purchase_date():
    receipt = RECEIPT_EXAMPLES[0] | {"purchaseDate": "2025-32-01"}
    response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
    assert response.status_code == 400
    assert str(response.json()) == "{'detail': 'The receipt is invalid.'}"
    print(f"✅ Testing post receipt with invalid purchase date - Passed")

def test_post_receipt_with_invalid_purchase_time():
    receipt = RECEIPT_EXAMPLES[0] | {"purchaseTime": "25:01"}
    response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
    assert response.status_code == 400
    assert str(response.json()) == "{'detail': 'The receipt is invalid.'}"
    print(f"✅ Testing post receipt with invalid purchase time - Passed")

def test_post_receipt_with_no_item():
    receipt = RECEIPT_EXAMPLES[0] | {"items": []}
    response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
    assert response.status_code == 400
    assert str(response.json()) == "{'detail': 'The receipt is invalid.'}"
    print(f"✅ Testing post receipt with no item - Passed")

def test_post_receipt_with_invalid_item_price():
    receipt = RECEIPT_EXAMPLES[0] | {"items": [{
      "shortDescription": "Mountain Dew 12PK",
      "price": "-1"
    }]}
    response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
    assert response.status_code == 400
    assert str(response.json()) == "{'detail': 'The receipt is invalid.'}"
    print(f"✅ Testing post receipt with invalid item price - Passed")

def test_post_receipt_with_invalid_total_price():
    receipt = RECEIPT_EXAMPLES[0] | {"total": "1.234"}
    response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
    assert response.status_code == 400
    assert str(response.json()) == "{'detail': 'The receipt is invalid.'}"
    print(f"✅ Testing post receipt with invalid total price - Passed")

if __name__ == "__main__":
    test_root_url()
    test_get_points_with_nonexisting_id()
    test_post_receipt_and_retrive_points()
    test_post_receipt_with_invalid_retailer()
    test_post_receipt_with_invalid_purchase_date()
    test_post_receipt_with_invalid_purchase_time()
    test_post_receipt_with_no_item()
    test_post_receipt_with_invalid_item_price()
    test_post_receipt_with_invalid_total_price()