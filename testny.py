"""
This program takes a list of cities (with distance to other cities) and a starting
city of the user's choice.
It then creates a tour starting in starting city, visiting all other cities,
and goes back to starting city. It uses the nearest neighbour algorithm to
choose what city to visit next (visit whatever unvisited city which is closest),
in hope to minimize total distance travelled.

We have opted to let the user create several Tours and therefor also let them
choose the ID for each tour they generate, since it could be a tour per salesman,
or simply to compare different tours.

Input: TourID, List of cities, starting city
Output: Tour of cities to visit in order, and total distance travelled.

We assume the user is able to provide the input list in the format of
"City1", {"City2": Distance, "City3": Distance}" for each city, as shown
in the test.

Our interpretation of the task is that the user will only provide a list of
cities they actually want to include in tour.
"""
# Creating class City

class City:
    # Using init to pass name and distance list
    def __init__(self, name, distances):
        self.name = name
        if type(distances) == dict:
            self.distances = distances
        else:
            print("Invalid data input, distance list is not in dict format")
            exit()



    # Using magic repr method for printable representation
    def __repr__(self):
        return self.name

    # Creating method to check distance to given city:
    def distanceTo(self, toCity):
        # Using try except to catch unexpected errors
        try:
            # Returns the distance to the toCity
            return self.distances[toCity]
            # If toCity key not found in distances dictionary of city:
        except KeyError:
            # Print error
            print("Cannot retrieve distance from {city} to {toCity}. Please revise dataset.")
            # And exit, as it makes no sense to continue if data is missing for this task.
            exit()

# Create class tour

class Tour:
    # Using init to pass variable tourID and create tourCities dict
    def __init__(self, tourid):
        # First pass tourID
        self.tourid = tourid
        # Create list to put the cities for the tour
        self.tourCities = {}

    # Using magic method __str__ for a printable representation
    def __str__(self):
        # Returning the tour ID and the list of cities to visit by the keys
        # in the dictionary tourCities. This is turned into a list then string
        # to print (and stripped of brackets), for better readability for the user than simply
        # printing the dictionary keys directly.
        return("Tour ID: #{} \nCities to visit: {}".format(self.tourid, str(list(self.tourCities.keys())).strip("[]")))

    # Create method addCity
    def addCity(self, name, distances):
        """
        This method adds a city to the tours tourCities list. It takes the
        city name and dictionary of distances as variables.
        """
        # Create instance of city(with distances) and add it to tourCities
        self.tourCities[name] = City(name, distances)



    # Creating findTour method
    def findTour(self, startCity, inputList):
        """
        This method takes starting city startCity and list of cities
        inputList as input. It returns an ordered list of cities to visit and
        the total distance travelled. The order is determined by the nearest
        neighbour algorithm where it chooses the next city by whatever
        unvisited city is closest.
        """

        # Start for loop to add all cities from inputList to tourCity
        # This is put here as it is our interpretation that the user would not
        # provide cities in inputList that should not be added to the Tour.
        # If that was the case, this for loop could be removed and the user could
        # use addCity function for the cities wanted.
        for cityname, distances in inputList:
            # Calling addCity method for all elements in inputList
            self.addCity(cityname, distances)

        # Creating a list of unvisited cities by tourCities dictionary keys
        self.citiesLeft = list(self.tourCities.keys())

        # Removing starting city from the unvisited cities list
        self.citiesLeft.remove(startCity)

        # Initialize list of final route, starting with the starting city
        # In this list we only store the names(strings).
        finalTour = [startCity]

        # Initialize variable for final distance
        finalDistance = 0

        # Setting starting city as variable fromCity for first step
        fromCity = startCity

    #    Starting while loop
    #    Will keep going until there are no cities left to visit
        while (self.citiesLeft):

            # Create bestCity variable which will be city we go to
            bestCity = None

            # Create empty list of distances to remaining cities from fromCity
            possibleDistances = []

            # Starting for loop for each unvisited city left:
            for city in self.citiesLeft:
                #Get the distance from fromCity to other cities in list
                # Adding name of city and distance from fromCity to city to possibleDistances as a tuple
                possibleDistances.append((self.tourCities[city].name, self.tourCities[fromCity].distanceTo(city)))
                # The above operation could have been solved with list comprehension but as we
                # wish to return 2 values, we found that using a for loop gives better readability
                # in the code.

            # End for loop

            # To sort the list of possible distances, we make use of lambda to make a
            # quick function so we can sort by value (which is stored at position 1
            # in each element of the list)
            possibleDistances.sort(key=lambda x: x[1])
            # The list is now sorted.

            # Set variable bestCity to be the city at the first spot in the now sorted list
            # of distances, ie the closest City.
            bestCity = possibleDistances[0][0]

            # Add name of city to final tour list of cities to visit in order
            finalTour.append(bestCity)

            # Add distance from previous city to bestCity to total distance.
            # The distance is stored in possibleDistance list at position 1 in each element.
            # We know it is element 0 as the list is sorted in ascending order.
            finalDistance = finalDistance + possibleDistances[0][1]

            # Remove the name of best city from citiesLeft
            self.citiesLeft.remove(bestCity)

            # Change fromCity to the new city
            fromCity = bestCity

            # The salesman has now travelled to a new city and the loop can
            # start over as long as there are unvisited cities left.

        # End while loop

        # Return to starting city: Adding starting city as final city
        finalTour.append(self.tourCities[startCity].name)

        # Adding distance from current city to starting city.
        finalDistance = finalDistance + self.tourCities[fromCity].distanceTo(startCity)

        # Return the ordered list of cities to visit as well as the final distance travelled
        return(finalTour, finalDistance)




