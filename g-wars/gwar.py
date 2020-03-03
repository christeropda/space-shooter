import pygame, math
from precode2 import Vector2D
from config import *
from random import randrange

class Rocket(pygame.sprite.Sprite):
	def __init__(self, pos, speed, speed2):
		pygame.sprite.Sprite.__init__(self)
		self.img = pygame.image.load("img/blue.png")
		self.image = pygame.transform.scale(self.img, PLAYER_SIZE)
		self.copy = self.image
		self.rect = self.image.get_rect()
		self.rect.centerx = pos.x
		self.rect.centery = pos.y
		self.speed = speed
		self.angle = 0
		self.hp = 100
		self.ammo = 100000

	def shoot(self, key, projlist, sprlist):
		if key == True:
			if self.ammo > 0:
				projectile = Projectile(Vector2D((self.rect.centerx),(self.rect.centery)),Vector2D(self.speed2.x, self.speed2.y))
				sprlist.add(projectile)
				projlist.append(projectile)
				self.ammo -= 1

	def update(self):
		self.rect.centerx += self.speed.x
		self.rect.centery += self.speed.y

	def forward(self, key):
		angle = (self.angle + 90)
		rad = (math.pi/180) * angle

		x = math.cos(rad) 
		y = -math.sin(rad) 

		#adding x and y to fint top of ship
		tmpx = self.rect.centerx + x * 1.5
		tmpy = self.rect.centery + y * 1.5

		#desired = target - location
		speedx = (tmpx - self.rect.centerx)
		speedy = (tmpy - self.rect.centery)

		#if W/Key-up is pushed and has fuel, add to speed
		if key == True:
			self.speed += Vector2D(speedx, speedy)

		self.speed2 = Vector2D((speedx*20),(speedy*20))

	def backward(self, key):
		angle = (self.angle + 90)
		rad = (math.pi/180) * angle

		x = math.cos(rad) 
		y = -math.sin(rad) 

		#adding x and y to fint top of ship
		tmpx = self.rect.centerx + x * 1
		tmpy = self.rect.centery + y * 1

		#desired = target - location
		speedx = (tmpx - self.rect.centerx)*-1
		speedy = (tmpy - self.rect.centery)*-1

		#if W/Key-up is pushed and has fuel, add to speed
		if key == True:
			self.speed += Vector2D(speedx, speedy)
			

	def rotate(self, left, right):
		if left == True:
			self.angle = (self.angle + 10) % 360

			prev_center = self.rect.center

			self.image = pygame.transform.rotate(self.copy, self.angle)

			self.rect = self.image.get_rect()

			self.rect.center = prev_center

		if right == True:
			self.angle = (self.angle - 10) % 360
			
			prev_center = self.rect.center

			self.image = pygame.transform.rotate(self.copy, self.angle)

			self.rect = self.image.get_rect()

			self.rect.center = prev_center

	def edge(self):
		if self.rect.centerx >= SCREEN_W:
			self.speed.x -= 20
		if self.rect.centerx <= 0:
			self.speed.x += 20

		if self.rect.centery >= SCREEN_H:
			self.speed.y -= 20
		if self.rect.centery <= 0:
			self.speed.y += 20

	def max_speed(self):
		if self.speed.y > 10:
			self.speed.y = 10
		if self.speed.y < -10:
			self.speed.y = -10
		if self.speed.x > 10:
			self.speed.x = 10
		if self.speed.x < -10:
			self.speed.x = -10

	def handle_meteor_hit(self, obslist, sprlist):
		for meteor in obslist:
			col = pygame.sprite.collide_rect(self, meteor)
			if col == True:
				obslist.remove(meteor)
				sprlist.remove(meteor)
				self.hp -= 10

	def get_ammo(self, ammolist, sprlist, score):
		for ammo in ammolist:
			col = pygame.sprite.collide_rect(self, ammo)
			if col == True:
				ammolist.remove(ammo)
				sprlist.remove(ammo)
				self.ammo += 10
	

class Projectile(pygame.sprite.Sprite):
	def __init__(self, pos, speed):
		pygame.sprite.Sprite.__init__(self)
		self.img = pygame.image.load("img/bullet2.png")
		self.image = pygame.transform.scale(self.img, PROJ_SIZE)
		self.rect = self.image.get_rect()
		self.rect.centerx = pos.x
		self.rect.centery = pos.y
		self.speed = speed

	def update(self):
		self.rect.centerx += self.speed.x
		self.rect.centery += self.speed.y


