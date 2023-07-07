from flask import Flask, render_template
from geojson_scraper import RightmoveData
import json
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Example URLs
urls = [
    # Your URLs here
]

# Cache variable to store the GeoJSON data
cache = None

def scrape_data():
    # Scrape data from each URL
    results = []
    for url in urls:
        data = RightmoveData(url)
        results.extend(data.get_results["features"])

    # Merge GeoJSON features into one GeoJSON object
    geojson_obj = {
        "type": "FeatureCollection",
        "features": results
    }

    # Convert to JSON string
    geojson_str = json.dumps(geojson_obj)

    logging.debug(f"Scraped GeoJSON: {geojson_str}")

    return geojson_str

def populate_cache():
    global cache
    if cache is None:
        # Get the GeoJSON data if it's not cached
        cache = scrape_data()

@app.route('/')
def index():
    logging.debug("Rendering index page")
    return render_template('index.html', geojson=cache)


if __name__ == '__main__':
    # Populate the cache before starting the Flask server
    populate_cache()

    # Run the Flask server
    app.run()
