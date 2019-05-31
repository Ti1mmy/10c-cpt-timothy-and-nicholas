import arcade
import random
import os

WIDTH = 1600
HEIGHT = 960

# Loading Textures -----------------------------------------------------------------------------------------------------

title_text = arcade.load_texture('assets' + os.sep + 'text' + os.sep +
                                 'title.png', 0, 0, 505, 150)

background = arcade.load_texture('assets' + os.sep + 'backgrounds' + os.sep +
                                 'title screen background.jpg', 0, 0, 3194, 1200)

bird = arcade.load_texture('assets' + os.sep + 'sprites' + os.sep +
                           'bird.png', 0, 0, 1200, 1200)

plane = arcade.load_texture('assets' + os.sep + 'sprites' + os.sep +
                            'plane.png', 0, 0, 420, 420)

start = arcade.load_texture('assets' + os.sep + 'text' + os.sep +
                            'start.png', 0, 0, 250, 90)

highscores = arcade.load_texture('assets' + os.sep + 'sprites' + os.sep +
                                 'scores.png', 0, 0, 244, 204)

shop = arcade.load_texture('assets' + os.sep + 'sprites' + os.sep +
                           'shop.png', 0, 0, 520, 459)

score_title = arcade.load_texture('assets' + os.sep + 'text' + os.sep +
                                  'leaderboard.tiff', 0, 0, 590, 190)

home = arcade.load_texture('assets' + os.sep + 'sprites' + os.sep +
                           'home.png', 0, 0, 512, 512)

reset = arcade.load_texture('assets' + os.sep + 'sprites' + os.sep +
                            'reset.png', 0, 0, 420, 420)

gameover = arcade.load_texture('assets' + os.sep + 'text' + os.sep +
                               'gameover.png', 0, 0, 495, 170)

plane1 = arcade.load_texture('assets' + os.sep + 'backgrounds' + os.sep +
                             'planecrash1.png', 0, 0, 1458, 1000)

plane2 = arcade.load_texture('assets' + os.sep + 'backgrounds' + os.sep +
                             'planecrash2.png', 0, 0, 1458, 1000)

plane3 = arcade.load_texture('assets' + os.sep + 'backgrounds' + os.sep +
                             'planecrash3.png', 0, 0, 1458, 1000)

plane4 = arcade.load_texture('assets' + os.sep + 'backgrounds' + os.sep +
                             'planecrash4.png', 0, 0, 1458, 1000)

pause_background = arcade.load_texture('assets' + os.sep + 'backgrounds' + os.sep +
                                       'pause_background.png', 0, 0, 1600, 900)

pause_text = arcade.load_texture('assets' + os.sep + 'text' + os.sep +
                                 'game_paused.tiff', 0, 0, 649, 227)

instructions = arcade.load_texture('assets' + os.sep + 'text' + os.sep +
                                   'instructions.png', 0, 0, 702, 262)

info_text = arcade.load_texture('assets' + os.sep + 'text' + os.sep +
                                'information.png', 0, 0, 810, 563)

planes = [plane1, plane2, plane3, plane4]
# Global Variables -----------------------------------------------------------------------------------------------------

bird_pos = [
    [1200, 800],
    [1400, 720],
    [1100, 670]
]
bird_shift_y = 0
bird_down = False
bird_up = True
x_background = WIDTH / 2
scroll_left = True
scroll_right = False

plane_x = 300
plane_y = HEIGHT / 2
plane_up = True
plane_down = False

background_repetitions = 1
mouse_x = 0
mouse_y = 0

frame_time = 0

game_over_frametime = 0
game_over_animation = 0

start_click = False
mouse_press = False
mouse_release = False
pressed = False
shop_pressed = False
high_scores_pressed = False

scores = open('scores.txt', 'a')

scores_read = open('scores.txt', 'r')
scores_save = []
for length in scores_read:
    scores_save.append(int(length.replace(', \n', '')))
scores_save.sort(reverse=True)

home_pressed = False
reset_pressed = True
restart_pressed = False
game_main_menu_pressed = False

