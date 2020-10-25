import pygame as pg
from random import uniform
from random import randint
import globalvariables


class Boid(pg.sprite.Sprite):

    perception = 50
    crowding = 40
    avoiding = 40

    # image = pg.Surface((50, 50), pg.SRCALPHA)
    image = pg.Surface((perception*2, perception*2), pg.SRCALPHA)
    pg.draw.circle(image, pg.Color('white'), (perception, perception), 5)
    # pg.draw.polygon(image,pg.Color('white'), [(35, 25), (, 2), (0, 8)])
    # pg.draw.circle(image, pg.Color('white'), (perception, perception), perception, 1)


    # image2 = pg.Surface((perception*2, perception*2), pg.SRCALPHA)
    # pg.draw.circle(image2, pg.Color('red'), (perception, perception), 5)
    # pg.draw.circle(image2, pg.Color('red'), (perception, perception), perception, 1)
    max_x = 0
    max_y = 0
    # CONFIG
    speed = 1.2
    # min_speed = 1.2
    # max_speed = 1.2

    ############################################################
    ###   best forces values for weighting factors = 1     ##### 
    max_force = .04 
    separation_max_force = .3

    ############################################################
    ###   best forces values for dynamic weighting factors ##### 
    # max_force = .03 
    # separation_max_force = .03   

    ############################################################
    ###   best forces values for fixed weighting factors   #####
    # max_force = .02 
    # separation_max_force = .05   

    ############################################################

    def __init__(self, ld):
        super(Boid,self).__init__()
        if Boid.max_x == 0:
            info = pg.display.Info()
            Boid.max_x = info.current_w
            Boid.max_y= info.current_h

        self.leader = ld

        if self.leader ==1:
            self.connected = 1
        else: 
            self.connected = 0
        self.image = Boid.image.copy()
        self.rect = self.image.get_rect()

        self.pos = pg.math.Vector2(
            uniform(30, Boid.max_x/4),
            uniform(30, Boid.max_y/4))
        self.rect = self.image.get_rect(center=self.pos)

        while True:
            self.vel = pg.math.Vector2(
                uniform(-1, 1) * Boid.speed,
                uniform(-1, 1) * Boid.speed)
            if self.vel.magnitude() != 0:
                break

        self.accel = pg.math.Vector2()


 
#############################################################################################
###   Reynolds rules + custom rule (avoid) with no weighting factors (all factors = 1)   ####

    def separation(self, boids):
        v = pg.Vector2()
        if boids:
            for boid in boids:
                dist = self.pos.distance_to(boid.pos)
                if dist < self.crowding:
                    vn = pg.Vector2(boid.pos - self.pos)
                    vn.normalize()
                    vn = vn*dist
                    v -= vn
            v = self.separation_force(v)
        return v


    def alignment(self, boids):
        v = pg.Vector2()
        if boids:
            for boid in boids:
                v += boid.vel
            v /= len(boids)
            v = self.clamp_force(v)
        return v


    def avoid(self, obs):
        v = pg.Vector2()
        if obs:
            for ob in obs:
                dist = self.pos.distance_to(ob.pos)
                if dist < self.avoiding:
                    vn = pg.Vector2(ob.pos - self.pos)
                    vn.normalize()
                    vn = vn*dist
                    v -= vn
            v = self.separation_force(v)
        return v

    def cohesion(self, boids):
        v = pg.Vector2()
        if boids:
            for boid in boids:
                v += boid.pos
            v /= len(boids)
            v -= self.pos
            v = self.clamp_force(v)
        return v
##################################################################################
    def migration(self):
        steering = pg.Vector2()
        weight = 1
        if globalvariables.click == 1:
            if globalvariables.target:
                steering = pg.Vector2(globalvariables.target[0].pos - self.pos)
                # if self.pos.distance_to(globalvariables.target[0].pos)< self.perception:
                #     globalvariables.target.pop(0)
                #     if len(globalvariables.target)==0:
                #         globalvariables.click = 0
                steering = self.clamp_force(steering)
                return steering*weight
            else:
                return steering
        else:
            return steering

    def checktarget(self,obs):
        for ob in obs:
            if self.pos.distance_to(ob.pos)< 5:
                return True
        if self.pos.distance_to(globalvariables.target[0].pos)< self.perception:
            return True
        else:
            return False

    def update(self, boids, obs):
        # update velocity
        neighbors = self.get_neighbors(boids)
        obs_neighbors = self.get_obs_neighbors(obs)

        separation = pg.Vector2()
        alignment = pg.Vector2()
        cohesion = pg.Vector2()
        avoid = pg.Vector2()
        migration = pg.Vector2()

        avoid = self.avoid(obs_neighbors)
        separation = self.separation(neighbors)
        alignment = self.alignment(neighbors)
        cohesion = self.cohesion(neighbors)
        migration = self.migration()
        self.accel = separation + avoid + alignment + cohesion + migration

        # move and turn
        self.pos += self.vel
        self.wrap()
        _, angle = self.vel.as_polar()
        self.vel += self.accel
        
        # enforce speed limit
        # while self.vel.magnitude() < self.min_speed:
        #     _, angle = self.vel.as_polar()
        #     self.vel.from_polar((self.min_speed * 1.1, angle))
        # if self.vel.magnitude() > self.max_speed:
        #     self.vel.scale_to_length(self.max_speed)
        if self.vel.magnitude() ==0:
            self.vel.from_polar((self.speed, angle))
        else:
            self.vel.scale_to_length(self.speed)
        # print(self.vel.magnitude())
        
        # make boid
        if self.leader ==0:
            self.image = pg.transform.rotate(Boid.image, -angle)
            self.rect = self.image.get_rect(center=self.pos)
        else:
            self.image = pg.transform.rotate(Boid.image2, -angle)
            self.rect = self.image.get_rect(center=self.pos)

    def wrap(self):
        if self.pos.x < 0:
            self.pos.x += Boid.max_x

        elif self.pos.x > Boid.max_x:
            self.pos.x -= Boid.max_x

        if self.pos.y < 0:
            self.pos.y += Boid.max_y

        elif self.pos.y > Boid.max_y:
            self.pos.y -= Boid.max_y

    def get_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid != self:
                dist = self.pos - boid.pos
                if dist.magnitude() < self.perception:
                    neighbors.append(boid)
        return neighbors

    def get_obs_neighbors(self, obs):
        obs_neighbors = []
        for ob in obs:
            if ob != self:
                dist = self.pos - ob.pos
                if dist.magnitude() < self.perception:
                    obs_neighbors.append(ob)
        return obs_neighbors

    def clamp_force(self, force):
        if force.magnitude() > self.speed:
            force = force.normalize() * self.speed
        force -= self.vel
        if force.magnitude() > self.max_force:
            force = force.normalize() * self.max_force
        return force

    def separation_force(self, force):
        if force.magnitude() > self.speed:
            force = force.normalize() * self.speed
        force -= self.vel
        if force.magnitude() > self.separation_max_force:
            force = force.normalize() * self.separation_max_force
        return force
