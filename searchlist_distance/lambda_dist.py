import json
from pusher import Pusher
import os


pusher = Pusher(app_id = os.environ['pusher_app_id'], key = os.environ['pusher_key'], secret = os.environ['pusher_secret'], cluster = os.environ['pusher_cluster'])

# pusher_client = pusher.Pusher(
  # app_id='390402',
  # key='c49898a8563981b623a0',
  # secret='8baa875d8f6bbe1772e1',
  # cluster='us2',
  # ssl=True
# )

class Distance:

  def __init__(self):
    try:
      with open('distance_matrix.json') as json_file:
        self.dist_matrix = json.load(json_file)
    except:
      print("Unable to load distance matrix")
      exit(400)     
      
  def calc_distance(self, city, distance):
    #Initialize an empty array to use for all of our matches at the end
    matches = []
    
    #This next line selects the Array item in our distance matrix that matches the passed city
    #So if we pass 'auburn' it will return: {	"city": "auburn",	"url": "http://auburn.craigslist.org/",	"state": "alabama",	"dist": [1,2,3,etc]}
    city_array_item = next(d for d in self.dist_matrix if d['city'] == city)
    
    #Now we have to iterate through the dist array in the above selection for every item that is smaller than our distance.  This returns an array of the inidices of the matched distances
    #So for auburn less than 200 miles it returns: [0, 1, 2, 4, 7, 8, 82, 88, 92, 93, 94, 97, 98, 99]  Again, these are just the indicies of the matching distances less than 200 miles.
    distance_match_array_indicies = [i for i,x in enumerate(city_array_item['dist']) if int(x) <= int(distance)]
    
    #Now with each of these indicies, we can select each city that matches by using the indicie and create a dict containing the city, url, and states.
    for x in distance_match_array_indicies:
      d = {}
      d['city'] = self.dist_matrix[x]['city']
      d['url'] = self.dist_matrix[x]['url']
      d['state'] = self.dist_matrix[x]['state']
      matches.append(d)
    return(matches)
    #Our matches here look like: [{'city': 'auburn', 'url': 'http://auburn.craigslist.org/'}, {'city': 'birmingham', 'url': 'http://bham.craigslist.org/'}, {'city': 'dothan', 'url': 'http://dothan.craigslist.org/'}, {'city': 'gadsden-anniston', 'url': 'http://gadsden.craigslist.org/'}, {'city': 'montgomery', 'url': 'http://montgomery.craigslist.org/'}, {'city': 'tuscaloosa', 'url': 'http://tuscaloosa.craigslist.org/'}, {'city': 'panama city', 'url': 'http://panamacity.craigslist.org/'}, {'city': 'tallahassee', 'url': 'http://tallahassee.craigslist.org/'}, {'city': 'albany', 'url': 'http://albanyga.craigslist.org/'}, {'city': 'athens', 'url': 'http://athensga.craigslist.org/'}, {'city': 'atlanta', 'url': 'http://atlanta.craigslist.org/'}, {'city': 'columbus', 'url': 'http://columbusga.craigslist.org/'}, {'city': 'macon', 'url': 'http://macon.craigslist.org/'}, {'city': 'northwest ga', 'url': 'http://nwga.craigslist.org/'}]

    # The reason this whole thing works is because there are exactly 420 cities in the matrix.  And each dist array under each city is exactly 420 distances.
    # So by selecting the indicies in any 'dist' array, we can use those indicies to select the matching city json data from the master list by that indicie.
  
    # Usage:
    # d = Distance()
    # print(d.calc_distance('kansas city', 1))
    # [{'city': 'kansas city', 'url': 'http://kansascity.craigslist.org/', 'state': 'missouri'}]



def lambda_handler(event, context):
  city = event['city']
  distance = int(event['distance'])
  query = event['query']
  pusher_channel = event['pusher_channel']
  pusher_event = 'return_cities'
  
  d = Distance()
  results = d.calc_distance(city, distance)
  for result in results:
    pusher.trigger(pusher_channel, pusher_event, {u'city': result['city'],  u'url': result['url'], u'state': result['state']})

  #Add handler to kick off lambda function for each search    
  
  

  

  

  
