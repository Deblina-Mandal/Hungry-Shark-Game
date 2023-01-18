import pygame, sys, random 
             
class BG(object):
                    
    def __init__(self) :
        self.ocean_bed_x_pos = 0
        self.ocean_bed = ocean_bed
    def draw_floor(self):
            screen.blit(self.ocean_bed,(self.ocean_bed_x_pos,0))
            screen.blit(self.ocean_bed,(self.ocean_bed_x_pos + 1000,0))
          
    def update(self,speed):
        self.ocean_bed_x_pos-= speed
        self.draw_floor()
        if self.ocean_bed_x_pos<=-1000:
            self.ocean_bed_x_pos=0     
 

class player(object):
    def __init__(self,x,y,shark_changex,shark_changey,shark_surface) :
        # game variables
        self.x=x
        self.y=y
        self.shark_changex = shark_changex 
        self.shark_changey = shark_changey
        self.shark_surface= shark_surface
        self.shark_rect = self.shark_surface.get_rect(center=(x, y)) 
        self.mask = pygame.mask.from_surface(self.shark_surface)
        

    def screen_condition(self):
        if self.shark_rect.top <= 30:
            self.shark_rect.top = 30
        if self.shark_rect.bottom >= 700:
            self.shark_rect.bottom = 700
        if self.shark_rect.left <= 0:
            self.shark_rect.left = 0
        if self.shark_rect.right >= 1000:
            self.shark_rect.right = 1000
  
  
    def draw_shark(self,screen):
              
        self.shark_rect.x += self.shark_changex
        self.shark_rect.y += self.shark_changey 
        self.x= self.shark_rect.x
        self.y= self.shark_rect.y
       
        self.screen_condition()
        screen.blit(self.shark_surface,self.shark_rect)
        

    def get_width(self):
        return self.shark_surface.get_width()

    def get_height(self):
        return self.shark_surface.get_height()

    def collide(self,obj,screen): 
             
        if abs(self.shark_rect.right- obj.fish_rect.left) <= 10:
            return True   
        if abs(self.shark_rect.top - obj.fish_rect.bottom) <= 10:
            return True
        if abs(self.shark_rect.bottom - obj.fish_rect.top)<= 10:
            return True
       
class Fish(object):
      
    def __init__(self,x,y,fish) : 
          self.x = x
          self.y = y
          self.fish_img = fish
          self.fish_rect = self.fish_img.get_rect(center=(x, y)) 
          self.mask = pygame.mask.from_surface(self.fish_img) 

    def move(self,vel):
        self.x -= vel
        self.fish_rect.x = self.x
    def draw(self,screen):
        screen.blit(self.fish_img,(self.x , self.y))
 
    def get_width(self):
        return self.fish_img.get_width()

    def get_height(self):
        return self.fish_img.get_height()

    def collide(self,obj,screen):
        return collision(obj,self) 
            
                       
def collision(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None

class GameState():
    def __init__(self):
        self.state='intro'
    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                 self.state = 'instruction'

        intro1_text = basic_font.render('Click anywhere to continue ^_^', True, red)
        intro1_rect = intro1_text.get_rect(center=(500, 650))

        pygame.mixer.Sound.set_volume(welcome_sound,0.5)
        pygame.mixer.Sound.play(welcome_sound)

        screen.blit(introduction1, (0,0))
        screen.blit(intro1_text, intro1_rect)

        pygame.display.update()

    def instruction(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                welcome_sound.stop()
                self.state = 'main_game'

       
        screen.blit(start_button, (0, 0))

        pygame.display.update()
  
    def main_game(self):
            # background
            Bg = BG()            
            shark = player(0,0,0,0,shark_closedmouth)
            level = 0 
            lives = 3
            lost = False
            lost_count = 0
            score = 0
            fish_list = []
            wave_length = 5
            fish_vel = 1

            def redraw_window():
                #ocean background 
                Bg.update(fish_vel)
 
                lives_label = basic_font.render(f"Lives: {lives}" ,True , (0,0,0))
                level_label = basic_font.render(f"Level: {level}" ,True , (0,0,0))
                score_label = basic_font.render(f"Score: {score}" ,True , (0,0,0))
                pygame.draw.rect(screen, white, pygame.Rect(10, 10, lives_label.get_width(), lives_label.get_height()))
                screen.blit(lives_label,(10,10))
                pygame.draw.rect(screen, white, pygame.Rect(450, 10, score_label.get_width(), score_label.get_height()))
                screen.blit(score_label,(450,10))
                pygame.draw.rect(screen, white, pygame.Rect(1000 - level_label.get_width() - 10, 10, level_label.get_width(), level_label.get_height()))
                screen.blit(level_label,(1000 - level_label.get_width() - 10 ,10))
                #fish
                for fish in fish_list:
                    fish.draw(screen)
                 
                
                if lost :
                    if lives == 0 : 
                        shark.shark_surface = shark_dead                                    
                    shark.draw_shark(screen)

                    if level == 6 and lives > 0:
                        lost_label = basic_font.render("You Won!!" ,True, (0,0,0))
                    else:
                        lost_label = basic_font.render("You Lose!!" ,True, (0,0,0))
                    pygame.draw.rect(screen, white, pygame.Rect(500 - lost_label.get_width()//2 -10, 340, lost_label.get_width()+10, lost_label.get_height()+10))
                    screen.blit(lost_label,(500 - lost_label.get_width()//2 , 350))
                                      
                else:         
                    shark.draw_shark(screen)
                    
                  
            run=True
            while run:
                if lives <= 0 or level == 6:
                    lost = True
                if lost:
                        run = False
                            
                if len(fish_list) == 0 :
                    level += 1
                    fish_vel += 0.5

                    Bg.ocean_bed=random.choice(bg_list)
                     
                    wave_length += 5
                    for i in range(wave_length):
                        fish = Fish(random.randrange(1000,3000), random.randrange(150,600), random.choice([fish1,fish2,fish3,crab]))
                        fish_list.append(fish)
  
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit
                    
                    if event.type==pygame.KEYDOWN:
                        if event.key == pygame.K_UP :
                            shark.shark_changey -=10

                        if event.key == pygame.K_DOWN :
                            shark.shark_changey +=10
                        
                        if event.key == pygame.K_LEFT :
                            shark.shark_changex -=10
                                
                        if event.key == pygame.K_RIGHT :
                            shark.shark_changex +=10
                            
                    if event.type==pygame.KEYUP:
                        if event.key == pygame.K_DOWN or event.key == pygame.K_UP :
                            shark.shark_changey=0
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            shark.shark_changex=0
                # fish
                 
                for fish in fish_list[:]:
                    flag=0
                    fish.move(fish_vel)
                    if shark.collide(fish,screen):
                        shark.shark_surface = shark_closedmouth
                    else:
                        shark.shark_surface = shark_openmouth

                    if fish.collide(shark,screen):
                        
                        if fish.fish_img == crab:
                            pygame.mixer.Sound.play(eat2_sound)
                            flag=1
                        else:
                            pygame.mixer.Sound.play(eat_sound)
                            score += 1
                        fish_list.remove(fish)
                        if flag == 1 :
                            lives -= 1
                    if fish.x + fish.get_width() < 0:
                         
                        fish_list.remove(fish)
                
                    
                redraw_window()
                
                    
                # Rendering
                pygame.display.update()

            if lost:
                        self.state = 'game_over'
                        self.stime=pygame.time.get_ticks()
                        if level==6 and lives >0:
                            win_sound.play()
                        else:
                            lose_sound.play()
                        self.active=0
                        
                                            
            
                        
                
    def game_over(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.active=0
                    self.state='main_game'
                if event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()
 
        self.active=1
        stime2 = pygame.time.get_ticks()
        if stime2-self.stime>=1700:
                                    lose_sound.stop()

        replay_text1 = gameover_font.render('Press Y to play again ', True, black)
        replay1_rect = replay_text1.get_rect(center=(500, 500))
         
        replay_text2 = gameover_font.render('and N to end the game ', True, black)
        replay2_rect = replay_text2.get_rect(center=(500, 550))

        pygame.draw.rect(screen, white, pygame.Rect(270, 480, 450, 110))
        screen.blit(replay_text1, replay1_rect)
        screen.blit(replay_text2, replay2_rect)

        pygame.display.update()

    def state_manager(self):
        if self.state == 'intro' :
            self.intro()

        if self.state == 'instruction':
            self.instruction()

        if self.state == 'main_game':
            self.main_game()

        if self.state == 'game_over':
            self.game_over()

# General setup
pygame.init()
clock = pygame.time.Clock()

game_state=GameState()

# Main Window
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hungry Shark')


# Global Variables
green = (0, 255, 0)
red = (255, 0, 0)
black = (0,0,0)
white = (255,255,255)
blue = (135,206,250)
yellow=(255,255,0)
purple=(154,50,205)
navy_blue =(0,0,100)
 
# ocean bed
ocean_bed=pygame.image.load('shark game media/underwater 5.jpg').convert()
ocean_bed_size=(1000,700)
ocean_bed=pygame.transform.scale(ocean_bed,ocean_bed_size)

ocean_bed1 = pygame.image.load('shark game media/images (2).jfif').convert()
ocean_bed1 =pygame.transform.scale(ocean_bed1,ocean_bed_size)


ocean_bed2 = pygame.image.load('shark game media/Presentation1.jpg').convert()
ocean_bed2 =pygame.transform.scale(ocean_bed2,ocean_bed_size)

ocean_bed3 = pygame.image.load('shark game media/b54909102085701.5f2e41a1c4148.jpg').convert()
ocean_bed3 =pygame.transform.scale(ocean_bed3,ocean_bed_size)
  
  
bg_list=[ocean_bed,ocean_bed3,ocean_bed2,ocean_bed1]

# shark
shark_openmouth=pygame.image.load('shark game media/shark11.png').convert_alpha()
shark_surface_size=(250,200)
shark_openmouth=pygame.transform.scale(shark_openmouth,shark_surface_size)
shark_rect=shark_openmouth.get_rect(center=(140,250))


shark_closedmouth = pygame.image.load('shark game media/shark_closedmouth.png').convert_alpha()
shark_closedmouth_size = (250,200)
shark_closedmouth=pygame.transform.scale(shark_closedmouth,shark_closedmouth_size)
shark_closedmouth_rect=shark_closedmouth.get_rect(center=(140,250))

shark_dead = pygame.image.load('shark game media/shark_dead.png').convert_alpha()
shark_dead_size = (250,150)
shark_dead = pygame.transform.scale(shark_dead,shark_dead_size)
shark_dead_rect = shark_dead.get_rect(center=(140,250))



#Fish1
fish1=pygame.image.load('shark game media/fish3.png').convert_alpha()
fish1_size=(100,100)
fish1=pygame.transform.scale(fish1,fish1_size)
fish1=pygame.transform.flip(fish1,True,False)


#Fish2
fish2=pygame.image.load('shark game media/fish1.png').convert_alpha()
fish2_size=(90,90)
fish2=pygame.transform.scale(fish2,fish2_size)
fish2=pygame.transform.flip(fish2,True,False)

#Fish3
fish3=pygame.image.load('shark game media/fish2.png').convert_alpha()
fish3_size=(100,100)
fish3=pygame.transform.scale(fish3,fish3_size)
fish3=pygame.transform.flip(fish3,True,False)

#Crab
crab=pygame.image.load('shark game media/crab.png').convert_alpha()
crab_size=(100,100)
crab=pygame.transform.scale(crab,crab_size)
crab=pygame.transform.flip(crab,True,False)


start_button_surface=pygame.image.load('shark game media/start.png').convert_alpha()
startbutton_size = (1000, 700)
start_button = pygame.transform.scale(start_button_surface, startbutton_size)

intro1_surface=pygame.image.load('shark game media/HUNGRY SHARK2.png').convert_alpha()
intro1_size = (1000, 700)
introduction1 = pygame.transform.scale(intro1_surface, intro1_size)

 
 
# fonts
basic_font = pygame.font.SysFont('freesansbold.ttf', 60,bold=True)
playerno_font = pygame.font.SysFont('freesansbold.ttf', 40,bold=True) 
instruction1_font=pygame.font.SysFont('freesansbold.ttf',50,bold=True,italic=True)
instruction2_font=pygame.font.SysFont('freesansbold.ttf',50,bold=True,italic=True)
instruction3_font=pygame.font.SysFont('freesansbold.ttf',40,bold=True,italic=True)
gameover_font=pygame.font.SysFont('freesansbold.ttf',50,bold=True,italic=True)

# sounds
welcome_sound = pygame.mixer.Sound("shark game media/085563291-shark-attack.wav")
eat_sound = pygame.mixer.Sound("shark game media/eat_sound.wav")
pygame.mixer.Sound.set_volume(eat_sound, 0.3)
eat2_sound = pygame.mixer.Sound("shark game media/eat2_sound.wav")
win_sound = pygame.mixer.Sound("shark game media/win")
pygame.mixer.Sound.set_volume(win_sound, 0.5)
lose_sound = pygame.mixer.Sound("shark game media/lose")
pygame.mixer.Sound.set_volume(lose_sound, 0.5)

# game objects
shark = player(0,0,0,0,shark_closedmouth)


while True:
    game_state.state_manager()
    clock.tick(60)

