import numpy as np


initial_number_sheep  = 100
sheep_gain_from_food  = 4
sheep_reproduce       = 0.04
sheep_speed           = 10

initial_number_wolves = 60
wolf_gain_from_food   = 35
wolf_reproduce        = 0.1
wolf_speed            = 20

heading_change        = np.pi / 6
grass_regrowht_time   = 30

field_size            = (1000, 1000)
field_height          = 50
field_width           = 50
cell_height           = int(field_size[0]/field_height)
cell_width            = int(field_size[1]/field_width)


animal_height         = round(cell_height*1,2)
animal_width          = round(cell_width*1.2)

# pygame params
screen_size = (field_width*cell_width, field_height*cell_height)
screen_caption = 'Wolf Sheep Predation'
fps = 30
tpf = 3
sprite_size = (50, 50)
