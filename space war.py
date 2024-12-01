import pygame
import random
import os
FPS = 60
WIDTH = 500
HEIGHT = 600

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

#遊戲初始化 and 創建視窗
pygame.init()#初始化
pygame.mixer.init()#初始化音效模組
screen = pygame.display.set_mode((WIDTH,HEIGHT))#傳入元組,表示畫面高度跟寬度
pygame.display.set_caption("太空生存戰")#設定視窗名稱
clock = pygame.time.Clock()

#載入圖片,!載入前需先做pygame.init()初始化,否則會發生錯誤
#統一路徑寫法
#.convert()將圖片轉換成pygame較好讀取的模式,可加快讀取速度
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
player_mini_img = pygame.transform.scale(player_img,(25,19))
pygame.display.set_icon(player_mini_img)#設定視窗icon
player_mini_img.set_colorkey(BLACK)
#rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
rock_imgs = []
for i in range(7):
    #在字串前使用f就可在字串中的{}裡使用變數
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())
expl_anim = {}#字典,爆炸動畫,分成大爆炸跟小爆炸
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img,(30,30)))
    player_expl_img = pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img","shield.png")).convert()    
power_imgs['gun'] = pygame.image.load(os.path.join("img","gun.png")).convert()


#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
expl_sound = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound","background.ogg"))

#font_name = pygame.font.match_font('arial')#引入字體
font_name = os.path.join("font.ttf")#引入自行下載的字體
def draw_text(surf,text,size,x,y):#將文字寫到畫面上
    font = pygame.font.Font(font_name,size)#文字物件,(字體,文字大小)
    text_surface = font.render(text,True,WHITE)#渲染,(要渲染的文字,是(True)否(False)要用反鋸齒(使字體看起來比較滑順),文字顏色)
    text_rect = text_surface.get_rect()#定位
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def new_rock():#生成石頭
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT =10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)#pygame矩形(座標,長寬)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)#畫矩形到平面上,(畫布,顏色,要畫的東西) #裡面的綠色條
    pygame.draw.rect(surf,WHITE,outline_rect,2)#多傳一個像素參數 #綠色條的外框

def draw_lives(surf,lives,img,x,y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32*i#間隔30像素後再畫
        img_rect.y = y
        surf.blit(img,img_rect)

def draw_init():
    screen.blit(background_img,(0,0))
    draw_text(screen,'太空生存戰!',64,WIDTH/2,HEIGHT/4)
    draw_text(screen,'← →移動飛船 空白鍵發射子彈~',22,WIDTH/2,HEIGHT/2)
    draw_text(screen,'按任意鍵開始遊戲',18,WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:#keyup按下後鬆開
                waiting = False
                return False


#sprite 畫面上的所有物件
#創建飛船
class Player(pygame.sprite.Sprite):#用自定義的類別繼承內建sprite類別
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#呼叫內建sprite初始函式
        #self.image = pygame.Surface((50,40))#屬性1,要顯示的圖片,初始以平面(pygame.Surface())表示
        #self.image.fill(GREEN)#設定圖片顏色
        self.image = pygame.transform.scale(player_img,(50,38))#轉換圖片大小,(圖片,像素)
        self.image.set_colorkey(BLACK)#把黑色的部分變透明
        self.rect = self.image.get_rect()#屬性2,定位圖片位置,把圖片框起來,就能設定位置相關數據
        #設定rect左上角座標
        #self.rect.x = 200
        #self.rect.y = 200
        #設定中心座標
        #self.rect.center = (WIDTH/2,HEIGHT/2)
        #設定速度變數
        self.radius = 20#半徑
        #畫出來確認碰撞範圍
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)#畫圓,(畫布,顏色,中心,半徑)
        self.speedx = 8

        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.health = 100
        self.lives = 3
        self.hidden = False #飛船是否在隱藏中
        self.hide_time = 0 #隱藏時間
        self.gun = 1 #子彈等級
        self.gun_time = 0

    def update(self):#更新函式
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:#閃電效果持續時間
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:#隱藏結束
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
        
        key_pressed = pygame.key.get_pressed()#回傳一整串布林值,代表鍵盤上的按鍵是(True)否(False)有被按下
        if key_pressed[pygame.K_RIGHT]:#判斷右鍵是否有被按下
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        #self.rect.x += 2
        #if self.rect.left > WIDTH:
        #    self.rect.right = 0
    
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                shoot_sound.play()


    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+500)#透過將飛船定位到視窗外面來達成隱藏效果

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()


