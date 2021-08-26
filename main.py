"""
To-Do:
    
    meow
    
Primer for humans reading this code:
    
    This is my attempt for bringing to life a system of permanence 
    in a roguelike/rpg type setting, with no prior reading of similar code,
    using a functional paradigm
    
    I do understand that this goal would be best accomplished with OOP,
    but I'm not very advanced in OOP programming, and I'm looking for peer 
    review for my current practices, before I move on to finding a tutor
    or self teaching how to accomplish these same functionalities with class
    based structures
    
    I'm very open to best practice suggestions! A better and easier way to 
    accomplish a goal I'm perhaps walking circles around for lack of thought
    or experience
    
NOTE:
    
     a normal coordinates system is x, y, with x as the 'length' and y 
     as the 'height''
      
     using a nested list structure for the map is resulting in me 
     using the y coordinate first, and x coordinate second
      
     it is unnatural but I dont think its too eggregious, just takes
     a bit of getting used to 
      
     Forgive my typos :)
    
Design Note:
    
    I intend to create the systems that encompass an action loop
    (the actual functionality that moves the game state and contains
    the players choice of actions) before I create the action loop
    and state system, so I can keep the system in mind when writing the
    game state function
"""

help_string = """
loot - pick up an object off the ground
look - view an object on the ground 
north, south, east, west - direction
also usable as n, s, e, w and 
right left up down
inventory - display your inventory
quit - exit out of the game loop into dev console"""

import random
from data import item_dictionary, move_options, life_list, class_dict

direction_list = ["north", "west", "south", "east"]

basic_map = []

#These variables are set in the sample code as 10, 10 for the sake of reference
y_dim = 0
x_dim = 0

#when calling this function, pass 2 integers for map size
def map_gen(y = 10, x = 10):
    """
    purpose: generates a nested list structure of map objects
    y - the y coordinate (height)
    x - the x coordinate (width)
    """
    for value in range(x):
        #this list is essentially a container for map objects
        basic_map.append(list())

    for num in range(y):
        for num in range(y):
            basic_map[num].append({
                #accessible is essentially a collision variable
                "accessible": True,
                "type:": "ground",
                "contents": {
                             #itemName: quantity
                             },
                "occupied": False,
                "occupant": None
                        })
    return y, x


#This function returns a randomly generated coordinate that is unoccupied
def free_space():
    """
    y: map coordinate y size
    x: map coordinate x size
    
    The purpose of this function is to randomly choose
    a non occupied map square coordinate if we want to generate
    a mob or NPC
    
    returns:
        a valid set of existable coordinates (idealy)
    """
    y, x = y_dim, x_dim
    while True:
        rand_y = random.randint(0, y-1)
        rand_x = random.randint(0, x-1)
        if move_check((rand_y, rand_x)):
            coordinates = [rand_y, rand_x]
            return coordinates
        else:
            continue

#This function changes the occupation status of a location on the map
def location_state_change(coordinates, name, old_coordinates = None):
    """
    This function serves the purpose of removing the occupation 
    status of a coordinate that was once occupied, after a character
    moves to another location
    """
    
    if coordinates:
        life_list[name]["location"] = coordinates
        basic_map[coordinates[0]][coordinates[1]]["occupied"] = True
        basic_map[coordinates[0]][coordinates[1]]["occupant"] = name
    
    if old_coordinates:
        old_location = basic_map[old_coordinates[0]][old_coordinates[1]]
        old_location["occupied"] = False
        old_location["occupant"] = None


#This function serves to turn directional options into a single string
def input_parse(inputted):
    """
    This function will take input and convert it into easily usable outputs    
    """
    inputted = inputted.lower()
    if inputted in ("n", "up", "north"):
        return "north"
    elif inputted in ("e", "right", "east"):
        return "east"
    elif inputted in ("w", "left", "west"):
        return "west"
    elif inputted in ("s", "down", "south"):
        return "south"
    else:
        return None
        

#Lmao idk
def return_location(coordinates):
    """
    purpose: to make a commonly used ugly piece of code bareable
    
    coordinates: a location to be called up
    """
    return basic_map[coordinates[0]][coordinates[1]]


