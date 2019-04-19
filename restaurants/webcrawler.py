import requests
from bs4 import BeautifulSoup
import json
import re
import threading
import os
from multiprocessing.pool import ThreadPool
state_abbreviation = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

def parse_local_url(city, state):
    city_str = city.split(" ")
    index = 0

    ret_url = "https://www.yelp.com/search?find_desc=&find_loc="

    while index < len(city_str):
        ret_url += city_str[index]
        if index < len(city_str) - 1:
            ret_url += "+"
        index += 1

    ret_url += "%2C+" + state_abbreviation[state]
    ret_url += "&ns=1&start="

    return ret_url


def concatenate_restaurant_data(item_url):
    url_source_html = requests.get(item_url)
    indiv_page_text = url_source_html.text
    soup = BeautifulSoup(indiv_page_text, features = "html5lib")

#    total_review = ""
#     i = 1
#     for item_name in soup.findAll('p', {'itemprop': 'description'}):
#         total_review += "\n\n  | Review #" + str(i) + " | ";
#         total_review += item_name.string + "  \n\n "
#         i += 1

    total_rating = 0
    rating_count = 0
    avg_rating = 0

    common_rating_str = re.compile('.*i-stars i-stars--.*')

    for item_name in soup.find_all("div", {"class": common_rating_str}):
        for find_img in item_name.find_all('img', alt=True):
            rating_str = find_img['alt']
            rating_split = rating_str.split(" ")
            indiv_rating = rating_split[0]
            total_rating += float(indiv_rating)
            rating_count += 1

    avg_rating = total_rating / rating_count

    first_string_found = False
    total_hours = ""

    class_str = 'lemon--p__373c0__3Qnnj text__373c0__2pB8f'
    class_str += 'no-wrap__373c0__3qDj1 text-color--normal'
    class_str += '__373c0__K_MKN text-align--left__373c0__2pnx_'

    daily_hours = False

    for item_name in soup.findAll('p', {
        'class': 'class_str'}):
        if item_name.string != "":
            total_hours += "Hours respectively from Monday to Sunday\n"
        total_hours += item_name.string

        if (item_name.string != None):
            first_string_found = True

    count_items = 1
    add_str = ""

    monday_hours = ""
    wednesday_hours = ""
    thursday_hours = ""
    friday_hours = ""
    saturday_hours = ""
    sunday_hours = ""

    for item_name in soup.findAll('span', {'class': 'nowrap'}):
        if total_hours == "" or first_string_found == False:
            daily_hours = True
            if item_name.string.find("Closed now") == -1:
                add_str += item_name.string
                if (count_items % 2 == 1):
                    add_str += " – "
                if (count_items == 2):
                    monday_hours = add_str
                    add_str = ""
                if (count_items == 4):
                    tuesday_hours = add_str
                    add_str = ""
                if (count_items == 6):
                    wednesday_hours = add_str
                    add_str = ""
                if (count_items == 8):
                    thursday_hours = add_str
                    add_str = ""
                if (count_items == 10):
                    friday_hours = add_str
                    add_str = ""
                if (count_items == 12):
                    saturday_hours = add_str
                    add_str = ""
                if (count_items == 14):
                    sunday_hours = add_str
                    add_str = ""

                count_items += 1

    if monday_hours != "":
        monday_hours = re.sub(u"\u2013", "-", monday_hours)
    if tuesday_hours != "":
        tuesday_hours = re.sub(u"\u2013", "-", tuesday_hours)
    if wednesday_hours != "":
        wednesday_hours = re.sub(u"\u2013", "-", wednesday_hours)
    if thursday_hours:
        thursday_hours = re.sub(u"\u2013", "-", thursday_hours)
    if friday_hours:
        friday_hours = re.sub(u"\u2013", "-", friday_hours)
    if saturday_hours:
        saturday_hours = re.sub(u"\u2013", "-", saturday_hours)
    if sunday_hours:
        sunday_hours = re.sub(u"\u2013", "-", sunday_hours)

    if daily_hours:
        restaurant_dict = {"hours": {
            "Monday": monday_hours,
            "Tuesday": tuesday_hours,
            "Wednesday": wednesday_hours,
            "Thursday": thursday_hours,
            "Friday": friday_hours,
            "Saturday": saturday_hours,
            "Sunday": sunday_hours
            },
            "avg_rating": round(avg_rating,3)
            }
    else:
        restaurant_dict = {"hours": total_hours, "avg_rating": round(avg_rating, 3)}

    json_str = json.dumps(restaurant_dict)

    return json_str

