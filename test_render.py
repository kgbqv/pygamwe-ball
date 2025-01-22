import pygame
import math

class RadialMenu:
    def __init__(self, center, radius, items, font):
        self.center = center
        self.radius = radius
        self.items = items
        self.font = font
        self.current_angle = 0
        self.target_angle = 0

    def render(self, screen):
        segment_angle = 360 / len(self.items)
        for i, item in enumerate(self.items):
            start_angle = self.current_angle + i * segment_angle
            end_angle = self.current_angle + (i + 1) * segment_angle
            #pygame.draw.arc(screen, SEGMENT_COLOR, (self.center[0] - self.radius, self.center[1] - self.radius, self.radius * 2, self.radius * 2), math.radians(start_angle), math.radians(end_angle), 2)
            self.draw_text_at_angle(screen, item, self.center, self.radius, start_angle, self.font, TEXT_COLOR)
        pygame.draw.circle(screen, CENTER_COLOR, self.center, CENTER_RADIUS)
        diff = self.get_angle_difference(self.current_angle, self.target_angle)
        if diff != 0:
            self.current_angle += ANIMATION_SPEED if diff > 0 else -ANIMATION_SPEED
        self.current_angle %= 360

    def update(self, key):
        if key == pygame.K_LEFT:
            self.target_angle += 360 / len(self.items)
        elif key == pygame.K_RIGHT:
            self.target_angle -= 360 / len(self.items)
        self.target_angle %= 360

    def get_index(self):
        segment_angle = 360 / len(self.items)
        index = int((self.target_angle % 360) / segment_angle)
        if index ==0:
            return index
        else:
            return len(self.items) - index

    def draw_text_at_angle(self, surface, text, center, radius, angle, font, color):
        x = center[0] + radius * math.cos(math.radians(angle))
        y = center[1] - radius * math.sin(math.radians(angle))
        rendered_text = font.render(text, True, color)
        angle = angle % 360
        if angle > 180:
            angle -= 360
        if angle < 90 and angle > -90:
            rendered_text = pygame.transform.scale(rendered_text, ((int((1.5 - 2 * abs(angle) / 180) * rendered_text.get_width())), int((1.5 - 2 * abs(angle) / 180) * rendered_text.get_height())))
            rendered_text = pygame.transform.rotate(rendered_text, angle/2)
            surface.blit(rendered_text, rendered_text.get_rect(center=(x, y)))

    def get_angle_difference(self, current, target):
        diff = (target - current + 180) % 360 - 180
        return diff if diff != -180 else 180

# Usage example:
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6"]
BACKGROUND_COLOR = (30, 30, 30)
SEGMENT_COLOR = (255, 0, 0)
CENTER_COLOR = (50, 50, 50)
TEXT_COLOR = (0,0,0)
MENU_RADIUS = 200
CENTER_RADIUS = 40
CENTER_POSITION = (0, HEIGHT // 2)
ANIMATION_SPEED = 2
font = pygame.font.SysFont("Arial", 50)

radial_menu = RadialMenu(CENTER_POSITION, MENU_RADIUS, items, font)

while False:
    screen.fill(BACKGROUND_COLOR)
    radial_menu.render(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            radial_menu.update(event.key)
            if event.key == pygame.K_RETURN:
                print(radial_menu.items[radial_menu.get_index()])
    pygame.display.flip()
    pygame.time.Clock().tick(60)