score_menu = False
game = False
main_menu = True
dead = False
paused = False
prev_speed = 0
times_paused = 0
too_many_pause = False
information = False
information_pressed = False
# Game Variables -------------------------------------------------------------------------------------------------------

star_x_positions = []
star_y_positions = []
game_y_plane = HEIGHT / 2
keydown = False
keyup = False
boom = False
game_frametime = 0
speed = 4

for i in range(10):
    game_x = random.randrange(WIDTH / 2, WIDTH * 2)
    game_y = random.randrange(HEIGHT)
    star_x_positions.append(game_x)
    star_y_positions.append(game_y)

# ----------------------------------------------------------------------------------------------------------------------


def setup():
    arcade.open_window(WIDTH, HEIGHT, "Plane Game Pre-pree-reee")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(update, 1 / 60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press
    window.on_mouse_release = on_mouse_release
    window.on_mouse_motion = on_mouse_motion

    arcade.run()


def update(delta_time):
    global frame_time
    if main_menu:
        frame_time += 1
    elif game:
        plane_game_logic()


def on_draw():
    arcade.start_render()
    if dead:
        game_over()
    elif main_menu:
        draw_background(0.5)
        title_plane()
        birds()
        title()
        draw_button(813, 360, 300, 70, arcade.color.GREEN, start,
                    arcade.color.LIGHT_GREEN, arcade.color.FOREST_GREEN)
        draw_shop_button(1078, 360, 150, 70, arcade.color.DARK_CYAN,
                         shop, arcade.color.LIGHT_BLUE, arcade.color.BLUE_BELL)
        draw_high_scores_button(535, 360, 150, 70, arcade.color.BLACK,
                                highscores, arcade.color.GRAY, arcade.color.LIGHT_GRAY)
        draw_information_button(813, 260, 300, 70,
                                arcade.color.GOLDEN_POPPY, instructions, arcade.color.GOLD, arcade.color.ORANGE_PEEL)
    elif score_menu:
        draw_background(0.5)
        title_plane()
        scores_menu()
        draw_home_button(50, HEIGHT - 50, 50, 50, arcade.color.WHITE, home,
                         arcade.color.LIGHT_GRAY, arcade.color.DARK_BLUE_GRAY)
        draw_reset_button(50, HEIGHT - 125, 50, 50, arcade.color.RED, reset, arcade.color.DARK_RED, arcade.color.PINK)
    elif paused:
        pause_menu()
    elif game:
        plane_game_draw()
    elif information:
        draw_background(0.5)
        title_plane()
        info_menu()
        draw_home_button(50, HEIGHT - 50, 50, 50, arcade.color.WHITE, home,
                         arcade.color.LIGHT_GRAY, arcade.color.DARK_BLUE_GRAY)


def on_key_press(key, modifiers):
    global keyup, keydown, dead, game, paused, times_paused, too_many_pause
    if game:
        if key == arcade.key.DOWN:
            keydown = True
        if key == arcade.key.UP:
            keyup = True
        if key == arcade.key.ESCAPE:
            game = False
            dead = True
        if key == arcade.key.SPACE and not paused and times_paused < 2:
            paused = True
            times_paused += 1
        elif key == arcade.key.SPACE and paused:
            paused = False


def on_key_release(key, modifiers):
    if game:
        global keyup, keydown
        if key == arcade.key.DOWN:
            keydown = False
        if key == arcade.key.UP:
            keyup = False


def on_mouse_press(x, y, button, modifiers):
    global mouse_press
    if button == arcade.MOUSE_BUTTON_LEFT:
        mouse_press = True


def on_mouse_release(x, y, button, modifiers):
    global mouse_press
    if button == arcade.MOUSE_BUTTON_LEFT:
        mouse_press = False


def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y


def draw_background(scroll_speed):
    global x_background, scroll_left, scroll_right

    arcade.draw_texture_rectangle(x_background, HEIGHT / 2, WIDTH, HEIGHT, background)
    arcade.draw_texture_rectangle(x_background + WIDTH, HEIGHT / 2, WIDTH, HEIGHT, background)
    x_background -= scroll_speed
    if x_background == -800:
        x_background = 800


def birds():
    global bird_pos, bird_shift_y, bird_down, bird_up
    for pos in range(len(bird_pos)):
        arcade.draw_texture_rectangle(bird_pos[pos][0], bird_pos[pos][1] + bird_shift_y, 100, 100, bird)
    if bird_shift_y == 20:
        bird_down = True
        bird_up = False
    elif bird_shift_y == -20:
        bird_down = False
        bird_up = True
    if bird_up:
        bird_shift_y += 0.5
    if bird_down:
        bird_shift_y -= 0.5


def title_plane():
    global plane_y, plane_up, plane_down
    arcade.draw_texture_rectangle(plane_x, plane_y, 100, 100, plane)
    if frame_time % 60 == 0:
        if random.randint(0, 1) == 1:
            plane_down = True
            plane_up = False
        else:
            plane_up = True
            plane_down = False
    if plane_down and plane_y > 53:
        plane_y -= 2
    elif plane_up and plane_y < HEIGHT - 53:
        plane_y += 2
    if plane_y > HEIGHT - 53:
        plane_down = True
        plane_up = False
    elif plane_y < 53:
        plane_down = False
        plane_up = True


def title():
    arcade.draw_texture_rectangle(WIDTH / 2, 500, 800, 268, title_text)


def draw_button(x, y, width, height, colour_default, texture, colour_hover, colour_press):
    global pressed
    if mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_press)
        pressed = True
    elif mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and not \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_hover)
        if pressed:
            game_start()
            pressed = False
    else:
        arcade.draw_rectangle_filled(x, y, width, height, colour_default)
        pressed = False
    arcade.draw_texture_rectangle(x, y, width * 0.9, height, texture)


