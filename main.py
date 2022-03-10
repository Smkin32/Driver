# Comms soon!
import pygame
import random
from os import path


class Title(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(path.join(img_dir, 'Title.png')).convert()
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 4)


class Button(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(path.join(img_dir, 'Button.png')).convert()
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 2)


class Car(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 65))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.lane = random.choice(lanes)
		lanes.remove(self.lane)
		self.spawning = True
		self.rect.midbottom = (self.lane, random.randrange(-200, -65))
		if self.lane > WIDTH / 2:
			self.image.blit(light, (0, 0))
			self.image.blit(light, (35, 0))
		else:
			self.image.blit(light, (0, 60))
			self.image.blit(light, (35, 60))
		self.speedy = 0

	def update(self):
		if self.rect.x > WIDTH / 2:
			self.speedy = 5
		elif self.rect.x < WIDTH / 2:
			self.speedy = 10

		if self.rect.top > 0 and self.spawning:
			lanes.append(self.lane)
			self.spawning = False
			self.lane = None

		if self.rect.top > HEIGHT:
			self.kill()
			car = Car()
			all_cars.add(car)
			all_sprites.add(car)

		self.rect.y += self.speedy


class Line(pygame.sprite.Sprite):
	def __init__(self, x, thk, striped):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((thk, HEIGHT * 2))
		if striped:
			stripe = pygame.Surface((thk, 30))
			stripe.fill(WHITE)
			for i in range(0, HEIGHT * 2, 60):
				self.image.blit(stripe, (0, i))
		else:
			self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.center = (x, HEIGHT / 2)

	def update(self):
		self.rect.y += 7
		if self.rect.centery > HEIGHT:
			self.rect.centery = 0


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 65))
		self.image.fill(BLUE)
		self.image.blit(light, (0, 0))
		self.image.blit(light, (35, 0))
		self.rect = self.image.get_rect()
		self.rect.midbottom = (WIDTH / 8 * 5, HEIGHT - 10)
		self.speedx = 0
		self.speedy = 0

	def update(self):
		self.speedx = 0
		self.speedy = 0

		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
			self.speedx = 0
		elif keys[pygame.K_LEFT]:
			self.speedx = -5
		elif keys[pygame.K_RIGHT]:
			self.speedx = 5

		if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
			self.speedy = 0
		elif keys[pygame.K_UP]:
			self.speedy = -5
		elif keys[pygame.K_DOWN]:
			self.speedy = 6

		self.rect.y += self.speedy
		self.rect.x += self.speedx

		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT


game_dir = path.dirname(__file__)
music_dir = path.join(game_dir, 'muz')
img_dir = path.join(game_dir, 'assets')

WIDTH = 360
HEIGHT = 600
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

light = pygame.Surface((15, 5))
light.fill(YELLOW)

pygame.init()

pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Driver")

clock = pygame.time.Clock()

running = True
while running:
	in_menu = True
	in_game = False

	startups = pygame.sprite.Group()
	start_button = Button()
	startups.add(start_button)
	title = Title()
	startups.add(title)

	pygame.mixer.music.load(path.join(music_dir, 'HM2_title.ogg'))
	pygame.mixer.music.play(-1)

	while in_menu:
		clock.tick(FPS)
		mouse = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				in_menu = False
				running = False
			if start_button.rect.collidepoint(mouse):
				start_button.image = pygame.image.load(path.join(img_dir, 'Button_active.png')).convert()
				if event.type == pygame.MOUSEBUTTONDOWN and start_button.rect.collidepoint(mouse):
					start_button.kill()
					title.kill()
					pygame.mixer.music.load(path.join(music_dir, 'Drive.ogg'))
					in_menu = False
					in_game = True
			else:
				start_button.image = pygame.image.load(path.join(img_dir, 'Button.png')).convert()

		screen.fill(BLACK)

		startups.draw(screen)

		pygame.display.flip()

	if not running:
		break

	lanes = [WIDTH / 8, WIDTH / 8 * 3, WIDTH / 8 * 5, WIDTH / 8 * 7]

	all_sprites = pygame.sprite.Group()
	all_lines = pygame.sprite.Group()
	all_cars = pygame.sprite.Group()

	midline = Line(WIDTH / 2, 10, False)
	qrt_line = Line(WIDTH / 4, 5, True)
	triqrt_line = Line(WIDTH / 4 * 3, 5, True)

	all_lines.add(midline, qrt_line, triqrt_line)
	all_sprites.add(all_lines)

	for i in range(3):
		car = Car()
		all_cars.add(car)
	all_sprites.add(all_cars)

	player = Player()
	all_sprites.add(player)

	pygame.mixer.music.play(loops=-1)

	while in_game:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				in_game = False

		all_sprites.update()

		hits = pygame.sprite.spritecollide(player, all_cars, False)
		if hits:
			in_game = False
			pygame.mixer.music.stop()
			for sprite in all_sprites.sprites():
				sprite.kill()

		screen.fill(BLACK)
		all_sprites.draw(screen)

		pygame.display.flip()

pygame.quit()
