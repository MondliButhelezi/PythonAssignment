# Assignment:
# 
# 1. Combine your functions into a Class named PointValidator
# 2. Add error handling at least on the lat and lon input. Think of any error that could be handled.
# 3. Add feature to export current history to a file. Filename must contain current date and time when the file is exported. 
# Example: "point-2023.02.14-00.15.01", the format is "point-{year}.{double digit month}.{double digit date}-{double digit hour}.{double digit minutes}.{double digit seconds}"
# 4. Add feature to read exported file. Use must input the filename and/or the full path of the file. The content of the file would be added to the current history.
# If you used list to store current history, then the file content would be added to that list.

import datetime
import os


class PointValidator:
    def __init__(self):
        self.history = []

    def validate_point(self, lat, lon):
        point = (lat, lon)
        valid = True
        reason = "Latitude and Longitude are within the acceptable range"

        try:
            lat = float(lat)
            lon = float(lon)

            if not (-90 <= lat <= 90):
                valid = False
                reason = "Latitude should be between -90 and 90."
            elif not (-180 <= lon <= 180):
                valid = False
                reason = "Longitude should be between -180 and 180."

        except ValueError:
            valid = False
            reason = "Latitude and Longitude must be numeric values."

        if valid:
            print("Point is valid.")
        else:
            print(f"Point is invalid. Reason: {reason}")

        return valid, reason

    def check_history(self):
        if len(self.history) == 0:
            print("No points in history.")
        else:
            print(f"Total points entered: {len(self.history)}")
            for point in self.history:
                lat, lon, valid, reason = point
                print(f"Lat: {lat}, Lon: {lon}, Valid: {valid}, Reason: {reason}")

    def export_history(self, file_path):
        if len(self.history) == 0:
            print("No points in history to export.")
        else:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y.%m.%d-%H.%M.%S")
            filename = f"point-{timestamp}.txt"
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(os.path.join(file_path, filename), "w") as file:
                    file.write(f"Count of Points: {len(self.history)}\n")
                    for point in self.history:
                        lat, lon, valid, reason = point
                        file.write(f"Lat: {lat}, Lon: {lon}, Valid: {valid}, Reason: {reason}\n")
                print(f"History exported to file: {os.path.join(file_path, filename)}")
            except IOError:
                print("An error occurred while exporting the history.")

    def read_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                file_content = file.readlines()

            for line in file_content:
                if line.strip().startswith("Lat:"):
                    point_info = line.strip().split(",")
                    lat = float(point_info[0].split(":")[1].strip())
                    lon = float(point_info[1].split(":")[1].strip())
                    valid = point_info[2].split(":")[1].strip()
                    reason = point_info[3].split(":")[1].strip()
                    self.history.append((lat, lon, valid, reason))

            print(f"File '{file_path}' read successfully.")

        except IOError:
            print("An error occurred while reading the file.")
    

    def run(self):
      while True:
          feature = input('''
                          To choose a feature: 
                          Press 1 to validate a point, 
                          Press 2 to check the history,
                          Press 3 to export the history to a file,
                          Press 4 to read a file and add to history,
                          or Press 5 to end the program
                          ''')

          if feature == "1":
              lat = input("Enter the latitude: ")
              lon = input("Enter the longitude: ")
              valid, reason = self.validate_point(lat, lon)
              self.history.append((lat, lon, valid, reason))

          elif feature == "2":
              self.check_history()
          
          elif feature == "3":
              file_path = input("Enter the file path to export the history: ")
              self.export_history(file_path)

          elif feature == "4":
                file_path = input("Enter the filename or full path of the file: ")
                self.read_file(file_path)

          elif feature == "5":
              break

          else:
              print("Command does not exist.")



# Create an instance of the PointValidator class and run the program
validator = PointValidator()
validator.run()
