"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything 
that you interact with on the screen is model: the ship, the laser bolts, and 
the aliens.

Just because something is a model does not mean there has to be a special 
class for it. Unless you need something special for your extra gameplay 
features, Ship and Aliens could just be an instance of GImage that you move 
across the screen. You only need a new class when you add extra features to 
an object. So technically Bolt, which has a velocity, is really the only model 
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is 
because there are a lot of constants in consts.py for initializing the 
objects, and you might want to add a custom initializer.  With that said, 
feel free to keep the pass underneath the class definitions if you do not want 
to do that.

You are free to add even more models to this module.  You may wish to do this 
when you add new features to your game, such as power-ups.  If you are unsure 
about whether to make a new class or not, please ask on Piazza.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other 
# than consts.py.  If you need extra information from Gameplay, then it should 
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships 
    dimensions. These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a 
    ship just means changing the x attribute (which you can do directly), 
    you want to prevent the player from moving the ship offscreen.  This 
    is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We 
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide 
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.  
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to 
    keep this straight is for this class to have its own collision method.
    
    However, there is no need for any more attributes other than those 
    inherited by GImage. You would only add attributes if you needed them 
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    
    # Attribute _animating: whether coroutine is animating or not
    # Invariant: _animating is boolean True or False

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setX(self, new_x):
        """
        Sets new x-coordinate for ship.

        Parameter new_x: new x coordinate
        Precondition: new_x is an int 
        """
        assert isinstance(new_x, int)
        if new_x>0:
            x_coor = min(self.x + new_x, GAME_WIDTH-22)
            self.x= x_coor
        else:
            x_coor = max(self.x + new_x, 22)
            self.x= x_coor
    
    def getX(self):
        """
        Returns x-coordinate of ship.
        """
        return self.x
    
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Initializes ship Gsprite object. 
        """
        super().__init__(x=GAME_WIDTH/2, bottom=SHIP_BOTTOM, height= SHIP_HEIGHT, 
        width=SHIP_WIDTH, source='ship-strip.png', format=(2,4))
        self._animating = True
    
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collide(self, bolt):
        """
        Checks for collision between ship and alien bolt. Returns true is there is 
        collision. False otherwise.

        Parameter bolt: the bolt to check if ship is colliding with
        Invariant: bolt is a Bolt() object
        """
        if bolt.is_player_bolt():
            return False
        if self.contains([bolt.left, bolt.top]):
            return True
        elif self.contains([bolt.right, bolt.top]):
            return True
        elif self.contains([bolt.right, bolt.bottom]):
            return True
        elif self.contains([bolt.left, bolt.bottom]):
            return True
        return False
    
    # COROUTINE METHOD TO ANIMATE THE SHIP
    def animate_ship(self, dt, count):
        """
        Coroutine to animate ship explosion.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # frames per second
        current_time = 0
        frame_rate = DEATH_SPEED/count
        while self._animating:
            # Get the current time
            dt = (yield) 
            current_time += dt
            amount = current_time/frame_rate
            self.frame = round(amount)
            # If we go to far, stop animating
            if self.frame > 7:
                self._animating = False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien 
    dimensions. These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We 
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide 
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.  
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to 
    keep this straight is for this class to have its own collision method.
    
    However, there is no need for any more attributes other than those 
    inherited by GImage. You would only add attributes if you needed them 
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLeft(self):
        """
        Returns x-coordinate of left edge of Alien.
        """
        return self.left

    def getX(self):
        """
        Returns x-coordinate of Alien.
        """
        return self.x

    def getBottom(self):
        """
        Returns y-coordinate of bottom edge of Alien.
        """
        return self.bottom

    def moveLeft(self):
        """
        Moves Alien left by ALIEN_H_WALK pixels.
        """
        self.left=self.left-ALIEN_H_WALK

    def moveRight(self):
        """
        Moves Alien right by ALIEN_H_WALK pixels.
        """
        self.left=self.left+ALIEN_H_WALK

    def moveDown(self):
        """
        Moves Alien down by ALIEN_V_WALK pixels.
        """
        self.top = self.top-ALIEN_V_WALK

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, new_x, new_y): # left and top edge
        """
        Initializes Alien object.

        Parameter new_x: the x value to set current position to
        Precondition: new_x is an int or float and less than GAME_WIDTH

        Parameter new_y: the y value to set current position to
        Precondition: new_y is an int or float and less than GAME_HEIGHT
        """  
        assert isinstance(new_x, int) or isinstance(new_x, float)
        assert isinstance(new_y, int) or isinstance(new_y, float)
        assert new_x<=800 and new_y<=700  

        super().__init__(width=ALIEN_WIDTH, height=ALIEN_HEIGHT, left=new_x, top=new_y, source='')
         
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collide(self, bolt):
        """
        Checks for collision between Alien and player bolt. Returns true is there is 
        collision. False otherwise.

        Parameter bolt: the bolt to check if ship is colliding with
        Precondition: bolt is a Bolt() object
        """
        if not bolt.is_player_bolt():
            return False
        if self.contains([bolt.left, bolt.top]):
            return True
        elif self.contains([bolt.right, bolt.top]):
            return True
        elif self.contains([bolt.right, bolt.bottom]):
            return True
        elif self.contains([bolt.left, bolt.bottom]):
            return True
        return False
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