#創建石頭
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((30,40))
        #self.image.fill(RED)
        self.image_ori = random.choice(rock_imgs)#從rock_imgs裡隨機挑一個出來
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2) 
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)#畫圓,(畫布,顏色,中心,半徑)
        
        #設定隨機掉落位置
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,10)#掉落速度
        self.speedx = random.randrange(-3,3)#水平速度

        self.total_degree = 0
        self.rot_dergee = random.randrange(-5,5)#設定旋轉角度

    def rotate(self):#選轉動畫
        self.total_degree += self.rot_dergee
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori,self.total_degree)#(要旋轉的圖片,旋轉角度),旋轉後會失真,不能疊加太多次
        #解決方法為每次都使用原始圖片進行旋轉,疊加的只有角度而不是圖片,就不會有失真問題
        
        #每次旋轉後如果還是用原先定位的中心點會變得很奇怪
        #重新定位
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:#重設數值,掉出去後重新回到上面
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)

#創建子彈
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):#需傳入飛船xy座標
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((10,20))
        #self.image.fill(YELLOW)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()#sprite函式,從所有有這個物件的sprite群組中移除

#爆炸動畫
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):#需傳入爆炸中心點及爆炸size(大或小)
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        #確保更新速度不會太快
        self.frame = 0 #更新到第幾張圖片
        self.last_update = pygame.time.get_ticks()#回傳初始化到現在經過的毫秒數
        self.frame_rate = 50 #至少要經過幾毫秒才會更新到下一張圖片,可控制更新速度,數值越小更新越快,反之則越慢


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:#如果更新時間到了就更新圖片
            self.last_update = now
            self.frame += 1
        if self.frame == len(expl_anim[self.size]):#如果更新到最後一張就刪掉
            self.kill()
        else:#不然就繼續更新+重新定位
            self.image = expl_anim[self.size][self.frame]
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center

#寶物
class Power(pygame.sprite.Sprite):
    def __init__(self,center):#需傳入飛船xy座標
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()




pygame.mixer.music.play(-1)#撥放音樂,傳入重複撥放次數,-1代表無限撥放
pygame.mixer.music.set_volume(0.5)#設定音樂大小,範圍為0~1

#遊戲迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0
    
    clock.tick(FPS)#此迴圈1秒鐘之內最多只能被執行10次(解決不同電腦效能不同的問題)
    #取得輸入
    for event in pygame.event.get():#pygame.event.get()回傳現在發生的所有事件,ex:滑鼠滑到哪或鍵盤按了甚麼按鍵,回傳列表
        if event.type == pygame.QUIT:#偵測事件類型是否把遊戲關閉
            running=False
        elif event.type == pygame.KEYDOWN:#判斷事件是否為"按下"按鍵
            if event.key == pygame.K_SPACE:#如果是空白鍵就發射子彈
                player.shoot()
    
    #更新遊戲
    all_sprites.update()#執行群組內每一個物件的update函式
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)#判斷碰撞,以及碰撞後該物件是否要刪除,回傳字典,包含碰撞到的物件
    for hit in hits:#碰撞刪除後補充物件
        random.choice(expl_sound).play()
        score += hit.radius
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:
            powe = Power(hit.rect.center)
            all_sprites.add(powe)
            powers.add(powe)
        new_rock()

    #碰撞到就扣血
    hits = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)#將碰撞判斷從預設的矩形改成圓形,要給半徑(radius)
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        if player.health <= 0:#死亡
            death_expl = Explosion(player.rect.center,'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()#緩衝一段時間後再復活
            #running = False

    #寶物飛船相撞
    hits = pygame.sprite.spritecollide(player,powers,True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()


    if player.lives == 0 and not(death_expl.alive()):#讓最後一次動畫撥放完再結束
        show_init = True

    #畫面顯示
    screen.fill(BLACK)#設定顏色(r,g,b)
    screen.blit(background_img,(0,0))#bilt()畫,(要畫的圖片,要畫的位置)
    all_sprites.draw(screen)#將群組內所有sprite物件畫到螢幕上
    draw_text(screen,str(score),18,WIDTH/2,10)#印出分數
    draw_health(screen,player.health,5,15)#印出生命條
    draw_lives(screen,player.lives,player_mini_img,WIDTH-100,15)
    pygame.display.update()#更新畫面

pygame.quit()

#在終端機輸入pip install auto-py-to-exe後輸入auto-py-to-exe可將py打包成exe

#網路上搜尋NSIS並下載使用可將zip打包成安裝檔

#以上打包方式都是在當前環境打包,在其他環境下可能無法使用