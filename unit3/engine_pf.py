from math import *
import random

# NOTE: Landmark coordinates are given in (y, x) form and NOT
# in the traditional (x, y) format!

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]]
#landmarks  = [[50.0, 0.0], [0.0, 100.0], [100.0, 100.0]]
#landmarks  = [[50.0, 0.0], [50.0, 50.0]]
#landmarks  = [[50.0, 50.0]]

# world is NOT cyclic. Robot is allowed to travel "out of bounds"
world_size = 100.0

# ------------------------------------------------
#
# this is the robot class
#

class robot:

    # --------
    # init:
    #    creates robot and initializes location/orientation
    #

    def __init__(self, length = 20.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero

    # --------
    # set:
    #    sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            print "orientation = ", new_orientation
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    # --------
    # set_noise:
    #    sets the noise parameters
    #
    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # measurement_prob
    #    computes the probability of a measurement
    #

    def measurement_prob(self, measurements):

        # calculate the correct measurement
        predicted_measurements = self.sense(0) # Our sense function took 0 as an argument to switch off noise.


        # compute errors
        error = 1.0
        for i in range(len(measurements)):
            error_bearing = abs(measurements[i] - predicted_measurements[i])
            error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate


            # update Gaussian
            error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) /
                      sqrt(2.0 * pi * (self.bearing_noise ** 2)))

        return error

    def __repr__(self): #allows us to print robot attributes.
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y),
                str(self.orientation))


    # --------
    # move:
    #

    def move(self, motion):

        turn = float(motion[0]) + random.gauss(0.0, self.steering_noise)
        if (turn < 0.0):
           turn = 0.0

        dist = float(motion[1]) + random.gauss(0.0, self.distance_noise)
        if (dist < 0.0):
            dist = 0.0

        beta = dist*tan(turn)/float(self.length)

        if (abs(beta) < 0.001):
            x = self.x + dist*cos(self.orientation)
            y = self.y + dist*sin(self.orientation)
            orientation = self.orientation + beta
            while (orientation >= 2.0*pi):
                orientation = orientation - 2.0*pi

        else:
            radius = dist/beta

            cx = self.x - radius*sin(self.orientation)
            cy = self.y + radius*cos(self.orientation)

            x = cx + radius*sin(self.orientation + beta)
            y = cy - radius*cos(self.orientation + beta)
            orientation = self.orientation + beta
            while (orientation >= 2.0*pi):
                orientation = orientation - 2.0*pi

        # set particle
        result = robot(self.length)
        result.set(x, y, orientation)
        result.set_noise(self.bearing_noise, self.steering_noise, self.distance_noise)

        return result


    # --------
    # sense:
    #

    def sense(self, add_noise = 1): #do not change the name of this function
        Z = []

        # ENTER CODE HERE
        # HINT: You will probably need to use the function atan2()

        for i in range(len(landmarks)):
            angle = atan2(landmarks[i][0] - self.y, landmarks[i][1] - self.x)
            if (angle < 0.0):
                angle += 2.0*pi
            if (angle >= self.orientation):
                bearing = angle - self.orientation
            else:
                bearing = 2.0*pi - self.orientation + angle

            if (add_noise > 0):
                bearing += random.gauss(0, self.bearing_noise)
            Z.append(bearing)

        return Z


