import zmq
import requests

def get_swell_data(latitude, longitude):
    api_key = '7f7c7133889241bb845213530240308'  
    url = f'http://api.worldweatheronline.com/premium/v1/marine.ashx?key={api_key}&format=json&q={latitude},{longitude}&tide=yes'
    response = requests.get(url)
    return response.json()

def format_response(swell_data, notifications):
    formatted_response = "Detailed Swell Data for the Past Week:\n"
    for day in swell_data['weather']:
        formatted_response += f"Date: {day['date']}\n"
        for hour in day['hourly']:
            formatted_response += f"  Time: {hour['time']}\n"
            formatted_response += f"  Swell Height: {hour['swellHeight_m']} m\n"
            formatted_response += f"  Swell Direction: {hour['swellDir16Point']}\n"
            formatted_response += f"  Swell Period: {hour['swellPeriod_secs']} s\n"
            formatted_response += f"  Water Temperature: {hour['waterTemp_C']} °C\n"
            formatted_response += "----------------------------------------\n"

    formatted_response += f"\nNumber of notifications: {len(notifications)}\n"
    for notification in notifications:
        formatted_response += f"Date: {notification['date']}\n"
        formatted_response += f"  Time: {notification['time']}\n"
        formatted_response += f"  Swell Height: {notification['swell_height']} m\n"
        formatted_response += f"  Swell Direction: {notification['swell_direction']}\n"
        formatted_response += f"  Swell Period: {notification['swell_period']} s\n"
        formatted_response += f"  Water Temperature: {notification['water_temp']} °C\n"
        formatted_response += "----------------------------------------\n"
    return formatted_response

def check_threshold(swell_data, threshold):
    notifications = []
    for day in swell_data['weather']:
        for hour in day['hourly']:
            if float(hour['swellHeight_m']) > threshold:
                notification = {
                    'date': day['date'],
                    'time': hour['time'],
                    'swell_height': hour['swellHeight_m'],
                    'swell_direction': hour['swellDir16Point'],
                    'swell_period': hour['swellPeriod_secs'],
                    'water_temp': hour['waterTemp_C']
                }
                notifications.append(notification)
    return notifications

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Producer is running and waiting for requests...")

    while True:
        request = socket.recv_string()
        print(f"Received request: {request}")
        latitude, longitude, threshold = map(float, request.split(','))

        swell_data = get_swell_data(latitude, longitude)
        notifications = check_threshold(swell_data['data'], threshold)
        response = format_response(swell_data['data'], notifications)

        socket.send_string(response)

if __name__ == "__main__":
    main()