# SUBCLASSES FOR DIFFERENT ALIEN TYPES   if self._direction==0:
class Alien1(Alien):
    """
    Subclass of Alien from 'alien1.png'
    """
    def __init__(self, new_x, new_y):
        super().__init__(new_x, new_y)
        self.source = 'alien1.png'

class Alien2(Alien):
    """
    Subclass of Alien from 'alien2.png'
    """
    def __init__(self, new_x, new_y):
        super().__init__(new_x, new_y)
        self.source='alien2.png'

class Alien3(Alien):
    """
    Subclass of Alien from 'alien3.png'
    """
    def __init__(self, new_x, new_y):
        super().__init__(new_x, new_y)
        self.source='alien3.png'

class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles. The size of the bolt 
    is determined by constants in consts.py. We MUST subclass GRectangle, 
    because we need to add an extra (hidden) attribute for the velocity of 
    the bolt.
    
    The class Wave will need to look at these attributes, so you will need 
    getters for them.  However, it is possible to write this assignment with 
    no setters for the velocities.  That is because the velocity is fixed and 
    cannot change once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set 
    the starting velocity. This __init__ method will need to call the __init__ 
    from GRectangle as a  helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the 
    bolt by adding the velocity to the y-position.  However, the getter 
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction 
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setY(self):
        """
        Moves Bolt up or down by its velocity.
        """
        self.y += self._velocity
    
    def getY(self):
        """
        Returns Bolt y-coordinate.
        """
        return self.y
    
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, direction, ship_x, ship_y):
        """
        Initalizes bolt object. 

        Parameter direction: Whether bolt is going up (player bolt) or down 
        (alien bolt).  True for player bolt and False for alien bolt.
        Precondition: direction must be boolean True or False. 

        Parameter ship_x: x-coordinate of Ship()
        Precondition: Must be an int or float the is between SHIP_WIDTH/2 and 
        GAME_WIDITH-SHIP_WIDTH/2

        Parameter ship_y: the y-coordinate of the top of the ship.
        Precondition: Must be an int or a float that is between SHIP_HEIGHT and
        GAME_HEIGHT
        """
        super().__init__(x=ship_x, y=ship_y, width=BOLT_WIDTH, 
        height=BOLT_HEIGHT, fillcolor='orange', linecolor='orange')
        if direction == True:
            self._velocity = BOLT_SPEED
        else:
            self._velocity = -BOLT_SPEED
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def is_player_bolt(self):
        """
        Returns whether bolt is player bolt. True for player bolt 
        and False otherwise.
        """
        return self._velocity>0

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE