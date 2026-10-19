import os
import pygame as pg

class PlayerAnimator:
    def __init__(self):
        self.current_action = "idle"
        self.frame_index = 0
        self.anim_timer = 0
        self.facing_right = True
        self.is_attacking = False
        self.is_dead=False
        self.death_done=False
        self.animations = None

    def init_frames(self):
        if self.animations is None:
            self.animations = self._load_animations()

    def _load_animations(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "assets", "players blue x1.png")

        if not os.path.exists(img_path):

            return {}

        try:
            sheet = pg.image.load(img_path).convert_alpha()

        except Exception as e:

            return {}



        def crop(x, y,w=16,h=16):

            frame = pg.Surface((w, h), pg.SRCALPHA)
            frame.blit(sheet, (0, 0), pg.Rect(x, y, w, h))
            return pg.transform.scale(frame, (w*3, h*3))
        return {
            "idle": [
                crop(10, 16)
            ],
            "run": [
                crop(8, 108,16,20),
                crop(40, 108,16,20),
                crop(72, 108,16,20),
                crop(104, 108,16,20)

            ],
            "shoot": [
                crop(10,144),
                crop(42,144),
                crop(74,144),
                crop(106,144)
            ],
            "death": [
                crop(5,175,20,18),
                crop(37,175,21,22),
                crop(68,170,23,23)
            ]
        }

    def trigger_attack(self):
        if not self.is_attacking and not self.is_dead:
            self.is_attacking = True
            self.current_action = "shoot"
            self.frame_index = 0
            self.anim_timer = 0

    def trigger_death(self):
        if not self.is_dead:
            self.is_dead = True
            self.death_done = False
            self.is_attacking = False
            self.current_action="death"
            self.frame_index = 0
            self.anim_timer = 0

    def update(self, is_moving, facing_right):
        self.init_frames()
        self.facing_right = facing_right

        if self.is_dead:
            frames = self.animations.get("death", [])
            if not frames:
                self.death_done = True
                return
            self.anim_timer += 1
            if self.anim_timer >= 6:
                self.anim_timer = 0
                self.frame_index +=1
                if self.frame_index >= len(frames):
                    self.frame_index=len(frames)-1
                    self.death_done = True
            return

        if self.is_attacking:
            frames = self.animations.get("shoot", [])
            if not frames:
                self.is_attacking = False
                self.current_action = "idle"
                return
            self.anim_timer += 1
            if self.anim_timer >= 6:
                self.anim_timer = 0
                self.frame_index += 1
                if self.frame_index >= len(frames):
                    self.is_attacking = False
                    self.current_action = "idle"
                    self.frame_index = 0
            return

        new_action = "run" if is_moving else "idle"

        if new_action != self.current_action:
            self.current_action = new_action
            self.frame_index = 0
            self.anim_timer = 0

        frames = self.animations.get(self.current_action, [])
        if not frames:
            return

        self.anim_timer += 1
        if self.anim_timer >= 8:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

    def draw(self, screen, rect):
        self.init_frames()


        frames = self.animations.get(self.current_action, [])
        if not frames:
            return

        if self.frame_index >= len(frames):
            self.frame_index = 0

        img = frames[self.frame_index]

        if not self.facing_right:
            img = pg.transform.flip(img, True, False)

        img_rect = img.get_rect(midbottom=(rect.centerx, rect.centery+24))
        screen.blit(img, img_rect)

animator = PlayerAnimator()







