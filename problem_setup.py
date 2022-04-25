import json
import os


#Load JSON
path= os.path.join(os.getcwd(),'ieee123.json')
file= open(path)
data= json.load(file)
# file.close()
data.items()

import pandas as pd 
df= pd.DataFrame.from_dict(data)
data.keys()

#Convert JSON to matrix of load points
import json2df
df=json2df.convert(input_file=path,output_file='')

objects= data['objects']
objects.items()
#Need to get the underground and over head line status of each line in the area



# import json2csv_profile
# json2csv_profile.convert(input_file=path,output_file='')

#Notes
#Class of Lines- overhead or underground
