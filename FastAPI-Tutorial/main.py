# pyrefly: ignore [missing-import]
from pydantic import type_adapter
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Path, HTTPException , Query
# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal,Optional
import json 

app = FastAPI()

class patient(BaseModel):
    id: Annotated [str, Field(..., description='Id of patient', example= 'P001')]
    name: Annotated [str,Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description= 'city of the patient')]
    age: Annotated[int,Field(..., description='Age of the patient')]
    gender: Annotated[Literal["male", "female", "other"], Field(..., description='Gender of the patient')]
    height: Annotated[float,Field(...,gt =0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(...,gt=0, description='Weight of the patient in Kgs')]    
    

    @computed_field
    @property
    def bmi(self)-> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field 
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal weight'
        elif self.bmi <30:
            return 'Normal'
        else:
            return 'Obese'

class patient_updated(BaseModel):
    name: Annotated [Optional[str],Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int],Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female"]], Field(default=None)]
    height: Annotated[Optional[float],Field(default=None ,gt =0)]
    weight: Annotated[Optional[float], Field(default=None ,gt =0)]

def load_data():
    with open('patients.json', 'r') as f:
        data =json.load(f)
    return data 

def save_data(data):
    with open('patients.json','w') as f :
        json.dump(data,f)

@app.get('/')
def hello ():
    return {"Message" : "Patient Management System API "}

@app.get('/about')
def msg ():
    return {"Message" : "A fully Functional API To manage Your Patient Records"}

@app.get('/view')
def view():
    data = load_data()

    return data
@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(..., description="Id of the patient in the db", example = "P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code= 404, detail= "Patient Not Found")

@app.get('/Sort')
def sort_patients(sort_by: str = Query(..., description =' Sort on the basis of height , weight or bmi'), order: str = Query('asc', description ='Sort in asc or dsc order')):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field Select from {valid_fields}")

    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code= 400, detail= "Invalid order Select Between asc and desc")

    data = load_data()
    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key= lambda x : x.get(sort_by,0) , reverse = sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient:patient): 
    #Load Data 
    data = load_data() 
    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail=f"Patient with id {patient.id} already exists")
    #new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code = 201, content={'message' : 'Patient Created Successfully' })

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update:patient_updated):
    data = load_data()

    if patient_id not in data:
        raise HTTPException (status_code = 404, detail = "Patient Not Found ")
    
    existing_patient_info = data[patient_id]
    Updated_patient_info= patient_update.model_dump(exclude_unset= True)

    for key,value in Updated_patient_info.items():
        existing_patient_info[key] = value
    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    save_data(data)
    return JSONResponse(status_code = 200, content={'message' : 'Patient Updated Successfully' })

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Not Found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})