class Obsticles(pygame.sprite.Sprite):
	def __init__(self, pos, speed):
		pygame.sprite.Sprite.__init__(self)
		self.img = pygame.image.load("img/meteor.png")
		self.image = pygame.transform.scale(self.img, OBS_SIZE)
		self.rect = self.image.get_rect()
		self.rect.centerx = pos.x
		self.rect.centery = pos.y 
		self.speed = speed

	def update(self):
		self.rect.centerx += self.speed.x
		self.rect.centery += self.speed.y

	def find_neighbour(self, boidlist, limit):
		"""
		takes  a list of objects as argument
		checks if the object is close enough to the "self"-boid be added to a list for all the close objects.
		returns this list.
		"""
		in_area = []

		for i in boidlist:
			if i is not self:
				if i.rect.centerx - self.rect.centerx > -limit and i.rect.centerx -self.rect.centerx < limit:
					if i.rect.centery  - self.rect.centery > -limit and i.rect.centery -self.rect.centery < limit:
						in_area.append(i)


		return in_area

	def seek_rocket(self, rocket, magnitude):
		"""
		makes the hoik seek the closest boid. finds the vector of the closest boid,
		normalises it, and adds a normalised "target" vector devided by a given magnitude
		to the speed of the hoik 
		"""
		#nearest = None
		#shortest = None
	

		
		#sum_x = rocket.rect.centerx - self.rect.centerx
		#sum_y = rocket.rect.centery - self.rect.centery

		try:
			vectorx = rocket.rect.centerx - self.rect.centerx
			vectory = rocket.rect.centery- self.rect.centery

			norm = math.sqrt((vectorx*vectorx)+(vectory*vectory))

			self.speed.x += (vectorx/norm) * 5 / magnitude 
			self.speed.y += (vectory/norm) * 5 / magnitude 
		except:
			ZeroDivisionError

	def separate(self, obslist, magnitude):
		in_area = self.find_neighbour(obslist, 30)
		
		sum_x = 0
		sum_y = 0 

		if len(in_area)>0:			
			for i in in_area:
				sum_x = self.rect.centerx - i.rect.centerx 
				sum_y = self.rect.centery - i.rect.centery

				try:
					normalize = -math.sqrt((sum_x*sum_x)+(sum_y*sum_y))

					self.speed.x -= (sum_x/normalize) * 5 / magnitude
					self.speed.y -= (sum_y/normalize) * 5 / magnitude
				except:
					ZeroDivisionError

	def intersect(self, obsticle, turnspeed):
		"""
		if the boid is close enough to the obsticle to be appended to the in_area list,
		the boids speed will be incremented, depending on where the boid is relative to the obsticle 
		"""
		in_area = self.find_neighbour(obsticle, 70)
		
		for i in in_area:
			if i.pos_vec.x - self.pos_vec.x > 0:
				i.speed.x += turnspeed
			else:
				i.speed.x -= turnspeed
			if i.pos_vec.y - self.pos_vec.y > 0:
				i.speed.y += turnspeed
			else:
				i.speed.y -= turnspeed

	def max_speed(self):
		if self.speed.y > 5:
			self.speed.y = 5
		if self.speed.y < -5:
			self.speed.y = -5
		if self.speed.x > 5:
			self.speed.x = 5
		if self.speed.x < -5:
			self.speed.x = -5

class Ammo(pygame.sprite.Sprite):
	def __init__(self, pos, speed):
		pygame.sprite.Sprite.__init__(self)
		self.img = pygame.image.load("img/ammo.png")
		self.image = pygame.transform.scale(self.img, AMMO_SIZE)
		self.rect = self.image.get_rect()
		self.rect.centerx = pos.x
		self.rect.centery = pos.y 
		self.speed = speed

	def update(self):
		self.rect.centerx += self.speed.x
		self.rect.centery += self.speed.y


