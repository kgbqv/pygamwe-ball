import pygame
import random
import sys
import os
import math

from head_pose import *

import time
import random


previous_time = time.time()

def track_fps():
    global previous_time
    current_time = time.time()
    delta_time = current_time - previous_time
    previous_time = current_time
    fps = 1.0 / delta_time if delta_time > 0 else 0
    return fps
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
CODE = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]

running = False
prev_result = 0
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
FRAME_COUNTER = 0
stats = {}
speed = 0
accel = 0.6
decel = 0.5
counter = 0
volume = 1.0
BROKEN = False
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.mixer.quit()
pygame.mixer.init()
pygame.mixer.music.load("menu.mp3")
pygame.mixer.music.play(-1)
sound_files = [f"effect/eff-{i:02d}.wav" for i in range(1, 7)]
sounds = [pygame.mixer.Sound(file) for file in sound_files]

def draw_main_menu():
    screen.fill(WHITE)
    title_font = pygame.font.SysFont('arial', 40)
    option_font = pygame.font.SysFont('arial', 30)

    title_text = title_font.render("Main Menu", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    start_text = option_font.render("1. Start Game", True, BLACK)
    options_text = option_font.render("2. Options", True, BLACK)
    help_text = option_font.render("3. Help", True, BLACK)
    stat_text = option_font.render("4. Statistics", True, BLACK)
    quit_text = option_font.render("5. Quit", True, BLACK)

    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 200))
    screen.blit(options_text, (SCREEN_WIDTH // 2 - options_text.get_width() // 2, 250))
    screen.blit(help_text, (SCREEN_WIDTH // 2 - help_text.get_width() // 2, 300))
    screen.blit(stat_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 350))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 400))

    pygame.display.flip()
def update_stats():
    global stats
    global score
    global stun_count
    stats["last_score"] = str(score)
    stats["high_score"] = str(max(score, int(stats.get("high_score", "0"))))
    stats["total_score"] = str(int(stats.get("total_score", "0")) + score)
    stats["stun_count"] = str(int(stats.get("stun_count", "0")) + stun_count)
    stats["hist_score"] = str(eval(stats.get("hist_score", "[]")) + [score])

    with open("statistics.txt", "w") as f:
        for key, value in stats.items():
            f.write(f"{key} {value}\n")
    score = 0
def draw_stats_menu():
    global stats
    screen.fill(WHITE)
    title_font = pygame.font.SysFont('arial', 40)
    option_font = pygame.font.SysFont('arial', 30)

    title_text = title_font.render("Statistics", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    stats_text = option_font.render("1. Last Score: " + stats.get("last_score", "0"), True, BLACK)
    stats1_text = option_font.render("2. Best Score: " + stats.get("high_score", "0"), True, BLACK)
    stats2_text = option_font.render("3. Total Score: " + stats.get("total_score", "0"), True, BLACK)
    stats3_text = option_font.render("4. Total Stuns: " + stats.get("stun_count", "0"), True, BLACK)
    stats4_text = option_font.render("You have found the secret!" if stats.get("secret") != "0" else "You haven't found the secret", True, BLACK)
    
    
    if False:
        hist = eval(stats.get("hist_score"))
        hist = [int(x) for x in hist]
        bar_width = (SCREEN_WIDTH-100) // len(hist)
        x = 0
        y = SCREEN_HEIGHT - int(stats.get("high_score"))
        bar_color = BLUE
        for i, score in enumerate(hist):
            bar_height = int((score / int(stats.get("high_score"))) *int(stats.get("high_score")))
            bar_x = 50 + x + i * bar_width
            bar_y = y + (int(stats.get("high_score")) - bar_height)
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_width, bar_height))

    back_text = option_font.render("Press B to go back", True, BLACK)

    screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, 100))
    screen.blit(stats1_text, (SCREEN_WIDTH // 2 - stats1_text.get_width() // 2, 150))
    screen.blit(stats2_text, (SCREEN_WIDTH // 2 - stats2_text.get_width() // 2, 200))
    screen.blit(stats3_text, (SCREEN_WIDTH // 2 - stats3_text.get_width() // 2, 250))
    screen.blit(stats4_text, (SCREEN_WIDTH // 2 - stats4_text.get_width() // 2, 300))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 350))
    pygame.display.flip()
def draw_options_menu():
    screen.fill(WHITE)
    title_font = pygame.font.SysFont('arial', 40)
    option_font = pygame.font.SysFont('arial', 30)

    title_text = title_font.render("Options", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    volume_text = option_font.render(f"Volume: {int(volume * 100)}%", True, BLACK)
    controls1_text = option_font.render("Controls: Arrow keys to move", True, BLACK)
    controls2_text = option_font.render("F to toggle face tracking, look left/right to move.", True, BLACK)
    controls3_text = option_font.render("M to return to the main menu", True, BLACK)
    controls4_text = option_font.render("Up/Down to adjust volume (only in options)", True, BLACK)
    controls5_text = option_font.render("Q to change webcam (also only here)", True, BLACK)
    back_text = option_font.render("Press B to go back", True, BLACK)

    screen.blit(volume_text, (SCREEN_WIDTH // 2 - volume_text.get_width() // 2, 100))
    screen.blit(controls1_text, (SCREEN_WIDTH // 2 - controls1_text.get_width() // 2, 150))
    screen.blit(controls2_text, (SCREEN_WIDTH // 2 - controls2_text.get_width() // 2, 200))
    screen.blit(controls3_text, (SCREEN_WIDTH // 2 - controls3_text.get_width() // 2, 250))
    screen.blit(controls4_text, (SCREEN_WIDTH // 2 - controls4_text.get_width() // 2, 300))
    screen.blit(controls5_text, (SCREEN_WIDTH // 2 - controls5_text.get_width() // 2, 350))
    frame = head_pose.get_head_pose()
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
    frame_surface = pygame.transform.scale(frame_surface, (100, 50))
    screen.blit(frame_surface, (SCREEN_WIDTH//2 -50, 400))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 450))

    pygame.display.flip()
def draw_help_menu():
    screen.fill(WHITE)
    title_font = pygame.font.SysFont('arial', 40)
    option_font = pygame.font.SysFont('arial', 30)

    title_text = title_font.render("Help Menu", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    help_text = option_font.render("1. How to play", True, BLACK)
    help1_text = option_font.render("- Use the arrow keys to move the basket sideways", True, BLACK)
    help2_text = option_font.render("- Catch the balls to score points", True, BLACK)
    help3_text = option_font.render("- Avoid the beams, they stun you", True, BLACK)
    help4_text = option_font.render("- Power zones spawn randomly", True, BLACK)
    help5_text = option_font.render("- Power zones have random functionalities,", True, BLACK)
    help6_text = option_font.render("ranging from speeding up the balls to duplicating them", True, BLACK)
    help7_text = option_font.render("Next, head to the options menu", True, BLACK)
    back_text = option_font.render("Press B to go back", True, BLACK)

    screen.blit(help_text, (SCREEN_WIDTH // 2 - help_text.get_width() // 2, 100))
    screen.blit(help1_text, (SCREEN_WIDTH // 2 - help1_text.get_width() // 2, 150))
    screen.blit(help2_text, (SCREEN_WIDTH // 2 - help2_text.get_width() // 2, 200))
    screen.blit(help3_text, (SCREEN_WIDTH // 2 - help3_text.get_width() // 2, 250))
    screen.blit(help4_text, (SCREEN_WIDTH // 2 - help4_text.get_width() // 2, 300))
    screen.blit(help5_text, (SCREEN_WIDTH // 2 - help5_text.get_width() // 2, 350))
    screen.blit(help6_text, (SCREEN_WIDTH // 2 - help6_text.get_width() // 2, 400))
    screen.blit(help7_text, (SCREEN_WIDTH // 2 - help7_text.get_width() // 2, 450))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 500))

    pygame.display.flip()

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
    
    if USE_FACE:
        frame = head_pose.get_head_pose()
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
        frame_surface = pygame.transform.scale(frame_surface, (100, 50))
        screen.blit(frame_surface, (675, 75))
    button_color = GREEN if USE_FACE else RED
    pygame.draw.rect(screen, button_color, (10, 90, 140, 50))
    text = font.render('USE_FACE' if USE_FACE else 'NO_FACE', True, WHITE)
    screen.blit(text, (20, 95))
    fps = track_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, BLACK)
    screen.blit(fps_text, (10, SCREEN_HEIGHT - 30))
    if rick_frame_count > -1:
        screen.fill(BLACK)
        rick_frame = pygame.image.load(f"FRAMES/converted/ffmpeg_{rick_frame_count}.png")
        rick_frame = pygame.transform.scale(rick_frame, (SCREEN_WIDTH, SCREEN_HEIGHT/1.5))
        screen.blit(rick_frame, (0,0+SCREEN_HEIGHT/6))
        rick_frame_count += 1
        print(rick_frame_count)
        if rick_frame_count == 125:
            print(FRAME_COUNTER)
            if FRAME_COUNTER %7==0:
                rick_frame_count = -1
            else:
                rick_frame_count = 1
    pygame.display.flip()

def move_basket(keys):
    global speed
    global accel
    global prev_result
    if not USE_FACE:
        if not (BROKEN or random.randint(0,100) < 5):
            if keys[pygame.K_LEFT] and basket.left > 0:
                speed -= accel
            if keys[pygame.K_RIGHT] and basket.right < SCREEN_WIDTH:
                speed += accel
    else:
        if FRAME_COUNTER % 5 == 0:
            prev_result = head_pose.get_face_result()
        if not (BROKEN or random.randint(0,100) < 5):
            if prev_result < -20 and basket.left > 0:
                speed -= accel * -prev_result/10
            if prev_result > 20 and basket.right < SCREEN_WIDTH:
                speed += accel * prev_result/10

def update_ball(balls):
    global score
    global counter
    global power_field
    global power_type
    for ball in balls:
        ball["y"] += ball["speed"]
        ball["x"] += ball["direction"]/360 * ball["speed"]
        ball["direction"] += counter
        change = 15/(1+math.e**(0.05*score))+1
        if ball["direction"] < -100:
            ball["direction"]+=change
        if ball["direction"] > 100:
            ball["direction"]-=change
        if ball["y"] > SCREEN_HEIGHT:
            reset_ball(ball)
        if basket.collidepoint(ball["x"], ball["y"]) and not BROKEN:
            sound = random.choice(sounds)
            sound.play()
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
    ball["speed"] = min(10/(1+math.e**(-0.05*score)), ball["speed"])
    if random.randint(0,100) < 5:
        ball["speed"] = 5
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
        if random.randint(0, 50) < len(balls)*2.5:
            try:
                balls.remove(ball)
            except:
                pass

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
    global stats
    global stun_count
    global FRAME_COUNTER
    menu_running = True
    options_running = False
    help_running = False
    running = False
    stats_running = False
    global volume
    with open("statistics.txt", "r") as f:
        lines = f.readlines()
        stats = {line.split()[0]: ' '.join(line.split()[1:]) for line in lines}
    while True:
        if menu_running:
            draw_main_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    update_stats()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        running = True
                        menu_running = False
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("game.mp3")
                        pygame.mixer.music.play(-1)
                    elif event.key == pygame.K_2:
                        options_running = True
                        menu_running = False
                    elif event.key == pygame.K_3:
                        help_running = True
                        menu_running = False
                    elif event.key == pygame.K_5:
                        menu_running = False
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_4:
                        stats_running = True
                        menu_running = False
        if stats_running:
            draw_stats_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stats_running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        stats_running = False
                        menu_running = True
                    
        if options_running:
            draw_options_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    options_running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        volume = min(1.0, volume + 0.1)
                        pygame.mixer.music.set_volume(volume)
                    elif event.key == pygame.K_DOWN:
                        volume = max(0.0, volume - 0.1)
                        pygame.mixer.music.set_volume(volume)
                    elif event.key == pygame.K_b:
                        options_running = False
                        menu_running = True
                    elif event.key == pygame.K_q:
                        head_pose.change_webcam()
        if help_running:
            draw_help_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    help_running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        help_running = False
                        menu_running = True
        if running:
            FRAME_COUNTER+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        running = False
                        update_stats()
                        pygame.quit()
                        sys.exit()
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
                            score = 1000
                            stats["secret"] = "1"
                    else:
                        code = []
                        index = 0
                    if event.key == pygame.K_m:
                        running = False
                        menu_running = True
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("menu.mp3")
                        pygame.mixer.music.play(-1)
                        update_stats()
            keys = pygame.key.get_pressed()
            if score == 100 and rick_frame_count == -1:
                rick_frame_count = 1
                score+=1
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
            if FRAME_COUNTER % 5 == 0:
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
            if rick_frame_count < 0:
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
                        stun_count += 1
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
head_pose = HeadPoseDetector()
power_field = None
power_type = None
# 0: speed up
# 1: teleport
# 2: duplicate
score = 0
stun_count = 0

font = pygame.font.SysFont('arial', 24)

button_font = pygame.font.SysFont('arial', 15)
button_text = button_font.render("Thoát Game", True, WHITE)
button_rect = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40)

if __name__ == "__main__":
    main()