def draw_shop_button(x, y, width, height, colour_default, texture, colour_hover, colour_press):
    global shop_pressed
    if mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_press)
        shop_pressed = True
    elif mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and not \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_hover)
        if shop_pressed:
            shop_pressed = False
    else:
        arcade.draw_rectangle_filled(x, y, width, height, colour_default)
        shop_pressed = False
    arcade.draw_texture_rectangle(x, y + 5, width, height * 1.15, texture)


def draw_high_scores_button(x, y, width, height, colour_default, texture, colour_hover, colour_press):
    global high_scores_pressed, score_menu, main_menu
    if mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_press)
        high_scores_pressed = True
    elif mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and not \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_hover)
        if high_scores_pressed:
            list_scores()
            score_menu = True
            main_menu = False
            high_scores_pressed = False
    else:
        arcade.draw_rectangle_filled(x, y, width, height, colour_default)
        high_scores_pressed = False
        score_menu = False
    arcade.draw_texture_rectangle(x, y - 3, width, height * 1.15, texture)


def draw_home_button(x, y, width, height, colour_default, texture, colour_hover, colour_press):
    global home_pressed, main_menu, score_menu, information
    if mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_press)
        home_pressed = True
    elif mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and not \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_hover)
        if home_pressed:
            home_pressed = False
            main_menu = True
            if score_menu:
                score_menu = False
            elif information:
                information = False
    else:
        arcade.draw_rectangle_filled(x, y, width, height, colour_default)
        home_pressed = False
    arcade.draw_texture_rectangle(x, y, width * 0.95, height * 0.95, texture)


def draw_reset_button(x, y, width, height, colour_default, texture, colour_hover, colour_press):
    global reset_pressed, scores_save
    if mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_press)
        reset_pressed = True
    elif mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and not \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_hover)
        if reset_pressed:
            reset_pressed = False
            scores_reset = open('scores.txt', 'w')
            scores_reset.write("")
            scores_save = []
    else:
        arcade.draw_rectangle_filled(x, y, width, height, colour_default)
        reset_pressed = False
    arcade.draw_texture_rectangle(x, y, width * 0.95, height * 0.95, texture)


