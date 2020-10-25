import sys
from boid import Boid
from obstacle import Obstacle
import pygame as pg
from random import randint
from random import uniform
import globalvariables
from targetpoint import Targetpoint
import averagedistance
import time

def obs_gen(obs):
    for i in range(int(3*700/4),700,5):
        obs.append(Obstacle([1200,i]))
    for i in range(int(3*1200/4),1200,5):
        obs.append(Obstacle([i,700]))

    for m in range(0,8):
        w = randint(200,950)
        h = randint(200,450)
        print(w,h)

        for k in range(0,25,3):
            obs.append(Obstacle([w+k,h-k]))
            obs.append(Obstacle([w+k,h+k]))
        for k in range(25,50,3):
            obs.append(Obstacle([w+k,h-k+50]))
            obs.append(Obstacle([w+k,h+k-50]))
        # for i in [h,h+100]:
        #     for j in range(w,w+100,5):
        #         obs.append(Obstacle([j,i]))
        # for i in [w,w+100]:
        #     for j in range(h,h+100,5):
        #         obs.append(Obstacle([i,j]))


# def obs_gen(obs):
#     a = [(360,259), (509, 190),(550, 330),(250, 235),(744, 200),(317, 446),(719, 410),(300, 370)]
#     for i in range(int(3*700/4),700,5):
#         obs.append(Obstacle([1200,i]))
#     for i in range(int(3*1200/4),1200,5):
#         obs.append(Obstacle([i,700]))

#     for m in a:
#         for k in range(0,25,3):
#             obs.append(Obstacle([m[0]+k,m[1]-k]))
#             obs.append(Obstacle([m[0]+k,m[1]+k]))
#         for k in range(25,50,3):
#             obs.append(Obstacle([m[0]+k,m[1]-k+50]))
#             obs.append(Obstacle([m[0]+k,m[1]+k-50]))



    # for i in [randint(100,200),randint(300,400),randint(500,600)]:
    #     for j in range(randint(200,300),randint(500,600),5):
    #         obs.append(Obstacle([j,i]))
    #     for j in range(randint(600,700),randint(900,1000),5):
    #         obs.append(Obstacle([j,i]))
    # for i in [randint(200,300),randint(500,600),randint(600,700),randint(900,1000)]:
    #     for j in range(int(1.5*height/4),int(1.70*height/4),5):
    #         obs.append(Obstacle([i,j]))
    #     for j in range(int(2.30*height/4),int(2.5*height/4),5):
    #         obs.append(Obstacle([i,j]))

    # for i in [int(1.5*height/4),int(1.70*height/4),int(2.30*height/4),int(2.5*height/4)]:
    #     for j in range(int(1.5*width/4),int(2.5*width/4),5):
    #         obs.append(Obstacle([j,i]))
    # for i in [int(1.5*width/4),int(1.5*width/4+2),int(2.5*width/4),int(2.5*width/4+2)]:
    #     for j in range(int(1.5*height/4),int(1.70*height/4),5):
    #         obs.append(Obstacle([i,j]))
    #     for j in range(int(2.30*height/4),int(2.5*height/4),5):
    #         obs.append(Obstacle([i,j]))


