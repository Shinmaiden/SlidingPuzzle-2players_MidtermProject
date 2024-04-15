from setting import *
import pygame, sys, os, threading, pickle
from puzzle import Puzzle
from displayPuzzle import DisplayPuzzle
from slider import Slider
from animation import Animation

pygame.init()


def updateDemo(deltaTime: int) -> None:
    global time_since_last_demo_move, previous_frame_time

    current_frame_time = pygame.time.get_ticks()
    time_since_last_demo_move += current_frame_time - previous_frame_time
    previous_frame_time = current_frame_time

    screen.blit(title_card_line_one, title_card_line_one_rect)
    screen.blit(title_card_line_two, title_card_line_two_rect)
    screen.blit(title_card_line_three, title_card_line_three_rect)

    if time_since_last_demo_move > 500:
        puzzle1.update(puzzle1.getDemoMove(), deltaTime)
        time_since_last_demo_move = 0
    else:
        puzzle1.update(None, deltaTime)


def formatTime(time: int) -> str:
    if time == None:
        return '--:--:---'

    minutes = time // 60000
    seconds = time // 1000 % 60
    milliseconds = time % 1000

    result_string = ''
    if minutes < 10:
        result_string += '0'
    result_string += f'{minutes}:'
    if seconds < 10:
        result_string += '0'
    result_string += f'{seconds}:'
    if milliseconds < 10:
        result_string += '00'
    elif milliseconds < 100:
        result_string += '0'
    result_string += str(milliseconds)

    return result_string


# retrieve save data
try:
    with open('data.pkl', 'rb') as file:
        data = pickle.load(file)

        music_volume = data['music_volume']
        sfx_volume = data['sfx_volume']
        best_time = data['best_time']
        current_difficulty = data['current_difficulty']
except:
    music_volume = 0.5
    sfx_volume = 0.5
    best_time = {
        3: None,
        4: None,
        5: None,
    }
    current_difficulty = 4

# initialising global variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2P Number Slider')
pygame.display.set_icon(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile1.png')))

pygame.mixer.music.load(os.path.join(LOCAL_DIR, 'Assets/bgmusic.mp3'))
click_sound = pygame.mixer.Sound(os.path.join(LOCAL_DIR, 'Assets/click.ogg'))
slide_sound = pygame.mixer.Sound(os.path.join(LOCAL_DIR, 'Assets/slide.wav'))
pygame.mixer.music.set_volume(music_volume)
click_sound.set_volume(sfx_volume)
slide_sound.set_volume(sfx_volume)
pygame.mixer.music.play(-1)

puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'demo')
puzzle2 = None
previous_mode = None
current_mode = 'main-menu'
time_since_last_demo_move = 0
previous_frame_time = pygame.time.get_ticks()

player_one_score = 0
player_two_score = 0
race_finished = False


def addPuzzle(difficulty: int) -> None:
    global three_by_three_puzzles, four_by_four_puzzles, current_puzzle_index

    puzzle_list = three_by_three_puzzles if difficulty == 3 else four_by_four_puzzles

    puzzle = Puzzle(difficulty, True)
    initial_state = deepcopy(puzzle.getState())

    puzzle_list.append([initial_state, deepcopy(puzzle), deepcopy(move_list)])

    while updating:
        pass

    puzzle_list.pop(0)
    current_puzzle_index -= 1


updating = False


def updatePuzzles(difficulty: int) -> None:
    global three_by_three_puzzles, updating

    puzzle_list = three_by_three_puzzles if difficulty == 3 else four_by_four_puzzles

    initial_state, puzzle, move_list = puzzle_list[current_puzzle_index]
    new_move_list = ai.getOptimalMove(puzzle.getState(), move_list[-1])
    for move in new_move_list:
        puzzle.move(move)
    move_list += new_move_list
    puzzle_list[current_puzzle_index] = deepcopy([initial_state, puzzle, move_list])

    if puzzle.isSolved():
        updating = False


font_name = "comicsansms"
font_size = 30
medium_font = pygame.font.SysFont(font_name, font_size)

