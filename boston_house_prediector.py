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

print('model fit succesfuly')

import pickle
with open('bhp_model.pkl', 'wb') as f: 
    pickle.dump(model, f)
    
#    print('model saved successfully')

#rom sklearn.metrics import accuracy_score, r2_score 

#test_pred = model.predict(x_test) 
#test_acc = r2_score(y_test, test_pred)
#ad_r2_score = (1 - (1 - test_acc))*((df.shape[0] - 1 )/(df.shape[0] - 4  -1) )
#print('Model Accuracy: ', ad_r2_score)
