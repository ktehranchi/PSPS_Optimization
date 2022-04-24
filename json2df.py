import json 
import os 
import sys, getopt
from datetime import datetime 
import csv

def convert(input_file,output_file=None, options={}):

	if output_file == '':
		if input_file[-5:] == ".json":
			output_file = input_file[:-5] + ".csv" 
		else: 
			output_file = input_file + ".csv"

	with open(input_file,"r") as f :
		data = json.load(f)
		assert(data['application']=='gridlabd')
		assert(data['version'] >= '4.2.0')
	
    #appends list of all objects with criteria property key = value
	def find(objects,property,value):
		result = []
		for name,values in objects.items():
			if property in values.keys() and values[property] == value:
				result.append(name)
		return result

	def get_string(values,key):
		return values[key]

	def get_complex(values,prop):
		return complex(get_string(values,prop).split(" ")[0].replace('i','j'))

	def get_real(values,prop):
		return get_complex(values,prop).real

	def get_load_vals(values):
		cn = values["class"]
		bt = values["bustype"]
		bf = values["busflags"]
		gid = values["groupid"]
		lat = values["latitude"]
		long = values["longitude"]

		if values['class'] == "triplex_meter":
			parent = values['parent']
			fn = ""
			tn = ""
			mre=get_real(values,"measured_real_energy")
		else:
			parent,fn, tn, mre = "","","",""

		return cn,bt,bf,gid,parent,fn,tn,mre,lat,long

	def profile(writer,objects,root,pos=0):
		fromdata = objects[root]
		class_name,bustype,busflags,groupid,parent,from_name,to_name,mre,latitude,longitude = get_load_vals(fromdata)
		writer.writerow([root,class_name,bustype,busflags,groupid,parent,from_name,to_name,mre,latitude,longitude])
		for meter in find(objects,"groupid",root):
			meterdata = objects[meter]
			class_name,bustype,busflags,groupid,parent,from_name,to_name,mre,latitude,longitude = get_load_vals(meterdata)
			writer.writerow([meter,class_name,bustype,busflags,groupid,parent,from_name,to_name,mre,latitude,longitude])

			# if "to" in meterdata.keys():
			# 	to = meterdata["to"]
			# 	todata = objects[to]
			# 	profile(writer,objects,to,pos+linklen)

	with open(output_file,"w") as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["node","class","bustype","busflags","group_id","parent","from","to","Load (W)","Lat","Long"])
		#obj is the object that met the find criteria
		for obj in find(objects=data["objects"],property="class",value="load"):
			profile(csvwriter,objects=data["objects"],root=obj)