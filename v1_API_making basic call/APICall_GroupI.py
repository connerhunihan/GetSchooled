# Sep 24, 2017 – CH
# Set up basic API call to return all information/fields from schools inside locale=11 Field Parameter (lare cities of at least 250,000 population)
# Tried to limit results by using region_id Option Perimeter, but kept getting <400> error code.  Not sure why it's not working... 

import requests
import json

response = requests.get("https://api.data.gov/ed/collegescorecard/v1/schools.json?school.locale=11&api_key=JDp4XdkhgSrFGMsLCBzDs882S5PRbGpJMtMbAFDS")
data = json.loads(response.content)
print(data)