font_name = "timesnewroman"
font_size = 50
big_font = pygame.font.SysFont(font_name, font_size)

font_name = "timesnewroman"
font_size = 30
small_font = pygame.font.SysFont(font_name, font_size)

# main menu buttons and labels
title_card_line_one = big_font.render('Two Player', False, WHITE)
title_card_line_one_rect = title_card_line_one.get_rect(center=(930, 100))

title_card_line_two = big_font.render('Number', False, WHITE)
title_card_line_two_rect = title_card_line_two.get_rect(center=(930, 160))

title_card_line_three = big_font.render('Slider', False, WHITE)
title_card_line_three_rect = title_card_line_three.get_rect(center=(930, 220))

play_button_background = pygame.Rect(800, 512, 250, 60)
play_button_text = medium_font.render('Play', False, WHITE)
play_button_rect = play_button_text.get_rect(center=(925, 545))

main_menu_options_button_background = pygame.Rect(800, 592, 250, 60)
main_menu_options_button_text = medium_font.render('options', False, WHITE)
main_menu_options_button_rect = main_menu_options_button_text.get_rect(center=(925, 625))

# options menu buttons, labels and sliders
music_slider = Slider(screen, 0, 1, (640, 450), 750, 40, 50, 100, 2, music_volume)
sfx_slider = Slider(screen, 0, 1, (640, 570), 750, 40, 50, 100, 2, sfx_volume)

options_label = big_font.render('Options', False, WHITE)
options_label_rect = options_label.get_rect(center=(550, 50))

three_by_three_button_background = pygame.Rect(148, 210, 250, 66)
three_by_three_button_text = big_font.render('3x3', False, WHITE)
three_by_three_button_rect = three_by_three_button_text.get_rect(center=(275, 250))

four_by_four_button_background = pygame.Rect(423, 210, 250, 66)
four_by_four_button_text = big_font.render('4x4', False, WHITE)
four_by_four_button_rect = four_by_four_button_text.get_rect(center=(550, 250))

five_by_five_button_background = pygame.Rect(698, 210, 250, 66)
five_by_five_button_text = big_font.render('5x5', False, WHITE)
five_by_five_button_rect = five_by_five_button_text.get_rect(center=(825, 250))

volumn_label = medium_font.render('Volume:', False, WHITE)
volumn_label_rect = volumn_label.get_rect(topleft=(50, 320))

music_label = big_font.render('Music', False, WHITE)
music_label_rect = music_label.get_rect(topleft=(75, 425))

sfx_label = big_font.render('SFX', False, WHITE)
sfx_label_rect = sfx_label.get_rect(topleft=(75, 545))

return_button_background = pygame.Rect(420, 660, 250, 66)
return_button_text = big_font.render('Return', False, WHITE)
return_button_rect = return_button_text.get_rect(center=(550, 700))

# play screen buttons and labels
time_trial_button_background = pygame.Rect(785, 380, 280, 60)
time_trial_button_text = medium_font.render('One Player', False, WHITE)
time_trial_button_rect = time_trial_button_text.get_rect(center=(925, 410))

two_players_button_background = pygame.Rect(785, 470, 280, 60)
two_players_button_text = medium_font.render('Two Players', False, WHITE)
two_players_button_rect = two_players_button_text.get_rect(center=(925, 505))

play_screen_back_to_menu_background = pygame.Rect(785, 630, 280, 60)
play_screen_back_to_menu_button_text = medium_font.render('Back to menu', False, WHITE)
player_screen_back_to_menu_button_rect = play_screen_back_to_menu_button_text.get_rect(center=(925, 665))

# time trial mode buttons and labels
time_trial_best_time_label = medium_font.render('Best Time: ', False, WHITE)
time_trial_best_time_rect = time_trial_best_time_label.get_rect(topleft=(770, 100))

time_trial_time_label = medium_font.render('Time: ', False, WHITE)
time_trial_time_rect = time_trial_time_label.get_rect(topleft=(770, 230))

