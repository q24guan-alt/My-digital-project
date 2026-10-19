#import pygame
import os
import pygame as pg
#design dimensions and frame rate of artpack and document different behavor name
cell_size=100
ROW_ACTIONS=["idle","walk","attack","attack2","hurt","death"]
ROW_FRAME_COUNTS={"idle":6,"walk":8,"attack":8,"attack2":8,"hurt":4,"death":4}

class AiAnimator:
    _sheets={}

    def __init__(self,sheet_name,scale=3):
        self.sheet_name=sheet_name
        self.scale=scale
        self.current_action="idle"
        self.frame_index=0
        self.anim_timer=0
        self.facing_right=True
        self.is_attacking=False
        self.is_hurting=False
        self.is_dead=False
        self.death_done=False
        self.frames=None

    def _load(self):
        if self.sheet_name not in AiAnimator._sheets:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir,"assets/"+self.sheet_name)
            sheet = pg.image.load(path).convert_alpha()
            frames={}
            for row,action in enumerate(ROW_ACTIONS):
                count=ROW_FRAME_COUNTS[action]
                action_frames=[]
                for col in range(count):
                    cell=pg.Surface((cell_size,cell_size),pg.SRCALPHA)
                    cell.blit(sheet,(0,0),pg.Rect(col*cell_size,row*cell_size,cell_size,cell_size))
                    action_frames.append(cell)
                frames[action]=action_frames
            AiAnimator._sheets[self.sheet_name]=frames
        self.frames=AiAnimator._sheets[self.sheet_name]

    def _scaled(self,img):
        w,h=img.get_size()
        return pg.transform.scale(img,(int(w*self.scale),int(h*self.scale)))

    def trigger_attack(self):
        if not self.is_dead and not self.is_attacking:
            self.is_attacking=True
            self.current_action="attack"
            self.frame_index=0
            self.anim_timer=0

    def trigger_hurt(self):
        if not self.is_dead and not self.is_attacking:
            self.is_hurting=True
            self.current_action="hurt"
            self.frame_index=0
            self.anim_timer=0

    def trigger_death(self):
        if not self.is_dead:
            self.is_dead=True
            self.death_done=True
            self.is_attacking=False
            self.is_hurting=False
            self.current_action="death"
            self.frame_index=0
            self.anim_timer=0

    def update(self,is_moving):
        if self.frames is None:
            self._load()

        if self.is_dead:
            frames=self.frames["death"]
            self.anim_timer+=1
            if self.anim_timer>=8:
                self.anim_timer=0
                self.frame_index+=1
                if self.frame_index>=len(frames):
                    self.frame_index=len(frames)-1
                    self.death_done=True
            return

        if self.is_hurting:
            frames=self.frames["hurt"]
            self.anim_timer+=1
            if self.anim_timer>=5:
                self.anim_timer=0
                self.frame_index+=1
                if self.frame_index>=len(frames):
                    self.is_hurting=False
                    self.current_action="idle"
                    self.frame_index=0
            return

        if self.is_attacking:
            frames=self.frames["attack"]
            self.anim_timer+=1
            if self.anim_timer>=5:
                self.anim_timer=0
                self.frame_index+=1
                if self.frame_index>=len(frames):
                    self.is_attacking=False
                    self.current_action="idle"
                    self.frame_index=0
            return

        new_action="walk" if is_moving else "idle"
        if new_action!=self.current_action:
            self.current_action=new_action
            self.frame_index=0
            self.anim_timer=0
        frames=self.frames[self.current_action]
        self.anim_timer+=1
        if self.anim_timer>=8:
            self.anim_timer=0
            self.frame_index=(self.frame_index+1)%len(frames)

    def draw(self,screen,rect):
        if self.frames is None:
            self._load()
        frames= self.frames.get(self.current_action) or self.frames["idle"]
        if self.frame_index>=len(frames):
            self.frame_index=0
        img=self._scaled(frames[self.frame_index])
        if not self.facing_right:
            img=pg.transform.flip(img,True,False)
        img_rect=img.get_rect(center=rect.center)
        screen.blit(img,img_rect)