def main():
    pg.init()
    pg.display.set_caption("Swarm")
    # CONFIG
    width = 1200
    height = 700

    clock = pg.time.Clock()
    num_boids = 10

    screen = pg.display.set_mode((width, height))
    background = pg.Surface(screen.get_size()).convert()
    background.fill(pg.Color('black'))
    running = True
    #pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

    all_sprites = pg.sprite.RenderUpdates()
    obs_sprites = pg.sprite.RenderUpdates()

    boids = [Boid(i) for i in range(num_boids)]
    obs = []
    globalvariables.target.append(Targetpoint((width-50,height-50)))
    
    '''obstacles'''


    # for i in range(0, int(height/4),5):
    #     obs.append(Obstacle([0,i]))
    # for i in range(int(3*height/4),height,5):
    #     obs.append(Obstacle([width,i]))
    # for i in range(0, int(width/4),5):
    #     obs.append(Obstacle([i,0]))
    # for i in range(int(3*width/4),width,5):
    #     obs.append(Obstacle([i,height]))

    if len(sys.argv)>1:
        obs_gen(obs)

    for boid in boids:
        all_sprites.add(boid)
    for ob in obs:
        obs_sprites.add(ob)
    ###################################################################################
    fail_count = 0
    frame_count = 0
    averdist = 0
    filewriter = open('scenario3_no_ob.csv', 'a')
    if len(sys.argv)>1:
        filewriter.close()
        filewriter = open('scenario3.csv', 'a')
        vel_breakdown_filewriter = open('scenario3_breakdown.csv', 'a')
    b0 = boids[5] # for logging
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                globalvariables.point = pg.math.Vector2(pos[0], pos[1])
                globalvariables.target.append(Targetpoint(pos))
                globalvariables.click = 1  
            if pg.mouse.get_pressed()[2]:
                pos = pg.mouse.get_pos()
                obs.append(Obstacle(pos))
                obs_sprites.add(Obstacle(pos))
            if event.type == pg.KEYDOWN and  event.key == pg.K_UP:
                boids.append(Boid(0))
                all_sprites.add(boids[len(boids)-1])
            if event.type == pg.KEYDOWN and  event.key == pg.K_DOWN:
                boid = boids.pop(len(boids)-1)
                all_sprites.remove(boid)   
        #############################################################
        
        for b in boids:
            if b.checktarget() == True:
                boids.remove(b)
                all_sprites.remove(b)
            elif  b.checkcolision_ob(obs) == True:
                boids.remove(b)
                all_sprites.remove(b)
                fail_count += 1
            elif frame_count>=50 and b.checkcolision_neigh(boids) == True:
                boids.remove(b)
                all_sprites.remove(b)
                fail_count += 1
                for b1 in boids:
                    if b1.checkcolision_neigh([b]) == True:
                        boids.remove(b1)
                        all_sprites.remove(b1)
                        fail_count += 1
            else:
                stat = b.update(boids,obs)
                if b0.id == b.id:    
                    if len(sys.argv)>1:
                        vel_breakdown_filewriter.write('%f,%f,%f,%f,%f\n'%(stat[0],stat[1],stat[2],stat[3],stat[4]))
        averdist += averagedistance.AverageDistancePerFrame(boids)
        if len(boids) == 0 or frame_count>1000:
            if frame_count<1000:
                print("average distance: "+str(averdist/frame_count))
                filewriter.write('%f,%d\n'%((averdist/frame_count),fail_count))
            fail_count = 0
            frame_count = 0
            averdist = 0
            # time.sleep(3)
            for boid in boids:
                all_sprites.remove(boid)
            boids.clear()
            boids = [Boid(i) for i in range(num_boids)]
            for boid in boids:
                all_sprites.add(boid)
            for ob in obs:
                obs_sprites.remove(ob)
            obs.clear()
            obs_gen(obs)
            for ob in obs:
                obs_sprites.add(ob)
            b0 = boids[5]

        globalvariables.target_sprites = pg.sprite.RenderUpdates(globalvariables.target)
        all_sprites.clear(screen, background)
        all_sprites.update(boids,obs)
        obs_sprites.clear(screen, background)
        # if frame_count % 10 ==0:
        dirty = all_sprites.draw(screen)
        pg.display.update(dirty)
        dirty1 = obs_sprites.draw(screen)
        pg.display.update(dirty1)
        globalvariables.target_sprites.clear(screen, background)
        dirty2 = globalvariables.target_sprites.draw(screen)
        pg.display.update(dirty2)
        frame_count += 1
        # clock.tick(1)


if __name__ == "__main__":
    main()
