# -*- coding: utf-8 -*-
"""
Created on Thu Nov 5 19:58:55 2022

@author: Emirh
"""
import time
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random
import pygame
import pygame.key
# from grafik import plot #GRAFIK
import matplotlib.pyplot as plt#GRAFIK ICIN
from IPython import display#GRAFIK ICIN

#Ajan hareketleri NUMPAD tuşları ile gerçekleşiyor.'''''

#kullanılacak renkleri belirtme
Rsiyah= pygame.Color(0,0,0)
Rbeyaz =pygame.Color(255,255,255)
Rsari =pygame.Color(155,155,0)
Rkirmizi=pygame.Color(200,0,0)
Rgri=pygame.Color(150,150,150)
Rmavi=pygame.Color(0,0,200)
transparan=pygame.Color(0,0,0,127)
#pencere boyutu belirtme
Pgenislik=400 #pencere boyutları
Pyukseklik=600
fps=60 #oyunun çalışma hızı

class Gemi(pygame.sprite.Sprite):#inhrt-

    # kullanılacak ajan karakterinin şekil özelliklerini belirtme
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,50))#boyutu
        self.image.fill(Rbeyaz)#arkaplan rengi
        self.rect = self.image.get_rect() #burda yapılan şey işimizi kolaylaştırır.
        self.radius = 20 #görünmez yarıçap, sonradan etkileşimde işe yarayacak.
       
        self.rect.center =(Pgenislik/2,Pyukseklik-40) #şeklin ilk konumu.

        
    def update(self,action):#şeklin(gemi) konum-hareketini güncelleyecek fonksiyon.

            self.x_speed = 0
            self.y_speed = 0
            keystate = pygame.key.get_pressed()
            #numpad tuşlarına konum değiştirme değerlerini atama.
            if keystate[pygame.K_KP4] or action == 4: #"K_KP4 (4) tuşu x ekseninde azalma meydana getirir."
                self.x_speed = -7
            elif keystate[pygame.K_KP6] or action == 6:#"_" veya action == ne ise .
                self.x_speed = 7
            elif keystate[pygame.K_KP8] or action == 8:#"_"
                self.y_speed = -7  
            elif keystate[pygame.K_KP2] or action == 2:#"_"
                self.y_speed = 7            
            elif keystate[pygame.K_KP7] or action == 7:#"_"
                self.x_speed = -6
                self.y_speed = -6                
            elif keystate[pygame.K_KP9] or action == 9:#"_"
                self.x_speed = 6
                self.y_speed = -6     
            elif keystate[pygame.K_KP1] or action == 1:#"_"
                self.x_speed = -6
                self.y_speed = 6     
            elif keystate[pygame.K_KP3] or action == 3:#"_"
                self.x_speed = 6
                self.y_speed = 6     
            
            else:#Hareket yok ise x ve y ekseni hizlari 0.
                self.x_speed = 0
                self.y_speed = 0
                
            self.rect.x +=self.x_speed
            self.rect.y +=self.y_speed
            
            #Şeklin pencereden taşmasını önleme.
            if self.rect.top < Pyukseklik-250: 
                self.rect.top = Pyukseklik-250
            if self.rect.bottom >Pyukseklik-20:
                self.rect.bottom=Pyukseklik-20
            if self.rect.right > Pgenislik-15:
                self.rect.right = Pgenislik-15
            if self.rect.left < 15:
                self.rect.left = 15
                
    def getCoordinates(self):#x ve y koordinat degerleri dondur.
        return (self.rect.x, self.rect.y)
#------------------------------atmosfer--------------            
class atm(pygame.sprite.Sprite):#Hüzme efektleri.
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1,100))
        self.image.fill(Rbeyaz)
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(40, Pgenislik -40)#Şekillerin rastgele ilk konum alması x ekseni.
        self.rect.y = random.randrange(1,Pyukseklik-200)#Şekillerin rastgele ilk konum alması y ekseni.
        
        self.speedx = 0
        self.speedy = 30
    
    def update(self):
        #Şekil pencerenin dışına çıkana kadar alacağı x ve y değerleri update'i.
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #Şekil pencerenin dışına çıktıktan sonra yeniden başka bir ilk konuma yerleşmesi.
        if self.rect.top > Pyukseklik + 100:
            self.rect.x = random.randrange(40, Pgenislik-40)
            self.rect.y = random.randrange(1,Pyukseklik-200)
            
