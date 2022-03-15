import pygame
import random
from cmath import sqrt
from pygame import mixer
import json
import operator

#initialising the pygame module
pygame.init()
pygame.font.init()
mixer.init()
#game loop
run = True
#game status
game_status = False
#game status
leader_status = False
# Loading the song
mixer.music.load("explosion.wav")
  
# Setting the volume
mixer.music.set_volume(2)
#screen
width,height = 600,600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

#bg image
bg_img = pygame.transform.scale(pygame.image.load('bg.jpg'),(600,600))

#button
button =  pygame.rect.Rect(250,500,120,60)
#loading image
jet = pygame.transform.scale(pygame.image.load('jet.png'),(90,90)).convert_alpha()
jetX,jetY=250,400
tree,treeX,treeY =[],[],[]
coin,coinX,coinY =[],[],[]

for i in range(8):
    tree.append(pygame.transform.scale(pygame.image.load('pine-tree.png'),(90,90)).convert_alpha())
    treeX.append(random.randint(0,550))
    treeY.append(random.randint(0,500))
    coin.append(pygame.transform.scale(pygame.image.load('coin.png'),(20,20)))
    coinX.append(random.randint(0,550))
    coinY.append(random.randint(0,500))
# bullet
bullet =pygame.transform.scale(pygame.image.load('bullet.png'),(40,40)).convert_alpha()
bulletX,bulletY=jetX,jetY # jet position fire
ready = False
#enemy
enemy,enemyX,enemyY=[],[],[]
def enemies():
    global enemy,enemyX,enemyY
    for i in range(8):
        enemy.append(pygame.transform.scale(pygame.image.load('enemy.png'),(60,60)).convert_alpha())
        enemyX.append(random.randint(0,550))
        enemyY.append(random.randint(0,500))
    for i in range(8):
        enemyY[i]+=4
        if enemyY[i]>600:
            enemyY[i]= 10
            enemyX[i] = random.randint(-50,550)
        
   
  
#text
font_button_text = pygame.font.SysFont('Consolas', 20)

#score
score =0
#lives total 5
lives = 5
#kills
kill =0
# restrictng jet to move out of the frame window
def jetFrame():
    global jetX
    if jetX <0:
        jetX=0
    if jetX > 520:
        jetX = 520

# collision detection
def tree_colision(x,y):
    global lives,leader_status
    distance_tree_jet = sqrt(abs(pow((x-jetX),2) + pow((y-jetY),2)))
    if distance_tree_jet.real <27:
        lives-=1
        treeY[i]= 10
        treeX[i] = random.randint(0,550)
        
        if lives==0:
            leader_status = True
            pygame.quit()
            

#collision with coin score +1
def coin_colision(x,y):
    global score
    distance_tree_jet = sqrt(abs(pow((x-jetX),2) + pow((y-jetY),2)))
    if distance_tree_jet.real <27:
        score+=1
        coinY[i]= 10
        coinX[i] = random.randint(0,550)
        
        pass



def bullet_collision(enemyX,enemyY): 
    global kill
    distance_bullet_enemy = sqrt(abs(pow((enemyX-bulletX),2) + pow((enemyY-bulletY),2)))
    
    if distance_bullet_enemy.real <27:
        explosion = Explosion(enemyX, enemyY)
        explosion_group.add(explosion)
        mixer.music.play()
        kill+=1
        enemyY= 10
        enemyX = random.randint(0,550)
   
def bullet_Move():
    global bulletY,ready
    bulletX = jetX
    bulletY -=10
    
    if bulletY < 0:
        bulletY =jetY
        screen.blit(bullet,(bulletX,bulletY))
        ready = False


#create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"exp{num}.png")
			img = pygame.transform.scale(img, (300, 300))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 5
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()


explosion_group = pygame.sprite.Group()


while run:
    if game_status:
        screen.fill((255,255,255))
        explosion_group.draw(screen)
        explosion_group.update()
        for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    leader_status = True
                    run = False
                    print(f"your highest score is:{score}")
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
                jetX-=10
                bulletX=jetX
        if keys[pygame.K_RIGHT]:
                jetX+=10
                bulletX=jetX
        if keys[pygame.K_SPACE]:
            bulletX = jetX
            bulletY=jetY
            ready = True
        if ready:
            bullet_Move()
        screen.blit(bullet,(bulletX,bulletY))
        enemies()
        screen.blit(enemy[i],(enemyX[i],enemyY[i]))
        bullet_collision(enemyX[i],enemyY[i])
        #displaying on the objects on the screen
        screen.blit(jet,(jetX,jetY))
        jetFrame()
        for i in range(8):
            treeY[i]+=8
            coinY[i]+=9
            if treeY[i]>600:
                treeY[i]= 10
                treeX[i] = random.randint(-50,550)
            if coinY[i]>600:
                coinY[i]= 10
                coinX[i] = random.randint(0,550)
        screen.blit(tree[i],(treeX[i],treeY[i]))
        screen.blit(coin[i],(coinX[i],coinY[i]))
        enemies()
        tree_colision(treeX[i],treeY[i])
        coin_colision(coinX[i],coinY[i])
        screen.blit(font_button_text.render("Score:"+ str(score),True, (0,0,0)),(0,0))
        screen.blit(font_button_text.render("lives:"+ str(lives),True, (0,0,0)),(0,20))
        screen.blit(font_button_text.render("kills:"+ str(kill),True, (0,0,0)),(0,40))

    else:
        #menu
        screen.blit(bg_img,(0,0))
        pygame.draw.rect(screen,(255,0,0),button)
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                print("click")
                game_status = True
        screen.blit(font_button_text.render("START", True,(255,255,255)),(280, 520))
    
    pygame.display.update()
    clock.tick(30)

if leader_status == True:

    #loading the data
    with open('Leaderboard.txt') as f:
        data = f.read()
    js = json.loads(data)
    
    #names and scores store
    h_score = score + kill
    user_input = input("Enter Your First Name")
    js[user_input] = h_score
    
    #display names and score
    print("Player:",user_input)
    print("Score:",h_score)
    #sorting the leaderboard
    new_leader_b = dict( sorted(js.items(), key=operator.itemgetter(1),reverse=True))
    
    #updating
    with open('Leaderboard.txt', 'w') as file:
        file.write(json.dumps(js))
    #Rank display of the current player
    for i in range(1, len(new_leader_b)):
        if user_input == list(new_leader_b.keys())[i]:
            print("Your Rank is",i)

    print("our top 3 players")
    print("Names\t\t\t\tScore")
    #leaderboard
    for i in range(1, 4):
        print(i,list(new_leader_b.keys())[i],"\t\t\t\t",list(new_leader_b.values())[i])

   
else:
    pass