class Game():
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Geometric War Clone")

		self.background = pygame.image.load("img/stars.png")
		self.image = pygame.transform.scale(self.background,(SCREEN_W,SCREEN_H))
		self.background_rect = self.image.get_rect()

		self.done = False
		self.score = 0

	def handle_events(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.done = True

			if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
				self.left = True
			if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
				self.left = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
				self.right = True
			if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
				self.right = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				self.forward = True
			if event.type == pygame.KEYUP and event.key == pygame.K_UP:
				self.forward = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				self.stop = True
			if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
				self.stop = False

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.shoot = True
			if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
				self.shoot = False

				#projectile = Projectile(Vector2D((self.rocket.rect.centerx),(self.rocket.rect.centery)),Vector2D(self.rocket.speed2.x, self.rocket.speed2.y))
				#self.all_sprites.add(projectile)
				#self.all_proj.append(projectile)

	def handle_events2(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.setup()
				self.done = True

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.setup()


	def spawn_obs(self):
		if len(self.all_obs) < 10:
			obs = Obsticles(Vector2D(randrange(0,SCREEN_W),-10),Vector2D(randrange(-10,10), randrange(2,10)))
			self.all_sprites.add(obs)
			self.all_obs.append(obs)

	def spawn_ammo(self):
		if len(self.ammoList) == 0:
			rand = randrange(0,10000)
			if rand < 150:
				ammo = Ammo(Vector2D(randrange(0,SCREEN_W),-10),Vector2D(randrange(-10,10), randrange(2,10)))
				self.all_sprites.add(ammo)
				self.ammoList.append(ammo)

	def delete_object(self, sprlist, objlist):
		for obj in objlist:
			try:
				if obj.rect.centerx > (SCREEN_W+50):
					sprlist.remove(obj)
					objlist.remove(obj)
				if obj.rect.centerx < -50:
					sprlist.remove(obj)
					objlist.remove(obj)
				if obj.rect.centery > (SCREEN_H+50):
					sprlist.remove(obj)
					objlist.remove(obj)
				if obj.rect.centery < -50:
					sprlist.remove(obj)
					objlist.remove(obj)
			except ValueError:
				continue

	def handle_bullet_hit(self):
		for bullet in self.all_proj:
			for meteor in self.all_obs:
				col = pygame.sprite.collide_rect(bullet, meteor)
				if col == True:
					try:
						self.all_proj.remove(bullet)
						self.all_obs.remove(meteor)
						self.all_sprites.remove(bullet)
						self.all_sprites.remove(meteor)
						self.score += 1
					except ValueError:
						continue

	def print_score_hp(self, rocket):
		"""
		printing the score of the given player
		"""
		myfont = pygame.font.SysFont("monospace", 30)
		
		score = myfont.render("score: {0}".format(self.score) ,1, (250,250,250))
		hp = myfont.render("hp: {0}".format(rocket.hp) ,1, (250,250,250))
		shot = myfont.render("Ammo: {0}".format(rocket.ammo) ,1, (250,0,0))
		
		self.screen.blit(score, (100,20))
		self.screen.blit(hp, (300,20))
		self.screen.blit(shot, (500,20))

	def check_loss(self, rocket):
		myfont = pygame.font.SysFont("monospace", 30)

		if rocket.hp <= 0:
			self.win = True


		while self.win == True:
			self.handle_events2()

			self.screen.fill((0,0,0))

			game = myfont.render("Game Over!" ,1, (250,250,250))
			score = myfont.render("score: {}".format(self.score), 1, (250,250,250))
			self.screen.blit(game, (500,300))
			self.screen.blit(score, (500, 400))

			pygame.display.flip()

		

	def setup(self):

		self.left = False
		self.right = False
		self.forward = False
		self.stop = False
		self.shoot = False
		self.win = False

		self.score = 0

		self.rocket = Rocket(Vector2D((SCREEN_W/2),(SCREEN_H/2)),Vector2D(0,0), Vector2D(0,0))

		self.all_sprites = pygame.sprite.Group()
		self.all_proj = []
		self.all_obs = []
		self.ammoList = []

		self.all_sprites.add(self.rocket)

	def run(self):
		self.setup()

		while not self.done:
			self.handle_events()
			self.time_passed = self.clock.tick(30)
			self.screen.blit(self.image,self.background_rect)

			self.rocket.rotate(self.left, self.right)
			self.rocket.forward(self.forward)
			self.rocket.backward(self.stop)
			self.rocket.edge()
			self.rocket.max_speed() 
			self.rocket.shoot(self.shoot, self.all_proj, self.all_sprites)
			self.rocket.get_ammo(self.ammoList, self.all_sprites, self.score)

			self.spawn_obs()

			for i in self.all_obs:
				i.seek_rocket(self.rocket, 2)
				i.separate(self.all_obs, 1.5)
				i.max_speed()

			self.spawn_ammo()
			self.delete_object(self.all_sprites, self.all_proj)
			self.delete_object(self.all_sprites, self.all_obs)
			self.delete_object(self.all_sprites, self.ammoList)

			self.handle_bullet_hit()
			self.rocket.handle_meteor_hit(self.all_obs, self.all_sprites)

			self.print_score_hp(self.rocket)

			self.check_loss(self.rocket)

			self.all_sprites.update()
			self.all_sprites.draw(self.screen)

			pygame.display.flip()

if __name__ == '__main__':
	game = Game() 
	game.run()
