from fastapi import FastAPI, HTTPException
from schemas import Receipt
from services import Services

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Receipt Processor!"}

@app.post("/receipts/process")
def process_receipt(receipt: Receipt):
    if not Services.validate_receipt(receipt):
        raise HTTPException(status_code=400, detail="The receipt is invalid.")
    receipt_id = Services.calculate_points_and_generate_id(receipt)
    return {"id": receipt_id}

@app.get("/receipts/{id}/points")
def get_receipt_points(id: str):
    points = Services.retrieve_points(id)
    if points is None:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    return {"points": points}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7676)