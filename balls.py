import pygame
import random
import sys
import os

from head_pose import *

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
CODE = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]

rick_frame_count = -1
USE_FACE = True
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
YELLOW  = (255, 255, 0)
FPS = 60
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
BALL_RADIUS = 15
BREAK_EVENT = False
BREAK_TIMING = -1
BROKEN_TIMING = -1
BREAK_X = 0
BREAK_WIDTH = 0
speed = 0
accel = 0.6
decel = 0.5
counter = 0
BROKEN = False
pygame.mixer.init()
pygame.mixer.music.load("audio.mp3")
pygame.mixer.music.play(-1)


def draw_screen(balls):
    global counter
    global rick_frame_count
    screen.fill(WHITE)
    if BROKEN:
        pygame.draw.rect(screen, RED, basket)
    else:
        pygame.draw.rect(screen, BLUE, basket)
    for ball in balls:
        pygame.draw.circle(screen, RED, (ball["x"], ball["y"]), BALL_RADIUS)
    score_text = font.render(f"Điểm: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.draw.rect(screen, GRAY, button_rect)
    screen.blit(button_text, (button_rect.x + 15, button_rect.y + 8))
    arrow_start = (150, 60)
    arrow_end = (150 + counter * 10, 60)
    pygame.draw.line(screen, BLACK, arrow_start, arrow_end, 3)
    direc = 1 if counter > 0 else -1
    pygame.draw.polygon(screen, BLACK, [(arrow_end[0] - 10*direc, arrow_end[1] - 10), (arrow_end[0] - 10*direc, arrow_end[1] + 10), (arrow_end[0], arrow_end[1])])
    gio_text = font.render("Gió", True, BLACK)
    screen.blit(gio_text, (35 - gio_text.get_width() // 2, 45))
    if power_field:
        pygame.draw.rect(screen, [(204, 204, 0), (0, 153, 0), (0, 153, 153), (153, 0, 153)][power_type], power_field)
    if rick_frame_count > -1:
        #blit FRAMES/ffmpeg_{rick_frame_count}.bmp
        rick_frame = pygame.image.load(f"FRAMES/converted/ffmpeg_{rick_frame_count}.png")
        screen.blit(rick_frame, (0,0))
        rick_frame_count += 1
        if rick_frame_count == 125:
            rick_frame_count = -1
    if USE_FACE:
        frame = get_head_pose()
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
        #scale to 100x50
        frame_surface = pygame.transform.scale(frame_surface, (100, 50))
        screen.blit(frame_surface, (675, 75))
    button_color = GREEN if USE_FACE else RED
    pygame.draw.rect(screen, button_color, (10, 10, 100, 50))
    text = font.render('USE_FACE' if USE_FACE else 'NO_FACE', True, WHITE)
    screen.blit(text, (20, 25))
    
    pygame.display.flip()

def move_basket(keys):
    global speed
    global accel
    if not USE_FACE:
        if not (BROKEN or random.randint(0,100) < 5):
            if keys[pygame.K_LEFT] and basket.left > 0:
                speed -= accel
            if keys[pygame.K_RIGHT] and basket.right < SCREEN_WIDTH:
                speed += accel
    else:
        if not (BROKEN or random.randint(0,100) < 5):
            if get_face_result() <-20 and basket.left > 0:
                speed -= accel * -get_face_result()/10
            if get_face_result()>20 and basket.right < SCREEN_WIDTH:
                speed += accel * get_face_result()/10

def update_ball(balls):
    global score
    global counter
    global power_field
    global power_type
    for ball in balls:
        ball["y"] += ball["speed"]
        ball["x"] += ball["direction"]/360 * ball["speed"]  # Calculate horizontal movement
        ball["direction"] += counter
        if ball["direction"] < -100:
            ball["direction"]+=2
        if ball["direction"] > 100:
            ball["direction"]-=2
        if ball["y"] > SCREEN_HEIGHT:
            reset_ball(ball)
        if basket.collidepoint(ball["x"], ball["y"]) and not BROKEN:
            if ball["abnormal"]:
                score += 3
            else:
                score += 1
            reset_ball(ball)
        if ball["x"] < 0 or ball["x"] > SCREEN_WIDTH:
            ball["direction"] *= -1
        if power_field and not ball["abnormal"]:
            if power_field.collidepoint(ball["x"], ball["y"]):
                if power_type == 0:
                    #faster
                    ball["speed"]*=2
                    ball["abnormal"] = True
                    if random.randint(0,100) < 5:
                        power_field=None
                elif power_type == 1:
                    #teleport
                    ball["x"] = random.randint(0, SCREEN_WIDTH - BALL_RADIUS)
                    ball["abnormal"] = True
                    if random.randint(0,100) < 5:
                        power_field=None
                elif power_type== 2:
                    #duplicate
                    new_ball = {
                        "x": ball["x"],
                        "y": ball["y"],
                        "speed": ball["speed"],
                        "direction" : -ball["direction"],
                        "abnormal": True
                    }
                    balls.append(new_ball)
                    ball["abnormal"] = True
                    if random.randint(0,100) < 5:
                        power_field=None
                else:
                    #all of the above!
                    ball["speed"]*=2
                    ball["abnormal"] = True
                    new_ball = {
                        "x": random.randint(0, SCREEN_WIDTH - BALL_RADIUS),
                        "y": ball["y"],
                        "speed": ball["speed"],
                        "direction" : -ball["direction"],
                        "abnormal": True
                    }
                    balls.append(new_ball)
                    new_ball["direction"] = 0
                    new_ball["x"]=random.randint(0, SCREEN_WIDTH - BALL_RADIUS)
                    ball["x"] = random.randint(0, SCREEN_WIDTH - BALL_RADIUS)
                    balls.append(new_ball)
                    if random.randint(0,10) < 2:
                        power_field=None

def reset_ball(ball):
    global balls
    try:
        if len(balls) > 5:
            balls.remove(ball)
    except:
        pass
    ball["x"] = random.randint(0, SCREEN_WIDTH - BALL_RADIUS)
    ball["y"] = 0
    ball["speed"] += 0.2
    ball["speed"] = min(10, ball["speed"])
    ball["abnormal"] = False
    if len(balls) < 5:
        if random.randint(0, 50) < (10-len(balls)):
            new_ball = {
                "x": random.randint(0, SCREEN_WIDTH - BALL_RADIUS),
                "y": 0,
                "speed": random.uniform(3, 7),
                "direction" : random.randint(-100,100),
                "abnormal": False
            }
            balls.append(new_ball)
    if len(balls) > 1:
        if random.randint(0, 50) < len(balls)*2:
            try:
                balls.remove(ball)
            except:
                pass

def show_start_screen():
    screen.fill(WHITE)
    title_font = pygame.font.SysFont('arial', 40)
    title_text = title_font.render("Chào mừng đến với Game Hứng Bóng!", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    instruction_font = pygame.font.SysFont('arial', 20)
    instruction_text = instruction_font.render("Nhấn phím bất kỳ để bắt đầu...", True, BLACK)
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
code = []
index = 0
def main():
    global score
    global counter
    global BREAK_TIMING
    global BREAK_EVENT
    global BREAK_X
    global BREAK_WIDTH
    global BROKEN
    global BROKEN_TIMING
    global power_field
    global power_type
    global code
    global index
    global rick_frame_count
    show_start_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    global USE_FACE
                    USE_FACE = not USE_FACE
                if event.key == CODE[index]:
                    code.append(event.key)
                    index += 1
                    if code == CODE:
                        index = 0
                        print('Bingo!')
                        score = 100000000000
                else:
                    code = []
                    index = 0

        keys = pygame.key.get_pressed()
        if score == 100 and rick_frame_count == -1:
            rick_frame_count = 1
        global speed
        global decel
        if not any(keys):
            speed += decel * -((speed > 0) * 2 - 1)
        move_basket(keys)
        update_ball(balls)
        basket.move_ip(speed, 0)
        if basket.left < 0 or basket.right > SCREEN_WIDTH:
            speed = 0
            basket.left = max(0, basket.left)
            basket.right = min(SCREEN_WIDTH, basket.right)
        draw_screen(balls)
        #counter random waklk with pid, limit is +-5
        counter += random.randint(-1,1)/2
        if counter > 10:
            counter = 10
        if counter < -10:
            counter = -10
        if counter > 5:
            counter -= 0.3
        if counter < -5:
            counter += 0.3
        BREAK_TIMING -=1
        BROKEN_TIMING -=1
        if random.randint(0,10000) <score  and (not BREAK_EVENT) and (BROKEN_TIMING < FPS/2):
            BREAK_EVENT = True
            BREAK_TIMING =FPS*random.randint(1,5)
            BREAK_X = random.randint(0, SCREEN_WIDTH - 100)
            BREAK_WIDTH = random.randint(min(50+score,150), min(100 + score,600))
        if BREAK_EVENT and BREAK_TIMING > FPS/2:
            pygame.draw.rect(screen, DARK_GRAY, (BREAK_X, 0, BREAK_WIDTH, SCREEN_HEIGHT), 2)
        if BREAK_EVENT and BREAK_TIMING <= FPS/2:
            pygame.draw.rect(screen, RED, (BREAK_X, 0, BREAK_WIDTH, SCREEN_HEIGHT), 2)
        if BREAK_TIMING == 0:
            BREAK_EVENT = False
            BREAK_TIMING = -1
            pygame.draw.rect(screen, RED, (BREAK_X, 0, BREAK_WIDTH, SCREEN_HEIGHT))
            if basket.colliderect(pygame.Rect(BREAK_X, 0, BREAK_WIDTH, SCREEN_HEIGHT)):
                BROKEN = True
                BROKEN_TIMING = FPS*random.randint(3,8)
        if BROKEN_TIMING == 0:
            BROKEN = False
            BROKEN_TIMING = -1
        if random.randint(1,100000) < score and power_field == None:
            power_type = random.randint(0,3)
            power_field = pygame.Rect(random.randint(0, SCREEN_WIDTH - 10), random.randint(0,SCREEN_HEIGHT-200), 100, 50)

        if random.randint(1,300) <= 1:
            power_field= None
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("")
basket = pygame.Rect(SCREEN_WIDTH // 2 - BASKET_WIDTH // 2, SCREEN_HEIGHT - 50, BASKET_WIDTH, BASKET_HEIGHT)
balls = [] 
ball = {
    "x": random.randint(0, SCREEN_WIDTH - BALL_RADIUS),
    "y": 0,
    "speed": random.uniform(3, 5) ,
    "direction" : random.randint(-100,100),
    "abnormal": False
}
balls = [ball]

power_field = None
power_type = None
# 0: speed up
# 1: teleport
# 2: duplicate

score = 65

font = pygame.font.SysFont('arial', 24)

button_font = pygame.font.SysFont('arial', 15)
button_text = button_font.render("Thoát Game", True, WHITE)
button_rect = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40)

if __name__ == "__main__":
    main()
