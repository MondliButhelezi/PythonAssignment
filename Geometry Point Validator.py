history = []

def validate_point(lat, lon):
    point = (lat, lon)
    valid = True
    reason = "Latitude and Longitude are between the acceptable range"

    if not (-90 <= lat <= 90):
        valid = False
        reason = "Latitude should be between -90 and 90."
    elif not (-180 <= lon <= 180):
        valid = False
        reason = "Longitude should be between -180 and 180."

    if valid:
        print("Point is valid.")
    else:
        print(f"Point is invalid. Reason: {reason}")

    return valid, reason

def check_history():
    if len(history) == 0:
        print("No points in history.")
    else:
        print(f"Total points entered: {len(history)}")
        for point in history:
            lat, lon, valid, reason = point
            print(f"Lat: {lat}, Lon: {lon}, Valid: {valid}, Reason: {reason}")

while True:
    feature = input('''
                    To Choose a feature: 
                    Press 1. to Validate Point, 
                    Press 2.  to Check History,
                    or Press 3. to End the program
                    ''' )
    
    if feature == "1":
        lat = float(input("Enter the latitude: "))
        lon = float(input("Enter the longitude: "))
        valid, reason = validate_point(lat, lon)
        history.append((lat, lon, valid, reason))
    
    elif feature == "2":
        check_history()
    
    elif feature == "3":
        break
    
    else:
        print("Command does not exist.")
