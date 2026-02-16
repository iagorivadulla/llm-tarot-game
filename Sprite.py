# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 16:34:49 2025

@author: Toxito
"""

import pygame



spritesheet = pygame.image.load('Sprites/sprite.png').convert_alpha()

sprite_width = 200
sprite_height = 200
sprites_per_row = 4
sprites_per_col = 3

cat_sprites = []

for row in range(sprites_per_row):
    for col in range(sprites_per_col):
        x = col * sprite_width
        y = row * sprite_height
        
        sprite = spritesheet.subsurface((x, y, sprite_width, sprite_height))
        cat_sprites.append(sprite)
        
