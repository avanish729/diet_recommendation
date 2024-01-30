from flask import Flask,request,render_template
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os
import re
os.environ["OPENAI_API_KEY"]="enter your key" 


app=Flask(__name__)
llm_restro=OpenAI(temperature=0.5)#temperature jitna kam rehega utna hi accurate output hoga hoga..
prompt_template=PromptTemplate(
    input_variables=['age','gender','height','veg_or_nonveg','disease','region','allergies','foodtype'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 6 restaurants names, 6 breakfast names, 5 dinner names, and 6 workout names,"
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person generic disease: {disease}\n"
             "Person region: {region}\n"
             "Person allergics: {allergics}\n"
             "Person foodtype: {foodtype}."
)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend',methods=['POST','GET'])
def recommend():
    if request.method=='POST':
        age=request.form['age']
        gender=request.form['gender']
        weight=request.form['weight']
        height=request.form['height']
        veg_or_nonveg=request.form['veg_or_nonveg']
        disease=['disease']
        region=request.form['region']
        allergics=request.form['allergics']
        foodtype=request.form['foodtype']

        #chain the open ai with prompt..
        chain=LLMChain(llm=llm_restro,prompt=prompt_template)
        chain_restro=LLMChain(llm=llm_restro,prompt=prompt_template)
        input_data={
            'age':60,
            'gender':'male',
            'weight':120,
            'height':5,
            'veg_or_nonveg':'veg',
            'disease':'anemia',
            'region':'pakistan',
            'allergics':'latex Allergy',
            'foodtype':'Fruits',
        }
        result=chain_restro.run(input_data)
        names=re.findall(r"Restaurants:(.*?)Breakfast:",result,re.DOTALL)#this find the the all item b/w restaurants and  breakfast)
        breakfast=re.findall(r"Breakfast:(.*?)Dinner:",result,re.DOTALL)
        dinner= re.findall(r'Dinner:(.*?)Workouts:', result, re.DOTALL)
        workout = re.findall(r'Workouts:(.*?)$', result, re.DOTALL)

        names=[name.strip()   for name in names[0].strip().split('\n') if name.strip()]if names else []
        breakfast=[name.strip() for name in breakfast[0].strip().split('\n') if name.strip()]if breakfast else []
        dinner=[name.strip()  for name in dinner[0].strip().split('\n') if name.strip()]if dinner else []
        workout=[name.strip() for name in workout[0].strip().split('\n') if name.strip()]if workout else []



    return render_template('result.html',names=names,breakfast=breakfast,dinner=dinner,workout=workout)




if __name__=="__main__":
    app.run(debug=True)