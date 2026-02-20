import pygame 
import time 
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
class label(area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)


    def draw(self, shift_x, shift_y):
        self.fill()
        background.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))



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


while True:
    background.fill(warna_background)
    for card in cards:
        card.draw(10, 30)

    pygame.display.update()
    jam.tick(40)

