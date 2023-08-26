


import pandas as pd
import matplotlib.pyplot as mpl
import numpy as np
import math
from scipy.stats import norm


data= "findata.csv"
sheet= "sheet 1"


spot_price_col= "spot price" 
strike_price_col= "strike Prce"
call_option_price_col= "call Option prices"
put_option_price_col= "put Opion prices"
call_volatility_col= "call volatility"
put_volatility_col= "put volatility"
time_period_col= "time period"
risk_free_return_col= "risk free return %"



stored_data= pd.read_csv(data)


spot_price_array= stored_data[spot_price_col].values
strike_price_array= stored_data[strike_price_col].values
call_option_price_array= stored_data[call_option_price_col].values
put_option_price_array= stored_data[put_option_price_col].values
call_volatility_array= stored_data[call_volatility_col].values
put_volatility_array= stored_data[put_volatility_col].values
time_period_array= stored_data[time_period_col].values
risk_free_return_array= stored_data[risk_free_return_col].values



def predict_call(s,k,r,t,v):
   
    d1= (math.log(s/k)+ (r+ ((v**2)/2))*t)/(v*(t**0.5))
    d2= d1- v*(t**0.5)
    C= (s*norm.cdf(d1))- (k*math.exp(-r*t)*norm.cdf(d2))
    return C


def predict_put(s,k,r,t,v):
    d1= (math.log(s/k)+ (r+ ((v**2)/2))*t)/(v*(t**0.5))
    d2= d1- v*(t**0.5)
    P = -(s*norm.cdf(-d1))+ (k*math.exp(-r*t)*norm.cdf(-d2))    
    return P




predicted_call_values= []
predicted_put_values= []
counter = 0;


for strike_price in strike_price_array:
    
    
    current_call_prediction= predict_call(spot_price_array[counter],strike_price,risk_free_return_array[counter],time_period_array[counter],call_volatility_array[counter]/100)
    predicted_call_values.append(current_call_prediction)
    current_put_prediction= predict_put(spot_price_array[counter],strike_price,risk_free_return_array[counter],time_period_array[counter],put_volatility_array[counter]/100)
    predicted_put_values.append(current_put_prediction)
    counter= counter+1


sum_percent_error=0
eteration=0

for c in predicted_call_values:
      if c>call_option_price_array[eteration]:
           percent_error= ((c-call_option_price_array[eteration])/call_option_price_array[eteration])*100
      else:
           percent_error= ((call_option_price_array[eteration]-c)/call_option_price_array[eteration])*100     
      sum_percent_error= sum_percent_error+ percent_error
      eteration= eteration+1
call_accuracy= 100-(sum_percent_error/len(predicted_call_values))
print("ACCURACY FOR PREDICTING CALL PRICES IS ",round(call_accuracy,2),"%")

sum_percent_error=0
eteration=0

for p in predicted_put_values:
      if p>put_option_price_array[eteration]:
           percent_error= ((p-put_option_price_array[eteration])/put_option_price_array[eteration])*100
      else:
           percent_error= ((put_option_price_array[eteration]-p)/put_option_price_array[eteration])*100     
      sum_percent_error= sum_percent_error+ percent_error
      eteration=eteration+1
put_accuracy= 100-(sum_percent_error/len(predicted_put_values))
print("ACCURACY FOR PREDICTING PUT PRICES IS ",round(put_accuracy,2),"%")


mpl.plot(predicted_call_values, strike_price_array, linestyle='-', color='purple', label='Calculated Call values')
mpl.xlabel= "Calculated call values"
mpl.ylabel= "Strike price"


mpl.plot(call_option_price_array, strike_price_array, linestyle='-', color='red', label='Actual Call values')
mpl.xlabel= "Calculated call values"
mpl.ylabel= "Strike price"

mpl.legend()
mpl.grid()
mpl.show()

mpl.plot(predicted_put_values, strike_price_array, linestyle='-', color='purple', label='Calculated Put values')
mpl.xlabel= "Calculated put values"
mpl.ylabel= "Strike price"


mpl.plot(put_option_price_array, strike_price_array, linestyle='-', color='red', label='Actual Put values')
mpl.xlabel= "Calculated put values"
mpl.ylabel= "Strike price"

mpl.legend()
mpl.grid()
mpl.show()








    