time_trial_move_label = medium_font.render('Moves:', False, WHITE)
time_trial_move_rect = time_trial_move_label.get_rect(topleft=(770, 365))

time_trial_restart_button_background = pygame.Rect(780, 500, 290, 60)
time_trial_restart_button_text = medium_font.render('Restart', False, WHITE)
time_trial_restart_button_rect = time_trial_restart_button_text.get_rect(center=(925, 535))

time_trial_back_to_menu_button_background = pygame.Rect(780, 580, 290, 60)
time_trial_back_to_menu_button_text = medium_font.render('Back to menu', False, WHITE)
time_trial_back_to_menu_button_rect = time_trial_back_to_menu_button_text.get_rect(center=(925, 615))

time_trial_options_button_background = pygame.Rect(780, 660, 290, 60)
time_trial_options_button_text = medium_font.render('Options', False, WHITE)
time_trial_options_button_rect = time_trial_options_button_text.get_rect(center=(925, 695))

# two players mode buttons and labels
player_one_label = big_font.render(f'Player 1', False, WHITE)
player_one_rect = player_one_label.get_rect(topleft=(25, 25))

player_two_label = big_font.render(f'Player 2', False, WHITE)
player_two_rect = player_two_label.get_rect(topright=(1075, 25))

score_label = medium_font.render(f'{player_one_score} vs {player_two_score}', False, WHITE)
score_rect = score_label.get_rect(center=(550, 75))

two_players_restart_button_background = pygame.Rect(38, 675, 290, 60)
two_players_restart_button_text = medium_font.render('Restart', False, WHITE)
two_players_restart_button_rect = two_players_restart_button_text.get_rect(center=(183, 710))

two_players_back_to_menu_button_background = pygame.Rect(405, 675, 290, 60)
two_players_back_to_menu_button_text = medium_font.render('Back to menu', False, WHITE)
two_players_back_to_menu_button_rect = two_players_back_to_menu_button_text.get_rect(center=(550, 710))

two_players_options_button_background = pygame.Rect(772, 675, 290, 60)
two_players_options_button_text = medium_font.render('Options', False, WHITE)
two_players_options_button_rect = two_players_options_button_text.get_rect(center=(917, 710))