class atm2(pygame.sprite.Sprite):# Yıldız efektleri.
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2,2))
        self.image.fill(Rbeyaz)
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(20, Pgenislik -20)
        self.rect.y = random.randrange(1,600)
        
        self.speedx = 0
        self.speedy =4
    
    def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy        
            if self.rect.top > Pyukseklik + 10:
                self.rect.x = random.randrange(20, Pgenislik-20)
                self.rect.y = random.randrange(1,3)            
                self.speedy=4
 

#-------------------METEORLAR--------------------          
class Meteor1(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill(transparan)
        self.rect = self.image.get_rect()
        self.radius = 10
        pygame.draw.circle(self.image, Rgri, self.rect.center,self.radius)
        self.rect.x = random.randrange(0, (Pgenislik/2) - self.rect.width)
        self.rect.y = random.randrange(2,10)
        
        self.speedx = 0
        self.speedy =18
    
    def update(self):
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.top > Pyukseklik + 20:
            self.rect.x = random.randrange(0, (Pgenislik/2)-self.rect.width)
            self.rect.y = random.randrange(2,10)
            self.speedy = 18

    def getCoordinates(self):
        return (self.rect.x, self.rect.y)  
          
class Meteor2(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill(transparan)
        self.rect = self.image.get_rect()
        self.radius = 10
        pygame.draw.circle(self.image, Rgri, self.rect.center,self.radius)
        self.rect.x = (Pgenislik/2)
        self.rect.y = random.randrange(2,10)
        
        self.speedx = 0
        self.speedy = 17
    
    def update(self):
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.top > Pyukseklik + 20:
            self.rect.x = random.randrange( (Pgenislik/2), Pgenislik - self.rect.width)
            self.rect.y = random.randrange(2,10)
            self.speedy = 17

    def getCoordinates(self):
        return (self.rect.x, self.rect.y)              

#----------------------------------
class DQLAgent:
    def __init__(self):
        
        self.state_size = 4 # mesafe durumlari (gemix-meteor1x),(gemiy-meteor1y),(gemix-meteor2x),(gemiy-meteor2y)
        self.action_size = 9 # hareketsiz,kuzey-batı,kuzey,kuzey-doğu,doğu,batı,güney-batı,güney,güney-doğu
        
        self.gamma = 0.95
        self.learning_rate = 1
        # 0.0001 90---- 0.00001  98
        self.epsilon = 1  # KESIF
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        
        self.memory = deque(maxlen = 1000)
        
        self.model = self.build_model()
        
        
    def build_model(self):
        # neural network for deep q learning
        model = Sequential()
        model.add(Dense(48, input_dim = self.state_size, activation = "relu"))
        model.add(Dense(self.action_size,activation = "linear"))
        model.compile(loss = "mse", optimizer = Adam(lr = self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        # DEPOLA
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        state = np.array(state) #state`i array`e cevir.
        
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
        
    def replay(self, batch_size):
        # EGİTİM
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory,batch_size)
        for state, action, reward, next_state, done in minibatch:
            state = np.array(state) #state`i array`e cevir.
            next_state = np.array(next_state)#nextstate`i array`e cevir.
            if done:
                target = reward 
            else:
                target = reward + self.gamma*np.amax(self.model.predict(next_state)[0])
            train_target = self.model.predict(state)
            train_target[0][action] = target
            self.model.fit(state,train_target, verbose = 0)
            
    def adaptiveEGreedy(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay



#-------------------------------ENVIRONMENT         
class Environment(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)    
        #SPRITE /group
        self.all_sprite = pygame.sprite.Group() #Hareket eden bütün objelere daha kolay özellik eklemek için gruplandırmak.
        self.enemy= pygame.sprite.Group()
        self.atmosferler= pygame.sprite.Group()
        #Class değer atamaları:
        self.gemi = Gemi()
        self.meteor1=Meteor1()
        self.meteor2=Meteor2()
        self.y1=atm2();self.y2=atm2();self.y3=atm2();self.y4=atm2();self.y5=atm2();self.y6=atm2();self.y7=atm2();self.y8=atm2();
        #Bazı sprite ların özelliklerini değiştirme:
        self.a1= atm();self.a1.speedy= 25
        self.a2= atm();self. a2.speedy=25 
        self.a3= atm();self.a3.speedy=15
        self.a4= atm();self.a4.speedy=15
        self.a5= atm();self.a5.speedy=20
        self.a6= atm();self.a6.speedy=20
        self.a7= atm();self.a7.speedy=10
        self.a8= atm();self.a8.speedy=10
        self.all_sprite.add(self.gemi) #gemi objesini sprite grubuna eklemek
        self.all_sprite.add(self.meteor1,self.meteor2) #meteor1 objesini sprite grubuna eklemek ,meteor2 objesini sprite grubuna eklemek
        self.all_sprite.add(self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,self.a7,self.a8) #atmosfer(hüzme) ürünlerini sprite gruba eklemek.
        self.all_sprite.add(self.y1,self.y2,self.y3,self.y4,self.y5,self.y6,self.y7,self.y8) #atmosfer(yıldız) ürünlerini sprite gruba eklemek.
        self.enemy.add(self.meteor1,self.meteor2)#meteor degişkenlerini enemy sprite grubuna ekleme
        self.atmosferler.add(self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,self.a7,self.a8,self.y1,self.y2,self.y3,self.y4,self.y5,self.y6,self.y7,self.y8)
        
        self.reward=0
        self.total_reward=0
        self.done=False
        self.agent= DQLAgent()
        
        
        
    def mesafeBul(self,a,b):
        c=a-b
        return c
    
    def step(self,action):
        state_list=[]
        
        #UPDATE ET
        self.gemi.update(action)
        self.enemy.update()
        self.atmosferler.update()
        
        #Koordinat al
        next_gemi_state= self.gemi.getCoordinates()
        next_meteor1_state= self.meteor1.getCoordinates()
        next_meteor2_state= self.meteor2.getCoordinates()
            
        #Gemi ve meteorlar arasindaki x ve y koordinat mesafelerini bul ve state list e ekle.
        state_list.append(self.mesafeBul(next_gemi_state[0],next_meteor1_state[0]))
        state_list.append(self.mesafeBul(next_gemi_state[1],next_meteor1_state[1]))
        state_list.append(self.mesafeBul(next_gemi_state[0],next_meteor2_state[0]))
        state_list.append(self.mesafeBul(next_gemi_state[1],next_meteor2_state[1]))  
        
        return [state_list]# state'leri döndür.
        
    
    def initialStates(self):#HER BİR BÖLÜMÜN SONUNDA RESET
        #SPRITE /group
        self.all_sprite = pygame.sprite.Group() #Hareket eden bütün objelere daha kolay özellik eklemek için gruplandırmak.
        self.enemy= pygame.sprite.Group()
        self.atmosferler= pygame.sprite.Group()
        #Class değer atamaları:
        self.gemi = Gemi()
        self.meteor1=Meteor1()
        self.meteor2=Meteor2()
        self.y1=atm2();self.y2=atm2();self.y3=atm2();self.y4=atm2();self.y5=atm2();self.y6=atm2();self.y7=atm2();self.y8=atm2();
        #Bazı sprite ların özelliklerini değiştirme:
        self.a1= atm();self.a1.speedy= 25
        self.a2= atm();self. a2.speedy=25 
        self.a3= atm();self.a3.speedy=15
        self.a4= atm();self.a4.speedy=15
        self.a5= atm();self.a5.speedy=20
        self.a6= atm();self.a6.speedy=20
        self.a7= atm();self.a7.speedy=10
        self.a8= atm();self.a8.speedy=10
        self.all_sprite.add(self.gemi) #gemi objesini sprite grubuna eklemek
        self.all_sprite.add(self.meteor1,self.meteor2) #meteor1 objesini sprite grubuna eklemek ,meteor2 objesini sprite grubuna eklemek
        self.all_sprite.add(self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,self.a7,self.a8) #atmosfer(hüzme) ürünlerini sprite gruba eklemek.
        self.all_sprite.add(self.y1,self.y2,self.y3,self.y4,self.y5,self.y6,self.y7,self.y8) #atmosfer(yıldız) ürünlerini sprite gruba eklemek.
        self.enemy.add(self.meteor1,self.meteor2)#meteor degişkenlerini enemy sprite grubuna ekleme
    
        self.atmosferler.add(self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,self.a7,self.a8,self.y1,self.y2,self.y3,self.y4,self.y5,self.y6,self.y7,self.y8)
        
        self.t=0
        self.reward=0
        self.total_reward=0
        self.done=False
        
        
        state_list=[] #state lerin saklandığı dizi
        
        #Koordinat al
        gemi_state= self.gemi.getCoordinates()
        meteor1_state= self.meteor1.getCoordinates()
        meteor2_state= self.meteor2.getCoordinates()
            
        #Gemi ve meteorlar arasindaki x ve y koordinat mesafelerini bul ve state list e ekle.
        state_list.append(self.mesafeBul(gemi_state[0],meteor1_state[0]))
        state_list.append(self.mesafeBul(gemi_state[1],meteor1_state[1]))
        state_list.append(self.mesafeBul(gemi_state[0],meteor2_state[0]))
        state_list.append(self.mesafeBul(gemi_state[1],meteor2_state[1])) 
        
        return [state_list]# stateleri döndür
        
    def run(self):
        #OYUN ÇALIŞTIĞI SÜRECE TEKRARLANACAK FONKSİYONLAR

        
        state= self.initialStates()#state leri Environment dan al
        batch_size =2
        running = True
        while running:
            self.reward=2
            
            #İşlem Girişleri
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            #Update Etme
            action=self.agent.act(state)
            next_state= self.step(action)
            self.total_reward += self.reward 
            
            #sprite`lar etkileşim kuruyor ise:
            crash= pygame.sprite.spritecollide(self.gemi, self.enemy,True)
            if crash:
                self.t+=1#bolum
                self.reward = -40 #reward`i dusur.
                self.total_reward += self.reward #reward`i toplam reward`a ekle.
                self.done = True 
                
                running= False
                print("--TOPLANILAN ODUL--:", self.total_reward)
                

            #DEPOLAMA
            self.agent.remember(state,action,self.reward,next_state, self.done)
            
            #State Güncelleme:
            state= next_state
            
            #EGITIM
            self.agent.replay(batch_size)
            
            #Bir sonraki bolumde hangi action secilecegini karar veren metod(epsilon greedy):
            self.agent.adaptiveEGreedy()
                
            #Sprite'ları draw/show et 
            self.all_sprite.draw(screen)

            
            #Tüm ekranın içeriğini güncellemek.
            pygame.display.flip()
            #Clear
            screen.fill(Rsiyah)

            #idle sleep
            clock.tick(fps) #Birim zamanda (fps) adım gerçekleştir.
        pygame.quit()               
            
    def grafik(self,top_reward,zaman,bolum):
        
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        if bolum!=0:
            plt.title("{}. Bölüme Kadar Geçen Süre : {} sn".format(bolum,zaman))
        plt.xlabel('BÖLÜM SAYISI')
        plt.ylabel('TOPLAM REWARD')
        # plt.plot(scores)
        plt.plot(top_reward)
        plt.ylim(ymin=0)
        # plt.text(len(scores)-1, scores[-1], str(scores[-1]))
        plt.text(len(top_reward)-1, top_reward[-1], str(top_reward[-1]))
        plt.show(block=False)
        plt.pause(.1)                            

# MAIN LOOP
if __name__ == "__main__":
    env= Environment()
    ilkZaman=time.time()

    t=0 #Bölüm sayısını tutan değişken. 
    plot_total_rewards=[]#reward`larin tutulacagi liste

    while True:
        #ZAMANLAYICI
        gecenZaman=time.time()-ilkZaman
        gecenZaman = round(gecenZaman,2)
        print ("GECEN ZAMAN : ",gecenZaman)

        # GRAFIK ISLEMLERI
        plot_total_rewards.append(env.total_reward)
        env.grafik( plot_total_rewards , gecenZaman,t)

        #KACINCI BOLUME BASLANACAGINI YAZDIR
        t += 1 
        print ("BOLUM :" ,t)
        
        #Pygame başlat, pencere oluştur.
        pygame.init()
        screen = pygame.display.set_mode((Pgenislik,Pyukseklik))
        pygame.display.set_caption("Uzay X Oyunu")
        clock = pygame.time.Clock()
        
        env.run()


              