#This function generates a simple npc with preset stat ranges and a random location
def npc_generator(name):
    """
    name:      a string to identify a living entity by
    hp:        health points
    inventory: a list containing possessed items
    
    returns:
        nothing
    """
    name = name.lower()
    
    coordinates = free_space()
    
    hp = random.randint(25, 50)
    life_list[name] = {
                       "hp": hp,
                       "hp_current": hp,
                       "defense": 10,
                       "dexterity": random.randint(1, 6),
                       "strength": random.randint(1, 6),
                       "constitution": random.randint(1, 6),
                       "intelligence": random.randint(1, 6),
                       "charisma": random.randint(1, 6),
                       "luck": 5,
                       "attack": 1,
                       "inventory": {1: 10}, #item_dictionary ID 1: quantity 10
                       "inventory_equiped": {},
                       "weapon": None,
                       "armor": None,
                       "accessories": None,
                       "shield": None,
                       "utility": None,
                       "hostile": False,
                       "npc": True  ,
                       "location": coordinates
                       }
    location_state_change((coordinates[0], coordinates[1]), name)
    

#Barebones right now, will need more information when main_loop exists
def pc_generator(name = None, pc_class = None):
    """
    Function Needs:
        create the player character
        name, base stats, inventory,
        location 
    """
    class_list = ["fighter", "rogue", "random"]
    
    if name == None and pc_class == None:
        name = input("Enter a name for your character: ").lower()
        while True:
            pc_class = input("Enter your choice of class: Fighter, Rogue, Random\n").lower()
            if pc_class in class_list:
                break
            else:
                print("Please enter one of the options printed.")
    
    stats = class_dict[pc_class]
    
    start_location = free_space()
    
    life_list[name] = stats
    life_list[name]["inventory_equiped"] = {}
    life_list[name]["location"] = start_location
    life_list[name]["npc"] = False
    life_list[name]["inventory"] = {}
    location_state_change(start_location, name)


#Needs Writing
def npc_level_up(npc_class, name):
    """
    will take an npc object in the life_list
    and raise stats according to their class,
    with an emphasis on randomization
    """
    pass


#This function takes a living entity and returns a dict containing
#a list of the directions that can be accesed next to it 
def is_adjacent(name):
    """
    TODO:
        make the returns of isadjacent a dictionary where
        the coordinates is a value of the key "direction"
        ie.. east: [3, 2]
    
    this function will determine whether or not a square
    is adjacent to a specific entity on life_list
    if yes, this will allow the picking up of ground inventory
    from adjacent squares, and allow for the interaction with
    npcs whether friend or foe
    """
    #this sets coordinates to an entity we want to find adjacent squares of
    coordinates = life_list[name]["location"]
    
    #test print for clarity
    #print("current coordinates: " + str(coordinates))
    
    adjacent_options = { "south": [coordinates[0] + 1, coordinates[1]],
                         "north": [coordinates[0] - 1, coordinates[1]],
                         "east": [coordinates[0], coordinates[1] + 1],
                         "west": [coordinates[0], coordinates[1] - 1]}
    
    adjacent_locations = {"location_list": []}
    
    for direction in adjacent_options:
        if move_check(adjacent_options[direction], is_adjacent = False):
            adjacent_locations["location_list"].append(adjacent_options[direction])
            adjacent_locations[direction] = adjacent_options[direction]
    
    return adjacent_locations


#Needs Writing
def npc_inventory_management():
    """
    will be ran upon npc creation and provide
    randomized inventory generation based on 
    class derived needs
    """    
    pass
    

def look_ground(coordinates):
    """
    this function will run after look to call up and format the 
    inventory of a location square
    """
    contents = basic_map[coordinates[0]][coordinates[1]]["contents"]
    
    #If the ground contains an object(s)
    if contents:
        for item in contents:
            
            #this is the name of the item on the ground in the inquired direction
            print()
            print("    ", end = "")
            print(str(contents[item]) + " ", end = "")
            print(item_dictionary[int(item)]["name"])


