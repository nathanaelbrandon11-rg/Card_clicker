import pygame 
import time 
from random import randint

pygame.init()
 
warna_background = (200, 255, 255)
background = pygame.display.set_mode((500, 500))
background.fill(warna_background)
jam = pygame.time.Clock()

class area():
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color
    def color(self,newcolor):
        self.fill_color = newcolor
    def fill(self):
       pygame.draw.rect(background, self.fill_color, self.rect)
    def outline(self, frame_color, thickness):
       pygame.draw.rect(background, frame_color, self.rect, thickness)
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
class label(area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)


    def draw(self, shift_x, shift_y):
        self.fill()
        background.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


RED =  (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
cards = []
num_cards = 4

x = 70

for i in range(num_cards):
    new_card = label(x, 170, 70, 100, YELLOW)
    new_card.outline(BLUE, 10)
    new_card.set_text('KLIK', 32)
    cards.append(new_card)
    x = x + 100

wait = 0

while True:
    if wait == 0:
        wait = 20
        click = randint(1, num_cards)
        for i in range (num_cards):
            cards [i].color(YELLOW)
            if (i + 1) == click:
                cards [i].draw(10, 40)
            else:
                cards[i].fill()
    else:
        wait -= 1 
    for event in pygame.event.get():
       if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
           x, y = event.pos
           for i in range(num_cards):
               
               if cards[i].collidepoint(x,y):
                   if i + 1 == click: 
                       cards[i].color(GREEN)
                   else: 
                       cards[i].color(RED)

                   cards[i].fill()
       elif event.type == pygame.QUIT:
            pygame.quit()
            exit()           
    pygame.display.update()
    jam.tick(40)
pygame.quit()
