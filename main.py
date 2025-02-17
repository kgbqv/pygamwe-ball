import pygame
import random
import sys
import os
import math
import pygame.gfxdraw
from test_render import RadialMenu

import time
import random
from PIL import Image, ImageFilter

def preprop_img():
    for i in range(1, 3):
        img = Image.open(f"bavkgrounds/{i}.png")
        img = img.filter(ImageFilter.GaussianBlur(2))
        img = img.point(lambda p: p * 0.7)
        #create a new image file
        img.save(f"tmp/bavkgrounds/{i}.png")
    img = Image.open("bavkgrounds/3.png")
    img.save("tmp/bavkgrounds/3.png")

preprop_img()
previous_time = time.time()
internal_score = 0
def get_rank(curr_heat):
    if curr_heat > 32:
        return "SSS"
    elif curr_heat > 26:
        return "SS"
    elif curr_heat > 16:
        return "S"
    elif curr_heat > 12:
        return "A"
    elif curr_heat > 8:
        return "B"
    elif curr_heat > 5:
        return "C"
    else:
        return "D"

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
currstage = 1
CODE = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]
def draw_rotated_rect(surface, color, center, size, angle):
    half_width, half_height = size[0] / 2, size[1] / 2
    angle_rad = math.radians(angle)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    points = [
        (center[0] + half_width * cos_angle - half_height * sin_angle, center[1] + half_width * sin_angle + half_height * cos_angle),
        (center[0] - half_width * cos_angle - half_height * sin_angle, center[1] - half_width * sin_angle + half_height * cos_angle),
        (center[0] - half_width * cos_angle + half_height * sin_angle, center[1] - half_width * sin_angle - half_height * cos_angle),
        (center[0] + half_width * cos_angle + half_height * sin_angle, center[1] + half_width * sin_angle - half_height * cos_angle)
    ]
    pygame.gfxdraw.filled_polygon(surface, points, color)
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
minimal = False
stats = {}
speed = 0
accel = 0.6
decel = 0.5
speed2=0
counter = 0
powerop_list = []
volume = 0
BROKEN = False
MAGNETIC_CATCH = False
DECREASE_STUN = 0
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.mixer.quit()
pygame.mixer.init()
pygame.mixer.music.load("menu.mp3")
pygame.mixer.music.play(-1)
sound_files = [f"effect/eff-{i:02d}.wav" for i in range(1, 7)]
sounds = [pygame.mixer.Sound(file) for file in sound_files]
curr_heat = 40
if not minimal:
    from head_pose import *
class bullet:
    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
    def update(self):
        self.x += self.speed * math.sin(math.radians(self.direction))
        self.y -= self.speed * math.cos(math.radians(self.direction))

