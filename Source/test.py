import pygame
from time import sleep
pygame.init()

s1 = pygame.display.set_mode((500,500))
s2 = pygame.Surface((200,60))
s2.fill((255,255,255))
pygame.draw.rect(s2, (0,255,0), (0,0,30,25))
s1.blit(s2, (10,10))
pygame.draw.circle(s2, (255,0,0), (10, 10), 10)
s1.blit(s2, (10,10))
pygame.display.update()
sleep(10)