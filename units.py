import config

import random
import numpy as np
import pygame
from functools import reduce


class Animal():
    def __init__(self, reproduce_rate, init_energy, speed, sprite_path):
        super().__init__()
        self.x = random.uniform(0, config.field_size[0])
        self.y = random.uniform(0, config.field_size[1])
        self.heading = random.uniform(0, 2*np.pi)
        self.reproduce_rate = reproduce_rate
        self.energy = random.randint(1, 2*init_energy)
        self.speed = speed
        self.image = pygame.transform.scale(
            pygame.image.load(sprite_path), (config.animal_width, config.animal_height)
        ).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.energy -= 1
        self.move()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.heading += random.uniform(-config.heading_change, config.heading_change)
        self.x += np.cos(self.heading) * self.speed
        self.y += np.sin(self.heading) * self.speed

        if not ((0 < self.x < config.field_size[0]) and ((0 < self.y < config.field_size[1]))):
            self.x = np.clip(self.x, 0, config.field_width*config.cell_width-1e-9)
            self.y = np.clip(self.y, 0, config.field_height*config.cell_height-1e-9)
            self.heading += np.pi
    
    @property
    def pose(self):
        return self.x // config.cell_width, self.y // config.cell_height

    
    @classmethod
    def _make_child(cls):
        return cls()

    def reproduce(self) -> 'Animal':
        e = max(1, self.energy/2)
        self.energy -= e
        new_x = np.clip(self.x + np.cos(self.heading) * 1, 0, config.field_width*config.cell_width-1e-9)
        new_y = np.clip(self.y + np.sin(self.heading) * 1, 0, config.field_width*config.cell_width-1e-9)
        child = self._make_child()
        child.x = self.x
        child.y = self.y
        child.energy = e
        child.rect = child.image.get_rect(center=(child.x, child.y))
        return child
    

class Sheep(Animal):
    def __init__(self):
        super().__init__(
            config.sheep_reproduce, 
            config.sheep_gain_from_food, 
            config.sheep_speed, 
            'assets/green_sheep.png'
        )

class Wolf(Animal):
    def __init__(self):
        super().__init__(
            config.wolf_reproduce, 
            config.wolf_gain_from_food, 
            config.sheep_speed, 
            'assets/red_wolf.png'
        )


class Cell():
    def __init__(self, x, y):
        super().__init__()
        self.timer = np.random.randint(-config.grass_regrowht_time, config.grass_regrowht_time)
        self.sprites = {
            'grass': 'assets/grass.png',
            'dirt': 'assets/dirt.png',
        }
        sprite_path = self.sprites['grass' if self.timer <= 0 else 'dirt']
        self.image = pygame.transform.scale(
            pygame.image.load(sprite_path), (config.cell_width, config.cell_width)
            ).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.timer -= 1
        sprite_path = self.sprites['grass' if self.timer <= 0 else 'dirt']
        self.image = pygame.transform.scale(
            pygame.image.load(sprite_path), (config.cell_width, config.cell_width)
            ).convert_alpha()
    
    def eat(self):
        self.timer = 30

    def is_grass(self):
        return self.timer <= 0
    
    def is_dirt(self):
        return self.timer > 0


def make_field() -> dict[tuple[int], Cell]:
    field = dict()
    for x in range(config.field_width):
        for y in range(config.field_height):
            cell_x = config.cell_width // 2 + x * (config.cell_width)
            cell_y = config.cell_height // 2 + y * (config.cell_height)
            field[(x, y)] = Cell(cell_x, cell_y)
    return field


class Supervizor:
    def __init__(self, sheeps_cnt, wolfs_cnt):
        self.sheeps = [Sheep() for _ in range(sheeps_cnt)]
        self.wolfs = [Wolf() for _ in range(wolfs_cnt)]
        self.field = make_field()
        self.stack = []
    
    def update(self):
        new_sheeps = dict()
        for s in self.sheeps:
            s.update()
            if self.field[s.pose].is_grass():
                s.energy += config.sheep_gain_from_food
                self.field[s.pose].eat()
            if s.energy > 0:
                new_sheeps[s.pose] = new_sheeps.get(s.pose, []) + [s]
            if random.uniform(0, 1) < (s.reproduce_rate):
                child = s.reproduce()
                new_sheeps[child.pose] = new_sheeps.get(child.pose, []) + [child]
        ...
        for cell in self.field.values():
            cell.update()

        new_wolfs = []
        for w in self.wolfs:
            w.update()
            if w.energy < 0:
                continue
            if new_sheeps.get(w.pose, []):
                new_sheeps[w.pose].pop()
                w.energy += config.wolf_gain_from_food
            if random.uniform(0, 1) < (w.reproduce_rate):
                new_wolfs.append(w.reproduce())
            if w.energy > 0:
                new_wolfs.append(w)
        
        self.wolfs = new_wolfs
        if new_sheeps.values():
            self.sheeps = reduce(lambda a,b: a+b, new_sheeps.values())
        else:
            self.sheeps = []
    
    def draw(self, window):
        # print(f'sum energy: {sum([w.energy for w in self.wolfs])}')#debug
        for s in (list(self.field.values())+self.sheeps+self.wolfs):
            s.draw(window)
        ...
        # self.stack.append([list(self.field.values()), self.sheeps, self.wolfs])
        # if len(self.stack) > 5:
        #     self.stack.pop(0)
    
    @property
    def sheeps_cnt(self):
        return len(self.sheeps)
    
    @property
    def wolves_cnt(self):
        return len(self.wolfs)
    
    @property
    def grass_cnt(self):
        return sum(c.is_grass() for c in self.field.values())
    