def draw_main_menu():
    screen.fill(WHITE)
    title_font = pygame.font.SysFont('arial', 40)
    option_font = pygame.font.SysFont('arial', 30)
    img = pygame.image.load("mainbg.png")
    screen.blit(img, (0,0))
    main_radbar.render(screen)

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
    internal_score = 0
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
    if not minimal:
        controls5_text = option_font.render("Q to change webcam (also only here)", True, BLACK)
    controls6_text = option_font.render("Space to shoot while in boss mode", True, BLACK)
    back_text = option_font.render("Press B to go back", True, BLACK)

    screen.blit(volume_text, (SCREEN_WIDTH // 2 - volume_text.get_width() // 2, 100))
    screen.blit(controls1_text, (SCREEN_WIDTH // 2 - controls1_text.get_width() // 2, 150))
    screen.blit(controls2_text, (SCREEN_WIDTH // 2 - controls2_text.get_width() // 2, 200))
    screen.blit(controls3_text, (SCREEN_WIDTH // 2 - controls3_text.get_width() // 2, 250))
    screen.blit(controls4_text, (SCREEN_WIDTH // 2 - controls4_text.get_width() // 2, 300))
    if not minimal:
        screen.blit(controls5_text, (SCREEN_WIDTH // 2 - controls5_text.get_width() // 2, 350))
    screen.blit(controls6_text, (SCREEN_WIDTH // 2 - controls6_text.get_width() // 2, 400))
    if not minimal:
        frame = head_pose.get_head_pose()
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
        frame_surface = pygame.transform.scale(frame_surface, (100, 50))
        screen.blit(frame_surface, (SCREEN_WIDTH//2 -50, 450))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 500))

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
    help7_text = option_font.render("- You can use space to shoot bullets", True, BLACK)
    help8_text = option_font.render("Next, head to the options menu", True, BLACK)
    back_text = option_font.render("Press B to go back", True, BLACK)

    screen.blit(help_text, (SCREEN_WIDTH // 2 - help_text.get_width() // 2, 100))
    screen.blit(help1_text, (SCREEN_WIDTH // 2 - help1_text.get_width() // 2, 150))
    screen.blit(help2_text, (SCREEN_WIDTH // 2 - help2_text.get_width() // 2, 200))
    screen.blit(help3_text, (SCREEN_WIDTH // 2 - help3_text.get_width() // 2, 250))
    screen.blit(help4_text, (SCREEN_WIDTH // 2 - help4_text.get_width() // 2, 300))
    screen.blit(help5_text, (SCREEN_WIDTH // 2 - help5_text.get_width() // 2, 350))
    screen.blit(help6_text, (SCREEN_WIDTH // 2 - help6_text.get_width() // 2, 400))
    screen.blit(help7_text, (SCREEN_WIDTH // 2 - help7_text.get_width() // 2, 450))
    screen.blit(help8_text, (SCREEN_WIDTH // 2 - help8_text.get_width() // 2, 500))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 550))

    pygame.display.flip()

def draw_screen(balls):
    global currstage
    global counter
    global speed
    global rick_frame_count
    global curr_heat
    global BLACK
    global WHITE
    if score < 20:
        #load background
        screen.fill(WHITE)
        img = pygame.image.load("tmp/bavkgrounds/1.png")
        screen.blit(img, (0,0))
    elif score < 50:
        screen.fill(WHITE)
        img = pygame.image.load("tmp/bavkgrounds/2.png")
        screen.blit(img, (0,0))
    else:
        screen.fill(WHITE)
        img = pygame.image.load("tmp/bavkgrounds/3.png")
        screen.blit(img, (0,0))
    global font
    basket_dir = speed
    if BROKEN:
        draw_rotated_rect(screen, RED, basket.center, (BASKET_WIDTH, BASKET_HEIGHT), basket_dir)
    else:
        draw_rotated_rect(screen, BLUE, basket.center, (BASKET_WIDTH, BASKET_HEIGHT), basket_dir)
    if currstage != 3:
        for ball in balls:
            pygame.draw.circle(screen, RED, (ball["x"], ball["y"]), BALL_RADIUS)
    else:
        WHITE, BLACK = BLACK, WHITE
        #simulate flashlight
        if not BROKEN:
            for ball in balls:
                dist = math.sqrt((ball["x"] - basket.centerx)**2 + (ball["y"] - basket.centery)**2)
                if dist < 200:
                    pygame.draw.circle(screen, RED, (ball["x"], ball["y"]), BALL_RADIUS)
            #also draw a light beam, partially transparent
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            s.set_alpha(128)
            pygame.draw.circle(s, WHITE, basket.center, 200)
            screen.blit(s, (0,0))
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
    heat = get_rank(curr_heat)
    heat_text = font.render(f"Rank:", True, (44,44,44))
    rank_font = pygame.font.SysFont('arial', 72)
    rank_font.set_bold(True)
    rank_color = (255, 215, 0) if heat == "SSS" else (255, 0, 0) if heat == "SS" else (205, 127, 50) if heat == "S" else (0, 128, 0) if heat == "A" else (0, 0, 255) if heat == "B" else (255, 0, 255) if heat == "C" else (128, 0, 128)
    rank_text = rank_font.render(heat, True, rank_color)
    shadow_text = rank_font.render(heat, True, (200,200,200))
    shake = random.randint(-curr_heat//6,curr_heat//6)
    screen.blit(shadow_text, (SCREEN_WIDTH - rank_text.get_width()+shake, SCREEN_HEIGHT - rank_text.get_height()+shake))
    screen.blit(heat_text, (SCREEN_WIDTH - heat_text.get_width() - rank_text.get_width()-5, SCREEN_HEIGHT - heat_text.get_height()-5))
    screen.blit(rank_text, (SCREEN_WIDTH - rank_text.get_width()-5+shake, SCREEN_HEIGHT - rank_text.get_height()-5+shake))
    if power_field:
        pygame.draw.rect(screen, [(204, 204, 0), (0, 153, 0), (0, 153, 153), (153, 0, 153)][power_type], power_field)
    
    if USE_FACE and not minimal:
        frame = head_pose.get_head_pose()
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
        frame_surface = pygame.transform.scale(frame_surface, (100, 50))
        screen.blit(frame_surface, (675, 75))
    button_color = GREEN if USE_FACE and not minimal else RED
    pygame.draw.rect(screen, button_color, (10, 90, 140, 50))
    text = font.render('USE_FACE' if USE_FACE else 'NO_FACE', True, WHITE)
    screen.blit(text, (20, 95))
    fps = track_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, BLACK)
    screen.blit(fps_text, (10, SCREEN_HEIGHT - 30))
    if rick_frame_count > -1 and not minimal:
        screen.fill(BLACK)
        rick_frame = pygame.image.load(f"FRAMES/converted/ffmpeg_{rick_frame_count}.png")
        rick_frame = pygame.transform.scale(rick_frame, (SCREEN_WIDTH, SCREEN_HEIGHT/1.5))
        screen.blit(rick_frame, (0,0+SCREEN_HEIGHT/6))
        rick_frame_count += 1
        
        if rick_frame_count == 125:
            if FRAME_COUNTER %7==0:
                rick_frame_count = -1
            else:
                rick_frame_count = 1
        fontt = pygame.font.SysFont('arial', 40)
        text = fontt.render('100 POINTS', True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    #render powerups
    for i, power in enumerate(powerop_list):
        text = font.render(power, True, BLACK)
        screen.blit(text, (10, SCREEN_HEIGHT - 50 - (i+1)*30))
    pygame.display.flip()

def move_basket(keys):
    global speed
    global speed2
    global accel
    global prev_result
    global currstage
    if currstage == 3:
        if keys[pygame.K_UP]:
            speed2 -= accel
        if keys[pygame.K_DOWN]:
            speed2 += accel
        if basket.top <= 0:
            speed2 = max(0, speed2)
            basket.top = 0
        if basket.bottom >= SCREEN_HEIGHT:
            speed2 = min(0, speed2)
            basket.bottom = SCREEN_HEIGHT
    if not USE_FACE or minimal:
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
    if basket.left <= 0:
        speed = max(0, speed)
        basket.left = 0
    if basket.right >= SCREEN_WIDTH:
        speed = min(0, speed)
        basket.right = SCREEN_WIDTH
def update_ball(balls):
    global score
    global internal_score
    global MAGNETIC_CATCH
    global counter
    global power_field
    global power_type
    for ball in balls:
        ball["y"] += ball["speed"]
        ball["x"] += ball["direction"]/360 * ball["speed"]
        if MAGNETIC_CATCH:
            dir_y = basket.centery - ball["y"] + basket.height//2
            if dir_y == 0:
                dir_y = 1
            dir_x = basket.centerx - ball["x"]
            q = dir_x/dir_y * 360 - counter
            if abs(dir_x) < 200 and abs(dir_y) < 300:
                ball["direction"] += (q-ball["direction"])/2
            if abs(dir_x) < 120 and abs(dir_y) < 200:
                ball["direction"] = q
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
                internal_score += 3
            else:
                score += 5
                internal_score += 5
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
    ball["speed"] = min(10/(1+math.e**(-0.05*internal_score)), ball["speed"])
    if random.randint(0,100) < 5:
        ball["speed"] = 5
    ball["abnormal"] = False
    ball["direction"] = min(100, max(-100, ball["direction"]))
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
    global currstage
    global tip1_act
    global tip2_act
    global tip3_act
    global tip4_act
    global tip5_act
    global score
    global internal_score
    global counter
    global BREAK_TIMING
    global BREAK_EVENT
    global DECREASE_STUN
    global MAGNETIC_CATCH
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
    global bullet_cd
    global stun_count
    global FRAME_COUNTER
    global bonus_score
    global boss_health
    global boss_dir
    global accel
    global decel
    global curr_heat
    global speed
    global speed2
    menu_running = True
    options_running = False
    help_running = False
    running = False
    stats_running = False
    card = False
    boss = False
    global volume
    with open("statistics.txt", "r") as f:
        lines = f.readlines()
        stats = {line.split()[0]: ' '.join(line.split()[1:]) for line in lines}
    while True:
        if menu_running:
            draw_main_menu()
            if not tip1_act:
                tip = font.render(tip1, True, WHITE)
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - tip.get_width() - 10, SCREEN_HEIGHT - tip.get_height() - 10, tip.get_width(), tip.get_height()))
                screen.blit(tip, (SCREEN_WIDTH - tip.get_width() - 10, SCREEN_HEIGHT - tip.get_height() - 10))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    update_stats()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_RETURN:
                        tip1_act = True
                    if event.key==pygame.K_RETURN:
                        if main_radbar.get_index() == 0:
                            running = True
                            menu_running = False
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("game.mp3")
                            pygame.mixer.music.play(-1)
                        elif main_radbar.get_index() == 1:
                            options_running = True
                            menu_running = False
                        elif main_radbar.get_index() == 2:
                            help_running = True
                            menu_running = False
                        elif main_radbar.get_index() == 4:
                            menu_running = False
                            pygame.quit()
                            sys.exit()
                        elif main_radbar.get_index() == 3:
                            stats_running = True
                            menu_running = False
                    else:
                        main_radbar.update(event.key)
            clock.tick(FPS*4)
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
                        if not minimal:
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
            if score >= 20:
                currstage = 2
            if score >= 50:
                currstage = 3
            if score == 10 or score == 20 or score == 50 or score == 100:
                boss = True
                boss_health = score
                running = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("boss.mp3")
                pygame.mixer.music.play(-1)
                continue
            FRAME_COUNTER+=1
            if not tip2_act:
                tip = font.render(tip2, True, WHITE)
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - tip.get_width() - 10, SCREEN_HEIGHT - tip.get_height() - 10, tip.get_width(), tip.get_height()))
                screen.blit(tip, (SCREEN_WIDTH - tip.get_width() - 10, SCREEN_HEIGHT - tip.get_height() - 10))
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
                        USE_FACE = (not USE_FACE) and (not minimal)
                    if event.key == CODE[index]:
                        code.append(event.key)
                        index += 1
                        if code == CODE:
                            index = 0
                            print('Bingo!')
                            score = 1000
                            internal_score = 10000
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
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                tip2_act = True
            if score == 100 and rick_frame_count == -1:
                rick_frame_count = 1
                score+=1
            prev_score = score
            if currstage == 1 or currstage == 2:
                if not any(keys):
                    if currstage == 1:
                        speed += decel * -((speed > 0) * 2 - 1)
                    if currstage == 2:
                        speed += decel * -((speed > 0) * 2 - 1) * 2
                dec_factor = score//10
                if currstage == 2:
                    accel = accel/dec_factor
                move_basket(keys)
                if currstage == 2:
                    accel = accel*dec_factor
                update_ball(balls)
                basket.move_ip(speed, 0)
            if currstage == 3:
                if not any(keys):
                    speed += decel * -((speed > 0) * 2 - 1)
                    speed2 += decel * -((speed2 > 0) * 2 - 1)
                accel = accel*0.4
                decel = 0.2
                move_basket(keys)
                accel = accel/0.4
                update_ball(balls)
                basket.move_ip(speed, speed2)
            draw_screen(balls)
            curr_heat += curr_heat * 0.25 * (score-prev_score)*4
            decay_rate = curr_heat * (math.e**(curr_heat/40) -0.5)/100
            curr_heat = max(1, curr_heat - decay_rate)
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
            if rick_frame_count < 0:
                if random.randint(0,10000) <internal_score  and (not BREAK_EVENT) and (BROKEN_TIMING < FPS/2):
                    BREAK_EVENT = True
                    BREAK_TIMING =FPS*random.randint(1,5)
                    BREAK_TIMING -= BREAK_TIMING * DECREASE_STUN
                    BREAK_X = random.randint(0, SCREEN_WIDTH - 100)
                    BREAK_WIDTH = random.randint(min(50+internal_score,150), min(100 + internal_score,600))
                if BREAK_EVENT and BREAK_TIMING > FPS/2:
                    pygame.draw.rect(screen, DARK_GRAY, (BREAK_X, 0, BREAK_WIDTH, SCREEN_HEIGHT), 2)
                if BREAK_EVENT and BREAK_TIMING <= FPS/2:
                    pygame.draw.rect(screen, RED, (BREAK_X, 0, BREAK_WIDTH, SCREEN_HEIGHT), 2)
                
                
                if random.randint(1,100000) < internal_score and power_field == None:
                    power_type = random.randint(0,3)
                    power_field = pygame.Rect(random.randint(0, SCREEN_WIDTH - 10), random.randint(0,SCREEN_HEIGHT-200), 100, 50)

                if random.randint(1,300) <= 1:
                    power_field= None
            pygame.display.flip()
            clock.tick(FPS)
        if boss:
            USE_FACE = False
            screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    boss = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        boss = False
                        menu_running = True
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("menu.mp3")
                        pygame.mixer.music.play(-1)
                        update_stats()
            keys = pygame.key.get_pressed()
            if not any(keys):
                speed += decel * -((speed > 0) * 2 - 1)
            move_basket(keys)
            update_ball(balls)
            if keys[pygame.K_SPACE]:
                if bullet_cd < 0:
                    bullets.append(bullet(basket.centerx, basket.centery, 3, speed))
                    bullet_cd = 10
                bullet_cd -=1
            basket.move_ip(speed, 0)
            draw_rotated_rect(screen, BLUE, basket.center, (BASKET_WIDTH, BASKET_HEIGHT), speed)
            global turret_dir
            if boss_health > 0:
                for b in bullets:
                    b.update()
                    pygame.draw.circle(screen, RED, (int(b.x), int(b.y)), 3)
                    if boss_enem.colliderect(pygame.Rect(b.x, b.y, 3, 3)):
                        boss_health -= 10
                        bullets.remove(b)
                if boss_enem.top < 100:
                    boss_enem.top += 2
                    help_text = font.render("PRESS SPACE TO SHOOT", True, BLACK)
                    screen.blit(help_text, (SCREEN_WIDTH // 2 - help_text.get_width() // 2, SCREEN_HEIGHT // 2 - help_text.get_height() // 2))
                else:
                    boss_enem.left += boss_dir
                    if boss_enem.left < 0 or boss_enem.right > SCREEN_WIDTH:
                        boss_dir *= -1
                pygame.draw.rect(screen, RED, boss_enem)
                boss_healthbar = boss_enem.copy()
                boss_healthbar.scale_by_ip(1- boss_health/score, 0.8)
                pygame.draw.rect(screen, WHITE, boss_healthbar)
            else:
                powe = random.randint(0,3)
                screen.blit(pygame.transform.scale(pygame.image.load("cards/backend.png"), (220,360)), (SCREEN_WIDTH//2-110, SCREEN_HEIGHT//2-180))
                card = True

            if card:
                if True:
                    if pygame.mouse.get_pressed()[0] and pygame.Rect(SCREEN_WIDTH//2-110, SCREEN_HEIGHT//2-180, 220, 360).collidepoint(pygame.mouse.get_pos()):
                        boss = False
                        running = True
                        score+=1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("game.mp3")
                        pygame.mixer.music.play(-1)
                        if powe == 0:
                            MAGNETIC_CATCH = True
                            powerop_list.append("Magnetic Catch")
                        elif powe == 1:
                            DECREASE_STUN+=0.2
                            powerop_list.append(f"Decrease Stun ({DECREASE_STUN})")
                        elif powe == 2:
                            accel += 0.1
                            decel += 0.1
                            if "Increase Speed" in powerop_list:
                                powerop_list.remove("Increase Speed")
                                powerop_list.append("Increase Speed II")
                            elif "Increase Speed II" in powerop_list:
                                powerop_list.remove("Increase Speed II")
                                powerop_list.append("Super Speed")
                            else:
                                powerop_list.append("Increase Speed")
                        elif powe == 3:
                            accel += 0.2
                            decel += 0.2
                            if "Super Speed" in powerop_list:
                                powerop_list.remove("Super Speed")
                                powerop_list.append("Hyper Speed")
                            else:
                                powerop_list.append("Super Speed")
                        card = False
                        #render front side for half a second
                        front = None
                        if powe == 0:
                            front = pygame.image.load("cards/magnet.png")
                        elif powe == 1:
                            front = pygame.image.load("cards/decreasestun.png")
                        elif powe == 2:
                            front = pygame.image.load("cards/increasespeed.png")
                        elif powe == 3:
                            front = pygame.image.load("cards/hyperspeed.png")
                        screen.blit(pygame.transform.scale(front, (220,360)), (SCREEN_WIDTH//2-110, SCREEN_HEIGHT//2-180))
                        pygame.display.flip()
                        #wait until player click outside
                        while not (pygame.mouse.get_pressed()[0] and not pygame.Rect(SCREEN_WIDTH//2-110, SCREEN_HEIGHT//2-180, 220, 360).collidepoint(pygame.mouse.get_pos())):
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    boss = False
                                    pygame.quit()
                                    sys.exit()
            pygame.display.flip()
            clock.tick(FPS*4 if card else FPS)
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
bullets = []
balls = [ball]
boss_dir = 4
turret_dir = 0
TURRET_LENGTH = 40
basket_dir = 0
bullet_cd = -1
boss_health = 1
boss_enem = pygame.Rect(SCREEN_WIDTH // 2 - BASKET_WIDTH // 2, 0, BASKET_WIDTH, BASKET_HEIGHT)
if not minimal:
    head_pose = HeadPoseDetector()
power_field = None
back_card = pygame.image.load("cards/backend.png")
power_type = None
# 0: speed up
# 1: teleport
# 2: duplicate
score = 0
stun_count = 0

main_radbar = RadialMenu((0, SCREEN_HEIGHT//2), 200, ["Start Game", "Options", "Help", "Statistics", "Quit"], pygame.font.SysFont('arial', 40))
tip1= "Tip: Use the arrow keys to select an option, and press Enter to confirm."
tip2 = "Use the arrow keys to move the basket sideways"
tip3 = "Catch the balls to score points"
tip4 = "Avoid the beams, they stun you"
tip5 = "Power zones spawn randomly"
tip1_act, tip2_act, tip3_act, tip4_act, tip5_act = False, False, False, False, False

font = pygame.font.SysFont('arial', 24)

button_font = pygame.font.SysFont('arial', 15)
button_text = button_font.render("Thoát Game", True, WHITE)
button_rect = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40)

if __name__ == "__main__":
    main()