def look(name, direction = None):
    """
    this function will be a command in the game loop
    it will allow you to observe the properties of adjacent squares
    and will lead into the ability to grab objects off the ground 
    """
    direction_options = ["north", "south", "east", "west"]
    
    if direction == None:
        while True:
            direction = input("Which direction would you like to look?\n").lower()
            direction = input_parse(direction)
            if direction not in direction_options:
                print("Please enter North East South or West.")
            else:
                break
    
    #relevant is a dictionary of all adjacent locations to "name"
    relevant = is_adjacent(name)
    
    for key in relevant:
        if key == direction:
            #relevant[key] is a list containing the coordinate of the
            #direction the player would like to look 
            look_ground(relevant[key])
            return None
            #return relevant[key]
        
    print("This square is not lookable")

    
#Needs Writing
def pc_inventory_management(name, action, direction):
    """
    will contain functionality that allows inventory
    to transfer from the ground or a trader, into the player
    inventory
    or from player inventory to the ground
    
    viable_locations: a list of coordinate values for adjacent squares
    """
    
    viable_locations = is_adjacent(name)
    if action == "loot":
        
        if direction in direction_list:
            
            try:
                location = viable_locations[direction]
                #print(location)
            except:
                print("That's not a viable direction from your current position")
                return None
            
            if return_location(location)["contents"]:
                
                #This is the relevant chars inventory dict
                inventory = life_list[name]["inventory"]
                
                #buffer copies a locations items and the next code deletes it
                buffer = basic_map[location[0]][location[1]]["contents"]
                basic_map[location[0]][location[1]]["contents"] = []
                
                #this iterates through every item present in the location
                for entry in buffer:
                    if inventory.get(entry):
                        print("this item is currently present in inventory")
                        #this will not work untill i make all inventory shit 
                        #adhere to integer form
                        inventory[entry] = int(inventory[entry]) + int(buffer[entry])
                    else:
                        inventory[entry] = buffer[entry]
    
    if action == "drop":
        pass
    
    if action == "trade":
        pass
        

def populate_ground():
    """
    this function runs once so far, mainly for testing 
    i want a 1 in 20 chance for an item to spawn
    """
    for row in basic_map:
        for location in row:
            if location["accessible"] == True:
                roll = random.choice(range(1, 20))
                if roll == 19:
                    #item equals the ID on item_dictionary
                    item = random.randint(1, 5)
                        
                    location["contents"][item] = 1
                
                    if item == 1:
                        location["contents"][1] = random.randint(1, 25)

#Needs Writing
def equip(name):
    """
    this function will take a weapon and or armor from 
    a living object's inventory and place it into their active
    use slot, which will then boost their stats by its 
    associated value
    NPC handling will be automated, with best weapon and armor available
    per equip slot
    PC handling will be manual, and will be an available command for use
    when the player is able to input an action
    """
    pass


#Needs Writing
def trading():
    """
    this functional will initially serve the purpose of transfering 
    inventory between PC and an adjacent non-hostile npc
    """
    pass


#Needs Writing
def attack_action():
    """
    this function will execute an attack from 1 living entity
    upon another
    """
    pass


#Needs Writing
def npc_ai(name):
    """
    name: the living object in reference
    
    this will take some consideration into the idea
    of code optimization, considering how many times this 
    functional will be ran
    """
    if life_list[name]["hostile"] == True:
        pass
    else:
        #friendly_ai: villagers/traders/followers/travelers
        pass


#needs fixed
def value_query(meta):
    """
    meta: metadata must be a dictionary of an item
    
    returns:
        total value in integer
    """
    #Expected meta input format: (item_id, item_quantity)
    identifyer = meta[0]
    quantity = meta[1]
    value = item_dictionary[identifyer]["value"]
    total_value = value * quantity
    return total_value


