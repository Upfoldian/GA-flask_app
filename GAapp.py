from flask import *
from helperlib import csvToChartJSON, updateUploadCSV, getUploadDict
from datetime import datetime
import csv
import gviz_api


app = Flask(__name__)

#Offloaded the code to read in my existing dataset to staticHelp module. Since this is just a day project, I haven't done any error checking, but I should if I intend to use this over thingspeak.
staticJSON = csvToChartJSON('thursday test.csv')
@app.route('/', methods = ['GET', 'POST'])
def display_data():


	if request.method == 'GET':
		uploadDesc = {"time": ("datetime", "Time"), "value": ("number", "value")}
		uploadData = getUploadDict('upload.csv')
		data_table = gviz_api.DataTable(uploadDesc)
		data_table.LoadData(uploadData)
		uploadJSON = data_table.ToJSon(columns_order=("time", "value"), order_by="time")
  		return render_template('display.j2', static=staticJSON, upload=uploadJSON)
  	elif request.method == 'POST':
  		value = int(request.form['value'])
  		updateUploadCSV('upload.csv', datetime.now(), value)
		return 'uploaded value %d' % value
  	else:
  		return 'how did you get here?'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000) #run app in debug mode on port 5000 