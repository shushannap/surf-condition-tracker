import zmq

def request_swell_data(latitude, longitude, threshold):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    request = f"{latitude},{longitude},{threshold}"
    print(f"Sent request: {request}")
    socket.send_string(request)

    response = socket.recv_string()
    return response

# Update the latitude and longitude based on information from city_lookup.py
# Update threshold value for notifications
def main():
    latitude = 34.4221319
    longitude = -119.702667
    threshold = 0.5

    response = request_swell_data(latitude, longitude, threshold)
    print("Response received:")
    print(response)

if __name__ == "__main__":
    main()
