from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# In-memory data store
iot_data = []

class SensorData(BaseModel):
    temperature: float
    humidity: float

@app.post("/update")
def update_data(data: SensorData):
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "temperature": data.temperature,
        "humidity": data.humidity
    }
    iot_data.append(entry)

    # Keep last 50 entries
    if len(iot_data) > 50:
        iot_data.pop(0)

    return {"status": "success", "data": entry}

@app.get("/data")
def get_data():
    return iot_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