# the main program
def main() -> None:
    global current_mode, music_volume, sfx_volume, current_difficulty, puzzle1, puzzle2, best_time, player_one_score, player_two_score, player_two_rect, race_finished, score_label, score_rect, three_by_three_puzzles, four_by_four_puzzles, current_puzzle_index, updating
    previous_frame_time = pygame.time.get_ticks()
    current_frame_time = pygame.time.get_ticks()
    added_animations = False

    while True:
        player_one_direction = None
        player_two_direction = None

        # checking deltaTime
        current_frame_time = pygame.time.get_ticks()
        deltatime = current_frame_time - previous_frame_time
        previous_frame_time = current_frame_time

        for event in pygame.event.get():
            # closing the game
            if event.type == pygame.QUIT:
                data = {
                    'music_volume': music_volume,
                    'sfx_volume': sfx_volume,
                    'best_time': best_time,
                    'current_difficulty': current_difficulty
                }

                with open('data.pkl', 'wb') as file:
                    pickle.dump(data, file)

                pygame.quit()
                sys.exit()

                # mouse click events

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if current_mode == 'main-menu':
                    if play_button_background.collidepoint(mouse_pos):
                        pygame.mixer.Sound.play(click_sound)
                        current_mode = 'play'
                    elif main_menu_options_button_background.collidepoint(mouse_pos):
                        pygame.mixer.Sound.play(click_sound)
                        previous_mode = 'main-menu'
                        current_mode = 'options'
                elif current_mode == 'options':
                    if music_slider.mouseOnKnob(mouse_pos):
                        music_slider.setDragging(True)
                    elif sfx_slider.mouseOnKnob(mouse_pos):
                        sfx_slider.setDragging(True)
                    elif three_by_three_button_background.collidepoint(mouse_pos):
                        current_difficulty = 3
                        pygame.mixer.Sound.play(click_sound)
                    elif four_by_four_button_background.collidepoint(mouse_pos):
                        current_difficulty = 4
                        pygame.mixer.Sound.play(click_sound)
                    elif five_by_five_button_background.collidepoint(mouse_pos):
                        if previous_mode != '':
                            current_difficulty = 5
                            pygame.mixer.Sound.play(click_sound)
                    elif return_button_background.collidepoint(mouse_pos):
                        current_mode = previous_mode
                        pygame.mixer.Sound.play(click_sound)
                elif current_mode == 'play':
                    if time_trial_button_background.collidepoint(mouse_pos):
                        current_mode = 'time-trial'
                        pygame.mixer.Sound.play(click_sound)
                        puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'time-trial')
                    elif two_players_button_background.collidepoint(mouse_pos):
                        current_mode = 'two-players'
                        player_one_score = 0
                        player_two_score = 0
                        puzzle1 = DisplayPuzzle(current_difficulty, 550, screen, (0, 100), 'two-players')
                        puzzle2 = DisplayPuzzle(current_difficulty, 550, screen, (550, 100), 'two-players')

                        score_label = medium_font.render(f'{player_one_score} vs {player_two_score}', False, WHITE)
                        score_rect = score_label.get_rect(center=(550, 75))
                        race_finished = False
                        pygame.mixer.Sound.play(click_sound)
                    elif play_screen_back_to_menu_background.collidepoint(mouse_pos):
                        current_mode = 'main-menu'
                        pygame.mixer.Sound.play(click_sound)

                    start = False
                    if start:
                        pygame.mixer.Sound.play(click_sound)
                        puzzle_list = three_by_three_puzzles if current_difficulty == 3 else four_by_four_puzzles
                        puzzle2.setState(deepcopy(puzzle_list[current_puzzle_index][0]))
                        player_one_score = 0
                        player_two_score = 0
                        race_finished = False

                elif current_mode == 'time-trial':
                    if puzzle1.getGameWon() and puzzle1.getBoardRect().collidepoint(mouse_pos):
                        puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'time-trial')

                    if time_trial_restart_button_background.collidepoint(mouse_pos):
                        puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'time-trial')
                        pygame.mixer.Sound.play(click_sound)
                    elif time_trial_back_to_menu_button_background.collidepoint(mouse_pos):
                        current_mode = "main-menu"
                        puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'demo')
                        pygame.mixer.Sound.play(click_sound)
                    elif time_trial_options_button_background.collidepoint(mouse_pos):
                        previous_mode = current_mode
                        current_mode = "options"
                        pygame.mixer.Sound.play(click_sound)

                elif current_mode == 'two-players':
                    if two_players_restart_button_background.collidepoint(mouse_pos):
                        puzzle1 = DisplayPuzzle(current_difficulty, 550, screen, (0, 100), 'two-players')
                        puzzle2 = DisplayPuzzle(current_difficulty, 550, screen, (550, 100), 'two-players')
                        race_finished = False
                        pygame.mixer.Sound.play(click_sound)
                    elif two_players_back_to_menu_button_background.collidepoint(mouse_pos):
                        current_mode = "main-menu"
                        puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'demo')
                        pygame.mixer.Sound.play(click_sound)
                    elif two_players_options_button_background.collidepoint(mouse_pos):
                        previous_mode = current_mode
                        current_mode = "options"
                        pygame.mixer.Sound.play(click_sound)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if current_mode == 'options':
                    if music_slider.getDragging():
                        music_slider.setDragging(False)
                    elif sfx_slider.getDragging():
                        sfx_slider.setDragging(False)

            elif event.type == pygame.KEYDOWN:
                if current_mode == 'main-menu':
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(click_sound)
                        current_mode = 'play'
                    elif event.key == pygame.K_o:
                        pygame.mixer.Sound.play(click_sound)
                        previous_mode = 'main-menu'
                        current_mode = 'options'

                elif current_mode == 'options':
                    if event.key == pygame.K_3:
                        current_difficulty = 3
                        pygame.mixer.Sound.play(click_sound)
                    elif event.key == pygame.K_4:
                        current_difficulty = 4
                        pygame.mixer.Sound.play(click_sound)
                    elif event.key == pygame.K_ESCAPE:
                        current_mode = previous_mode
                        pygame.mixer.Sound.play(click_sound)


                elif current_mode == 'play':
                    if event.key == pygame.K_1:
                        current_mode = 'time-trial'
                        pygame.mixer.Sound.play(click_sound)
                        puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'time-trial')

                    elif event.key == pygame.K_3:
                        current_mode = 'two-players'
                        player_one_score = 0
                        player_two_score = 0
                        puzzle1 = DisplayPuzzle(current_difficulty, 550, screen, (0, 100), 'two-players')
                        puzzle2 = DisplayPuzzle(current_difficulty, 550, screen, (550, 100), 'two-players')
                        score_label = medium_font.render(f'{player_one_score} vs {player_two_score}', False, WHITE)

                        score_rect = score_label.get_rect(center=(550, 75))

                        race_finished = False

                        pygame.mixer.Sound.play(click_sound)

                    elif event.key == pygame.K_ESCAPE:
                        current_mode = 'main-menu'
                        pygame.mixer.Sound.play(click_sound)

                    if start:
                        pygame.mixer.Sound.play(click_sound)
                        puzzle_list = three_by_three_puzzles if current_difficulty == 3 else four_by_four_puzzles
                        puzzle2.setState(deepcopy(puzzle_list[current_puzzle_index][0]))
                        player_one_score = 0
                        player_two_score = 0
                        race_finished = False

                    elif event.key == pygame.K_m:
                        current_mode = "main-menu"
                        puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'demo')
                        pygame.mixer.Sound.play(click_sound)
                    elif event.key == pygame.K_o:
                        previous_mode = current_mode
                        current_mode = "options"
                        pygame.mixer.Sound.play(click_sound)

                if current_mode in ['time-trial']:
                    if event.key == pygame.K_LEFT:
                        player_one_direction = 'left'
                    if event.key == pygame.K_RIGHT:
                        player_one_direction = 'right'
                    if event.key == pygame.K_UP:
                        player_one_direction = 'up'
                    if event.key == pygame.K_DOWN:
                        player_one_direction = 'down'

                    if event.key == pygame.K_a:
                        player_one_direction = 'left'
                    if event.key == pygame.K_d:
                        player_one_direction = 'right'
                    if event.key == pygame.K_w:
                        player_one_direction = 'up'
                    if event.key == pygame.K_s:
                        player_one_direction = 'down'

                    if event.key == pygame.K_r:
                        if current_mode == 'time-trial':
                            puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'time-trial')

                elif current_mode == 'two-players':

                    if event.key == pygame.K_a:
                        player_one_direction = 'left'
                    if event.key == pygame.K_d:
                        player_one_direction = 'right'
                    if event.key == pygame.K_w:
                        player_one_direction = 'up'
                    if event.key == pygame.K_s:
                        player_one_direction = 'down'

                    if event.key == pygame.K_LEFT:
                        player_two_direction = 'left'
                    if event.key == pygame.K_RIGHT:
                        player_two_direction = 'right'
                    if event.key == pygame.K_UP:
                        player_two_direction = 'up'
                    if event.key == pygame.K_DOWN:
                        player_two_direction = 'down'

                    if event.key == pygame.K_r:
                        puzzle1 = DisplayPuzzle(current_difficulty, 550, screen, (0, 100), 'two-players')
                        puzzle2 = DisplayPuzzle(current_difficulty, 550, screen, (550, 100), 'two-players')
                        race_finished = False
                        pygame.mixer.Sound.play(click_sound)
                    elif event.key == pygame.K_m:
                        current_mode = "main-menu"
                        puzzle1 = DisplayPuzzle(current_difficulty, SCREEN_HEIGHT, screen, (0, 0), 'demo')
                        pygame.mixer.Sound.play(click_sound)
                    elif event.key == pygame.K_o:
                        previous_mode = current_mode
                        current_mode = "options"
                        pygame.mixer.Sound.play(click_sound)

        screen.fill(BLACK)

        # displays the elements in main menu
        if current_mode == 'main-menu':
            updateDemo(deltatime)

            pygame.draw.rect(screen, WHITE, play_button_background, 3)
            screen.blit(play_button_text, play_button_rect)

            pygame.draw.rect(screen, WHITE, main_menu_options_button_background, 3)
            screen.blit(main_menu_options_button_text, main_menu_options_button_rect)

        # displays the elements in options menu
        elif current_mode == 'options':
            if music_slider.getDragging():
                music_slider.drag(pygame.mouse.get_pos()[0])
                music_volume = music_slider.getValue()
                pygame.mixer.music.set_volume(music_volume)
            if sfx_slider.getDragging():
                sfx_slider.drag(pygame.mouse.get_pos()[0])
                sfx_volume = sfx_slider.getValue()
                click_sound.set_volume(sfx_volume)
                slide_sound.set_volume(sfx_volume)

            screen.blit(options_label, options_label_rect)

            screen.blit(three_by_three_button_text, three_by_three_button_rect)
            screen.blit(four_by_four_button_text, four_by_four_button_rect)

            five_by_five_button_text = big_font.render('5x5', False,
                                                       WHITE if previous_mode != '' else DISABLED)
            five_by_five_button_rect = five_by_five_button_text.get_rect(center=(825, 250))
            screen.blit(five_by_five_button_text, five_by_five_button_rect)

            if current_difficulty == 3:
                pygame.draw.rect(screen, WHITE, three_by_three_button_background, 3)
            elif current_difficulty == 4:
                pygame.draw.rect(screen, WHITE, four_by_four_button_background, 3)
            else:
                pygame.draw.rect(screen, WHITE, five_by_five_button_background, 3)

            screen.blit(volumn_label, volumn_label_rect)
            screen.blit(music_label, music_label_rect)
            music_slider.draw()
            screen.blit(sfx_label, sfx_label_rect)
            sfx_slider.draw()

            pygame.draw.rect(screen, WHITE, return_button_background, 3)
            screen.blit(return_button_text, return_button_rect)

        elif current_mode == 'play':
            updateDemo(deltatime)

            pygame.draw.rect(screen, WHITE, time_trial_button_background, 3)
            screen.blit(time_trial_button_text, time_trial_button_rect)

            pygame.draw.rect(screen, WHITE, two_players_button_background, 3)
            screen.blit(two_players_button_text, two_players_button_rect)

            pygame.draw.rect(screen, WHITE, play_screen_back_to_menu_background, 3)
            screen.blit(play_screen_back_to_menu_button_text, player_screen_back_to_menu_button_rect)


        elif current_mode == 'time-trial':
            puzzle1.update(player_one_direction, deltatime)
            screen.blit(time_trial_best_time_label, time_trial_best_time_rect)

            best_time_text = big_font.render(formatTime(best_time[puzzle1.getDifficulty()]), False, WHITE)
            best_time_text_rect = best_time_text.get_rect(topleft=(775, 160))
            screen.blit(best_time_text, best_time_text_rect)

            screen.blit(time_trial_time_label, time_trial_time_rect)

            if not puzzle1.getGameWon():
                time_passed = pygame.time.get_ticks() - puzzle1.getCreationTime()
                time_label = big_font.render(formatTime(time_passed), False, WHITE)
                time_rect = time_label.get_rect(topleft=(775, 285))
            elif not puzzle1.getCheckedAgainstBestTime():
                if best_time[puzzle1.getDifficulty()] == None:
                    best_time[puzzle1.getDifficulty()] = time_passed
                elif time_passed < best_time[puzzle1.getDifficulty()]:
                    best_time[puzzle1.getDifficulty()] = time_passed
                puzzle1.setCheckedAgainstBestTime(True)

            screen.blit(time_label, time_rect)
            screen.blit(time_trial_move_label, time_trial_move_rect)

            move_label = big_font.render(f'{puzzle1.getMoves()}', False, WHITE)
            move_rect = move_label.get_rect(topleft=(775, 410))
            screen.blit(move_label, move_rect)

            pygame.draw.rect(screen, WHITE, time_trial_restart_button_background, 3)
            screen.blit(time_trial_restart_button_text, time_trial_restart_button_rect)

            pygame.draw.rect(screen, WHITE, time_trial_back_to_menu_button_background, 3)
            screen.blit(time_trial_back_to_menu_button_text, time_trial_back_to_menu_button_rect)

            pygame.draw.rect(screen, WHITE, time_trial_options_button_background, 3)
            screen.blit(time_trial_options_button_text, time_trial_options_button_rect)

        elif current_mode == 'two-players':
            puzzle1.update(player_one_direction, deltatime)
            puzzle2.update(player_two_direction, deltatime)
            if (puzzle1.getGameWon() or puzzle2.getGameWon()) and not race_finished:
                puzzle1.setRaceFinished(True)
                puzzle2.setRaceFinished(True)
                race_finished = True

                if puzzle1.getGameWon():
                    player_one_score += 1
                else:
                    player_two_score += 1

                score_label = medium_font.render(f'{player_one_score} vs {player_two_score}', False, WHITE)
                score_rect = score_label.get_rect(center=(550, 75))

            if not race_finished:
                time_passed = pygame.time.get_ticks()
                time_string = formatTime(time_passed - puzzle1.getCreationTime())
                time_label = small_font.render(f'Time: {time_string}', False, WHITE)
                time_rect = time_label.get_rect(topleft=(450, 20))

            screen.blit(player_one_label, player_one_rect)
            screen.blit(player_two_label, player_two_rect)
            screen.blit(score_label, score_rect)

            pygame.draw.rect(screen, WHITE, two_players_restart_button_background, 3)
            screen.blit(two_players_restart_button_text, two_players_restart_button_rect)

            pygame.draw.rect(screen, WHITE, two_players_back_to_menu_button_background, 3)
            screen.blit(two_players_back_to_menu_button_text, two_players_back_to_menu_button_rect)

            pygame.draw.rect(screen, WHITE, two_players_options_button_background, 3)
            screen.blit(two_players_options_button_text, two_players_options_button_rect)

            screen.blit(time_label, time_rect)

        elif current_mode == '':
            puzzle1.update(player_one_direction, deltatime)
            screen.blit(objective_label, objective_rect)
            puzzle1.update(player_one_direction, deltatime)

            if (puzzle1.getGameWon() or puzzle2.getGameWon()) and not race_finished:
                puzzle1.setRaceFinished(True)
                puzzle2.setRaceFinished(True)
                race_finished = True

                if puzzle1.getGameWon():
                    player_one_score += 1
                    if best_time[puzzle1.getDifficulty()] == None:
                        best_time[puzzle1.getDifficulty()] = time_passed
                    elif time_passed < best_time[puzzle1.getDifficulty()]:
                        best_time[puzzle1.getDifficulty()] = time_passed
                    puzzle1.setCheckedAgainstBestTime(True)
                else:
                    player_two_score += 1

            if not race_finished:
                time_passed = pygame.time.get_ticks() - puzzle1.getCreationTime()
                time_label = big_font.render(formatTime(time_passed), False, WHITE)
                time_rect = time_label.get_rect(topleft=(675, 235))

            screen.blit(players_game_label, players_game_rect)

            best_time_text = big_font.render(formatTime(best_time[puzzle1.getDifficulty()]), False, WHITE)
            best_time_text_rect = best_time_text.get_rect(topleft=(675, 110))
            screen.blit(best_time_text, best_time_text_rect)
            screen.blit(time_label, time_rect)

            player_score_label = big_font.render(f'{player_one_score}', False, WHITE)
            player_score_rect = player_score_label.get_rect(topleft=(575, 450))

        pygame.display.update()


if __name__ == '__main__':
    main()
