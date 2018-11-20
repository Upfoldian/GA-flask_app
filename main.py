from flask import Flask, render_template
import gviz_api
import csv

from datetime import datetime
from pytz import timezone

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def display_data():
	solarDesc = {"time": ("date", "Time"), "trackV": ("number", "Tracked Voltage"), "untrackV": ("number", "Untracked Voltage")}
	solarData = [];
	with open('thursday test.csv') as csvfile:
		#fieldnames = ['created_at','entry_id','people','temp','humid','trackV','trackI','untrackV','untrackI','motorpos' ]
		reader = csv.DictReader(csvfile)
		for row in reader:
			time = datetime.strptime(row['created_at'],  "%Y-%m-%d %H:%M:%S %Z").replace(tzinfo=timezone('UTC'))
			time = time.astimezone(timezone('Australia/Sydney'))
			print time
			if row['trackV'] == "":
				row['trackV'] = 0 
			if row['untrackV'] == "":
				row['untrackV'] = 0


			solarData.append({"time": time, "trackV": int(row['trackV']), "untrackV": int(row['untrackV'])})
	print (solarData[-1])
	data_table = gviz_api.DataTable(solarDesc)
	data_table.LoadData(solarData)
  	json = data_table.ToJSon(columns_order=("time", "trackV", "untrackV"), order_by="time")
  	return render_template('display.j2', chartJSON=json)

@app.route('/', methods = ['POST'])
def save_data():
	#Do some stuff
	return 'POST'