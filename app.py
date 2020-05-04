from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flaskt
app = Flask(__name__, template_folder='templates')

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrapeMars_DB")

@app.route("/")

def home():

    
    mars_collection = mongo.db.mars_collection.find_one()

    return render_template("index.html", mars_collection = mars_collection)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_collection = scrape_mars.scrape_marsInfo(mongo)

    # Update the Mongo database using update and upsert=True
    #mongo.db.mars_collection.replace_one({}, mars_collection, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    
