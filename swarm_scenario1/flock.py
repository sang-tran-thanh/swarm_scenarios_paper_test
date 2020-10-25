from boid import Boid
from obstacle import Obstacle
import pygame as pg
from random import randint
import globalvariables
from targetpoint import Targetpoint
import averagedistance

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
    background.fill((0, 0, 0))
    running = True
    #pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

    all_sprites = pg.sprite.RenderUpdates()
    obs_sprites = pg.sprite.RenderUpdates()

    boids = [Boid(0) for i in range(num_boids)]
    obs = []
    globalvariables.target.append(Targetpoint((width-50,height-50)))
    
    '''obstacles'''



    # for i in range(0, int(height/4),10):
    #     for j in[0]:
    #         obs.append(Obstacle([j,i]))
    # for i in range(0, int(width/4),10):
    #     for j in[0]:
    #         obs.append(Obstacle([i,j]))

    for i in range(0, height,10):
        for j in[0, width]:
            obs.append(Obstacle([j,i]))
    for i in range(0, width,10):
        for j in[0, height]:
            obs.append(Obstacle([i,j]))


    for i in [int(1.5*height/4),int(1.75*height/4),int(2.25*height/4),int(2.5*height/4)]:
        for j in range(int(1.5*width/4),int(2.5*width/4),5):
            obs.append(Obstacle([j,i]))
    for i in [int(1.5*width/4),int(2.5*width/4)]:
        for j in range(int(1.5*height/4),int(1.75*height/4),5):
            obs.append(Obstacle([i,j]))
        for j in range(int(2.25*height/4),int(2.5*height/4),5):
            obs.append(Obstacle([i,j]))


    # for i in [int(1.5*height/4),int(2.5*height/4)]:
    #     for j in range(int(1.5*width/4),int(2.5*width/4),10):
    #         obs.append(Obstacle([j,i]))
        # for j in range(int(2.5*width/4),int(3*width/4),10):
        #     obs.append(Obstacle([j,i]))

    # for i in [int(0.5*width/4),int(1*width/4),int(1.75*width/4),int(2.25*width/4),int(3*width/4),int(3.5*width/4)]:
    #     for j in range(int(0.5*height/4),int(1.5*height/4),10):
    #         obs.append(Obstacle([i,j]))
    #     for j in range(int(2.5*height/4),int(3.5*height/4),10):
    #         obs.append(Obstacle([i,j]))

    for boid in boids:
        all_sprites.add(boid)
    for ob in obs:
        obs_sprites.add(ob)
    ###################################################################################

    frame_count = 0
    averdist = 0
    filewriter = open('scenario1.csv', 'a')
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
        # for b in boids:
        #     b.update(boids,obs)
        for b in boids:
            if b.checktarget(obs) == True:
                boids.remove(b)
                all_sprites.remove(b)                
            else:
                b.update(boids,obs)
        averdist += averagedistance.AverageDistancePerFrame(boids)
        if len(boids) == 0:   
            print("average distance: "+str(averdist/frame_count))
            filewriter.write('%f\n'%(averdist/frame_count))
            frame_count = 0
            averdist = 0
            boids = [Boid(0) for i in range(num_boids)]
            for boid in boids:
                all_sprites.add(boid)

        globalvariables.target_sprites = pg.sprite.RenderUpdates(globalvariables.target)
        all_sprites.clear(screen, background)
        all_sprites.update(boids,obs)
        dirty = all_sprites.draw(screen)
        pg.display.update(dirty)
        dirty1 = obs_sprites.draw(screen)
        pg.display.update(dirty1)
        globalvariables.target_sprites.clear(screen, background)
        dirty2 = globalvariables.target_sprites.draw(screen)
        pg.display.update(dirty2)
        frame_count += 1
        clock.tick(120)


if __name__ == "__main__":
    main()
