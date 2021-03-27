import numpy as np


class Robot:

    def __init__(self, position, ID, robot_type=0):

        assert isinstance(position, np.ndarray) == True

        self._type = robot_type  # Type will be an integer
        self._position = position  # X-Y position
        self._ID = ID

        # added by max
        self._path_of_node_integers = []

        # Initialise values
        self._medical_payload = 0  # Set initial payloads to 0
        self._life_payload = 0
        self._is_full = False

        # For each type of robot define capabilities

        # Basic type
        if self._type == 0:
            self._capacity = 10  # Payload capacity
            self._speed = 1  # Speed
            self._fuelcap = 100  # Fuel capacity
            self._fuel = self._fuelcap  # Set initial fuel as a full tank
            self._weight = 10

        elif self._type == 1:
            self._capacity = 10  # Payload capacity
            self._speed = 1  # Speed
            self._fuelcap = 100  # Fuel capacity
            self._fuel = self._fuelcap  # Set initial fuel as a full tank
            self._weight = 10

        else:
            raise Exception("Invalid robot type given")

        # Set up the fuel drain rate, the same for all types as we assume engines are the same
        # self._drainrate = self.get_drainrate()

    # def node_move(self, start_node, end_node):
    #     self._position = end_node.position      """Need to check that this is what Marcin has done!"""

    def move(self, start_position, end_position):
        self._position = end_position
        # Could also return a distance here because why not
        return np.linalg.norm(end_position - start_position)

    def use_fuel(self, start_node, end_node):
        distance = np.linalg.norm(end_node.position - start_node.position)
        drain_rate = self.get_drainrate()
        self._fuel -= drain_rate * distance
        # Could do some stuff here with negative fuel, but leave it for now as its too complex

    def get_drainrate(self):
        """ Need to change these coefficients so that it makes sense"""
        a = 1
        b = 1
        c = 1
        return a * (self._medical_payload + self._life_payload) + b * self._speed + c * self._weight

    def add_unit_life(self):
        """ Should be adding these one at a time, so don't need to pass anything?"""
        if self._is_full:
            print("Robot at full capacity")
            return False  # Returning False here so that the super code could figure out a failure?
        else:
            self._life_payload += 1
            if (self._life_payload + self._medical_payload) == self._capacity:
                self._is_full = True
            return True

    def add_unit_medical(self):
        if self._is_full:
            print("Robot at full capacity")
            return False  # Returning False here so that the super code could figure out a failure?
        else:
            self._medical_payload += 1
            if (self._life_payload + self._medical_payload) == self._capacity:
                self._is_full = True
            return True

    @property
    def is_full(self):
        return self._is_full

    @property
    def type(self):
        return self._type

    @property
    def position(self):
        return self._position

    @property
    def capacity(self):
        return self._capacity

    @property
    def speed(self):
        return self._speed

    @property
    def fuel(self):
        return self._fuel

    @property
    def fuel_capacity(self):
        return self._fuelcap

    @property
    def medical_payload(self):
        return self._medical_payload

    @property
    def life_payload(self):
        return self._life_payload

    @property
    def payload(self):
        return self._life_payload + self._medical_payload

    @property
    def weight(self):
        return self._weight

    @property
    def ID(self):
        return self._ID

    @property
    def path_of_node_integers(self):
        return self._path_of_node_integers
