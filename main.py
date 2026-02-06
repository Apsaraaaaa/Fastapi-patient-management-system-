from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

DATA_FILE = "patients.json"

#models

class Patient(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    disease: str
    admitted: bool


#helpers functions

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


#routes

@app.get("/")
def home():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage patient records"}

#view all patients
@app.get("/patients")
def view_patients():
    data = load_data()
    return data

#View single patient
@app.get("/patients/{patient_id}")
def view_patient(patient_id: int):
    data = load_data()
    for patient in data:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

# ADD
@app.post("/patients")
def add_patient(patient: Patient):
    data = load_data()

    
    for p in data:
        if p["id"] == patient.id:
            raise HTTPException(status_code=400, detail="Patient ID already exists")

    data.append(patient.dict())
    save_data(data)
    return {"message": "Patient added successfully", "patient": patient}

#update
@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, updated_patient: Patient):
    data = load_data()
    for i, patient in enumerate(data):
        if patient["id"] == patient_id:
            data[i] = updated_patient.dict()
            save_data(data)
            return {"message": "Patient updated successfully", "patient": updated_patient}

    raise HTTPException(status_code=404, detail="Patient not found")

# delete
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    data = load_data()
    for i, patient in enumerate(data):
        if patient["id"] == patient_id:
            deleted = data.pop(i)
            save_data(data)
            return {"message": "Patient deleted successfully", "patient": deleted}

    raise HTTPException(status_code=404, detail="Patient not found")
