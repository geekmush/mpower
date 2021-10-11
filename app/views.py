# -*- encoding: utf-8 -*-

# Flask modules
from flask   import render_template, request
from jinja2  import TemplateNotFound

# App modules
from app import app

import json
import requests

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    try:

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path, segment=segment )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None   

# Product Search Results
@app.route('/product_search', methods=['POST', 'GET'])
def product_search():
  items = []

  if request.method == 'POST':
    searchstring = request.form.get("searchstring")

    url = 'https://mpowerapi.azurewebsites.net/api/v1/Items/search?pageNumber=1'

    data = json.dumps({"search": searchstring})
    headers = { 'Content-Type': 'application/json-patch+json', 
                'accept': 'text/plain',
                'Authorization': f'Bearer {app.config["API_TOKEN"]}'
              }

    response = requests.post(url, data=data, headers=headers)
    product_data = json.loads(response.text)

    for i in range(len(product_data['Results'])):
      print(f"Name={product_data['Results'][i]['Name']}")
      print(f"Name={product_data['Results'][i]['Size']}")
      print(f"Name={product_data['Results'][i]['Retail']}")
      print(f"Name={product_data['Results'][i]['QuantityOnHand']}")
      print(f"Name={product_data['Results'][i]['SoldLast90']}")
    #item = dict(name = f"{product_data['Results'][i]['Name']:80s}",
    #            size = f"{product_data['Results'][i]['Size']:10}",
    #            retail = f"{str(product_data['Results'][i]['Retail']):10}",
    #            qoh = f"{str(product_data['Results'][i]['QuantityOnHand']):10}",
    #            last90 = f"{str(product_data['Results'][i]['SoldLast90']):10}")
      item = dict(name = f"{product_data['Results'][i]['Name']}",
                  size = f"{product_data['Results'][i]['Size']}",
                  retail = f"{str(product_data['Results'][i]['Retail'])}",
                  qoh = f"{int(product_data['Results'][i]['QuantityOnHand'])}",
                  last90 = f"{int(product_data['Results'][i]['SoldLast90'])}")
      items.append(item)

   #if response.status_code == 200:
   # return render_template("index.html", searchstring=searchstring, product_data=foo)

  try:

    # Serve the file (if exists) from app/templates/FILE.html
    return render_template( '/product_search.html', items=items )
    
  except TemplateNotFound:
    return render_template('page-404.html'), 404

