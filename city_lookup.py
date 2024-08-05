import requests

def get_lat_long(city_name, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        raise ValueError("City not found")


if __name__ == "__main__":
    api_key = "d02c426200964ca8abe2035dfc0e187d"
    city_name = "Santa Barbara" # Type in whatever city name you want the latitude/longitude for
    try:
        lat, lon = get_lat_long(city_name, api_key)
        print(f"Latitude: {lat}, Longitude: {lon}")
    except ValueError as e:
        print(e)
