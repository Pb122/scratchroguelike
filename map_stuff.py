# -*- coding: utf-8 -*-"

from main import *
from data import *

"""
this file serves for scratch ideas before comitting,
"""

def place_wall(start, end):
    """
    This function will place a wall between 2 defined points
    
    NOTE: this function only works in a straight line and for 
          map generation aspects behind the scenes
    
    the input will be 2 sets where the first number of each is the lateral
    location, and the second number is the longitudinal number 
    """
    #start example (3, 2)
    #where 3 is the row and 2 is the position in that row
    wall_positions = list()
    relation = "none"
    
    #This code segment determines if its a vertical or horizontal line
    if start[0] == end[0]:
        relation = "row"
    elif start[1] == end[1]:
        relation = "column"
    #This else determines if it isnt a straight line 
    else:
        print("The relationship is not currently supported in my code")


    #This code segment here determines if the start or end coordinate
    #has the non relation value as numerically lower or higher
    if relation == "row":
        if start[1] > end[1]:
            print(end, "is the first position")
            low = end
            high = start
        else:
            print(start, "is the first position")
            low = start
            high = end
    elif relation == "column":
        if start[0] > end[0]:
            print(end, "is the first position")
            low = end
            high = start
        if end[0] > start[0]:
            print(start, "is the first position")
            low = start
            high = end
        
    """
    #This comment is for clarity and understanding what has happened
    #start         = the numerically lower position
    #end           = the numerically higher position
    #relation      = the static coordinate being a row or column
    #low           = the lower non static coordinate
    #high          = the higher non static coordinate
    wall positions = a list of sets() containing each location 
                     inbetween start and end
    """
    
    #This next section will start from the start and increment untill
    #it equals the end, with each intermediary added to wall positions
    if relation == "row":
        for num in range(low[1], high[1] + 1):
            wall_positions.append((low[0], num))
    elif relation == "column":
        for num in range(low[0], high[0] + 1):
            wall_positions.append((num, low[1]))

    
    for position in wall_positions:
        
        basic_map[position[0]][position[1]]["accessible"] = False
        basic_map[position[0]][position[1]]["type"] = "wall"
        #print(basic_map[position[0]][position[1]])
        
    
    return relation


def draw_view():
    """
    This function will serve as a basic means to depict the world map 
    in a console print
    
    NEEDS:
        -the ability to be configured to print out a specified size
        -the ability for views to be created and centered around the PC
         ^(post chargen)
    """
    
    for row in basic_map:
        for location in row:
            if location["occupied"] == True:
                print("@ ", end = "")
            elif location["accessible"] == True:
                print(". ", end = "")
            elif location["accessible"] == False:
                print("# ", end = "")
        print()
                
    #Create a nested list out of basic map to print