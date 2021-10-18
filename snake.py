from tkinter import Tk, Canvas
import random

class Field:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.SEG_SIZE = 20

f = Field(800, 600)

IN_GAME = True


class Rabbit:
    
    def new_weight(self):
        weight = random.randint(1,9)
        return weight

    def create_rabbit(self):
        """ Creates an apple to be eaten """
        global BLOCK
        posx = f.SEG_SIZE * random.randint(1, (f.WIDTH-f.SEG_SIZE) / f.SEG_SIZE)
        posy = f.SEG_SIZE * random.randint(1, (f.HEIGHT-f.SEG_SIZE) / f.SEG_SIZE)
        BLOCK = c.create_oval(posx, posy,
                            posx+f.SEG_SIZE, posy+f.SEG_SIZE,
                            fill="red")


def main():
    """ Handles game process """
    global IN_GAME
    if IN_GAME:  
        # sc.create_score()
        # set_state(sc.text, 'normal')
        s.move()
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Check for collision with gamefield edges
        if x2 > f.WIDTH or x1 < 0 or y1 < 0 or y2 > f.HEIGHT:
            IN_GAME = False
        # Eating rabbits
        elif head_coords == c.coords(BLOCK):
            # set_state(sc.text, 'hidden')
            weight = r1.new_weight()
            # sc.update_score(weight)
            # set_state(sc.text, 'normal')
            for i in range(weight):
                s.add_segment()

            c.delete(BLOCK)
            r1.create_rabbit()
            # set_state(sc.text, 'hidden')
        # Self-eating
        else:
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False

        root.after(100, main)
    # Not IN_GAME -> stop game and print message
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')
        

class Segment(object):
    """ Single snake segment """
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x+f.SEG_SIZE, y+f.SEG_SIZE,
                                           fill="white")


class Snake(object):
    """ Simple Snake class """
    score = 0
    
    def __init__(self, segments):
        self.segments = segments
        # possible moves
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # initial movement direction
        self.vector = self.mapping["Right"]

    def move(self):
        """ Moves the snake with the specified vector"""
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*f.SEG_SIZE, y1+self.vector[1]*f.SEG_SIZE,
                 x2+self.vector[0]*f.SEG_SIZE, y2+self.vector[1]*f.SEG_SIZE)

    def add_segment(self):
        """ Adds segment to the snake """
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - f.SEG_SIZE
        y = last_seg[3] - f.SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        """ Changes direction of snake """
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)

    def update_score(self, plus_score):
        self.score+=plus_score

def set_state(item, state):
    c.itemconfigure(item, state=state)


def clicked(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    start_game()

r1 = Rabbit()

def start_game():
    global s
    r1.create_rabbit()
    s = create_snake()
    # Reaction on keypress
    c.bind("<KeyPress>", s.change_direction)
    main()


def create_snake():
    # creating segments and snake
    segments = [Segment(f.SEG_SIZE, f.SEG_SIZE),
                Segment(f.SEG_SIZE*2, f.SEG_SIZE),
                 ]
    return Snake(segments)


# Setting up window
root = Tk()
root.title("PythonicWay Snake")


c = Canvas(root, width=f.WIDTH, height=f.HEIGHT, bg="#003300")
c.grid()
# catch keypressing
c.focus_set()

# class Score_text: 
    
#     def create_score(self):
#         self.score = 0
#         self.text = c.create_text(f.WIDTH/2, f.HEIGHT/17, text=f"Score:{self.score}",
#                                 font='Arial 20', fill='red',
#                                 state='hidden')
    
#     def update_score(self, plus):
#         self.score = self.score+plus
#         print(self.score)

# sc = Score_text()


game_over_text = c.create_text(f.WIDTH/2, f.HEIGHT/2, text="GAME OVER!",
                               font='Arial 20', fill='red',
                               state='hidden')
restart_text = c.create_text(f.WIDTH/2, f.HEIGHT-f.HEIGHT/3,
                             font='Arial 30',
                             fill='white',
                             text="Click here to restart",
                             state='hidden')
c.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
root.mainloop()