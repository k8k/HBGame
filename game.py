import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % len(player.inventory))
        if len(player.inventory) > 4:
            player.change_image("Cat")
            GAME_BOARD.draw_msg("You are now a CAT! Meow")

class Rock(GameElement):
   
    IMAGE = "Rock"
    SOLID = True

    def interact(self, player):

        if player.IMAGE == "Bug":
            self.SOLID = False
            GAME_BOARD.base_board[self.y][self.x] = "Block"
            GAME_BOARD.draw_game_map()

            player.rock_inventory.append(self)
            if len(player.rock_inventory) > 11:
                # Create a key
                akey = Key()
                GAME_BOARD.register(akey)
                GAME_BOARD.set_el(4,4,akey)

                # Create a door
                door = Door()
                # Set the key that opens this door
                door.key = akey

                GAME_BOARD.register(door)
                GAME_BOARD.set_el(5,0, door)
                player.change_image("Princess")
                # bad_guy = BadGuy()
                # GAME_BOARD.register(bad_guy)
                # GAME_BOARD.set_el(1,5, bad_guy)
                GAME_BOARD.draw_msg("Now you're a princess again! Take the key and open the door")


        else:
            self.SOLID = True



class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
    key = None

    def interact(self, player):

        if self.key in player.inventory:
            self.change_image("DoorOpen")
            GAME_BOARD.draw_msg("Congratulations! You cut down the forest. You progress to level 2.")
            GAME_BOARD.del_el(player.x, player.y)
            
            GAME_BOARD.draw_board()
            GAME_BOARD.set_el(0,7,player)


            for i in range(8):
                GAME_BOARD.base_board[0][i] = "WaterBlock"
                GAME_BOARD.base_board[1][i] = "WaterBlock"
                GAME_BOARD.base_board[2][i] = "WaterBlock"
                GAME_BOARD.base_board[3][i] = "WoodBlock"
                GAME_BOARD.base_board[4][i] = "WoodBlock"
                GAME_BOARD.base_board[5][i] = "WoodBlock"
                GAME_BOARD.base_board[6][i] = "WoodBlock"
                GAME_BOARD.base_board[7][i] = "WoodBlock"

            wall_positions = [
                (0,3),
                (1,3),
                (3,3),
                (4,3),
                (6,3),
                (7,3),
                ]

            walls = []

            for pos in wall_positions:
                wall = Walls()
                GAME_BOARD.register(wall)
                GAME_BOARD.set_el(pos[0], pos[1], wall)
                walls.append(wall)

            window1 = Window()
            GAME_BOARD.register(window1)
            GAME_BOARD.set_el(2,3,window1)

            window2 = Window()
            GAME_BOARD.register(window2)
            GAME_BOARD.set_el(5,3, window2)

            shrub = HousePlant()
            GAME_BOARD.register(shrub)
            GAME_BOARD.set_el(7,6,shrub)

            

            GAME_BOARD.draw_game_map()
            



class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = True
    def interact(self, player):
        if player.IMAGE == "Princess":
            GAME_BOARD.draw_msg("Hey. If you eat all the gems you can turn into a cat! I hear they are good at cutting down trees.")
        elif player.IMAGE == "Cat":
            GAME_BOARD.draw_msg("Cut down all the trees and see what happens!")
        elif player.IMAGE == "Bug":
            GAME_BOARD.draw_msg("Help us get rid of all the ugly grass!")


class Key(GameElement):
    IMAGE = "Key"  

    def interact(self,player):
        player.inventory.append(self)




class Heart(GameElement):
    IMAGE = "Heart"

    def interact(self, player):
        player.heart_inventory.append(self)
        if len(player.heart_inventory) >= 1:
            player.change_image("Bug")
            GAME_BOARD.draw_msg("You are now a BUG!")


class HousePlant(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class Window(GameElement):
    IMAGE = "Window"
    SOLID = True

class Walls(GameElement):
    IMAGE = "StoneBlock"
    SOLID = True

class Tree(GameElement):
    IMAGE = "TallTree"


    def interact(self, player):

        if player.IMAGE == "Cat":
            self.SOLID = False
            GAME_BOARD.base_board[self.y][self.x] = "Block"
            GAME_BOARD.draw_game_map()

            player.tree_inventory.append(self)
            if len(player.tree_inventory) > 7:
                heart = Heart()
                GAME_BOARD.register(heart)
                GAME_BOARD.set_el(5,6,heart)
                
        else:
            self.SOLID = True


class BadGuy(GameElement):
    IMAGE = "Horns"
    direction = 1
    SOLID = True

    def update(self, dt):

        next_x = self.x + self.direction

        if next_x < 0 or next_x >= self.board.width:
            self.direction *= -1
            next_x = self.x

        self.board.del_el(self.x, self.y)
        self.board.set_el(next_x, self.y, self)

    def interact(self, player):
        pass




class Character(GameElement):
    IMAGE = "Princess"

   

    def next_pos(self, direction):
        if direction == "up":
            return(self.x, self.y-1)
        elif direction == "down":
            return(self.x, self.y+1)
        elif direction == "left":
            return(self.x-1, self.y)
        elif direction == "right":
            return(self.x+1, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):
        direction = None
        
        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.LEFT:
            direction = "left"
        elif symbol == key.RIGHT:
            direction = "right"

        if direction:
            if 0 <= self.next_pos(direction)[0] <= GAME_WIDTH-1 and 0 <= self.next_pos(direction)[1] <= GAME_HEIGHT-1:

                next_location = self.next_pos(direction)

                if next_location:
            
                    next_x = next_location[0]
                    next_y = next_location[1]

                    existing_el = self.board.get_el(next_x, next_y)

                    if existing_el:
                        existing_el.interact(self)

                    if existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(next_x, next_y, self)

            else:
                next_location = (self.x, self.y)
                #self.board.draw_msg("You've reached the edge of the board! Go a different way!")

            if self.IMAGE == "Bug":
                GAME_BOARD.base_board[self.y][self.x] = "Block"
                GAME_BOARD.draw_game_map()
        

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        self.tree_inventory = []
        self.heart_inventory =[]
        self.rock_inventory =[]
        self.key_inventory = []




####   End class definitions    ####

def initialize():
    """Put game initialization code here"""


    rock_positions = [
        (1,1),
        (1,6),
        (2,2),
        (5,6),
        (6,2),
        (1,2),
        (1,3),
        (6,6),
        (2,3),
        (1,6),
        (2,6),
        (3,6),
        (2,5),
        (3,5),

    ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)



    boy = Boy()
    GAME_BOARD.register(boy)
    GAME_BOARD.set_el(3,4,boy)

    heart = Heart()
    GAME_BOARD.register(heart)


    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(3,3,player)

    GAME_BOARD.draw_msg("Can you chop down the trees? Welcome to our deforestation game.")

    
    gem_positions = [
        (0,3),
        (1,5),
        (2,1),
        (4,0),
        (5,5),
        ]

    gems = []

    for pos in gem_positions:
        gem = Gem()
        gemcolors = ["BlueGem", "OrangeGem", "GreenGem"]
        gem.IMAGE = random.choice(gemcolors)
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)
        gems.append(gem)


    tree_positions = [
        (0,0),
        (1,4),
        (4,6),
        (5,3),
        (6,1),
        (3,1),
        (4,1),
        (5,1),
        ]

    trees = []

    for pos in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        trees.append(tree)

 
    # bad_guy = BadGuy()
    # GAME_BOARD.register(bad_guy)
    # GAME_BOARD.set_el(1,5, bad_guy)

