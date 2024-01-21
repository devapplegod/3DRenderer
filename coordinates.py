import math


def find_closest_coordinates(X, Y, coordinates_list):
    min_distance = float('inf')
    index = None
    closest_coordinates = None

    for x, y in coordinates_list:
        distance = math.sqrt((X - x)**2 + (Y - y)**2)

        if distance < min_distance:
            min_distance = distance
            closest_coordinates = [x, y]
            index = coordinates_list.index([x, y])

    return [closest_coordinates[0], closest_coordinates[1], index]
