import json
import os
import pandas as pd

#Load JSON
path= os.path.join(os.getcwd(),'ieee123.json')

#Convert JSON to matrix of load points
import json2df
data=json2df.convert(input_file=path,output_file='')




#Notes
#Class of Lines- overhead or underground
