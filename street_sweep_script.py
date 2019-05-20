from flask import Flask, request, render_template
from flask_googlemaps import GoogleMaps
from shapely.geometry import LineString
from shapely.geometry import Polygon
from geopy.geocoders import Nominatim
import requests
import datetime
import calendar

app = Flask(__name__)

app.config['GOOGLEMAPS_KEY'] = API_KEY
GoogleMaps(app)

@app.route('/')
def start():
    return render_template('street_sweep_template.html')


@app.route('/sentHTML', methods=['GET', 'POST'])
def sentHTML():
    geolocator = Nominatim(timeout=5,user_agent="streep_sweep")
    address = (request.form['address'])
    location = geolocator.geocode(address)

    try: 
        og_lat = location.latitude # This is your latitude

    except AttributeError:          # If there is no value or the address doesn't exist, use template 'noaddress.html'
        result = 'No address found'
        return render_template('noaddress.html', result=result, location=location)

    # Creates a polygon around your coordinate
    og_long = location.longitude  # This is your longitude
    r = 0.0001
    first_coor = (og_long + r, og_lat + r)
    secon_coor = (og_long - r, og_lat - r)
    third_coor = (og_long + r, og_lat - r)
    fourt_coor = (og_long - r, og_lat + r)

    coord_list_tuple = [first_coor, secon_coor, third_coor, fourt_coor]     # Changes formating so that it fulfills shapelys requierements 
    polygon_1 = Polygon(coord_list_tuple)  #Creates a polygon (shapely module)

    r = requests.get('https://data.sfgov.org/resource/u2ac-gv9v.json?$limit=40000')    # Requests from database
    json_object = r.json()  # Changes to more readable format (json)

    alert=""
    ifweek=""
    iftoday=""
    whensweep=""
    current_date_time =""
    current_date_time2 = ""
    
    result={}
    i=1
    for dict in json_object:              
        new_list = []
        for coor in dict["geometry"]["coordinates"]:   # For every coordinate, make it a tuple and append it to list
            new_list.append(tuple(coor))
        line = LineString(new_list)                    # Out of he list, create a LineString (shapely module)
        intersect = line.intersects(polygon_1)         # Check if line and polygon intersects
        if intersect:                                  # If they do -> Add the dictionary to the dictionary
            result[i]=dict
            i+=1

            current_date_time = datetime.datetime.now()
            current_date_time2 = current_date_time.strftime("%a, %b %d, %Y")
            todays_day = current_date_time.strftime("%a")
            kalender = calendar.Calendar() 
            weeks = kalender.monthdayscalendar(current_date_time.year, current_date_time.month)

            for i in range(len(weeks)):
                if current_date_time.day in weeks[i]:
                    week_number = (i+1)
        
            if week_number == 1:
                week1 = 'Y'
                if week1 == dict['week1ofmon']:
                    ifweek = "This week!"
                else:
                    ifweek = "Not this week"


            elif week_number == 2:
                week2= 'Y'
                if week2 == dict['week2ofmon']:
                    ifweek = "This week!"
                else:
                    ifweek = "Not this week"

            elif week_number == 3:
                week3 = 'Y'
                if week3 == dict['week3ofmon']:
                    ifweek = "This week!"
                else:
                    ifweek = "Not this week"


            elif week_number == 4:
                week4 = 'Y'
                if week4 == dict['week4ofmon']:
                    ifweek = "This week!"
                else:
                    ifweek = "Not this week"


            elif week_number == 5:
                week5 = 'Y'
                if week5 == dict['week5ofmon']:
                    ifweek = "This week!"
                else:
                    ifweek = "Not this week"



            if todays_day == dict['weekday']:
                iftoday ='Today!'
                alert = "Not safe to park"
                return render_template('end_today.html', result=result, location=location, current_date_time=current_date_time, current_date_time2=current_date_time2, iftoday=iftoday, ifweek=ifweek, alert=alert)

            else:
                iftoday = "Not today"
                alert = "Safe to park"
                return render_template('end.html', result=result, location=location, current_date_time=current_date_time, current_date_time2=current_date_time2, iftoday=iftoday, ifweek=ifweek, whensweep=whensweep, alert=alert)

    return render_template('end.html', result=result, location=location, current_date_time=current_date_time, current_date_time2=current_date_time2, iftoday=iftoday, ifweek=ifweek, whensweep=whensweep, alert=alert)


            #     try: 
            #         current_hour = int(current_date_time.strftime("%H")) + 1
            #         dict_fromhour = int(dict['fromhour'].strip(':00'))
            #         dict_tohour = int(dict['tohour'].strip(':00'))
            #     except:
            #         print('Something went wrong!')

            #     if current_hour >= dict_fromhour and current_hour <= dict_tohour:
            #         ifnow = "They are sweeping right now!"

            #     elif current_hour < dict_fromhour:
            #         ifnow='The sweeper will come at {}!'.format(dict['fromhour'])
                
            # else:
            #     print('The sweeper has already sweept today (between {} and {})'.format(dict['fromhour'], dict['tohour']))






                    
                # if current_hour >= dict_fromhour and current_hour <= dict_tohour:
                #     whensweep = 'They are sweepin\' right now!'

                # elif current_hour < dict_fromhour:
                    # whensweep = 'The sweeper will come at {}!'.format(dict['fromhour'])
                    
            #     else:
            #         whensweep = 'The sweeper has already sweept today (between {} and {})'.format(dict['fromhour'], dict['tohour'])

            # else:
            #     whensweep = 'The sweeper will come on {} between {} and {}.'.format(dict['weekday'], dict['fromhour'], dict['tohour'])





@app.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method=='POST':
    #     if request.form['submit_button'] == 'Log in':
    return render_template('login.html')



if __name__ == '__main__':
	app.run(debug=True)