def move_check(coordinates, is_adjacent = False):
    """
    will check the desired coordinates for occupied and accessible values
    if occupied and or innaccessible, function will return False
    if not occupied AND accessible, will return True
    
    the purpose of is_adjacent being checked here is to recycle code
    a nuance for the is_adjacent use of this function is to return True
    
    
    is_adjacent: passed as True when using the is_adjacent function
    coordinates: a list containing the x and y coordinates of the player
    """
    try:
        #returns false (cant move to this location) if either coordinate is negative
        #reason: indexing a list with a negative value returns the last element
        for num in coordinates:
            if num > -1:
                pass
            else:
                return False
        
        if is_adjacent:
            return True
        
        if coordinates[0] > (y_dim -1):
            #print("Location is out of boundaries")
            return False
    
        if coordinates[1] > (x_dim -1):
            #print("Location is out of boundaries")
            return False
    
        
        #print("We are at the coordinates check section")
        #checks for 2 prerequisite variables for a square to be movable
        if basic_map[coordinates[0]][coordinates[1]]["accessible"] == False:
            #print("I am in move check and will not allow this move/check")
            return False
        elif basic_map[coordinates[0]][coordinates[1]]["occupied"] == False:
            #print("I am in move check and will successfully allow this move")
            return True
        else:
            return False
        
    except Exception as e:
        print("WE ARE AT MOVE_CHECK EXCEPT STATEMENT:")
        print(e)
        return False
    

#note: coordinates must be a list
def move_logic(direction, name):
    """
    coordinates: starting coordinates before move_logic function
    
    Explanation of purpose:
        this function serves the purpose of moving a coordinate pair to 
        a viable new location
        
        can and will be applied to the player character, npcs or mobs
    
    direction: 
    
    returns:
        a new coordinates for an entity
    """
    
    coordinates = life_list[name]["location"]
    coord_string = "New coordinates are: {}"
    bad_location = "This direction is not accessible"
    direction = direction.lower()
    
    #each "option" is a dictionary key that signifies a direction:
    #                north, east, south, west
    #the contents of each dictionary is a list of acceptable responses
    #to trigger movement in that direction, ie, "up" = "north", "n" = "north"
    
    
    for option in move_options:
        if direction in move_options[option]:
            
            #COORDINATES = THE CURRENT LOCATION OF THE CHAR IN QUESTION
            #change_presence(coordinates, new_coordinates, name)
            
            if option == "north":
                new_coordinates = (coordinates[0] - 1, coordinates[1])
                if move_check(new_coordinates):
                    location_state_change(new_coordinates, name, old_coordinates = coordinates)
                    coordinates = new_coordinates
                    print(coord_string.format(coordinates))
                    return coordinates
                else:
                    print(bad_location, "NORTH")
                    break
                    
            elif option == "east":
                new_coordinates = (coordinates[0], coordinates[1] + 1)
                if move_check(new_coordinates):
                    location_state_change(new_coordinates, name, old_coordinates = coordinates)
                    coordinates = new_coordinates
                    print(coord_string.format(coordinates))
                    return coordinates
                else:
                    print(bad_location, "EAST")
                    break
                    
            elif option == "south":
                new_coordinates = (coordinates[0] + 1, coordinates[1])
                if move_check(new_coordinates):
                    location_state_change(new_coordinates, name, old_coordinates = coordinates)
                    coordinates = new_coordinates
                    print(coord_string.format(new_coordinates))
                    return coordinates
                else:
                    print(bad_location, "SOUTH")
                    break
                
            elif option == "west":
                new_coordinates = (coordinates[0], coordinates[1] - 1)
                if move_check(new_coordinates):
                    location_state_change(new_coordinates, name, old_coordinates = coordinates)
                    coordinates = new_coordinates
                    print(coord_string.format(new_coordinates))
                    return coordinates
                else:
                    print(bad_location, "WEST")
                    break


def randomizer(y_range, x_range):
    """
    *INTENDED FOR COMMAND PROMPT USE*
    
    this function exists to generate random coordinates for
    "test_function" to test movement possibilities with
    
    y_range: the height of numbers that can be generated in the y coordinate
    x_range: the range of numbers that can be generates for the x coordinate
    
    returns: y, x
    """
    y = random.randint(0, y_range)
    x = random.randint(0, x_range)
    return y, x


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
            #print(end, "is the first position")
            low = end
            high = start
        else:
            #print(start, "is the first position")
            low = start
            high = end
    elif relation == "column":
        if start[0] > end[0]:
            #print(end, "is the first position")
            low = end
            high = start
        if end[0] > start[0]:
            #print(start, "is the first position")
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