def get_single_restaurant_data(restaurant_name, url):
    restaurant_page = 0
    found_restaurant = False
    latency_count = 0

    while found_restaurant == False:
        if latency_count > 10:
            break

        url += str(restaurant_page)
        url_source_html = requests.get(url)
        indiv_page_text = url_source_html.text
        soup_obj = BeautifulSoup(indiv_page_text, features="html5lib")

        for link in soup_obj.findAll('a', {
            'class': 'lemon--a__373c0__IEZFH link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5'}):
            indiv_link = "https://www.yelp.com" + link.get('href')
            title = link.string

            if (title.find(restaurant_name) != -1):
                found_restaurant = True
                return concatenate_restaurant_data(indiv_link)
            else:
                restaurant_page += 10
                latency_count += 1


def generate_list_of_similar_restaurants(restaurants, passed_url, restaurant_name):
    url = passed_url
    url_source_html = requests.get(url)
    indiv_page_text = url_source_html.text
    soup_obj = BeautifulSoup(indiv_page_text, features = "html5lib")

    soup_link = 'lemon--a__373c0__IEZFH link__373c0__29943 '
    soup_link += 'link-color--blue-dark__373c0__1mhJo link-size'
    soup_link += '--inherit__373c0__2JXk5'

    for link in soup_obj.findAll('a', {'class': soup_link}):
        indiv_link = "https://www.yelp.com" + link.get('href')
        title = link.string

        if (title.find("read more") == -1 & title.find(restaurant_name) == -1):
            title = re.sub(u"\u2019s", "-", title)
            restaurants["restaurants"].append({"title": title, "url": indiv_link})

    return restaurants

def scrape_restaurant_info(restaurant_name, city, state):
    url = parse_local_url(city, state)
    return get_single_restaurant_data(restaurant_name, url)


def scrape_restaurant_list(restaurant_name, city, state, max_no_pages):
    url = parse_local_url(city, state)
    page = 0

    restaurants = { "restaurants": []}

    while page < (max_no_pages * 10):
        url += str(page)
        restaurants = generate_list_of_similar_restaurants(restaurants, url, restaurant_name)
        page += 10

    json_str = json.dumps(restaurants)

    return json_str


def restaurant_info_scraper(restaurant_name, city, state):
    name_valid = False
    city_valid = False
    state_valid = False

    if restaurant_name is not None:
        name_valid = True
    if city is not None:
        city_valid = True
    if state is not None:
        state_valid = True

    if name_valid & city_valid & state_valid:
        return scrape_restaurant_info(restaurant_name, city, state)

def restaurant_list_scraper(restaurant_name, city, state):
    name_valid = False
    city_valid = False
    state_valid = False

    if restaurant_name is not None:
        name_valid = True
    if city is not None:
        city_valid = True
    if state is not None:
        state_valid = True

    if name_valid & city_valid & state_valid:
        max_pages = 2
        return scrape_restaurant_list(restaurant_name, city, state, max_pages)


def multithread_functions(restaurant_name, city, state):
    total_threads = ThreadPool(processes = 2)

    rest_info_result = total_threads.apply_async(restaurant_info_scraper, (restaurant_name, city, state))
    rest_list_result = total_threads.apply_async(restaurant_list_scraper, (restaurant_name, city, state))

    info_ret = rest_info_result.get()
    list_ret = rest_list_result.get()

    # print(info_ret)
    # print(list_ret)

    return info_ret, list_ret

#POSSIBLE CALLS

#1)
    #MULTITHREADED CALL WHICH RETURNS BOTH INFO AND LIST AT SAME TIME
# multithread_functions("Happy Lemon", "Cupertino", "California")

#2)
    #CALL FOR INFORMATION ABOUT SINGLE RESTAURANT
#print(restaurant_info_scraper("Happy Lemon", "Cupertino", "California"))

    #CALL FOR LIST OF ALL SIMILAR RESTAURANTS
#print(restaurant_list_scraper("Happy Lemon", "Cupertino", "California"))

#NOTE:
#MULTITHREADED TIME:
#Approx 6 seconds for list

#Time for both individually
#Approx 11 seconds
