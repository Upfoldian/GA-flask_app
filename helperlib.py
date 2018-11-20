import csv
import gviz_api
from datetime import datetime
from pytz import timezone

def updateUploadCSV(filename, time, value):
	with open(filename, 'ab') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), value])

def getUploadDict(filename):
	retDict = []
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		print reader.fieldnames
		for row in reader:
			time = datetime.strptime(row['time'], "%Y-%m-%d %H:%M:%S")
			retDict.append({"time":time, "value":int(row['value'])})
	return retDict

def csvToChartJSON(filename):
	solarDesc = {"time": ("datetime", "Time"), "trackV": ("number", "Tracked Voltage"), "untrackV": ("number", "Untracked Voltage")}
	solarData = [];
	with open(filename) as csvfile:
		#fieldnames = ['created_at','entry_id','people','temp','humid','trackV','trackI','untrackV','untrackI','motorpos' ]
		reader = csv.DictReader(csvfile)
		for row in reader:
			time = datetime.strptime(row['created_at'],  "%Y-%m-%d %H:%M:%S %Z").replace(tzinfo=timezone('UTC'))
			time = time.astimezone(timezone('Australia/Sydney'))
			trackV = row['trackV']
			untrackV = row['untrackV']
			#A quirk in the dataset has the series have seperate datapoints so the empty entries need to be converted to None for Google Chart to render the lines properly
			if trackV != "":
				trackV = int(trackV)
			else:
				trackV = None

			if untrackV != "":
				untrackV = int(untrackV)
			else:
				untrackV = None

			solarData.append({"time": time, "trackV": trackV, "untrackV": untrackV})
	#Create the data table for the chart
	data_table = gviz_api.DataTable(solarDesc)
	data_table.LoadData(solarData)
	json = data_table.ToJSon(columns_order=("time", "trackV", "untrackV"), order_by="time")
	return json