"""
Code for testing the program:
"""
# Create a function to test with given starting city
def testScript(startCity, TourID, inputList):
    """
    This function is created to test the program.
    It will create a new tour with given TourID, and call the findTour function
    which will add the list of cities inputList to the Tour and create the
    tour itself starting (and ending) in startCity.
    This function then prints the results.
    """
    # Create a tour instance
    TourID = Tour(TourID)
    # Save the ordered list of tourOrder and variable tourDistance to 2 variables
    tourOrder, tourDistance = TourID.findTour(startCity, inputList)
    # Print the tour ID (and list of cities to visit, unordered)
    print("--- NEW TOUR --- \n"
    f"{TourID}")
    # Print the ordered list of cities, removing brackets for readability
    print("List of cities to visit in order: {}".format(str(tourOrder).strip("[]")))
    # Printing distance travelled, limiting answer to 2 decimals
    # This is done due the computer's format (floating-point) that cannot represent
    # a number like 0.1, 0.2 or 0.3.
    # Source: https://floating-point-gui.de/basic/
    # Solution inspired from: https://docs.python.org/3/library/string.html#grammar-token-format-spec
    print(f"Total distance travelled: {(tourDistance):.2f}) \n"
    "Thank you for using this program. \n")

# For testing function: activating when program is opened (not imported)
if __name__ == "__main__":

    # Adding list of example cities from task
    inputList = [
        ("Bergen", {"Oslo": 7.14, "Stavanger": 4.42, "Trondheim": 9.3, "Kristiansand": 7.39}),
        ("Oslo", {"Bergen": 6.47, "Stavanger": 7.10, "Trondheim": 6.10, "Kristiansand": 3.56}),
        ("Kristiansand", {"Oslo": 4.3, "Bergen": 7.45, "Trondheim": 10.17, "Stavanger": 3.33}),
        ("Stavanger", {"Oslo": 7, "Bergen": 4.48, "Trondheim": 13.37, "Kristiansand": 3.14}),
        ("Trondheim", {"Oslo": 6.24, "Bergen": 9.34, "Stavanger": 13.36, "Kristiansand": 10.12})
        ]

    # Running testScript function for Oslo and Bergen
    testScript("Oslo", "TestTour1Oslo", inputList)
    testScript("Bergen", "TestTour2Bergen", inputList)
