import config
import units

import pygame
import numpy as np
from matplotlib import pyplot as plt


pygame.init()
window = pygame.display.set_mode(config.screen_size)
clock = pygame.time.Clock()

game = units.Supervizor(
    sheeps_cnt=config.initial_number_sheep,
    wolfs_cnt=config.initial_number_wolves
)

run = True
frames = config.tpf
log_sheeps  = []
log_wolves  = []
log_grasses = []
max_v = 10
# fig, (ax_w, ax_s, ax_g) = plt.subplots(3)
while run:
    clock.tick(config.fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if frames == config.tpf:
        game.update()
        frames = 0
        log_sheeps.append(game.sheeps_cnt)
        log_wolves.append(game.wolves_cnt)
        log_grasses.append(game.grass_cnt/4)
        max_v = max(log_sheeps[-1]+10, log_grasses[-1]+10, log_wolves[-1]+10, max_v)
        
        # ax_s.clear()
        # ax_w.clear()
        # ax_g.clear()

        # ax_s.plot(log_sheeps, color='green')
        # ax_w.plot(log_wolves, color='red')
        # ax_g.plot(log_grasses, color='brown')
        plt.plot(log_sheeps, color='green')
        plt.plot(log_wolves, color='red')
        plt.plot(log_grasses, color='brown')
        plt.gca().legend(['sheep', 'wolves', 'grass/4'], loc='upper left')
        plt.ylim(bottom=0, top=max_v)
        plt.show(block=False)
        plt.pause(0.0001)

    window.fill(0)
    game.draw(window)
    pygame.display.flip()
    frames += 1

pygame.quit()
exit()