#import code from other file
import math
import random
import pygame as pg
from player import player_movement, player_statement
from AI import AI_character
from AI.AI_animation import AiAnimator

# design enemy and read enemy data from AI character for how many enemy in the room. and choice different animation for different type enemy
class EnemyAI:
    def __init__(self, x, y, ai_type_name):
        self.ai_type_name=ai_type_name
        data = AI_character.AI_types[ai_type_name]
        self.speed = data["speed"]
        self.attack_power = data["attack"]
        self.hp_max=data["HP"]
        self.hp = self.hp_max
        self.max_attack_time = data["attack_time"]
        self.rect = pg.Rect(x, y, 20, 20)
        self.attack_time = 0
        self.patrol_dir = 0
        self.patrol_time = 0
        room_bounds = pg.Rect(20, 20, 760, 660)
        self.rect.clamp_ip(room_bounds)
        if ai_type_name == "BOSS":
            self.animator=AiAnimator("Blood Monster_A.png",scale=5)
        else:
            self.animator=AiAnimator("Demon_A.png",scale=3)
        self._prev_hp = self.hp
#Control the enemy by distance between the AI with player and random variable, paused is check did other page is open pass behavior
    def update(self,paused=False):
        dx = player_movement.player_rect.centerx - self.rect.centerx
        dy = player_movement.player_rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if paused:
            return
        if self.hp<self._prev_hp and self.hp>0:
            self.animator.trigger_hurt()
        self._prev_hp = self.hp
        if distance > 500:
            if self.patrol_time <= 0:
                self.patrol_dir = random.randint(1, 4)
                self.patrol_time = 30
            if self.patrol_dir == 1:
                self.rect.x -= self.speed
            elif self.patrol_dir == 2:
                self.rect.x += self.speed
            elif self.patrol_dir == 3:
                self.rect.y -= self.speed
            elif self.patrol_dir == 4:
                self.rect.y += self.speed
            self.patrol_time -= 1
        elif 35 < distance <= 500:
            self.patrol_time = 0
            self.rect.x += round((dx / distance) * self.speed)
            self.rect.y += round((dy / distance) * self.speed)
        elif distance <= 35:
            if self.attack_time <= 0 and player_statement.hp>0:
                self.animator.trigger_attack()
                player_statement.hp -= self.attack_power
                self.attack_time = self.max_attack_time
        is_moving=self.patrol_time>0 or (35<distance<500)
        self.animator.update(is_moving)
        if self.attack_time > 0:
            self.attack_time -= 1
#check distance between AI and blocker, and stop or attack then when AI close different blocker
        from map import map_manager
        from map import room as room_module
        current_room = map_manager._instance.current
        for col, row, ox, oy in current_room.obstacles:
            obstacle = pg.Rect(ox, oy, room_module.Tile_size, room_module.Tile_size)
            if self.rect.colliderect(obstacle):
                if self.rect.centery < obstacle.centery:
                    self.rect.right = obstacle.left
                else:
                    self.rect.left = obstacle.right
                if self.rect.centerx > obstacle.centerx:
                    self.rect.bottom = obstacle.top
                else:
                    self.rect.top = obstacle.bottom

# draw the enemy and check equipment need show the hp bar or still hide hp, and calculate by equation get place for draw AI hp bar.
    def draw(self, screen):
        self.animator.draw(screen,self.rect)
        if self.hp<self.hp_max:
            ratio=max(0,self.hp/self.hp_max)
            bar_w,bar_h=24,4
            x=self.rect.centerx-bar_w//2
            y=self.rect.top-8
            pg.draw.rect(screen,(40,40,40),(x,y,bar_w,bar_h))
            pg.draw.rect(screen,(70,220,90),(x,y,int(bar_w*ratio),bar_h))