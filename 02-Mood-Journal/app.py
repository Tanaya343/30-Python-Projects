from flask import Flask, render_template, request, redirect 
#flask = creates web app object 
#render_template = loads html files from your templates/ folder
#request = access form data 
#redirect = sends user to another route after saving
import csv
#save entries to .csv file like a database
from datetime import datetime
#to capture date and time when the entry is submitted
app = Flask(__name__)
#for app creation
#name = tells flask where it is being run
#app = main instance

CSV_FILE = "journal.csv"
#storing name of csv file
#if file doesnt exists, python will create it when the first entry is saved

@app.route('/')
#route decorator in flask - maps URL to a function
#/ is home route
#visiting local host will trigger this function
def home():
    return render_template("index.html")
#when visit at homepage, show index.html
#render_template = renders HTML file and display in browser

@app.route('/submit', methods=['POST'])
#sets up new route for path /submit but only for post requests
#why post? = for sending data securely to the server
def submit(): #define functio 
    mood = request.form['mood']
    journal = request.form['journal' ]#pulling values from the form using request.form
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

    with open(CSV_FILE, mode='a', newline='') as file: #opens/creates csv file
        #appends a new row with timestamp, mood, journal
        writer = csv.writer(file)
        writer.writerow([timestamp, mood, journal])
    
    return redirect('/view') #redirects user to view.html

@app.route('/view') #defines URL path /view
#triggers when user visits /view on browser
def view_entries(): #defines the fucntion that will be executed when someones accesses the /view route
    entries = []
    try:
        with open(CSV_FILE, mode='r') as file: #opens csv file in read mode
            reader = csv.reader(file) #creates a csv reader object to read the rows from the csv
            for row in reader:
                if len(row) == 3:
                    entries.append(row)
    except FileNotFoundError: #if no entries yet handles the error
        pass
    return render_template("view.html", entries=entries) #renders view.html and passes entries list to it

if __name__ == '__main__':
    app.run(debug=True)
