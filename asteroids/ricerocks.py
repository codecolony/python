# implementation of Spaceship - program template for RiceRocks
# working program at http://www.codeskulptor.org/#user16_J4a2H1OId7_14.py
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])
ROCK_VELOCITY = .6
global_time_count = 0
high_score = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

#second explosion which looks more violent
violent_explosion_info = ImageInfo([50, 50], [100, 100], 10, 40, True)
violent_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def mid_point(p, q):
    return [(p[0]+q[0])//2, (p[1]+q[1])//2]

# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global a_missile, missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        a_missile.set_lifespan(40)
        missile_group.add(a_missile)
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.fiery = False
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated == True:
            k = self.age
            #self.image_center = [self.image_size[0]+self.image_center[0], self.image_center[1]]
            if not self.fiery:
                canvas.draw_image(self.image, [k*128+64,64], self.image_size,
                          self.pos, self.image_size, self.angle)
            else:
                explosion_index = [k % 9, (k // 9) % 9]
                canvas.draw_image(violent_explosion_image, 
                    [50 + explosion_index[0] * 100, 
                     50 + explosion_index[1] * 100], 
                     [100,100], self.pos, [100,100])
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def get_radius(self):
        return self.radius
    
    def set_fiery_explosion(self):
        self.fiery = True
    
    def get_position(self):
        return self.pos
    
    def set_lifespan(self, lifespan):
        self.lifespan = lifespan
        
    def get_age(self):
        return self.age
    
    def get_lifespan(self):
        return self.lifespan
    
    def set_animated(self):
        self.animated = True
        
    def set_sound(self):
        self.sound = explosion_sound
        
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) < self.radius+other_object.get_radius():
            return True
        else:
            return False
        
    def safe_distance(self, other_object):
        if dist(self.pos, other_object.get_position()) < self.radius+other_object.get_radius()+100:
            return False
        else:
            return True
        
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
  
        #update age
        self.age += 1
        
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    
    if (not started) and inwidth and inheight:
        #started = True
        init_game()
        
def draw(canvas):
    global time, started, rock_group, lives, score, missile_group, high_score
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text("High Score", [350, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    canvas.draw_text(str(high_score), [350, 80], 22, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group,canvas)
    
    # update ship and sprites
    my_ship.update()
    
    #detecting rock and ship collisions
    collide = group_collide(rock_group, my_ship, True)
    if collide > 0:
        lives -= 1
        score -= collide*10
    
    if lives <= 0 or not started:
        started = False
        rock_group = set([])
        #explosion_group = set([])
        timer.stop()
        
    #detecting rock and missile collisions
    collide = group_group_collide(rock_group, missile_group)
    if collide > 0:
        #lives -= 1
        score += collide*10
        
    # draw splash screen if not started
    if not started:
        soundtrack.rewind()
        if high_score < score:
            high_score = score
            
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    else:
        timer.start()
        
def exit_all():
    soundtrack.pause()
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, ROCK_VELOCITY, global_time_count
    
    if frame.get_canvas_textwidth("test",50) < 10:        
        exit_all() 
        
    global_time_count += 1
    
    #Every 10 seconds, the rocks fall twice as faster
    if global_time_count%10 == 0:
        ROCK_VELOCITY += 0.6
        
    if len(rock_group) <= 12:
        if random.randrange(0,2)==0:
            dir_decider = 1
        else:
            dir_decider = -1
            
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * ROCK_VELOCITY * dir_decider - .3, random.random() * ROCK_VELOCITY * dir_decider - .3]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        
        if a_rock.safe_distance(my_ship):
            rock_group.add(a_rock)
    
def process_sprite_group(rock_group, canvas):
    #show rocks
    remove = set([])
    
    for rock in rock_group:
        rock.draw(canvas)
        rock.update()
        if rock.get_age()>= rock.get_lifespan():
            remove.add(rock)
    rock_group.difference_update(remove)
    
def group_collide(group, other_object, violent_explosion_required = False):
    global explosion_group
    count = 0
    remove = set([])
    for object in group:
        if object.collide(other_object):
            count += 1
            remove.add(object)
            
            if violent_explosion_required:
                an_explosion = Sprite(mid_point(object.get_position(),other_object.get_position()), [0, 0], 0, 0, violent_explosion_image, violent_explosion_info, explosion_sound)
                an_explosion.set_animated()
                an_explosion.set_lifespan(81)
                an_explosion.set_fiery_explosion()
            else:
                an_explosion = Sprite(other_object.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
                
            explosion_group.add(an_explosion)
            
    group.difference_update(remove)
    return count

def group_group_collide(rock_group, missile_group):
    global explosion_group
    count = 0
    remove = set([])
    for rock in rock_group:
        k = group_collide(missile_group, rock) 
        if k > 0:
            remove.add(rock)
            count += k
            #an_explosion = Sprite(rock.get_position(), [0, 0], 0, 0, explosion_image, explosion_info)
            #an_explosion.set_animated()
            #explosion_group.add(an_explosion)
            
    rock_group.difference_update(remove)
    return count

def init_game():
    global lives, score, started, ROCK_VELOCITY, global_time_count
    lives = 3
    score = 0
    global_time_count = 0
    ROCK_VELOCITY = 0.6
    soundtrack.play()
    started = True
    
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
#an_explosion = Sprite([WIDTH / 3, HEIGHT / 3], [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
