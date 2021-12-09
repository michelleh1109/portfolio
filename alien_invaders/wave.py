"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever 
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on 
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or 
models.py. Whether a helper method belongs in this module or models.py is 
often a complicated issue.  If you do not know, ask on Piazza and we will 
answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not 
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts 
    on screen. It animates the laser bolts, removing any aliens as necessary. 
    It also marches the aliens back and forth across the screen until they are 
    all destroyed or they reach the defense line (at which point the player 
    loses). When the wave is complete, you  should create a NEW instance of 
    Wave (in Invaders) if you want to make a new wave of aliens.
    
    If you want to pause the game, tell this controller to draw, but do not 
    update.  See subcontrollers.py from Lecture 24 for an example.  This 
    class will be similar to than one in how it interacts with the main class 
    Invaders.
    
    All of the attributes of this class ar to be hidden. You may find that 
    you want to access an attribute in class Invaders. It is okay if you do, 
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter 
    and/or setter for any attribute that you need to access in Invaders.  
    Only add the getters and setters that you need for Invaders. You can keep 
    everything else hidden.
    
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control 
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave 
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None 
    #
    # Attribute _bolts: the laser bolts currently on screen 
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected 
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step" 
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _direction: direction that aliens are currently going in. 0 for 
    # right and 1 for left.
    # Invariant: _direction can only be int of 0 or 1

    #Attribute _down: tracking whether aliens are moving down or horizontal. 
    # 0 is horitzontal. 1 is down.
    # Invariant: _down can only be int 0 or 1

    # Attribute _fire_rate: the amount of alien steps before firing an alien bolt
    # Invariant: _fire_rate: an int between 0 and BOLT_RATE

    # Attribute _steps: counts total steps taken by aliens
    # Invariant: _steps is an int greater than or equal to 0 

    # Attribute _animator: ship animator
    # Invariant: _animator is ship animator or none
    
    # Attribute _ship_collided: whether ship has collided or not
    # Invariant: _ship is boolean True or False
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setShip(self, input):
        """
        Moves ship left or right horitzontally based on input.

        Parameter input: The input from player keyboard.
        Precondition: input is a Ginput object.
        """
        dx = 0
        if input.is_key_down('left'):
           dx -= SHIP_MOVEMENT
        if input.is_key_down('right'):
           dx += SHIP_MOVEMENT
        self._ship.setX(dx)

    def setAliens(self):
        """
        Moves aliens automatically based on amount of steps that have been taken.
        """
        if self._down== 0:
            if self._direction==0:
                self.move_aliens_right()
                
                max = self.get_right_alien()
                x_max = self._aliens[max[0]][max[1]].getLeft()
                if x_max >=(GAME_WIDTH- ALIEN_WIDTH - ALIEN_H_SEP):
                    self._down=1
            else:
                self.move_aliens_left()
                min = self.get_left_alien()
                x_min = self._aliens[min[0]][min[1]].getLeft()
                if x_min <= ALIEN_H_SEP:
                    self._down=1
        else:
            self.move_aliens_down()
            if self._direction == 0:
                self._direction=1
            else:
                self._direction=0
            self._down=0
    
    def setTime(self, dt):
        """
        Counts the amount of time that has passed since last alien step.

        Parameter dt:
        Precondition dt:
        """
        self._time += dt

    def getLives(self):
        """
        Returns amount of player lives left.
        """
        return self._lives

    def getShip(self):
        """
        Returns Ship object.
        """
        return self._ship 

    def get_player_win(self):
        """
        Returns whether all aliens are destroyed (aka player won).
        """
        return self.viable_aliens()==[]
    
    def get_player_lose(self):
        """
        Returns whether aliens have crossed the defense line (aka player lost).
        """
        alien_col = self.viable_aliens()[0]
        alien_row = self.viable_aliens()[1]
        alien = self._aliens[alien_row][alien_col[0]]
        return alien.getBottom()<= DEFENSE_LINE
        
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes Wave object.
        """
        self._aliens=self.create_aliens_list()
        self._ship = Ship()
        self._dline=GPath(width=10, points=[0,110, GAME_WIDTH, 110], linecolor='black')
        self._time=0
        self._bolts=[]
        self._lives = SHIP_LIVES

        # ADDITIONAL ATTRIBUTES
        self._direction = 0
        self._down = 0
        self._fire_rate = random.randrange(1,BOLT_RATE)
        self._steps = 0
        self._animator = None
        self._ship_collided = False
        
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input):
        """
        Updates Wave object.

        Parameter input: keys that player is pressing
        Precondition: input is a Ginput object
        """
        # update ship
        if self._ship_collided==False:
            self.setShip(input)

            # player bolts
            if input.is_key_down('up') and self.rate_of_fire():
                self._bolts.append(Bolt(True, self._ship.getX(), SHIP_BOTTOM+SHIP_HEIGHT))

        # update alien steps
        if self._time>=ALIEN_SPEED:
            self.setAliens()
            self._time=0
            self._steps += 1
        else:
            self.setTime(DT)
        
        # alien bolts
        if self._fire_rate == self._steps:
            self.alien_bolt()
            self._steps = 0
            self._fire = random.randrange(1,BOLT_RATE)

        # moving and removing bolts
        self.move_bolts()
        self.track_bolts()

        # detecting collisions
        self.aliens_collide()
        if self._ship_collided == False:
            self.ship_collide(DT)
        else:
            self.run_ship_animator(DT)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws Wave object.
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)
        self._dline.draw(view)
        if self._ship != None:
            self._ship.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)
    
    # HELPERS FUNCTIONS TO CREATE LIST OF ALIENS
    def create_aliens_list(self):
        """
        HELPER FUNCTION FOR self._aliens.

        Creates 2D list of alien objects. 
        """
        aliens_list = []
        for row in reversed(range(ALIEN_ROWS)):
            alien_row = []
            for col in range(1, ALIENS_IN_ROW+1):
                if row%6==5 or row%6==0:
                    alien_row.append(Alien3(self.alien_pos_x(col), self.alien_pos_y(row)))
                elif row%6 == 4 or row%6 == 3:
                    alien_row.append(Alien1(self.alien_pos_x(col), self.alien_pos_y(row)))
                elif row%6 == 2 or row%6 == 1:
                    alien_row.append(Alien2(self.alien_pos_x(col), self.alien_pos_y(row)))
            aliens_list.insert(0, alien_row)
        return aliens_list

    def alien_pos_x(self, col_pos):
        """
        HELPER FUNCTION FOR list_aliens().

        Returns Alien x-coordinate based on its column position in self._aliens.

        Parameter col_pos: position from the top of screen
        Precondition: int that is >0 and <=number of columns
        """
        return ALIEN_H_SEP*col_pos + ALIEN_WIDTH*(col_pos-1)

    def alien_pos_y(self, row_pos):
        """
        HELPER FUNCTION FOR list_aliens().

        Returns Alien y-coordinate based on its row position in self._aliens.

        Parameter row_pos: position from the top of screen
        Precondition: int that is >0 and <=number of rows
        """
        return 700-(ALIEN_CEILING + ALIEN_V_SEP*(row_pos-1) + ALIEN_HEIGHT*(row_pos-1))

    # HELPER FUNCTION TO MOVE ALIENS
    def move_aliens_right(self):
        """
        HELPER FUNCTION FOR set_aliens().

        Moves self._aliens right.
        """
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    alien.moveRight()
    
    def move_aliens_left(self):
        """
        HELPER FUNCTION FOR set_aliens().

        Moves self._aliens left.
        """
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    alien.moveLeft()

    def move_aliens_down(self):
        """
        HELPER FUNCTION FOR set_aliens().

        Moves self._aliens down.
        """
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    alien.moveDown()

    def get_right_alien(self):
        """
        HELPER FUNCTION FOR set_aliens().

        Returns a tuple indicating the row and column position of 
        the right most alien.
        """
        right_alien = (0,0)
        for row in range(len(self._aliens)):
            for alien in range(len(self._aliens[row])):
                if self._aliens[row][alien]!=None and right_alien[1]<alien:
                    right_alien = (row, alien)
        return right_alien

    def get_left_alien(self):
        """
        HELPER FUNCTION FOR set_aliens().

        Returns a tuple indicating the row and column position of 
        the left most alien.
        """
        left_alien = (ALIEN_ROWS, ALIENS_IN_ROW)
        for row in range(len(self._aliens)):
            for alien in range(len(self._aliens[row])):
                if self._aliens[row][alien]!=None and left_alien[1]>alien:
                    left_alien = (row, alien)
        return left_alien
    
    # HELPER FUNCTIONS TO CREATE, MOVE, AND REMOVE BOLTS
    def move_bolts(self):
        """
        HELPER FUNCTION for update().

        Moves all bolts on the screen up or down.
        """
        for bolt in self._bolts:
            bolt.setY()

    def rate_of_fire(self):
        """
        HELPER FUNCTION FOR update().

        Returns False if there is already one player bolt on the screen.
        True if player can fire another bolt.
        """
        for bolt in self._bolts:
            if bolt.is_player_bolt()==True:
                return False
        return True
    
    def alien_bolt(self):
        """
        HELPER FUNCTION FOR update().

        Creates a Bolt object from a random alien in self._aliens.
        """
        aliens = self.viable_aliens()
        alien_row = aliens[1]
        aliens_list= aliens[0]

        firing_alien = random.choice(aliens_list)

        self._bolts.append(Bolt(False, self._aliens[alien_row][firing_alien].getX(), 
        self._aliens[alien_row][firing_alien].getBottom()-ALIEN_HEIGHT))
    
    def viable_aliens(self):
        """
        HELPER FUNCTION FOR alien_bolt().

        Returns a 2D list containing (1) a list of ints indexing the position of 
        alien objects in the bottom most row with at least one alien and (2) the 
        corresponding row number of the bottom most row. 

        The row number is the first row from bottom that contains at least one viable alien. 
        Viable aliens are alien objects in self._aliens (not None). The list of alien positions 
        are all the viable aliens in the specific row.
        """
        viable_list = []
        for row in reversed(range(len(self._aliens))):
            for alien in range(len(self._aliens[row])):
                if self._aliens[row][alien]!=None:
                    viable_list.append(alien)
            if viable_list != []:
                return [viable_list, row]
        return []
        
    def track_bolts(self):
        """
        HELPER FUNCTION FOR update().

        Removes bolt from self._bolts when it leaves the screen.
        """
        for bolt in self._bolts:
            if bolt.getY()>=GAME_HEIGHT or bolt.getY()<= 0:
                self._bolts.remove(bolt)
                
    # HELPER METHODS FOR COLLISION DETECTION
    def aliens_collide(self):
        """
        HELPER FUNCTION FOR update().

        Returns True if any of the aliens in self._aliens has collided with player bolt.
        If there is collision, bolt is removed from self._bolts and alien is removed 
        from self._aliens.

        Returns False otherwise.
        """
        for row in range(len(self._aliens)):
            for alien in range(len(self._aliens[row])):
                for bolt in self._bolts:
                    if self._aliens[row][alien]!=None and self._aliens[row][alien].collide(bolt):
                        self._bolts.remove(bolt)
                        self._aliens[row][alien] = None
                        return True
        return False

    def ship_collide(self, dt):
        """
        HELPER FUNCTION FOR update().

        Returns True if Ship collided with Alien Bolt. Removes bolt from self._bolts.
        False otherwise.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        for bolt in self._bolts:
            if self._ship.collide(bolt):
                self._bolts.remove(bolt)
                # animating ship explosion
                self._ship_collided = True
                self.run_ship_animator(dt)
                return True
        return False

    # HELPER FUNCTIONS TO ANIMATE SHIP
    def run_ship_animator(self, dt):
        """
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if not self._animator is None:
            try:
                self._animator.send(dt)
            except:
                self._animator = None 
                self._ship = None
                self._bolts = []
                self._lives-= 1
        elif self._ship_collided: 
            count = 0
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        count +=1
            self._animator = self._ship.animate_ship(dt, count)
            next(self._animator)

        # HELPER FUNCTION TO START NEW ROUND
    def reset(self):
        """
        Resets _ship and _ship_collided to start new roundof game.
        """
        self._ship = Ship()
        self._ship_collided = False
