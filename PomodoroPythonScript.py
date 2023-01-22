import random
import tkinter as tk
from tkinter import *
import time
import math
import os

# from pynput.keyboard import Key, Controller

# create tkinter instance
root = tk.Tk()

# transparent colour
TRANS_COLOR = '#abcdef'

# make the window transparent and without window border
root.overrideredirect(1)
root.wm_attributes('-transparentcolor', TRANS_COLOR)

# find the display resolution
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")

# creating flower windows and canvas
flower_root = tk.Toplevel()

flower_root.overrideredirect(1)
flower_root.wm_attributes('-transparentcolor', TRANS_COLOR)

flower_root.geometry(f"{screen_width}x{screen_height}")

flower_canvas = Canvas(flower_root, bg=TRANS_COLOR, highlightthickness=0)
flower_canvas.pack(fill=BOTH, expand=1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
flower1_DIR = os.path.join(IMAGE_DIR, 'flower1.png')
flower2_DIR = os.path.join(IMAGE_DIR, 'flower2.png')
flower3_DIR = os.path.join(IMAGE_DIR, 'flower3.png')
flower4_DIR = os.path.join(IMAGE_DIR, 'flower4.png')
flower5_DIR = os.path.join(IMAGE_DIR, 'flower5.png')


# load in flower images
flower1 = PhotoImage(file=f'{flower5_DIR}')
flower2 = PhotoImage(file=f'{flower5_DIR}')
flower3 = PhotoImage(file=f'{flower5_DIR}')
flower4 = PhotoImage(file=f'{flower5_DIR}')
flower5 = PhotoImage(file=f'{flower5_DIR}')
flower = [flower1, flower2, flower3, flower4, flower5]


bee_DIR = os.path.join(IMAGE_DIR, 'bee.png')
bee_canvas = Canvas(root, bg=TRANS_COLOR, highlightthickness=0)
bee_canvas.pack(fill=BOTH, expand=1)
bee = PhotoImage(file=f'{bee_DIR}')
animal_on_canvas = bee_canvas.create_image(-100, -100, image=bee, anchor=N + W)

# timer canvas

time_root = tk.Toplevel()

time_root.overrideredirect(1)
time_root.wm_attributes('-transparentcolor', TRANS_COLOR)

time_root.geometry(f"{screen_width}x{screen_height}")

time_canvas = Canvas(time_root, bg=TRANS_COLOR, highlightthickness=0)
time_canvas.pack(fill=BOTH, expand=1)
seconds_time = 1
minutes_time = 25
def tick(counter):

    list_of_times = [5, 25, 5, 25, 5, 25, 30]

    time_canvas.delete(ALL)

    global seconds_time
    global minutes_time
    seconds_time -= 1

    time_canvas.create_text(230, 22, fill='purple', text=minutes_time, font=('Helvetica', '40', 'bold'))
    time_canvas.create_text(265, 18, fill='purple', text=':', font=('Helvetica', '40', 'bold'))
    time_canvas.create_text(300, 22, fill='purple', text=seconds_time, font=('Helvetica', '40', 'bold'))

    if minutes_time < 0:
        if counter > len(list_of_times)-1:
            minutes_time = list_of_times[counter]
            counter = 0
        else:
            minutes_time = list_of_times[counter]
            counter += 1

    if seconds_time == 0:
        minutes_time -= 1
        seconds_time = 60

    root.after(1000, tick, counter)


tick(0)


# frequency of bees path
frequency = 0.0298252467

# create flower positions on display (width, height)
flower1_pos = (140, 400)
flower2_pos = (300, 270)
flower3_pos = (600, 680)
flower4_pos = (750, 430)
flower5_pos = (1050, 180)
flower6_pos = (1200, 500)

# create bee to flower movement data structure to
# be accessed when random flowers are spawned
flower_pos_list = [flower1_pos, flower2_pos, flower3_pos, flower4_pos, flower5_pos, flower6_pos]

# all flowers that the bee will have flying actions between
# the flowers will act like edges of a graph where the bee
# makes vectors between


bee_start = (-100, -100)

bee_movements = [[(240, 0.019), (400, 0.0045), (700, 0.0032), (850, 0.0022), (1100, 0.000001), (1285, 0.001)],
                 [(120, -0.13), (400, 0.005), (600, -0.0001), (860, 0.0013), (1015, 0.0000001)],
                 [(-180, 0.006), (300, 0.004), (420, 0.003), (750, -0.003), (880, 0.0006)],
                 [(-500, -0.0095), (-330, -0.028), (130, -0.135), (430, -0.0115), (570, -0.005)],
                 [(-640, -0.0008), (-475, -0.007), (-190, 0.021), (255, -0.026), (410, 0.001)],
                 [(-925, -0.0003), (-780, -0.001), (-490, 0.004), (-330, -0.003), (120, -0.003)],
                 [(-1080, -0.00055), (-940, -0.0026), (-640, 0.0015), (-490, -0.006), (-190, -0.042)]]


def left(e):
    x = -20
    y = 0
    bee_canvas.move(animal_on_canvas, x, y)


def right(e):
    x = 20
    y = 0
    bee_canvas.move(animal_on_canvas, x, y)


def up(e):
    x = 0
    y = -20
    bee_canvas.move(animal_on_canvas, x, y)


def down(e):
    x = 0
    y = 20
    bee_canvas.move(animal_on_canvas, x, y)


# Define a function to allow the image to move within the canvas
def move(e):
    global bee
    bee = PhotoImage(file='C:/Users/mrktr/OneDrive - University of Glasgow/Code/DesktopAnimal/bee.png')
    animal_on_canvas = bee_canvas.create_image(e.x, e.y, image=bee)

# to implement a stable pause button, when time is pressed the pomodoro timer will
# pause and then once pressed again the timer will start again.
def time_pause(event):
    return minutes_time, seconds_time

def end_root(event):
    return root.destroy()


def move_during_event(image_to_move, x, y):
    bee_canvas.move(image_to_move, x, y)
    root.update()
    time.sleep(0.01)


def fly_path(place_to_go, place_from, image_to_move=animal_on_canvas, bee_movements=bee_movements):
    def move(to_move, gradient):
        previous_w_pixel = 0
        if to_move >= 0:
            for i in range(to_move):
                w_pixel = 10 * (math.sin(frequency * i)) + (i * gradient)

                w_pixel = w_pixel - previous_w_pixel
                previous_w_pixel = w_pixel

                move_during_event(image_to_move, 1, w_pixel)

        else:
            for i in range(-1 * to_move):
                w_pixel = 10 * (math.sin(frequency * i)) + (i * gradient)

                w_pixel = w_pixel - previous_w_pixel
                previous_w_pixel = w_pixel

                move_during_event(image_to_move, -1, w_pixel)

    if type(place_from) == list:
        place_from = place_from[0]
        to_move = bee_movements[place_from][place_to_go][0]
        gradient = bee_movements[place_from][place_to_go][1]
        print(bee_movements[place_from][place_to_go], "in here")
        move(to_move, gradient)
        return
    else:
        pass
    bee_movements2 = [[(120, -0.13), (400, 0.005), (600, -0.0001), (860, 0.0013), (1015, 0.0000001)],
                      [(-180, 0.006), (300, 0.004), (420, 0.003), (750, -0.003), (880, 0.0006)],
                      [(-500, -0.0095), (-330, -0.028), (130, -0.135), (430, -0.0115), (570, -0.005)],
                      [(-640, -0.0008), (-475, -0.007), (-190, 0.021), (255, -0.026), (410, 0.001)],
                      [(-925, -0.0003), (-780, -0.001), (-490, 0.004), (-330, -0.003), (120, -0.003)],
                      [(-1080, -0.00055), (-940, -0.0026), (-640, 0.0015), (-490, -0.006), (-190, -0.042)]]
    if place_from < place_to_go:
        place_to_go -= 1

        print(bee_movements2[place_from][place_to_go])
        to_move = bee_movements2[place_from][place_to_go][0]
        gradient = bee_movements2[place_from][place_to_go][1]
        move(to_move, gradient)
        return
    else:
        print(bee_movements2[place_from][place_to_go])
        to_move = bee_movements2[place_from][place_to_go][0]
        gradient = bee_movements2[place_from][place_to_go][1]
        move(to_move, gradient)
        return


used_index = []


def create_random_pos(used_index=used_index):
    randomint = random.randint(0, 5)
    if randomint in used_index:
        return create_random_pos(used_index)
    else:
        used_index.append(randomint)
        return randomint

def spawn_crazy_flowers(flowers_to_spawn = 10, flower_canvas = flower_canvas):
    flower_spawns = [(190, 660), (658, 230), (430, 100), (330, 820), (900, 750),
                     (780, 150), (560, 470), (1300, 760), (1100, 690), (930, 485),
                     (780, 830)]

    def random_flower_spawn():
        random_flower = random.randint(0, 4)

        flower_canvas.create_image(flower_spawns[10 - flowers_to_spawn][0], flower_spawns[10 - flowers_to_spawn][1], image=flower[random_flower])

        if flowers_to_spawn > 0:
            return root.after(500, spawn_crazy_flowers, flowers_to_spawn - 1)
        else:
            return

    random_flower_spawn()



def spawn_flower(previous_index=[0], flower_canvas=flower_canvas, used_index=used_index):

    random_flower = random.randint(0, 4)
    random_flower2 = random.randint(0, 4)

    random_flower_pos = create_random_pos(used_index)
    random_flower_pos2 = create_random_pos(used_index)

    flower_canvas.create_image(flower_pos_list[random_flower_pos][0], flower_pos_list[random_flower_pos][1],
                               image=flower[random_flower])
    flower_canvas.create_image(flower_pos_list[random_flower_pos2][0], flower_pos_list[random_flower_pos2][1],
                               image=flower[random_flower2])

    if len(used_index) < 6:
        fly_to_index = used_index[-2]
        fly_path(fly_to_index, previous_index)
        previous_index = fly_to_index

        return root.after(1000*60*30, spawn_flower, previous_index)
    elif len(used_index) >= 6:
        fly_to_index = used_index[-2]
        fly_path(fly_to_index, previous_index)
        return root.after(1000*60*115, spawn_crazy_flowers)
    else:
        return

root.after(1000*60*25, spawn_flower)

previous_w_pixel = 0

# Bind the move function
bee_canvas.bind("<B1-Motion>", move)
# Bind bee right click
time_canvas.bind('<Button-3>', end_root)

root.mainloop()