def draw_restart_button(x, y, width, height, colour_default, texture, colour_hover, colour_press):
    global restart_pressed, dead, game, game_frametime
    if mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_press)
        restart_pressed = True
    elif mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and not \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_hover)
        if restart_pressed:
            restart_pressed = False
            dead = False
            game = True
            game_frametime = 0
    else:
        arcade.draw_rectangle_filled(x, y, width, height, colour_default)
        restart_pressed = False
    arcade.draw_texture_rectangle(x, y, width * 0.95, height * 0.95, texture)


def draw_game_main_menu_button(x, y, width, height, colour_default, texture, colour_hover, colour_press):
    global game_main_menu_pressed, main_menu, dead, game_frametime
    if mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_press)
        game_main_menu_pressed = True
    elif mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and not \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_hover)
        if game_main_menu_pressed:
            game_main_menu_pressed = False
            main_menu = True
            dead = False
            game_frametime = 0
    else:
        arcade.draw_rectangle_filled(x, y, width, height, colour_default)
        game_main_menu_pressed = False
    arcade.draw_texture_rectangle(x, y, width * 0.95, height * 0.95, texture)


def draw_information_button(x, y, width, height, colour_default, texture, colour_hover, colour_press):
    global information_pressed, information, main_menu
    if mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_press)
        information_pressed = True
    elif mouse_x > x - (width / 2) and \
            mouse_x < x + (width / 2) and \
            mouse_y < y + (height / 2) and \
            mouse_y > y - (height / 2) and not \
            mouse_press:
        arcade.draw_rectangle_filled(x, y, width, height, colour_hover)
        if information_pressed:
            information_pressed = False
            information = True
            main_menu = False
    else:
        arcade.draw_rectangle_filled(x, y, width, height, colour_default)
        information_pressed = False
        information = False
    arcade.draw_texture_rectangle(x + 5, y, width * 0.8, height * 0.8, texture)


def plane_game_draw():
    arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)
    for x_star, y_star in zip(star_x_positions, star_y_positions):
        arcade.draw_circle_filled(x_star, y_star, 2, arcade.color.WHITE)
    arcade.draw_texture_rectangle(250, game_y_plane, 100, 100, plane)
    arcade.draw_text(str(game_frametime), WIDTH - 50, HEIGHT - 20, arcade.color.WHITE)


def plane_game_logic():
    global game_y_plane, boom, game_frametime, speed, main_menu, scores_save, dead, times_paused
    global keyup, keydown, game_x, game_y, star_x_positions, star_y_positions, game
    if not paused:
        game_frametime += 1
        for x_range in range(len(star_x_positions)):
            star_x_positions[x_range] -= speed
            if star_x_positions[x_range] <= 0:
                star_y_positions[x_range] = random.randrange(0, HEIGHT)
                star_x_positions[x_range] = random.randrange(WIDTH, WIDTH * 2)
        if game_y_plane >= 50:
            if keydown:
                game_y_plane -= 8
        if game_y_plane <= HEIGHT - 50:
            if keyup:
                game_y_plane += 8
        if game_frametime % 120 == 0 and game_frametime != 0:
            speed += 0.35
        for detect in range(len(star_x_positions)):
            if ((200 <= star_x_positions[detect] <= 284) and (
                    star_y_positions[detect] - 50 <= game_y_plane <= star_y_positions[detect] + 50)) or \
                    ((300 >= star_x_positions[detect] >= 285) and (
                            star_y_positions[detect] - 22 <= game_y_plane <= star_y_positions[detect] + 22)):

                scores.write(f'{str(game_frametime)}, \n')
                scores_save.append(game_frametime)
                scores_save.sort(reverse=True)
                star_x_positions = []
                star_y_positions = []
                game_y_plane = HEIGHT / 2
                keydown = False
                keyup = False
                boom = False
                speed = 4

                for i in range(10):
                    game_x = random.randrange(WIDTH / 2, WIDTH * 2)
                    game_y = random.randrange(HEIGHT)
                    star_x_positions.append(game_x)
                    star_y_positions.append(game_y)
                dead = True
                game = False
                times_paused = 0


