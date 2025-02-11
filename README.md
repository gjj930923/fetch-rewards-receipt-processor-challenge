# Receipt Rewards Challenge – Take-home Assessment

This web service processes receipt data, assigns a unique ID to each receipt, and calculates reward points based on the receipt details.

## Running the Web Service with Docker

Follow these steps to build and launch the service locally:

1. **Build the Docker image**:  
   ```sh
   docker build -t receipt-processor .
   ```
2. **Run the container**:
   ```sh
   docker run -d -p 7676:7676 receipt-processor
   ```
   This binds the service to port 7676. You may use any available port.
3. **Verify the service**:
   
   Visit http://localhost:7676. If the service is running, it returns:
   ```json
   {"message": "Hello, Receipt Processor!"}
   ```

## API Endpoints

This service exposes three RESTful endpoints. No authentication is required.

### **1. GET /**  
**Purpose**: Health check to confirm the server is running.  

#### **Response**
```json
{"message": "Hello, Receipt Processor!"}
```

### **2. POST /receipts/process**  
**Purpose**: Processes receipt data, generates a UUID, calculates points, and stores the information in memory.

#### **Request Body (JSON)**
```json
{
  "retailer": "Target",
  "purchaseDate": "2025-02-10",
  "purchaseTime": "22:00",
  "items": [
    {"shortDescription": "Mountain Dew 12PK", "price": "5.99"},
    {"shortDescription": "Doritos Nacho Cheese", "price": "3.99"}
  ],
  "total": "9.98"
}
```

#### **Fields**
* retailer (string) – Store name (e.g., "Target").
* purchaseDate (string, YYYY-MM-DD) – Purchase date (e.g., "2025-02-10").
* purchaseTime (string, HH:MM, 24-hour format) – Purchase time (e.g., "22:00").
* items (array) – List of purchased items, each with:
  * shortDescription (string) – Item name.
  * price (string, two decimal places) – Item price.
* total (string, two decimal places) – Receipt total.

#### **Response**
```json
{"id": "<uuid-string>"}
```

#### **Errors**
* 400 Bad Request if any field is invalid.

### **3. GET /receipts/{id}/points**  
**Purpose**: Retrieves points associated with a receipt by its UUID.

#### **Request**
- `id` (string) – Receipt UUID.

#### **Response**
```json
{"points": <number>}
```
#### **Errors**
* 404 Not Found if the given `id` does not exist.