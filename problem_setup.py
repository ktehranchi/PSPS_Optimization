import json
import os


#Load JSON
filepath='/Users/kamrantehranchi/Documents/GradSchool/Research/PSPS_Optimization/ieee123.json'
path= os.path.join(os.getcwd(),'ieee123.json')
file= open(path)
data= json.load(file)
# file.close()
data.items()

import pandas as pd 
df= pd.DataFrame.from_dict(data)

data.keys()

# import json2csv_profile
# json2csv_profile.convert(input_file=filepath,output_file='')


#Convert JSON to matrix of load points
import json2df
json2df.convert(input_file=filepath,output_file='')


objects= data['objects']
objects.items()
#Need to get the underground and over head line status of each line in the area


#General Notes
#Class of Lines- overhead or underground


# https://stackoverflow.com/questions/8383136/parsing-json-and-searching-through-it
# https://github.com/slacgismo/gridlabd/blob/03d4dbc4da75e0b0092e3ddd3dc40fe7c06bebd2/python_external/stanford/model.py


#