def scores_menu():
    arcade.draw_texture_rectangle(WIDTH / 2, HEIGHT - 160, 590, 190, score_title)
    height = 700
    if 10 > len(scores_save) != 0:
        for i in range(len(scores_save)):
            if i == 0:
                arcade.draw_text(f'[{i + 1}]: {str(scores_save[i])}', WIDTH / 2, height, arcade.color.GOLD, 24)
            elif i == 1:
                arcade.draw_text(f'[{i + 1}]: {str(scores_save[i])}', WIDTH / 2, height, arcade.color.SILVER, 24)
            elif i == 2:
                arcade.draw_text(f'[{i + 1}]: {str(scores_save[i])}', WIDTH / 2, height, arcade.color.BRONZE, 24)
            else:
                arcade.draw_text(f'[{i + 1}]: {str(scores_save[i])}', WIDTH / 2, height, arcade.color.BLACK, 24)
            height -= 70
    elif len(scores_save) >= 10:
        for i in range(10):
            if i == 0:
                arcade.draw_text(f'[{i + 1}]: {str(scores_save[i])}', WIDTH / 2, height, arcade.color.GOLD, 24)
            elif i == 1:
                arcade.draw_text(f'[{i + 1}]: {str(scores_save[i])}', WIDTH / 2, height, arcade.color.SILVER, 24)
            elif i == 2:
                arcade.draw_text(f'[{i + 1}]: {str(scores_save[i])}', WIDTH / 2, height, arcade.color.BRONZE, 24)
            else:
                arcade.draw_text(f'[{i + 1}]: {str(scores_save[i])}', WIDTH / 2, height, arcade.color.BLACK, 24)
            height -= 70
    else:
        arcade.draw_text('No game progress is present', WIDTH / 2 - 180, HEIGHT / 2, arcade.color.BLACK, 24)


def list_scores():
    print('Here are the top 10 scores: ')
    if len(scores_save) < 10:
        for top in range(len(scores_save)):
            print(f'[{top + 1}]: {scores_save[top]}')
    else:
        for top in range(10):
            print(f'[{top + 1}]: {scores_save[top]}')


def game_start():
    global main_menu, game
    main_menu = False
    game = True
    print('game started')


def game_over_background():
    global game_over_frametime, game_over_animation
    arcade.draw_texture_rectangle(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT, planes[game_over_animation])

    if game_over_frametime % 15 == 0 and game_over_frametime != 0:
        game_over_animation += 1

    if game_over_animation == 4:
        game_over_animation = 0
    game_over_frametime += 1


def game_over():
    game_over_background()
    arcade.draw_texture_rectangle(WIDTH / 2 + 20, HEIGHT - 160, 495, 170, gameover)
    draw_restart_button(WIDTH / 2, 500, 100, 100, arcade.color.ORANGE, reset,
                        arcade.color.GOLD, arcade.color.YELLOW)
    draw_game_main_menu_button(WIDTH / 2, 350, 100, 100, arcade.color.RED, home,
                               arcade.color.DARK_RED, arcade.color.PINK)
    arcade.draw_rectangle_filled(WIDTH / 2 - 10, HEIGHT - 290, 200, 48, arcade.color.LIGHT_GRAY)
    arcade.draw_text(f'Score: {game_frametime}', WIDTH / 2 - 75, HEIGHT - 300, arcade.color.BLACK, 24)


def pause_menu():
    arcade.draw_xywh_rectangle_textured(0, 0, WIDTH, HEIGHT, pause_background, 0, 100)
    arcade.draw_texture_rectangle(WIDTH / 2, HEIGHT - 200, 649, 227, pause_text)
    for x_star, y_star in zip(star_x_positions, star_y_positions):
        arcade.draw_circle_filled(x_star, y_star, 2, arcade.color.WHITE)
    arcade.draw_texture_rectangle(250, game_y_plane, 100, 100, plane)
    arcade.draw_text(str(game_frametime), WIDTH - 50, HEIGHT - 20, arcade.color.WHITE)


def info_menu():
    arcade.draw_texture_rectangle(WIDTH / 2, HEIGHT / 2 + 100, 810 * 1.75, 563 * 1.75, info_text)


if __name__ == '__main__':
    setup()
