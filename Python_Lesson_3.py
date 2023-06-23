# Assignment 3:
# A. Make a class representation of the SQL table that you have created.
# B. Make Shapefile Validator Program
# 1. Make a class that operates on a shapefile with these features as options. Each point would be a separate option on the screen.
# 1. Validate each feature, whether they are valid geometry or not.
# 2. Check the intersection among features. This will only be valid if the geometry type is LineString, MultiLineString, Polygon, or MultiPolygon. If the geometry type is not one of them, then show a warning that this feature is not applicable.
# 3. Remove invalid geometry and export to a shapefile. 
# 4. Remove intersecting geometry and export to a shapefile.
# 5. Convert to CSV. This will only be valid if the geometry type is Point. If the shapefile's geometry type is not Point, then show warning that this feature is not applicable.
# The flow of the program would be:
# 1. Program is executed.
# 2. Display prompts for Shapefile path input
# 3. If path is a valid shapefile, show the options.
# 4. Option selected.
# 5. If it is option 1 and 2, the result would only be printed on the screen.
# 6. If it is option 3 and 4, the screen would only show how many invalid/intersection feature it found. Then the valid/non-intersecting feature will be exported.
# 7. If option 3 and 4 are selected, display with prompt input for filename and path.
# 8. Program is terminated. It means after validation has finished, it will not redisplay its menu/options. 


import fiona
from shapely.geometry import shape, Point, LineString, MultiLineString, Polygon, MultiPolygon
from shapely.validation import explain_validity


class ShapefileProcessor:
    def __init__(self):
        self.file_path = None
        self.features = []
        self.geometry_type = None

    def prompt_shapefile_path(self):
        self.file_path = input("Enter the path to the shapefile: ")

    def load_shapefile(self):
        try:
            with fiona.open(self.file_path) as shp:
                self.features = list(shp)
                self.geometry_type = shp.schema['geometry']
        except FileNotFoundError:
            print("Invalid shapefile path.")
            return False
        except Exception as e:
            print(f"Error loading shapefile: {str(e)}")
            return False
        return True

    def validate_features(self):
        for feature in self.features:
            geometry = shape(feature['geometry'])
            is_valid = geometry.is_valid
            explanation = explain_validity(geometry)
            print(f"Feature ID: {feature['id']}, Valid: {is_valid}")
            if not is_valid:
                print(f"Explanation: {explanation}")

    def check_intersection(self):
        if self.geometry_type in (LineString, MultiLineString, Polygon, MultiPolygon):
            print("Intersection check not applicable for this geometry type.")
            return

        for i, feature1 in enumerate(self.features):
            geometry1 = shape(feature1['geometry'])
            for j, feature2 in enumerate(self.features[i + 1:]):
                geometry2 = shape(feature2['geometry'])
                if geometry1.intersects(geometry2):
                    print(f"Features {feature1['id']} and {feature2['id']} intersect.")

    def remove_invalid_geometry(self):
        self.features = [feature for feature in self.features if shape(feature['geometry']).is_valid]

    def remove_intersecting_geometry(self):
        new_features = []
        removed_features = []
        for i, feature1 in enumerate(self.features):
            geometry1 = shape(feature1['geometry'])
            is_intersecting = False
            for j, feature2 in enumerate(self.features[i + 1:]):
                geometry2 = shape(feature2['geometry'])
                if geometry1.intersects(geometry2):
                    is_intersecting = True
                    removed_features.append(feature2)
            if not is_intersecting:
                new_features.append(feature1)
        self.features = new_features

        for feature in removed_features:
            print(f"Removed feature with ID: {feature['id']} due to intersection.")

    def export_to_shapefile(self):
        output_file = input("Enter the output shapefile path: ")
        try:
            with fiona.open(
                output_file, 'w',
                driver='ESRI Shapefile',
                crs=self.get_crs_from_shapefile(),  # Retrieve CRS from shapefile metadata
                schema=self.get_schema_from_shapefile()  # Retrieve schema from shapefile
            ) as shp:
                for feature in self.features:
                    shp.write(feature)
            print("Export successful.")
        except Exception as e:
            print(f"Error exporting to shapefile: {str(e)}")

    def get_crs_from_shapefile(self):
        with fiona.open(self.file_path) as shp:
            return shp.crs

    def get_schema_from_shapefile(self):
        with fiona.open(self.file_path) as shp:
            return shp.schema

    def convert_to_csv(self):
        if self.geometry_type != Point:
            print("Conversion to CSV not applicable for this geometry type.")
            return

        for feature in self.features:
            coordinates = shape(feature['geometry']).coords[0]
            print(f"Feature ID: {feature['id']}, Coordinates: {coordinates[0]}, {coordinates[1]}")


def display_menu():
    print("Main Menu Selection:")
    print("1. Validate features")
    print("2. Check for intersections")
    print("3. Remove invalid geometry")
    print("4. Remove intersecting geometry")
    print("5. Export to shapefile")
    print("6. Convert to CSV")
    print("7. Exit")


def main():
    processor = ShapefileProcessor()

    # Prompt for shapefile path
    processor.prompt_shapefile_path()

    # Load shapefile
    if not processor.load_shapefile():
        return

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            processor.validate_features()
        elif choice == "2":
            processor.check_intersection()
        elif choice == "3":
            processor.remove_invalid_geometry()
            print("Invalid geometry removed.")
        elif choice == "4":
            processor.remove_intersecting_geometry()
            print("Intersecting geometry removed.")
        elif choice == "5":
            processor.export_to_shapefile()
        elif choice == "6":
            processor.convert_to_csv()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again!")


if __name__ == "__main__":
    main()