def return_stats(name):
    """
    This function will return a formatted string containing
    the stats of the specified life_list entry
    """
    stats = life_list[name]
    
    stats_string = """
    Health Current : {}
    Health Max     : {}
    Constitution   : {}
    Defense        : {}
    Dexterity      : {}
    Intelligence   : {}
    Charisma       : {}
    Luck           : {}
    
        *Currently Equiped*
        
    Weapon         : {}
    Armor          : {}
    Accessory      : {}
    Shield         : {}
    Utility        : {}
        
    """.format(stats["hp_current"],
               stats["hp"],
               stats["constitution"],
               stats["defense"],
               stats["dexterity"],
               stats["intelligence"],
               stats["charisma"],
               stats["luck"],
               stats["weapon"],
               stats["armor"],
               stats["accessories"],
               stats["shield"],
               stats["utility"])
    
    print(stats_string)


def draw_view():
    """
    This function will serve as a basic means to depict the world map 
    in a console print
    
    NEEDS:
        -the ability to be configured to print out a specified size
        -the ability for views to be created and centered around the PC
         ^(post chargen)
    """
    
    #this is basic code for a "view" system to track the player through 
    # a large map
    
    """
    planning for new view method
    
    
    """
        
    
    
    for row in basic_map:
        for location in row:
            if location["occupied"] == True:
                print("@ ", end = "")
            elif location["contents"]:
                print(",", end = " ")
            elif location["accessible"] == True:
                print(". ", end = "")
            elif location["accessible"] == False:
                print("# ", end = "")
        print()
                
    #Create a nested list out of basic map to print


def stats_update(name):
    """
    This function will occur every single time an action occurs 
    that modifies the stats of a life_list entity
    basically it alters stats based on what is equipped or what
    actions have been taken
    """
    #So basically its gonna take a look at every slot
    #If anything is equiped, then it will add that stat onto 
    #your main stats
    pass


def game_loop(name):
    """
    This function will process the game activities and keep track of time 
    and all actions
    """
    while True:
        count = 0
        draw_view()
        
        action = input(">")
        
        
        #This checks if action is a movement action
        for direction in move_options:
            if action == "":
                break
            
            if action in move_options[direction]:
                #test print if debugging
                #print(action, direction)
                move_logic(direction, name)
                count = 1
                break
        
        if action == "equip":
            """
            This is some messy ass code
            basically my goal is to ensure that the input HAS to be 
            one of the ids in inventory, and print 
            the inventory items you have, with the id preceding it
            ie... (1) gold
                  (2) short sword
            """
            inventory = life_list[name]["inventory"]
            while True:        
                selection = input("Which item would you like to equip?"
                                  "\nType the ID of the item."
                                  "\nnote: \n if you have an item already equiped "
                                  "of the same \ntype, it will replace your previous"
                                  "item")
                try:
                    selection = int(selection)
                    for identification in inventory:
                        if selection == identification:
                            equip_item == selection
                            break
                except:
                    print("Please input a valid number")
                print("The id is out of range")
            
            
        if action == "inventory":
            #This section of code will print a formatted
            #output of the player inventory
            inventory = life_list[name]["inventory"]
            print()
            for entry in inventory:
                print("    ", end = "")
                print(inventory[entry], end = " ")
                print(item_dictionary[int(entry)]["name"])
            
            count = 1
        
        if action == "quit":
            return None
        
        if action == "look":
            look(name)
            count = 1
            
        if action == "loot":
            direction = input("which direction would you like to loot?\n>")
            for choice in move_options:
                if direction in move_options[choice]:
                    direction = input_parse(direction)
                    pc_inventory_management(name, "loot", direction)
                    count = 1
                    break
                
        if action == "help":
            print(help_string)
            count = 1
            
        if action == "stats":
            return_stats(name)
            count = 1
            
        if not count:
            print("That was not a recognized command, type help to see options")
        
        
        print()


y_dim, x_dim = map_gen(y = 10, x = 10)
    
place_wall((3, 1), (3, 5))
place_wall((6, 1), (6, 5))
place_wall((3, 1), (6, 1))
place_wall((6, 5), (5, 5))
    
populate_ground()

pc_generator(name = "ian",  pc_class = "fighter")
    
life_list["ian"]["inventory"][1] = "34"
    
basic_map[4][5]["contents"][1] = "50"
    
game_loop("ian")

