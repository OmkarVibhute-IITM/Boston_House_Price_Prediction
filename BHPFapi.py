#--------------------------------------------------------------------------------------
  #Model

import pandas as pd
from sklearn.tree import DecisionTreeRegressor 

set = "D:\\omkarvibhute\\Pandas Library\\USA_Housing (1).csv"
df = pd.read_csv("D:\\omkarvibhute\\Pandas Library\\USA_Housing (1).csv") 
df.drop(columns = ['Address','Avg. Area Number of Bedrooms'], inplace =True) 

from sklearn.model_selection import train_test_split as tts 

x = df.iloc[:,0:4]
y = df.iloc[:,-1]
x_train, x_test, y_train, y_test = tts(x, y, test_size = .2, random_state = 42)

from matplotlib.transforms import TransformedBbox
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso

scale_pip = Pipeline(steps = [('scale',StandardScaler())]) 

processor = ColumnTransformer(transformers = [('scale', scale_pip, [0,1,2,3])])

model = Pipeline(steps = [('processor', processor), ('regressor', Lasso())])

model.fit(x_train, y_train) 

import pickle
with open('bhp_model.pkl', 'wb') as f: 
    pickle.dump(model, f)

#--------------------------------------------------------------------------------------
# ----------------------------------------------------
# API 
# ----------------------------------------------------
#--------------------------------------------------------------------------------------

import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
import logging
from fastapi import HTTPException
from fastapi.responses import JSONResponse

# ----------------------------------------------------
# Load Model
# ----------------------------------------------------
try:

    with open("bhp_model.pkl", "rb") as f:
        model = pickle.load(f)

except FileNotFoundError as e:

    raise RuntimeError(
        "Model file 'bhp_model.pkl' was not found."
    ) from e

except pickle.UnpicklingError as e:

    raise RuntimeError(
        "Unable to load the pickle model."
    ) from e

except Exception as e:

    raise RuntimeError(
        f"Unexpected error while loading model: {e}"
    ) from e

# ----------------------------------------------------
# Create FastAPI App
# ----------------------------------------------------

app = FastAPI(
    title="USA Housing Price Prediction API",
    description="Predicts the selling price of a house in Boston, California, USA.",
    version="1.0.0"
)

# ----------------------------------------------------
# Pydantic Model
# ----------------------------------------------------

class User_Inputs(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "Avg_Area_Income": 79545,
                "Avg_Area_House_Age": 5,
                "Avg_Area_Number_of_Rooms": 7,
                "Area_Population": 23086
            }
        }
    )

    Avg_Area_Income: Annotated[
        int,
        Field(gt=0, description="Average annual income of people living in the area.")
    ]
    
    Avg_Area_House_Age: Annotated[
        int,
        Field(
            gt=0,
            description="Average age of houses in the area (in years)."
        )
    ]
    Avg_Area_Number_of_Rooms: Annotated[
        int,
        Field(
            gt=0,
            description="Average number of rooms per house."
        )
    ]
    Area_Population: Annotated[
        int,
        Field(
            gt=0,
            description="Total population residing in the area."
        )
    ]
# ----------------------------------------------------
# Home Route
# ----------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to the USA Housing Price Prediction Application.",
    }
# ----------------------------------------------------
# Liveness Probe
# ----------------------------------------------------

@app.get("/api_health")
def backend_health():
    
    return {
        "status": "Ok",
        "service": "USA Housing Price Prediction API",
        "version": "1.0.0 (last update 04-07-2026)"
    }
# ----------------------------------------------------
#  Model load check
# ----------------------------------------------------
@app.get('/ready')
def model_ready():
    if model is None: 
        return JSONResponse(status_code= 200, content= {"model_load_status": "True, ready to run"})
    else:
        return JSONResponse(status_code= 500, content= {'model_load_status': "False, not ready to run"})
# ----------------------------------------------------
# Prediction Route
# ----------------------------------------------------
@app.post("/predict")
def predict(data: User_Inputs):

    try:
        input_df = pd.DataFrame([{
            "Avg. Area Income": data.Avg_Area_Income,
            "Avg. Area House Age": data.Avg_Area_House_Age,
            "Avg. Area Number of Rooms": data.Avg_Area_Number_of_Rooms,
            "Area Population": data.Area_Population
        }])
        
        prediction = model.predict(input_df)[0] 
        
            
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s"
        )
        logging.info("Prediction request received.")
        logging.info(f"Input Data: {input_df.iloc[0]}")
        logging.info(f"Prediction : {prediction}")

        return JSONResponse(status_code= 200, 
           content = {"Predicted House Price": round(float(prediction), 2)
        })

    except Exception as e:
        logging.error(f"Prediction Error: {e}")
     
    raise HTTPException(
        status_code=500,
        massage = "internal server error"
    )

