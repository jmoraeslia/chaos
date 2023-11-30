# importing modules

import pygame  # pygame used for creating the graphics window and handling user input.
import pandas as pd  # pandas library used for data manipulation and saving data to CSV.
from pygame.locals import *  # constants for pygame, like QUIT and DOUBLEBUF.
from OpenGL.GL import *  # OpenGL for 3D graphics rendering.
from OpenGL.GLU import *  # OpenGL Utility Library for additional functionalities.
import random  # random module for generating random numbers.
import colorsys  # colorsys for color manipulation.

class lorenz_attractor:  # define a class for the simulation.

    # define screen resolution and rotation speed constants for better organization.
    screen_width = 1920
    screen_height = 1080
    rotation_speed = 0.2  

    def __init__(self, x, y, z):  # initialize the class with initial coordinates (x, y, z).
        self.dt = 0.01  # time step. 
        self.sigma, self.rho, self.beta = 10, 28, 8/3  # constants for the lorenz equations. please, be cautious when making alterations!! it can affect the reliability of the generated systems.
        self.points = [(x, y, z)]  # list to store the simulation points (x, y, z).
        self.colors = []  # list to store colors associated with points.

    def step(self):  # function to compute the next step in the simulation.
        x, y, z = self.points[-1]  # get the last point.
        dx = self.sigma * (y - x) * self.dt  # calculate the change in x.
        dy = (x * (self.rho - z) - y) * self.dt  # calculate the change in y.
        dz = (x * y - self.beta * z) * self.dt  # calculate the change in z.
        self.points.append((x + dx, y + dy, z + dz))  # add the new point to the list.
        hue = (len(self.points) % 1000) / 1000.0  # generate a color based on the point's position.
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)  # convert the hue to an RGB color.
        self.colors.append(rgb)  # add the color to the list.

    def save_to_csv(self, filename):  # function to save the points to a CSV file.
        df = pd.DataFrame(self.points, columns=['x', 'y', 'z'])  # create a DataFrame from the points.
        df.to_csv(filename, index=False)  # save the DataFrame to a CSV file.

    def save_to_txt(self, filename):  # function to save data points to a text file for later analysis.
        with open(filename, 'w') as file:  # open the specified file in write ('w') mode, creating it if it doesn't exist.
            for point in self.points:  # iterate through each point in the self.points list.
                file.write(f'{point[0]}, {point[1]}, {point[2]}\n')  # write each point's x, y, and z coordinates to the file, followed by a newline.

def draw_lorenz(lorenz):  # function to draw the model in the OpenGL window.

    point_size = 2.0 # set the point size. you can change it here.

    glPointSize(point_size) # set the point size for drawing. 
    glBegin(GL_POINTS)  # start drawing points.
   
    for point, color in zip(lorenz.points, lorenz.colors): # this iterate through the data points and their corresponding colors;
        glColor3fv(color)  # set the color for the current data point.
        glVertex3fv(point)  # draw the current data point in 3D space.
    glEnd()  # finish drawing and close the point rendering.

def main_viewer(x, y, z):  # function for non-interactive visualization of the model.
    display = (lorenz_attractor.screen_width, lorenz_attractor.screen_height)  # display resolution. (you can change the values of this parameters too).
    pygame.init()  # initialize the pygame library.
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # create a pygame window with OpenGL support.
    gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)  # set the perspective for 3D rendering.
    glTranslatef(1, 1, -100)  # position the camera. 

    lorenz = lorenz_attractor(x, y, z)  # create a lorenz attractor object.

    while True:  # main simulation loop.
        for event in pygame.event.get():  # check for user events.
            if event.type == pygame.QUIT:  # if the user closes the window.
                pygame.quit()  # quit pygame.
                quit()  # exit the program.

        lorenz.step()  # compute the next step in the simulation.

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen.
        glRotatef(1, 2, 3, 1)  # rotate the view slightly.
        draw_lorenz(lorenz)  # draw the lorenz attractor.
        pygame.display.flip()  # update the display.
        pygame.time.wait(20)  # add a delay to control the simulation speed.
        lorenz.save_to_txt('lorenz_points.txt')  # save the points to a text file.

def main_interactive(x, y, z):  # function for interactive visualization of the model.
    display = (lorenz_attractor.screen_width, lorenz_attractor.screen_height)  # display resolution.
    pygame.init()  # initialize the pygame library.
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # create a pygame window with OpenGL support.
    gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)  # set the perspective for 3D rendering.
    glTranslatef(1, 1, -100)  # position the camera.

    lorenz = lorenz_attractor(x, y, z)  # create a Lorenz Attractor object.

    # for camera control:
    rotation_speed = lorenz_attractor.rotation_speed  # sets the rotation speed of the object in response to mouse movement.
    mouse_pressed = False  # nouse button not pressed: initializes a flag indicating whether the mouse button is pressed or not.
    prev_mouse_pos = None  # Previous mouse position: Initializes a variable to track the previous position of the mouse cursor.

    while True:  # main simulation loop.
        for event in pygame.event.get():  # check for user events.
            if event.type == pygame.QUIT:  # if the user closes the window.
                pygame.quit()  # quit pygame.
                quit()  # exit the program.
            elif event.type == pygame.MOUSEBUTTONDOWN: # if a mouse button was pressed...
                if event.button == 1: # check if the left mouse button (button 1) was pressed.
                    mouse_pressed = True # set the flag to indicate that the mouse button is pressed.
                    prev_mouse_pos = pygame.mouse.get_pos()  # record the current mouse cursor position.

            elif event.type == pygame.MOUSEBUTTONUP:  # if a mouse button was released...
                if event.button == 1: # if the left mouse button (button 1) was released...
                    mouse_pressed = False # set the flag to indicate this.

        if mouse_pressed:  # handle mouse interaction.
            current_mouse_pos = pygame.mouse.get_pos()  # get the current mouse position.

            if prev_mouse_pos:  # check if there is a previous mouse position.
                dx, dy = current_mouse_pos[0] - prev_mouse_pos[0], current_mouse_pos[1] - prev_mouse_pos[1]  # calculate changes in 'x' and 'y' mouse coordinates.
                # the glRotatef() is used to apply rotation transformations to a 3D scene or object.
                glRotatef(dx * rotation_speed, 0, 1, 0)  # based on horizontal mouse movement.
                glRotatef(dy * rotation_speed, 1, 0, 0)  # based on vertical mouse movement.

            prev_mouse_pos = current_mouse_pos  # update the previous mouse position to the current position.

        lorenz.step()  # compute the next step in the simulation.

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen.
        draw_lorenz(lorenz)  # draw the lorenz attractor.
        pygame.display.flip()  # update the display.
        pygame.time.wait(20)  # add a delay to control the simulation speed.

if __name__ == "__main__":
    x = float(input("type the first x value: "))  # get the initial x-coordinate.
    y = float(input("type the first y value: "))  # get the initial y-coordinate.
    z = float(input("type the first z value: "))  # get the initial z-coordinate.

    choice = input("type 'v' for just visualize the simulation or 'i' in order to interact: ").strip().lower()  # choose mode. the ".strip().lower()" methods are used to process the string received from the user in order to prevent errors.
    if choice == "v":
        main_viewer(x, y, z)  # start non-interactive visualization.
    elif choice == "i":
        main_interactive(x, y, z)  # start interactive visualization.
    else:
        print("exiting...")  # if an invalid choice is made, print a message and exit the program.

