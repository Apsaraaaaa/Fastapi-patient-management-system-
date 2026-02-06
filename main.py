from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI(title="Patient Management System API")
PATIENT_FILE = "patients.json"
APPOINTMENT_FILE = "appointments.json"
MEDICAL_FILE = "medical_records.json"

#models
class Patient(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    admitted: bool

class Appointment(BaseModel):
    id: int
    patient_id: int
    date: str
    time: str
    doctor: str
    reason: str

class MedicalRecord(BaseModel):
    id: int
    patient_id: int
    diagnosis: str
    treatment: str
    notes: str

#helpers
def load_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

#home
@app.get("/")
def home():
    return {"message": "Patient Management System API"}

#patients
@app.get("/patients")
def get_patients():
    return load_data(PATIENT_FILE)

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    patients = load_data(PATIENT_FILE)
    for p in patients:
        if p["id"] == patient_id:
            return p
    raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/patients")
def add_patient(patient: Patient):
    patients = load_data(PATIENT_FILE)
    if any(p["id"] == patient.id for p in patients):
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    patients.append(patient.dict())
    save_data(PATIENT_FILE, patients)
    return {"message": "Patient added successfully", "patient": patient}

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, updated_patient: Patient):
    patients = load_data(PATIENT_FILE)
    for i, p in enumerate(patients):
        if p["id"] == patient_id:
            patients[i] = updated_patient.dict()
            save_data(PATIENT_FILE, patients)
            return {"message": "Patient updated successfully", "patient": updated_patient}
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    patients = load_data(PATIENT_FILE)
    for i, p in enumerate(patients):
        if p["id"] == patient_id:
            deleted = patients.pop(i)
            save_data(PATIENT_FILE, patients)
            return {"message": "Patient deleted successfully", "patient": deleted}
    raise HTTPException(status_code=404, detail="Patient not found")

#appointments
@app.get("/appointments")
def get_appointments():
    return load_data(APPOINTMENT_FILE)

@app.post("/appointments")
def add_appointment(appointment: Appointment):
    appointments = load_data(APPOINTMENT_FILE)
    if any(a["id"] == appointment.id for a in appointments):
        raise HTTPException(status_code=400, detail="Appointment ID already exists")
    # Check patient exists
    patients = load_data(PATIENT_FILE)
    if not any(p["id"] == appointment.patient_id for p in patients):
        raise HTTPException(status_code=404, detail="Patient not found")
    appointments.append(appointment.dict())
    save_data(APPOINTMENT_FILE, appointments)
    return {"message": "Appointment added successfully", "appointment": appointment}

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    appointments = load_data(APPOINTMENT_FILE)
    for i, a in enumerate(appointments):
        if a["id"] == appointment_id:
            deleted = appointments.pop(i)
            save_data(APPOINTMENT_FILE, appointments)
            return {"message": "Appointment deleted successfully", "appointment": deleted}
    raise HTTPException(status_code=404, detail="Appointment not found")

#medical records
@app.get("/medical_records")
def get_medical_records():
    return load_data(MEDICAL_FILE)

@app.post("/medical_records")
def add_medical_record(record: MedicalRecord):
    records = load_data(MEDICAL_FILE)
    if any(r["id"] == record.id for r in records):
        raise HTTPException(status_code=400, detail="Medical Record ID already exists")
    # Check patient exists
    patients = load_data(PATIENT_FILE)
    if not any(p["id"] == record.patient_id for p in patients):
        raise HTTPException(status_code=404, detail="Patient not found")
    records.append(record.dict())
    save_data(MEDICAL_FILE, records)
    return {"message": "Medical record added successfully", "record": record}
