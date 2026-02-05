from fastapi import FastAPI
import json

app=FastAPI()

def load_data():
    with open("patients.json","r") as f:
        data = json.load(f)
    return data  


#endpoiunt ko laagi route/path/url define garne
@app.get("/")
def hello():
    return {"message":"patient management system api"}

@app.get("/about")
def about():
    return{"message":"A fully functional API to manage the oatient records"}

@app.get("/view")
def view():
    data=load_data()
    return data
    