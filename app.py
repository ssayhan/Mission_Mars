
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import Mars_scraping

#  Set up Flask
app = Flask(__name__)

#  Connect tho Mongo using Python
#  Use Flask_pymongo to set uo mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for HTML
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#Add next route and function to our code

@app.route("/scrape")

def scrape():
    mars= mongo.db.mars
    mars_data = Mars_scraping.scrape_all()
    # mars.update{}, mars_data, upsert = True)
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

# Run the code

if __name__ =="__main__":
    app.run(host="localhost", port=5001, debug=True)

