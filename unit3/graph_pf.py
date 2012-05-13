
# How to use it :
#   1)  Copy and save this file
#   2) Copy your code in homework 3-6 and save it as engine_pf.py in the same directory
#   3) Execute this file

from Tkinter import *
from engine_pf import *

# some global params

bearing_noise = 0.1
steering_noise = 0.1
distance_noise = 5.0

class ParticleFilterLogic(Tk):

    def __init__(self, motions, measurements, actual_robot, N = 500):

        Tk.__init__(self)
        self.title( 'Particle Filter Visualization')
        self.motions = motions
        self.measurements = measurements
        self.actual_robot = actual_robot
        self.N = N

        # init particle filter
        self.initFilter()

        # init renderer
        self.margin = 100       # margin
        self.zoom_factor = 3    # zoom factor

        self.can = ParticleFilterRenderer(self.margin, self.zoom_factor)
        self.can.configure(bg = 'ivory', bd = 2, relief = SUNKEN)
        self.can.pack(side = TOP, padx = 5, pady = 5)
        self.can.draw_all(self.actual_robot[self.actualState], self.p)

        # buttons
        self.button1 = Button(self, text = 'Reset', command = self.resetFilter)
        self.button1.pack(side = LEFT, padx = 5, pady = 5)
        self.button2 = Button(self, text = 'Next step', command = self.nextStep)
        self.button2.pack(side = LEFT, padx = 5, pady = 5)

        # label
        textLabel = 'Current state = ' + str(self.actualState) + '/' + str(len(motions)-1)
        self.label = Label(self, text = textLabel)
        self.label.pack(side = BOTTOM, padx = 5, pady = 5)

    def resetFilter(self):
        self.initFilter()

        # draw initial configuration
        self.can.draw_all(self.actual_robot[self.actualState], self.p)

    def initFilter(self):

        # create particles
        self.p = []
        for i in range(self.N):
            r = robot()
            r.set_noise(bearing_noise, steering_noise, distance_noise)

            # uncomment next line if initial robot position is known
            #r.set(actual_robot[0][0], actual_robot[0][1], actual_robot[0][2])

            self.p.append(r)

        self.actualState = 0

    def nextStep (self, event = None):
        self.actualState = self.actualState + 1
        if self.actualState < len(self.motions):

            # label
            stateString = 'Actual state = ' + str(self.actualState) + '/' + str(len(motions)-1)
            self.label.configure(text = stateString)

            #
            # particle filter algorithm
            #

            # motion update (prediction)
            p2 = []
            for i in range(self.N):
                p2.append(self.p[i].move(self.motions[self.actualState]))

            self.p = p2

            # measurement update
            w = []
            for i in range(self.N):
                w.append(self.p[i].measurement_prob(self.measurements[self.actualState]))

            # resampling
            p3 = []
            index = int(random.random() * self.N)
            beta = 0.0
            mw = max(w)
            for i in range(self.N):
                beta += random.random() * 2.0 * mw
                while beta > w[index]:
                    beta -= w[index]
                    index = (index + 1) % self.N
                p3.append(self.p[index])
            self.p = p3

            # render new state
            self.can.draw_all(self.actual_robot[self.actualState], self.p)

class ParticleFilterRenderer(Canvas):

    def __init__(self, margin, zoom_factor):
        Canvas.__init__(self)
        #self.p = p
        self.margin = margin
        self.zoom_factor = zoom_factor
        self.larg = (2*margin + world_size) * zoom_factor
        self.haut = self.larg
        self.configure(width=self.larg, height=self.haut)
        self.larg, self.haut = (2*margin + world_size) * zoom_factor, (2*margin + world_size) * zoom_factor

        # landmarks
        self.landmarks_radius = 2
        self.landmarks_color = 'green'

        # particles
        self.particle_radius = 1
        self.particle_color = 'red'

        # actual robot position
        self.actual_robot_radius = 3
        self.actual_robot_color = 'yellow'

        # predicted robot position
        self.predicted_robot_radius = 4
        self.predicted_robot_color = 'blue'

    def draw_all(self, actual_robot, p):
        self.configure(bg = 'ivory', bd = 2, relief = SUNKEN)
        self.delete(ALL)

        self.p = p
        self.predicted_robot = get_position(self.p)

        self.plot_particles()
        self.plot_landmarks(landmarks, self.landmarks_radius, self.landmarks_color)
        self.plot_robot(self.predicted_robot, self.predicted_robot_radius, self.predicted_robot_color)
        self.plot_robot(actual_robot, self.actual_robot_radius, self.actual_robot_color)

    def plot_landmarks(self, lms, radius, l_color):
        for lm in lms:
            x0 = (self.margin + lm[1] - radius) * self.zoom_factor
            y0 = (self.margin + lm[0] - radius) * self.zoom_factor
            x1 = (self.margin + lm[1] + radius) * self.zoom_factor
            y1 = (self.margin + lm[0] + radius) * self.zoom_factor
            self.create_oval( x0, y0, x1, y1, fill = l_color )

    def plot_particles(self):
        for particle in self.p:
            self.draw_particle(particle, self.particle_radius, self.particle_color)

    def draw_particle(self, particle, radius, p_color):
        x2 = (self.margin + particle.x) * self.zoom_factor
        y2 = (self.margin + particle.y) * self.zoom_factor
        x3 = (self.margin + particle.x + 2*radius*cos(particle.orientation)) * self.zoom_factor
        y3 = (self.margin + particle.y + 2*radius*sin(particle.orientation)) * self.zoom_factor
        self.create_line( x2, y2, x3, y3, fill = p_color, width
                = self.zoom_factor, arrow = LAST, arrowshape =
                (2*self.zoom_factor, 3*self.zoom_factor, 1*self.zoom_factor))

    def plot_robot(self, robot, radius, r_color):
        x0 = (self.margin + robot[0] - radius) * self.zoom_factor
        y0 = (self.margin + robot[1] - radius) * self.zoom_factor
        x1 = (self.margin + robot[0] + radius) * self.zoom_factor
        y1 = (self.margin + robot[1] + radius) * self.zoom_factor
        self.create_oval(x0, y0, x1, y1, fill = r_color)

        x2 = (self.margin + robot[0]) * self.zoom_factor
        y2 = (self.margin + robot[1]) * self.zoom_factor
        x3 = (self.margin + robot[0] + 2*radius*cos(robot[2])) * self.zoom_factor
        y3 = (self.margin + robot[1] + 2*radius*sin(robot[2])) * self.zoom_factor
        self.create_line(x2, y2, x3, y3, fill = r_color, width = self.zoom_factor, arrow = LAST)

#
# global functions
#

def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi))
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]

def generate_ground_truth(motions):

    myrobot = robot()
    myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

    Z = []
    X = []
    T = len(motions)

    for t in range(T):
        myrobot = myrobot.move(motions[t])
        Z.append(myrobot.sense())
        X.append([myrobot.x, myrobot.y, myrobot.orientation])
    return [Z, X]

#
# main section
#

if __name__ == "__main__":

    # actual track and measurements
    motions = [[2. * pi / 20, 12.] for row in range(20)]

    x = generate_ground_truth(motions)

    measurements = x[0]
    actual_robot = x[1]

    # display window
    wind = ParticleFilterLogic(motions, measurements, actual_robot, 500)
    wind.mainloop()

