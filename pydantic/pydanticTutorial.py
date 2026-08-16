import weakref
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Optional , Annotated 
class Patient(BaseModel):
    name: Annotated [str, Field(max_lenght = 50, title = "Name of the patient", description = "Enter the name of the patient in 50 characters")]
    age: int = Field(gt = 0, lt = 120)
    email: EmailStr
    Linkedin_url: AnyUrl
    weight: float
    married: bool = False
    allergies: Optional[List[str]] = Field(max_length= 5)
    contact_details: dict[str,str]

def insert_patient_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('Inserted')


def Update_patient_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print('Updated')


patient_info = {'name': 'Vaibhav', 'age': '21', 'weight': '175', 'email': 'abc@gmail.com ', 'Linkedin_url': 'https://www.linkedin.com/in/vaibhav-saxena-123456789/', 'contact_details': {'email': 'abc@gmail.com ', 'phone': '1234567890'} }

pateint1= Patient(**patient_info)

insert_patient_data(pateint1)
