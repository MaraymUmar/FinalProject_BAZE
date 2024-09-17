from flask import Flask, render_template, request
import pickle
from sklearn.cluster import KMeans
#from sklearn.cluster import RandomForestClassifier
import numpy as np
import pandas as pd

app = Flask (__name__) 

with open('savedModels\clf.plk', 'rb') as f:
    clf = pickle.load(f)

with open('savedModels\kmeans.plk', 'rb') as f:
    kmeans = pickle.load(f)

food_data = pd.read_csv("dataSets.csv")

#food_data['Sodium_Content'] = food_data['Sodium_Content'].map({'low':1, 'high':0})
food_data['Glycemic_Index'] = food_data['Glycemic_Index'].map({'Low':1, 'High':0})


#def index():
   #return render_template('index.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommendation_form')
def recommendation_form():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_fasting():
    try:
        name = (request.form['name'])
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        blood_glucose_level = float(request.form['blood_glucose_level'])
        test_type = request.form['test_type']

        bmi = weight / ((height/100) ** 2)
        if bmi < 18.5:
            bmi_class = "Underweight."
        elif 18.5 <= bmi <= 24.9:
            bmi_class = "Normal Weight."
        elif 25.0 <= bmi <= 29.9:
            bmi_class = "Overweight."
        else:
            bmi_class = "Obese"
        
    

        if test_type == "fasting":
            if age >= 20:
                if 0.0 <= blood_glucose_level <= 3.8:
                    glycemic_index_class = 0
                    recommendation = f" Hello {name}, your fasting blood glucose level is low, you should consume high glycemic food like: "
                elif 3.9 <= blood_glucose_level <= 5.6:
                    glycemic_index_class = 1
                    recommendation = f" Hello {name}, your fasting blood glucose level is normal. Maintain diet or consume low glycemic food like: "
                else:
                    glycemic_index_class = 1
                    recommendation = f"Hello {name}, your fasting blood glucose level is high, you should consume low glycemic food like: "
            else:
                if 0.0 <= blood_glucose_level <= 3.8:
                    glycemic_index_class = 0
                    recommendation = f"Hello {name}, your fasting blood glucose level is low, you should consume high glycemic food like: "
                elif 3.9 <= blood_glucose_level <= 5.4:
                    glycemic_index_class = 1
                    recommendation = f"Hello {name}, your fasting blood glucose level is normal. Maintain diet or consume low glycemic food like: "
                else:
                    glycemic_index_class = 1
                    recommendation = f"Hello {name}, your fasting blood glucose level is high, you should consume low glycemic food like: "
        elif test_type == "random":
            if age >= 16:
                if 0.0 <= blood_glucose_level <= 6.9:
                    glycemic_index_class = 0
                    recommendation = f" Hello {name}, your fasting blood glucose level is low, you should consume high glycemic food like: "
                elif 7.0 <= blood_glucose_level <= 11.0:
                    glycemic_index_class = 1
                    recommendation = f" Hello {name}, your fasting blood glucose level is normal. Maintain diet or consume low glycemic food like: "
                else:
                    glycemic_index_class = 1
                    recommendation = f"Hello {name}, your fasting blood glucose level is high, you should consume low glycemic food like: "
            else:
                if 0.0 <= blood_glucose_level <= 6.9:
                    glycemic_index_class = 0
                    recommendation = f"Hello {name}, your fasting blood glucose level is low, you should consume high glycemic food like: "
                elif 7.0 <= blood_glucose_level <= 11.0:
                    glycemic_index_class = 1
                    recommendation = f"Hello {name}, your fasting blood glucose level is normal. Maintain diet or consume low glycemic food like: "
                else:
                    glycemic_index_class = 1
                    recommendation = f"Hello {name}, your fasting blood glucose level is high, you should consume low glycemic food like: "
        
        recommended_food = food_data[food_data['Glycemic_Index'] == glycemic_index_class]
            #print(food_data.head())
            #print (f"Glycemic Index Class: {glycemic_index_class}"} 
        
        if not recommended_food.empty:
            food_item = recommended_food.sample(n=5)['Food_Items'].tolist()
            food_list ='<br>'.join(food_item)
            recommendation += f"{food_list}."     
        else:
            recommendation = "Sorry, {name}! No food matches your criteria."

        return render_template('result.html', recommendation=recommendation, bmi=bmi, bmi_class=bmi_class)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=6800)
