import re
import pandas as pd
import pyttsx3
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import os
import warnings
import joblib
warnings.filterwarnings("ignore", category=DeprecationWarning)

training = pd.read_csv('chatbot/model/Data/Training.csv')
testing= pd.read_csv('chatbot/model/Data/Testing.csv')
cols= training.columns
cols= cols[:-1]
x = training[cols]
y = training['prognosis']
y1= y



reduced_data = training.groupby(training['prognosis']).max()

#mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx    = testing[cols]
testy    = testing['prognosis']  
testy    = le.transform(testy)




severityDictionary=dict()
description_list = dict()
precautionDictionary=dict()

def readn(nstr):
    engine = pyttsx3.init()

    engine.setProperty('voice', "english+f5")
    engine.setProperty('rate', 130)

    engine.say(nstr)
    engine.runAndWait()
    engine.stop()



def calc_condition(exp,days):
    sum=0
    for item in exp:
         sum=sum+severityDictionary[item]
    if((sum*days)/(len(exp)+1)>13):
        print("You should take the consultation from doctor. ")
    else:
        print("It might not be that bad but you should take precautions.")


def getDescription():
    global description_list
    with open('chatbot/model/MasterData/symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            description_list.update(_description)




def getSeverityDict():
    global severityDictionary
    with open('chatbot/model/MasterData/symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                _diction={row[0]:int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass


def getprecautionDict():
    global precautionDictionary
    with open('chatbot/model/MasterData/symptom_precaution.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautionDictionary.update(_prec)


def getInfo():
    print("-----------------------------------HealthCare ChatBot-----------------------------------")
    print("\nYour Name? \t\t\t\t",end="->")
    name=input("")
    print("Hello, ",name)

def check_pattern(dis_list,inp):
    pred_list=[]
    inp=inp.replace(' ','_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list=[item for item in dis_list if regexp.search(item)]
    if(len(pred_list)>0):
        return 1,pred_list
    else:
        return 0,[]
def sec_predict(symptoms_exp):
    df = pd.read_csv('chatbot/model/Data/Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
      input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])


def print_disease(node):
    node = node[0]
    val  = node.nonzero() 
    disease = le.inverse_transform(val[0])
    return list(map(lambda x:x.strip(),list(disease)))



def get_result(symptoms_exp,num_days,present_disease):
    getSeverityDict()
    getDescription()
    getprecautionDict()
    second_prediction=sec_predict(symptoms_exp)
    calc_condition(symptoms_exp,num_days)
    res={}
    if(present_disease[0]==second_prediction[0]):
        res={"disease":str(present_disease[0])+" => "+str(description_list[present_disease[0]])}
        print("You may have ", present_disease[0])
        print(description_list[present_disease[0]])

    else:
        res={"disease":str(present_disease[0])+" => "+
        str(description_list[present_disease[0]])+" OR "+
        str(second_prediction[0])+" => "+
        str(description_list[second_prediction[0]])}
        print("You may have ", present_disease[0], "or ", second_prediction[0])
        print(description_list[present_disease[0]])
        print(description_list[second_prediction[0]])

    # print(description_list[present_disease[0]])
    precution_list=precautionDictionary[present_disease[0]]
    res["precution_list"]=precution_list
    print("Take following measures : ")
    for  i,j in enumerate(precution_list):
        print(i+1,")",j)
    return res




def get_symfromissue(disease_input,num_days):
    clf= joblib.load('chatbot/model/model.sav')
    

    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    features = cols


    symptoms_dict = {}

    for index, symptom in enumerate(x):
        symptoms_dict[symptom] = index
        tree=clf
        feature_names=cols
    
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    chk_dis=",".join(feature_names).split(",")
    symptoms_present = []
    res=[]
    
    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]

            if name == disease_input:
                val = 1
            else:
                val = 0
            if  val <= threshold:
                return recurse(tree_.children_left[node], depth + 1)
            else:
                symptoms_present.append(name)
                return recurse(tree_.children_right[node], depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            red_cols = reduced_data.columns 
            symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
            
            res=list(symptoms_given)
            json_body={"res":res,"present_dis":present_disease}
            return json_body
    res = recurse(0, 1)
    return res






def tree_to_code(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    chk_dis=",".join(feature_names).split(",")
    symptoms_present = []
    disease_input=get_issue(chk_dis) 
    num_days=get_sickdays()
    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]

            if name == disease_input:
                val = 1
            else:
                val = 0
            if  val <= threshold:
                recurse(tree_.children_left[node], depth + 1)
            else:
                symptoms_present.append(name)
                recurse(tree_.children_right[node], depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            red_cols = reduced_data.columns 
            symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
            symp_res=get_symptoms(symptoms_given)
            get_result(symp_res,num_days,present_disease)

    recurse(0, 1)
#getInfo()
#tree_to_code(clf,cols)
print("----------------------------------------------------------------------------------------")

