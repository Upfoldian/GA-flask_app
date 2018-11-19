from flask import Flask, render_template
import gviz_api



app = Flask(__name__)

@app.route('/', methods = ['GET'])
def display_data():
	description = {"year": ("string", "Year"), "sales": ("number", "Sales"), "expenses": ("number", "Expenses")}
	data = [{"year": '2014', "sales": 1000, "expenses": 400},
    	    {"year": '2015', "sales": 2000, "expenses": 500},
    	    {"year": '2016', "sales": 3000, "expenses": 300},
    	    {"year": '2017', "sales": 1000, "expenses": 200}]

	data_table = gviz_api.DataTable(description)
	data_table.LoadData(data)
  	json = data_table.ToJSon(columns_order=("year", "sales", "expenses"), order_by="year")
  	return render_template('display.j2', chartJSON=json)

@app.route('/', methods = ['POST'])
def save_data():
	#Do some stuff
	return 'POST'