# Importing Dependencies and other python scripts (Note: A lot of this was gone over in my previous classes so there is not much to comment out on)
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_Mission"
mongo = PyMongo(app)

@app.route("/")
def echo():
    final_mars_data = mongo.db.collection.find_one()
    return render_template("index.html", final_mars_data = final_mars_data)

@app.route("/scrape")
def scrape():
    final_mars_data = scrape_mars.scrape()
    # print(type(final_mars_data))
    mongo.db.collection.drop()
    mongo.db.collection.insert_one(final_mars_data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)