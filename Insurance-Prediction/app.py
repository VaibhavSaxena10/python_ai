# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse

from Model.predict import predict_output, MODEL_VERSION
import pandas as pd
from schema.user_input import UserInput


app= FastAPI()



#pydantic model to validate data


#human Readable
@app.get('/')
def home():
    return {"message": "Welcome to the Insurance Premium Prediction API"}
#Machine Readable
@app.get('/health')
def health_check():
    return {"status":"ok", "version": MODEL_VERSION}

@app.post('/predict')
def predict__premium(data:UserInput):
    user_input={
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }
    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'predicted_category': prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': 'Internal server error', 'details': str(e)})