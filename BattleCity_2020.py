"""             Описание проекта"""


# -*- coding: utf-8 -*-
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame import *
import sys, random, math, time
import os, os.path, pyperclip
import configparser, webbrowser


from ctypes import *

init()

pygame.font.init()
# font = font.SysFont('calibri', 17)
# window_info_font = font.SysFont('data\\fonts\\serifer.fon', 17+9)
battlecity_font = pygame.font.Font(os.getcwd()+'\\data\\fonts\\2003.ttf', 34)
window_info_font = pygame.font.Font(os.getcwd()+'\\data\\fonts\\9303.ttf', 13)
battlecity_font_stage = pygame.font.Font(os.getcwd()+'\\data\\fonts\\2003.ttf', 33)

win_name = 'BattleCity 20.20'
icon_name = 'icon.ico'

# True если включить чит-режим
CHEAT_MODE = False


# ПЕРЕМЕННАЯ ДЛЯ ТЕСТИРОВАНИЯ МОДУЛЕЙ ИГРЫ
# ОТВЕЧАЕТ ЗА ЗАПУСК СЛАЙДОВ (1 - битва, 2 - экран счета очков, 3 - gameover, 4 - главное меню, 5 - серый фон с надписью stage N, 6 - слайд постройки уровня)
RUN_SLIDE_NOW = 4 #4
dict_RUN_SLIDE_NOW = {"g": RUN_SLIDE_NOW}
# ТИП БОКОВОГО ИНТЕРФЕЙСА (1 - BattleCity, 2 - Tank 1994 с ракетами, 3 - Tank 1994 без ракет)
TYPE_RIGHT_INTERFACE = 1


# dict_RUN_SLIDE_NOW["g"]
LIST_FOR_RANDOM_BONUS = ["immortality", "star", "grenade", "stoptime", "tank", 'shovel', "grenade", "stoptime"]
# LIST_FOR_RANDOM_BONUS = ["tank"]

# True если играют два игрока, False если один игрок.
TWO_PLAYERS = False

campaign_no_icon = "data/textures/gui/menu/buttons/campaign/no_icon.png"


dict_timer_shim_label_kill_block = {"now": 0, "all": 50}

# True если карта на конструкторе была загружена. False, если конструктор пустой.
dict_level_loaded_status = {"g": False}




# #---ЦВЕТА---

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREEN2 = (97,255,66)
GREEN3 =(97,255,89)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
# GREY = (102, 102, 102)
GREY = (99, 99, 99)
RED_COUNT = (181, 49, 32)
YELLOW_COUNT = (234, 158, 34)
YELLOW = (255,254,73)
GREY_BLACK = (61,61,61)
RED = (255,0,0)
GREY_BLACK_DLC = (20,20,20)
# BLACK = [0, 0, 0]
# WHITE = [255, 255, 255]
# GREEN = [0, 255, 0]
# GREEN2 = [97,255,66]
# GREEN3 = [97,255,89]
# BLUE = [0, 0, 255]
# RED = [255, 0, 0]
# # GREY = (102, 102, 102)
# GREY = [99, 99, 99]
# RED_COUNT = [181, 49, 32]
# YELLOW_COUNT = [234, 158, 34]
# YELLOW = [255,254,73]
# GREY_BLACK = [61,61,61]
# RED = [255,0,0]
# GREY_BLACK_DLC = [20,20,20]


BATTLE_BG_COLOR = GREY_BLACK # GREY
CONSTRUCTION_BG_COLOR = GREY_BLACK

# Логика ракет (1 - если похоже на Tank 1994, 2 - как обычные снаряды)
ROCKET_LOGIC = 2

# ПРИСУТСТВУЮТ ЛИ В ИГРЕ РАКЕТЫ (-1 если нет ракет, любое другое целое натуральное число - стартовое количество ракет)
if TYPE_RIGHT_INTERFACE in [1, 3]:
	RC = -1
elif TYPE_RIGHT_INTERFACE == 2:
	if CHEAT_MODE == False:
		RC = 3
	else:
		RC = 999

# RC = 999
ROCKET_COLUMN = {"start": RC, "now": RC}
# ROCKET_COLUMN["start"]


############

VIEW_GRID = {}

# Показывать ли сетку в режиме конструкции
VIEW_GRID["g"] = True


VIEW_BASE = {}

# Показывать ли орла, его стены и точки спавна игрока и врагов
VIEW_BASE["g"] = True

# Какие координаты по Х и У исключать и не ставить на них блоки
CONST_COORD_EXCEPTIONS = ((48, 25), (336, 25), (624, 25), (240, 601), (432, 601), (288, 601), (288, 553), (336, 553), (384, 553), (384, 601), (432, 601), (336, 601))




# тип загрузчика (строка, принимает значения "classic" если зaгружать дефолтные текстуры или "name_dlc" если загружать из dlc с именем папки name_dlc)
TYPE_LOADER = dict()
TYPE_LOADER["g"] = "classic" #"classic"

if TYPE_LOADER["g"] == "classic":
	# Откуда загружать текстуры (закинул удочку на обработку dlc)
	LOAD_TEXTURES = "data/textures/"
	LOAD_LEVELS = "data/configs/levels/"
else:
	try:
		LOAD_TEXTURES = f"dlc/{TYPE_LOADER['g']}/textures/"
		LOAD_LEVELS = f"dlc/{TYPE_LOADER['g']}/configs/levels/"
	except Exception:
		LOAD_TEXTURES = "data/textures/"
		LOAD_LEVELS = "data/configs/levels/"
	# LOAD_TEXTURES = "dlc/enemy_player/textures/"


# Если какой то текстуры не обнаруживается, загружается ее базовый аналог из этой папки
DEFAULT_TEXTURES = "data/textures/"

# Конструктор и обработчик dlc файлов
ALL_TEXTURES_TANKS = f'{LOAD_TEXTURES}tanks/'
ALL_BUTTONS_FOLDER = '%s/gui/menu/buttons/'

############


try:
	IMAGE_FULLSCREEN_BORDER = image.load(LOAD_TEXTURES+'/gui/menu/screens/full_screen_border.png')
except Exception:
	IMAGE_FULLSCREEN_BORDER = image.load(DEFAULT_TEXTURES+'/gui/menu/screens/full_screen_border.png')





# Какова вероятность того, что враг при контакте с КИРПИЧНОЙ стеной выстрелит (больше - вероятнее всего выстрелит)
Difficulty_of_enemies = 120 #80

# Как долго враг будет делать одно и то же действие (максимальное значение тактов)
TIMER_AI_MAKE_ONE = 220 #150

# Сколько жизней дается вначале уровня
START_RESPAWN_COUNT = 2 # 2
# clone_START_RESPAWN_COUNT = START_RESPAWN_COUNT

# dict_respawn_count = dict()
# dict_respawn_count["now"] =  START_RESPAWN_COUNT
# dict_respawn_count["all"] =  START_RESPAWN_COUNT

# ФЛАГ
flag_minus_restart = False




# Сколько тактов будет сохраняться скорость танка, если он едет по льду
SLIP_TIMER = {"all": 55**2, "now": 0}


# Запускаемый сейчас уровень (уровень 36 - кастомный, уровень 35 - финальный)
level_number = dict()
level_number["g"] = 1

# СПАВНЯТСЯ ЛИ ПРОТИВНИКИ В ИГРЕ. True ЕСЛИ ДА
SPAWN_ENEMY_STATUS = 1

# Если True то вырубает звук во всей игре
DESTROY_VOLUME = 0

# Какой стартовый уровень танка у игрока установлен по умолчанию (от 1 до 4 включительно)
PLAYER_LEVEL_START = 1


# Во сколько раз будет увеличиваться каждый элемент игры при переходе в полноэкранный режим
BUST_BIGGER_SPRITES_ALL_SCREEN = 2

# Через сколько выходить в главное меню после анимации GameOver
TIMER_EXIT_MENU_GAMEOVER = {"all": 160, "now": 0}


# ПРАВИЛА ПОДСЧЕТА И ПОКАЗА ОЧКОВ
COUNTER_RULES = {
	# уровень танка противника: количество начисляемых очков
	"1": "100",
	"2": "200",
	"3": "300", 
	"4": "400",
	"bonus_get": "500",
	"timer": 30, # сколько тактов существует надпись на экране
}


# ОБЩЕЕ КОЛИЧЕСТВО ОЧКОВ ЗА РАУНД
ROUND_COUNTS = {
	# уровень: сумма очков
	# Например запись "1": 400 означает что сумма очков всех убитых танков 1 уровня составляет 400 единиц
	# "1": 1800,
	# "2": 400,
	"1": 0,
	"2": 0,
	"3": 0,
	"4": 0,	
	"other": 0, # учитываются другие источники (взятие бонусов и т.д.)
}



# Словарь, который будет менятся во время игры
# Хранит в себе булевые значения бонусов, которые в данный момент действуют на танк
PLAYER1_NOW_BONUS = {
	"immortality": False,
	"star": False,
	"stoptime": False,
	"shovel": False,	
}


def clear_player1_bonus():
	PLAYER1_NOW_BONUS["immortality"] = False
	PLAYER1_NOW_BONUS["star"] = False
	PLAYER1_NOW_BONUS["stoptime"] = False
	PLAYER1_NOW_BONUS["shovel"] = False





# LIST_FOR_RANDOM_BONUS = ["shovel"]


# Счетчик бонусов для танков 4 лвл
counter_bonuses_lvl4 = 0

# бессмертие
BONUSCONFIG_immortality = {
	# сколько тактов действует после возрождения
	"timer_respawn": 160, 
	
	# сколько тактов действует после взятия бонуса
	"timer_bonus": 300,
}



# Сколько тактов бонус живет на карте
TIMER_LIVE_BONUS = 600

# КАК ДОЛГО РАБОТАЕТ БОНУС ЛОПАТЫ (после указанного количество тактов начнется мерцание стены, которое вскоре пропадает)
TIMER_SHOVEL = 500


dict_PAUSE_GAME = {"g": False}





'''
КОНФИГ ДЛЯ ПЕРВОГО КРУГА ПРОХОЖДЕНИЯ ИГРЫ

Так как в игре 35 разных уровней, а циклов их прохождения бесконечно много,
то для первого круга и всех последущих будет два конфига
- первый: упрощенный
- второй: усложненный

'''



CONFIG_ROUND1_LEVELS = { # Всего 20
		
		# "lvl1": 18,		
		# "lvl2": 2,
		# "lvl3": 0,
		# "lvl4": 0,


		"lvl1": 18,
		"lvl2": 2,
		"lvl3": 0,
		"lvl4": 0,

		# КАК ЧАСТО БУДЕТ ПОЯВЛЯТСЯ ПРОТИВНИК ПОСЛЕ УБИЙСТВА ПОСЛЕДНЕГО (меньше - быстрее)
		"timer_respawn": 70, #70,

		# СКОЛЬКО ПРОТИВНИКОВ МОЖЕТ БЫТЬ ОДНОВРЕМЕННО НА ПОЛЕ БОЯ
		"all_enemys_count_in_battle": 4,
		}

LOAD_ENEMY_CONFIG = dict()
LOAD_ENEMY_CONFIG["g"] = CONFIG_ROUND1_LEVELS


CONFIG_ROUND2_LEVELS = { # Всего 20

		"lvl1": 8,		
		"lvl2": 2,
		"lvl3": 8,
		"lvl4": 2,

		# КАК ЧАСТО БУДЕТ ПОЯВЛЯТСЯ ПРОТИВНИК ПОСЛЕ УБИЙСТВА ПОСЛЕДНЕГО (меньше - быстрее)
		"timer_respawn": 70, #70,

		# СКОЛЬКО ПРОТИВНИКОВ МОЖЕТ БЫТЬ ОДНОВРЕМЕННО НА ПОЛЕ БОЯ
		"all_enemys_count_in_battle": 4,
		}

CONFIG_ROUND3_LEVELS = { # Всего 20

		"lvl1": 0,		
		"lvl2": 6,
		"lvl3": 4,
		"lvl4": 10,

		# КАК ЧАСТО БУДЕТ ПОЯВЛЯТСЯ ПРОТИВНИК ПОСЛЕ УБИЙСТВА ПОСЛЕДНЕГО (меньше - быстрее)
		"timer_respawn": 70, #70,

		# СКОЛЬКО ПРОТИВНИКОВ МОЖЕТ БЫТЬ ОДНОВРЕМЕННО НА ПОЛЕ БОЯ
		"all_enemys_count_in_battle": 4,
		}


# СПИСОК СЛУЧАЙНЫХ СОБЫТИЙ ДЛЯ ВРАГА
LIST_RANDOM_EVENT_ENEMY = [ # ДВИЖЕНИЕ
							'up', 
							'down', 
							'left',
							'right', 
							# СТРЕЛЬБА
							# 'do_shooting',
							# 'stop_shooting',
							# ДРУГОЕ							
							]


# СИСТЕМНАЯ ПЕРЕМЕННАЯ ДЛЯ ОТКЛЮЧЕНИЯ УПРАВЛЕНИЯ ТАНКОМ ИГРОКА (True если заблокировать)
GAME_OVER = False

# СИСТЕМНАЯ ПЕРЕМЕННАЯ ДЛЯ СТАТУСА ПАУЗЫ ИГРЫ (True если пауза)
PAUSE_GAME = False






### ДРУГИЕ НАТРОЙКИ ТАНКОВ ###
# Скорость движения надписи GAME OVER снизу вверх
SPEED_MOVE_GAMEOVER = 2.5

# Сколько ХП у вражеского танка 4 уровня
HP_ENEMY_LVL4 = 300

# Тип анимации повреждений танка 4 уровня (1 - BattleCity, 2 - Tank 1990) (2 по умолчанию)
TYPE_ANIMATIONS_ENEMY_LVL4 = 2




# Список уровней танков, кто может ломать бетон (враги не могут ломать стены)
LEVEL_TANKS_MAY_KILL_BETON_PLAYER = [4]

# Счетчик пробитых стен (нужен для танков, пробивающих бетон)
count_destroyed_walls = 0

# Сколько стен может пробить танк игрока 4 уровня (2 по умолчанию)
HIGH_LEVEL_TANK_MAY_DESTROY_WALLBRICKS = 2

# Через сколько тактов должен возродится танк игрока
RESPAWN_TIMER_PLAYER = 30

# СКОЛЬКО ТАКТОВ ДЕЙСТВУЕТ БОНУС ОСТАНОВКИ ВСЕХ ТАНКОВ ПРОТИВНИКА
TIMER_STOPTIME = 600

# Сколько миганий стены на базе будет сделано (количество раз)
SHIM_SHOVEL_ANIMATION_COUNT = 7



SPAWN_BASE = (312, 577)



# WIDTH = 768
# HEIGHT = 673
WIDTH = 800
HEIGHT = 750



WIDTH_POLE = 624
HEIGHT_POLE = 624
SPAWN_POLE = (48, 25)

VERSION = '0.1beta'
GIT = __doc__

FPS = 60

# size = (768, 512)
win_size = (WIDTH, HEIGHT)
fpsClock=pygame.time.Clock()

screen = display.set_mode(win_size)
display.set_caption(win_name)
display.set_icon(image.load(icon_name))



# PARAMS_RECT_DESTROY_MOUSE_CONST = (250, 665, 320, 75)
# PARAMS_RECT_DESTROY_MOUSE_CONST = (720, SPAWN_POLE[1], 48, 48*12)
PARAMS_RECT_DESTROY_MOUSE_CONST = (720+6, SPAWN_POLE[1], 48-12, 48*12)





#### СЕКЦИЯ В КОТОРОЙ ЗАГРУЖАЕМ ЗВУКИ ДЛЯ ИГРЫ ####

path_sounds = 'data/sounds/'


MUSIC_shot_tanks = pygame.mixer.Sound(path_sounds+'shot.ogg')
MUSIC_bullet_collide = pygame.mixer.Sound(path_sounds+'bullet_collide.ogg')
MUSIC_kill_enemy = pygame.mixer.Sound(path_sounds+'kill_enemy.ogg')
MUSIC_bullet_collide_tank = pygame.mixer.Sound(path_sounds+'bullet_collide_tank.ogg')
MUSIC_bullet_collide_wall = pygame.mixer.Sound(path_sounds+'bullet_collide_wall.ogg')
MUSIC_bullet_collide_beton = pygame.mixer.Sound(path_sounds+'bullet_collide_beton.ogg')

MUSIC_use_bonus = pygame.mixer.Sound(path_sounds+'use_bonus.ogg')
MUSIC_get_bonus = pygame.mixer.Sound(path_sounds+'get_bonus.wav')

MUSIC_bonus_life = pygame.mixer.Sound(path_sounds+'bonus_life.wav')

MUSIC_total_tick = pygame.mixer.Sound(path_sounds+'total_tick.wav')

MUSIC_screenshot = pygame.mixer.Sound(path_sounds+'screenshot_sound.ogg')

MUSIC_INTRO = pygame.mixer.Sound(path_sounds+'intro.wav')





# MUSIC_kill_player = pygame.mixer.Sound(path_sounds+'kill_player.ogg')
MUSIC_kill_player = pygame.mixer.Sound(path_sounds+'buh.wav')


MUSIC_move_enemy = pygame.mixer.Sound(path_sounds+'enemy_move.wav')
MUSIC_move_player = pygame.mixer.Sound(path_sounds+'move.wav')
# MUSIC_move_player = pygame.mixer.Sound('data/sounds/tanks/ogg/move.ogg')


# MUSIC_pause_get = pygame.mixer.Sound(path_sounds+'pause_get.ogg')
MUSIC_pause_get = pygame.mixer.Sound(path_sounds+'pause_get.wav')

MUSIC_game_over = pygame.mixer.Sound(path_sounds+'game_over.wav')



#### СОЗДАЕМ ЗВУКОВЫЕ КАНАЛЫ ####
CHANNEL_enemy_move = pygame.mixer.Channel(1)
CHANNEL_player_move = pygame.mixer.Channel(2)

CHANNEL_bullet_collide_tank = pygame.mixer.Channel(3)
CHANNEL_bullet_collide_wall = pygame.mixer.Channel(4)
CHANNEL_shot_tanks = pygame.mixer.Channel(5)
CHANNEL_kill_enemy = pygame.mixer.Channel(6)
CHANNEL_get_bonus = pygame.mixer.Channel(7)

CHANNEL_gui_music = pygame.mixer.Channel(7)


#### НАСТРАИВАЕМ ЗВУКИ ДЛЯ ИГРЫ ####
set_volume = 0.4
CHANNEL_enemy_move.set_volume(set_volume)
CHANNEL_player_move.set_volume(set_volume)

CHANNEL_bullet_collide_tank.set_volume(set_volume)
CHANNEL_bullet_collide_wall.set_volume(set_volume)
CHANNEL_shot_tanks.set_volume(set_volume)
CHANNEL_kill_enemy.set_volume(set_volume)
CHANNEL_bullet_collide_wall.set_volume(set_volume)
CHANNEL_gui_music.set_volume(set_volume)
MUSIC_pause_get.set_volume(set_volume)
MUSIC_total_tick.set_volume(set_volume)
# MUSIC_get_bonus.set_volume(set_volume)
# MUSIC_use_bonus.set_volume(set_volume)


if DESTROY_VOLUME == True:
	MUSIC_move_player.set_volume(0.0)
	MUSIC_shot_tanks.set_volume(0.0)
	MUSIC_bullet_collide.set_volume(0.0)
	MUSIC_kill_enemy.set_volume(0.0)
	MUSIC_bullet_collide_tank.set_volume(0.0)
	MUSIC_bullet_collide_wall.set_volume(0.0)
	MUSIC_kill_player.set_volume(0.0)
	MUSIC_move_enemy.set_volume(0.0)
	MUSIC_pause_get.set_volume(0.0)
	MUSIC_bullet_collide_beton.set_volume(0.0)
	MUSIC_total_tick.set_volume(0.0)


PLAYER_SPAWN_X = 243

RANDOM_SPAWN_COORDINATS = [(48, SPAWN_POLE[1]), (336, SPAWN_POLE[1]), (624, SPAWN_POLE[1])]
CLONED_RANDOM_SPAWN_COORDINATS = RANDOM_SPAWN_COORDINATS




BULLET_SPEED = 7
BUST_BULLET_SPEED = 3
ROCKET_BUST_SPEED = 6

TANK_SPEED = 2

PLAYER = {
	"LVL1": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "player", 
	},

	"LVL2": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "player",
	},

	"LVL3": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "player",
	},

	"LVL4": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "player",
	},

	"lvl_start": PLAYER_LEVEL_START,
}


PLAYER_COPY = PLAYER

if TWO_PLAYERS == True:
	PLAYER_2 = {
	"LVL1": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "player", 
	},

	"LVL2": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "player",
	},

	"LVL3": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "player",
	},

	"LVL4": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "player",
	},

	"lvl_start": PLAYER_LEVEL_START,
}


ENEMY = {
	"LVL1": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL2": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED+1,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL3": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL4": {
		"hp": HP_ENEMY_LVL4,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"lvl_start": 1,
}



ENEMY_LVL2 = {
	"LVL1": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL2": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED+1,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL3": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL4": {
		"hp": HP_ENEMY_LVL4,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"lvl_start": 2,
}


ENEMY_LVL3 = {
	"LVL1": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL2": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED+1,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL3": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL4": {
		"hp": HP_ENEMY_LVL4,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"lvl_start": 3,
}


ENEMY_LVL4 = {
	"LVL1": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL2": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED+1,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL3": {
		"hp": 100,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
		"type_player": "enemy", 
	},

	"LVL4": {
		"hp": HP_ENEMY_LVL4,
		"damage": 100,
		"speed": TANK_SPEED,
		"bullet_speed": BULLET_SPEED,
		"type_player": "enemy", 
	},

	"lvl_start": 4,
}





################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
##################################################### КЛАССЫ, НЕОБХОДИМЫЕ ДЛЯ ОСТАЛЬНОГО ГРАФИЧЕСКОГО ИНТЕРФЕЙСА################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
timer_wait_end_game = 0

# Сколько тактов необходимо ждать перед тем, как завершить игру
TIMER_WAIT_END_GAME = 250

# ПЕРЕМЕННАЯ ДЛЯ ОКОНЧАНИЯ ПОБЕДНОЙ ИГРЫ (как GAME_OVER только вот эта)
GAME_WIN = False


class GAME_OVER_BRICKS(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)

		self.pos = pos
		'''LOAD_TEXTURES DEFAULT_TEXTURES'''

		try:
			self.image = image.load(f'{LOAD_TEXTURES}gui/gameover.png')
		except Exception:
			self.image = image.load(f'{DEFAULT_TEXTURES}gui/gameover.png')


		self.rect = self.image.get_rect()

		self.rect.center = self.pos




GAME_INTERFACE_DICT = {	
	# если равен 0, то звук воспроизведется 1 раз
	"game_over_bricks_sound": 0,

}



gameover_bricks_sprites = pygame.sprite.Group()
gameover_bricks_sprites.add(GAME_OVER_BRICKS(pos=(WIDTH//2, HEIGHT//2)))

def zero_counts():
	"""Обнуляет очки"""
	ROUND_COUNTS["1"], ROUND_COUNTS["2"], ROUND_COUNTS["3"], ROUND_COUNTS["4"] , ROUND_COUNTS["other"] = 0, 0, 0, 0, 0
	COUNT_LVL["1"], COUNT_LVL["2"], COUNT_LVL["3"], COUNT_LVL["4"] , COUNT_LVL["other"] = 0, 0, 0, 0, 0
	COUNT_KILLS_LVL["1"], COUNT_KILLS_LVL["2"], COUNT_KILLS_LVL["3"], COUNT_KILLS_LVL["4"] , COUNT_KILLS_LVL["other"] = 0, 0, 0, 0, 0
	COUNT_DEMONSTRATION_LVL["1"], COUNT_DEMONSTRATION_LVL["2"], COUNT_DEMONSTRATION_LVL["3"], COUNT_DEMONSTRATION_LVL["4"] , COUNT_DEMONSTRATION_LVL["other"] = " ", " ", " ", " ", " "
	COUNT_DEMONSTRATION_KILLS_LVL["1"], COUNT_DEMONSTRATION_KILLS_LVL["2"], COUNT_DEMONSTRATION_KILLS_LVL["3"], COUNT_DEMONSTRATION_KILLS_LVL["4"] , COUNT_DEMONSTRATION_KILLS_LVL["other"] = " ", " ", " ", " ", " "





def get_sum_counts():
	"""Возращает сумму очков за пройденный уровень"""
	return ROUND_COUNTS["1"]+ROUND_COUNTS["2"]+ROUND_COUNTS["3"]+ROUND_COUNTS["4"]+ROUND_COUNTS["other"]

def get_sum_desrtoyed_enemy():
	"""Возращает количество убитых врагов"""
	return ROUND_COUNTS["1"]//int(COUNTER_RULES["1"])+ROUND_COUNTS["2"]//int(COUNTER_RULES["2"])+ROUND_COUNTS["3"]//int(COUNTER_RULES["3"])+ROUND_COUNTS["4"]//int(COUNTER_RULES["4"])


# Сколько тактов проходит между прибавлением очков
TIMER_DEMONSTRATION_COUNT_LVL = 8 #8

timer_demonstration_count_lvl = 0

TIMER_TOTAL_COUNTER = {
	"all": TIMER_DEMONSTRATION_COUNT_LVL,
	"now": timer_demonstration_count_lvl,
}

# Во сколько раз значение тактов пройдет от того момента как все очки покажутся до момента переключения на уровень
BUST_TIMER_DEMONSTRATION_COUNT_LVL = 20





COUNT_LVL = {
	"1": 0,
	"2": 0,
	"3": 0,
	"4": 0,
	"total": 0,
}

COUNT_KILLS_LVL = {
	"1": 0,
	"2": 0,
	"3": 0,
	"4": 0,
}





COUNT_DEMONSTRATION_LVL = {
	"1": ' ',
	"2": ' ',
	"3": ' ',
	"4": ' ',
}

COUNT_DEMONSTRATION_KILLS_LVL = {
	"1": ' ',
	"2": ' ',
	"3": ' ',
	"4": ' ',
}


if TWO_PLAYERS == True:
	COUNT_LVL_P2 = {
		"1": 0,
		"2": 0,
		"3": 0,
		"4": 0,
		"total": 0,
	}

	COUNT_KILLS_LVL_P2 = {
		"1": 0,
		"2": 0,
		"3": 0,
		"4": 0,
	}


	COUNT_DEMONSTRATION_LVL_P2= {
		"1": ' ',
		"2": ' ',
		"3": ' ',
		"4": ' ',
	}

	COUNT_DEMONSTRATION_KILLS_LVL_P2 = {
		"1": ' ',
		"2": ' ',
		"3": ' ',
		"4": ' ',
	}


################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
##################################################### КЛАССЫ, НЕОБХОДИМЫЕ ДЛЯ СРАЖЕНИЙ #########################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################




class ScreenshotsWorker:
	def __init__(self, saved_name=f'screenshot{round(time.time())}', saved_format='png', saved_folder='screenshots/'):
		self.saved_name = saved_name
		self.saved_folder = saved_folder
		self.saved_format = saved_format

		if os.path.exists(self.saved_folder) == False:
			os.mkdir(self.saved_folder)

	def save_screen(self):
		pygame.image.save(screen, self.saved_folder+f"{self.saved_name}.{self.saved_format}")
		pyperclip.copy("")
		
		


# МАКРОСЫ, КОТОРЫЕ ОТВЕЧАЮТ ЗА ПОКАЗ ОПРЕДЕЛЕННОГО ТЕКСТА В ОКНЕ
SYS_TEXT_MACROS = {"win_name": False,
					"fps": True,
					"version": False,
					"git": False,
					"author": False,
					"level": False,
					}


# class SysText(pygame.sprite.Sprite):
class SysText():
	def __init__(self, level='None', bg=BATTLE_BG_COLOR, volume=str(not DESTROY_VOLUME), screen=screen, pos=(5, 0), macros=SYS_TEXT_MACROS, font=window_info_font):
		# pygame.sprite.Sprite.__init__(self)

		self.screen = screen

		self.pos = pos
		self.bg = bg
		self.macros = macros

		self.volume = volume

		self.window_info_font = window_info_font

		self.x = self.pos[0]
		self.y = self.pos[1]

		self.print_win_name = self.macros["win_name"]
		self.print_version = self.macros["version"]
		self.print_fps = self.macros["fps"]
		self.print_git = self.macros["git"]
		self.print_author = self.macros["author"]
		self.print_level = self.macros["level"]

		self.level = level



		self.end_text = ''

		if self.print_win_name == True:
			self.end_text += f'win_name: {win_name} | '

		if self.print_version == True:
			# self.end_text += f'v{VERSION} | '
			# lst_git_repository = sort(os.listdir(os.getcwd()+'/_git/'))
			lst_git_repository = sorted(os.listdir(os.getcwd()+'/_git/'))
			lst_git_repository.remove("_old")

			# string = lst_git_repository[len(lst_git_repository)-1][1:4]
			string = "0.1beta"

			self.end_text += f'v{string} | '


		if self.print_fps == True:
			now_clockfps_string = str(fpsClock)[11:16]
			self.end_text += f'FPS: {now_clockfps_string} '
			# fpsClock = fpsClock.replace('<Clock(fps=', '')

		if self.print_git == True:
			self.end_text += f'git: {GIT} | '

		if self.print_author == True:
			self.end_text += f'\t tankalxat34 | '

		if self.print_level == True:
			self.end_text += f' level: {self.level} | '

		# self.end_text += f'volume: {self.volume} | '+92*' '+'tankalxat34'


	def draw(self):
		text = self.window_info_font.render(self.end_text, 0, WHITE, (0,0,0))
		text.set_colorkey((0,0,0))
		(self.screen).blit(text, self.pos)
		# battlecity_font
		# pass



WALL_BUSH = {
	"form": "square",
	"texture": "bush",
}

WATER = {
	"form": "square",
	"texture": "water",
	"update_timer": 40,
}

WALL_BETON = {
	"texture": "betons",
	"form": "square",
}

WALL_BETON_24UP = {
	"texture": "betons",
	"form": "brick4",
}

WALL_BETON_24DOWN = {
	"texture": "betons",
	"form": "brick",
}

WALL_BETON_24LEFT = {
	"texture": "betons",
	"form": "brick2",
}

WALL_BETON_24RIGHT = {
	"texture": "betons",
	"form": "brick3",
}




WALL_BRICKS = {
	"form": "square",
	"texture": "bricks",
}

WALL_BRICKS_24 = {
	# вверх - 
	"form": "brick",
	"texture": "bricks",
}

WALL_BRICKS_24_R2 = {
	# влево \ 
	"form": "brick2",
	"texture": "bricks",
}

WALL_BRICKS_24_R3 = {
	# вправо /
	"form": "brick3",
	"texture": "bricks",
}

WALL_BRICKS_24_R4 = {
	# вниз _
	"form": "brick4",
	"texture": "bricks",
}

def AddExplosion(pos, sprite, big=False):
	"""
	Функция вызывает взрыв

	pos - кортеж из Х и У координат
	sprite - спрайт, на чем вызывается взрыв
	big - (необязателен) Если равен True, то проигрываются анимации большого взрыва
	"""

	explosion = Explosion(pos[0], pos[1], sprite, big)
	all_sprites.add(explosion)



class Wall(pygame.sprite.Sprite):
	def __init__(self, p, pos):
		pygame.sprite.Sprite.__init__(self)

		self.p = p
		self.pos = pos

		self.form = self.p["form"]
		self.texture = self.p["texture"]

		self.brick = None
		

		self.pos_x = self.pos[0]
		self.pos_y = self.pos[1]



		if self.form == 'square':
			# self.image = image.load('data/textures/map_objects/blocks/4_brick.png')
			for e in range(2):
				for t in range(2):
					for i in range(1, 5):
						self.brick = WallBrick(i, (self.pos_x, self.pos_y))
						walls_sprites.add(self.brick)
					self.pos_x += 24
				self.pos_y = pos[1]+24
				self.pos_x = pos[0]

		else:
			# print(self.form)
			if self.form == 'brick3':				
				for t in range(2):
					for i in range(1, 5):
						self.brick = WallBrick(i, (self.pos_x+24, self.pos_y))
						walls_sprites.add(self.brick)
					self.pos_y += 24

			if self.form == 'brick2':				
				for t in range(2):
					for i in range(1, 5):
						self.brick = WallBrick(i, (self.pos_x, self.pos_y))
						walls_sprites.add(self.brick)
					self.pos_y += 24

			if self.form == 'brick4':				
				for t in range(2):
					for i in range(1, 5):
						self.brick = WallBrick(i, (self.pos_x, self.pos_y))
						walls_sprites.add(self.brick)
					self.pos_x += 24

			if self.form == 'brick':				
				for t in range(2):
					for i in range(1, 5):
						self.brick = WallBrick(i, (self.pos_x, self.pos_y))
						walls_sprites.add(self.brick)
					self.pos_x += 24



		self.image = self.brick.image
		self.rect = self.image.get_rect()

		self.rect.x = -100
		self.rect.y = -100


class WallBrick(pygame.sprite.Sprite):
	"""Создает на экране маленький кирпичик"""
	def __init__(self, brick, pos):
		pygame.sprite.Sprite.__init__(self)

		self.brick = brick
		self.pos = pos
		'''LOAD_TEXTURES DEFAULT_TEXTURES'''

		self.data = f'{LOAD_TEXTURES}/map_objects/blocks/'
		try:
			self.image = image.load(self.data+f'1_brick_{self.brick}.png')
		except Exception:
			self.data = f'{DEFAULT_TEXTURES}/map_objects/blocks/'
			self.image = image.load(self.data+f'1_brick_{self.brick}.png')

		self.rect = self.image.get_rect()

		if self.brick == 1:
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]

		if self.brick == 2:
			self.rect.x = self.pos[0] - 12
			self.rect.y = self.pos[1]

		if self.brick == 3:
			self.rect.x = self.pos[0] - 12
			self.rect.y = self.pos[1] + 12

		if self.brick == 4:
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1] + 12


	def update(self):
		pass








class WallBetonBricks(pygame.sprite.Sprite):
	def __init__(self, brick, pos):
		pygame.sprite.Sprite.__init__(self)

		self.brick = brick
		self.pos = pos

		self.pos_x = self.pos[0]
		self.pos_y = self.pos[1]

		try:
			self.image = image.load(f'{LOAD_TEXTURES}/map_objects/blocks/1_beton.png')
		except Exception:
			self.image = image.load(f'{DEFAULT_TEXTURES}/map_objects/blocks/1_beton.png')

		self.rect = self.image.get_rect()

		self.rect.x = self.pos_x
		self.rect.y = self.pos_y

	def update(self):
		pass




class WallBeton(pygame.sprite.Sprite):
	def __init__(self, p, pos):
		pygame.sprite.Sprite.__init__(self)

		self.p = p

		self.form = self.p["form"]
		self.texture = self.p["texture"]

		self.pos_x = pos[0]
		self.pos_y = pos[1]


		if self.texture == 'betons':
			if self.form == 'square':
				for e in range(1, 3):
					for i in range(1, 3):
						self.beton = WallBetonBricks(i, (self.pos_x, self.pos_y))
						beton_sprites.add(self.beton)
						self.pos_x += 24

					self.pos_y = pos[1] + 24
					self.pos_x = pos[0]
			else:		
				if self.form == 'brick4':
					for i in range(1, 3):
						self.beton = WallBetonBricks(i, (self.pos_x, self.pos_y))
						beton_sprites.add(self.beton)
						self.pos_x += 24

				if self.form == 'brick':
					for i in range(1, 3):
						self.beton = WallBetonBricks(i, (self.pos_x, self.pos_y))
						beton_sprites.add(self.beton)
						self.pos_x += 24

				if self.form == 'brick2':
					for i in range(1, 3):
						self.beton = WallBetonBricks(i, (self.pos_x, self.pos_y))
						beton_sprites.add(self.beton)
						self.pos_y += 24

				if self.form == 'brick3':
					for i in range(1, 3):
						self.beton = WallBetonBricks(i, (self.pos_x, self.pos_y))
						beton_sprites.add(self.beton)
						self.pos_y += 24



		self.image = self.beton.image
		self.rect = self.image.get_rect()


		self.rect.x = -100
		self.rect.y = -100

	






class BaseEagle(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)

		self.pos = pos

		self.images = []
		# if os.path.exists('data_mods/textures/map_objects/base.png') == True:
		# 	self.images.append(image.load('data_mods/textures/map_objects/base.png'))
		# 	self.images.append(image.load('data_mods/textures/map_objects/base_lose.png'))
		# else:
		try:
			self.images.append(image.load(f'{LOAD_TEXTURES}/map_objects/base.png'))
		except Exception:
			self.images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/base.png'))


		try:
			self.images.append(image.load(f'{LOAD_TEXTURES}/map_objects/base_lose.png'))
		except Exception:
			self.images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/base_lose.png'))


		self.index = 0

		self.image = self.images[self.index]
		self.rect = self.image.get_rect()

		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]


	def update(self):
		self.rect.x = self.rect.x
		self.rect.y = self.rect.y


		if self.index == 0:
			collide_bullets = pygame.sprite.spritecollide(self, bullets, True)
			collide_bullets_enemy = pygame.sprite.spritecollide(self, bullets_enemy, True)
			if collide_bullets:
				MUSIC_kill_player.play()
				self.image = self.images[1]
				explosion = Explosion(self.rect.center[0], self.rect.center[1], self, True, killed_eagle=True)
				all_sprites.add(explosion)
				self.index = 1
				



			if collide_bullets_enemy:
				MUSIC_kill_player.play()
				self.image = self.images[1]
				explosion = Explosion(self.rect.center[0], self.rect.center[1], self, True, killed_eagle=True)
				all_sprites.add(explosion)
				self.index = 1
				


			


class Water(pygame.sprite.Sprite):
	def __init__(self, p, pos):
		pygame.sprite.Sprite.__init__(self)

		self.p = p

		self.form = self.p["form"]
		self.texture = self.p["texture"]
		self.update_timer = self.p["update_timer"]


		self.images = []
		self.index = 0

		self.counter = 0

		try:
			self.images.append(image.load(f'{LOAD_TEXTURES}/map_objects/water_a1.png'))
		except Exception:
			self.images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/water_a1.png'))

		try:
			self.images.append(image.load(f'{LOAD_TEXTURES}/map_objects/water_a2.png'))
		except Exception:
			self.images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/water_a2.png'))

		self.image = self.images[self.index]
		self.now_size = 24

		self.rect = self.image.get_rect()

		self.rect.x = pos[0]
		self.rect.y = pos[1]

		self.border_animation = 2
		self.index_border_animation = self.border_animation

	def update(self):
		self.counter += 1
		if self.counter >= self.update_timer:
			self.index += 1
			self.counter = 0
			if self.index >= self.border_animation:
				self.index = 0

		self.image = self.images[self.index]
			



class Bush(pygame.sprite.Sprite):
	def __init__(self, p, pos):
		pygame.sprite.Sprite.__init__(self)

		self.p = p

		self.form = self.p["form"]
		self.texture = self.p["texture"]

		try:
			self.image = image.load(f'{LOAD_TEXTURES}/map_objects/bush.png')
		except Exception:
			self.image = image.load(f'{DEFAULT_TEXTURES}/map_objects/bush.png')

		self.now_size = 24

		self.rect = self.image.get_rect()

		self.rect.x = pos[0]
		self.rect.y = pos[1]

	def update(self):
		self.image = self.image



class Ice(pygame.sprite.Sprite):
	def __init__(self, p, pos):
		pygame.sprite.Sprite.__init__(self)

		self.p = p

		self.form = self.p["form"]
		self.texture = self.p["texture"]

		try:
			self.image = image.load(f'{LOAD_TEXTURES}/map_objects/ice.png')
		except Exception:
			self.image = image.load(f'{DEFAULT_TEXTURES}/map_objects/ice.png')
		self.now_size = 24

		self.rect = self.image.get_rect()

		self.rect.x = pos[0]
		self.rect.y = pos[1]

	def update(self):
		self.image = self.image








flag = False









class Tank(pygame.sprite.Sprite):
	def __init__(self, p, pos_spawn=None, index_spawn=None, shim_tank=False, player2=False):
		pygame.sprite.Sprite.__init__(self)


		# True если танк будет мерцающий
		self.shim_tank = shim_tank

		# True если данный танк является вторым игроком
		self.player2 = player2

		self.p = p

		self.lvl_tank = str(p["lvl_start"])
		self.lvl_start = p["lvl_start"]

		self.pos_spawn = pos_spawn
		self.index_spawn = index_spawn

		self.hp = p[f"LVL{self.lvl_tank}"]["hp"]
		self.damage = p[f"LVL{self.lvl_tank}"]["damage"]
		self.speed = p[f"LVL{self.lvl_tank}"]["speed"]
		self.type_player = p[f"LVL{self.lvl_tank}"]["type_player"]

		if self.player2 == True:
			self.type_player += "2"
		

		self.images = []
		self.counter_shim = 0
		
		if self.lvl_start in [1, 2, 3, 4] and self.type_player == 'player':
			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r1.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r1.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r1.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r1.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r2.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r2.png'))
			
			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r2.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r2.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r3.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r3.png'))

			try:			
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r3.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r3.png'))

			try:			
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))

			try:			
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))

		elif self.lvl_start in [1, 2, 3] and self.type_player == 'enemy':
			# self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r1.png'))
			# self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r1.png'))
			# self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r2.png'))
			# self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r2.png'))
			# self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r3.png'))
			# self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r3.png'))
			# self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))
			# self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))
			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r1.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r1.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r1.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r1.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r2.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r2.png'))
			
			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r2.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r2.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r3.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r3.png'))

			try:			
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r3.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r3.png'))

			try:			
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))

			try:			
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))


		elif self.lvl_start == 4 and self.type_player!='player':
			if TYPE_ANIMATIONS_ENEMY_LVL4 == 1:
				color_texture = 'green'

				for i in range(2):
					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r1_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r1_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r1_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r1_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r2_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r2_{color_texture}.png'))
					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r2_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r2_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r3_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r3_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r3_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r3_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r4_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r4_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r4_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r4_{color_texture}.png'))
					color_texture = 'yellow'


				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r1.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r1.png'))

				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r1.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r1.png'))

				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r2.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r2.png'))
				
				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r2.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r2.png'))

				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r3.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r3.png'))

				try:			
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r3.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r3.png'))

				try:			
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))

				try:			
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))

				self.counter_shim = 0

			elif TYPE_ANIMATIONS_ENEMY_LVL4 == 2:
				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r1.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r1.png'))

				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r1.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r1.png'))

				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r2.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r2.png'))
				
				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r2.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r2.png'))

				try:
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r3.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r3.png'))

				try:			
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r3.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r3.png'))

				try:			
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))

				try:			
					self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))
				except Exception:
					self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))
				color_texture = 'yellow'		

				for i in range(2):
					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r1_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r1_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r1_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r1_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r2_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r2_{color_texture}.png'))
					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r2_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r2_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r3_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r3_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r3_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r3_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r4_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a1_r4_{color_texture}.png'))

					try:
						self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r4_{color_texture}.png'))
					except Exception:
						self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/heavy_tank/lvl{self.lvl_tank}_a2_r4_{color_texture}.png'))
					color_texture = 'green'


				self.counter_shim = 0



		# if self.shim_tank == True and self.lvl_start != 4 and self.type_player=='enemy':
		if self.shim_tank == True and self.type_player=='enemy':

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a1_r1.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a1_r1.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a2_r1.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a2_r1.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a1_r2.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a1_r2.png'))
			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a2_r2.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a2_r2.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a1_r3.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a1_r3.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a2_r3.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a2_r3.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a1_r4.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a1_r4.png'))

			try:
				self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a2_r4.png'))
			except Exception:
				self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/animations/bonus_tank/lvl{self.lvl_tank}_a2_r4.png'))
			self.counter_shim = 0


		# if len(enemys_sprites.sprites()) != 0:
		# CHANNEL_enemy_move.play(MUSIC_move_enemy, loops=-1)
		# elif len(enemys_sprites.sprites()) == 0:
		# 	CHANNEL_enemy_move.stop()

		# for e in self.images:
		# 	e = e.set_colorkey(BLACK)




		self.index = 0
		self.border_animation = 1
		self.index_border_animation = 0


		# self.counter_shot = 0
		
		self.image = self.images[self.index]
		# self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()

		self.counter = 0
		self.counter_shot = 0

		self.counter_shot_enemy = 0


		# self.random_anchor = random.choice(LIST_RANDOM_EVENT_ENEMY)
		self.random_anchor = 'down'

		self.now_enemy_event = ''

		self.counter_ai = 0
		self.random_timer_for_counter_ai = random.randint(0, TIMER_AI_MAKE_ONE)



		if self.type_player == 'player':

			if self.pos_spawn == None:
				self.rect.x = PLAYER_SPAWN_X
				# self.rect.y = WIDTH_POLE - SPAWN_POLE[1]
				self.rect.y = 678 - self.image.get_height()-26
			else:
				self.rect.x = self.pos_spawn[0]
				self.rect.y = self.pos_spawn[1]
				# self.index = self.index_spawn


		
		if self.type_player == 'enemy':

			self.started_timetime = 0
			self.lasted_timetime = 0

			self.index = 3
			self.border_animation = 5
			self.index_border_animation = 4

			self.ENEMY_now_speed_x = 0
			self.ENEMY_now_speed_y = 0




			random_spawn = random.choice(RANDOM_SPAWN_COORDINATS)
			# RANDOM_SPAWN_COORDINATS.remove(random_spawn)

			# if random_spawn != self.coords:
			# 	self.coords = random_spawn

			# self.default_list_coords.remove(random_spawn)


			if random_spawn[0] == 624:
				self.rect.x = WIDTH_POLE
			else:
				self.rect.x = random_spawn[0]

			
			self.rect.y = SPAWN_POLE[1]

			self.counter = 0


		# print(str(p["lvl_start"]))


	


	def shot(self):
		stop_shot = 12

		if self.type_player == 'player':

			if self.counter_shot > stop_shot:

				bullet = Bullet(self.p, self, count_destroyed_walls)
				if len(bullets.sprites()) == 0:
					
					CHANNEL_shot_tanks.play(MUSIC_shot_tanks)
					all_sprites.add(bullet)
					bullets.add(bullet)
					self.counter_shot = 0
				

		elif self.type_player == 'enemy':
			if self.counter_shot_enemy > stop_shot:
				bullet_enemy = Bullet(self.p, self, count_destroyed_walls)
				if len(bullets_enemy.sprites()) == 0:
					
					all_sprites.add(bullet_enemy)
					bullets_enemy.add(bullet_enemy)
					self.counter_shot_enemy = 0
					

	def shot_rocket(self):
		if ROCKET_COLUMN["now"] > 0 and ROCKET_COLUMN["start"] >= 0:
			stop_shot = 12

			if self.counter_shot > stop_shot:

				rocket = Rocket(self.p, self, count_destroyed_walls)
				if len(rockets_sprites.sprites()) == 0:
					
					CHANNEL_shot_tanks.play(MUSIC_shot_tanks)
					all_sprites.add(rocket)
					rockets_sprites.add(rocket)
					self.counter_shot = 0
					ROCKET_COLUMN["now"] -= 1
		

	def update(self):
		collide=False
		self.counter_shot += 1
		self.counter_shot_enemy += 1

		


		if self.type_player == 'player':





			now_speed_x = 0
			now_speed_y = 0
			
			self.counter += 1


			keystate = pygame.key.get_pressed()
			

			if self.hp <= 0:
				self.kill()
				MUSIC_kill_player.play()
				explosion = Explosion(self.rect.center[0], self.rect.center[1], self, True)
				all_sprites.add(explosion)
				explosions.add(explosion)
				player_sprites.remove(player)
				player_sprites.empty()



			if dict_PAUSE_GAME["g"] == False and GAME_OVER == False:
				if TWO_PLAYERS == False:
					if keystate[pygame.K_LEFT]: 
						# MUSIC_move_player.play()

						self.border_animation = 3
						self.index = 2
						self.index_border_animation = 2
						now_speed_x = -self.speed

					elif keystate[pygame.K_RIGHT]:
						# MUSIC_move_player.play()

						self.border_animation = 7
						self.index = 6
						self.index_border_animation = 6
						now_speed_x = self.speed

					elif keystate[pygame.K_UP]:
						# MUSIC_move_player.play()

						self.border_animation = 1
						self.index = 0
						self.index_border_animation = 0
						now_speed_y = -self.speed


					elif keystate[pygame.K_DOWN]:
						# MUSIC_move_player.play()

						self.border_animation = 5
						self.index = 4
						self.index_border_animation = 4
						now_speed_y = self.speed

					if keystate[pygame.K_LEFT]==False and keystate[pygame.K_RIGHT]==False and keystate[pygame.K_UP]==False and keystate[pygame.K_DOWN]==False:
						# MUSIC_move_player.stop()				
						CHANNEL_player_move.stop()
						self.border_animation, self.index, self.index_border_animation = 0, self.index, self.index_border_animation
					else:
						CHANNEL_player_move.set_volume(set_volume)
						CHANNEL_player_move.play(MUSIC_move_player, loops=-1)


					if keystate[pygame.K_SPACE]: # K_LALT
						self.shot()

					if keystate[pygame.K_r]:
						self.shot_rocket()


					# ДОДЕЛАЙ РЕЖИМ С ДВУМЯ ИГРОКАМИ!!!!
				elif TWO_PLAYERS == True:
					if self.player2 == True:
						# танк игрока зеленый
						if keystate[pygame.K_KP4]:  # left
							# MUSIC_move_player.play()

							self.border_animation = 3
							self.index = 2
							self.index_border_animation = 2
							now_speed_x = -self.speed

						elif keystate[pygame.K_KP6]: # right
							# MUSIC_move_player.play()

							self.border_animation = 7
							self.index = 6
							self.index_border_animation = 6
							now_speed_x = self.speed

						elif keystate[pygame.K_KP8]: # up
							# MUSIC_move_player.play()

							self.border_animation = 1
							self.index = 0
							self.index_border_animation = 0
							now_speed_y = -self.speed


						elif keystate[pygame.K_KP5]: # down
							# MUSIC_move_player.play()

							self.border_animation = 5
							self.index = 4
							self.index_border_animation = 4
							now_speed_y = self.speed

						if keystate[pygame.K_KP4]==False and keystate[pygame.K_KP6]==False and keystate[pygame.K_KP8]==False and keystate[pygame.K_KP5]==False:
							# MUSIC_move_player.stop()				
							CHANNEL_player_move.stop()
							self.border_animation, self.index, self.index_border_animation = 0, self.index, self.index_border_animation
						else:
							CHANNEL_player_move.set_volume(set_volume)
							CHANNEL_player_move.play(MUSIC_move_player, loops=-1)


						if keystate[pygame.K_KP0]: # SPACE K_LALT
							self.shot()

						if keystate[pygame.K_KP2]: # R
							self.shot_rocket()

					elif self.player2 == False:
						# танк игрока зеленый
						if keystate[pygame.K_a]:  # left
							# MUSIC_move_player.play()

							self.border_animation = 3
							self.index = 2
							self.index_border_animation = 2
							now_speed_x = -self.speed

						elif keystate[pygame.K_d]: # right
							# MUSIC_move_player.play()

							self.border_animation = 7
							self.index = 6
							self.index_border_animation = 6
							now_speed_x = self.speed

						elif keystate[pygame.K_w]: # up
							# MUSIC_move_player.play()

							self.border_animation = 1
							self.index = 0
							self.index_border_animation = 0
							now_speed_y = -self.speed


						elif keystate[pygame.K_s]: # down
							# MUSIC_move_player.play()

							self.border_animation = 5
							self.index = 4
							self.index_border_animation = 4
							now_speed_y = self.speed

						if keystate[pygame.K_a]==False and keystate[pygame.K_w]==False and keystate[pygame.K_s]==False and keystate[pygame.K_d]==False:
							# MUSIC_move_player.stop()				
							CHANNEL_player_move.stop()
							self.border_animation, self.index, self.index_border_animation = 0, self.index, self.index_border_animation
						else:
							CHANNEL_player_move.set_volume(set_volume)
							CHANNEL_player_move.play(MUSIC_move_player, loops=-1)


						if keystate[pygame.K_LALT]: # SPACE K_LALT
							self.shot()

						if keystate[pygame.K_x]: # R
							self.shot_rocket()

							#################################





			else:
				CHANNEL_player_move.stop()
				self.border_animation, self.index, self.index_border_animation = 0, self.index, self.index_border_animation

			
			if self.counter >= 3:
				self.index += 1
				self.counter = 0
				if self.index > self.border_animation:
					self.index = self.index_border_animation


			rectx = self.rect.x
			recty = self.rect.y

			# rectcenter = self.rect.center
			self.rect = self.image.get_rect()
			# self.rect.center = rectcenter

			self.rect.x = rectx
			self.rect.y = recty


			hits_ice = pygame.sprite.spritecollide(self, ice_sprites, False)
			if hits_ice:
				SLIP_TIMER["now"] = 1
			else:
				SLIP_TIMER["now"] = 0
				


			# collide = pygame.sprite.spritecollide(player, enemys_sprites, False)
			# if not collide:
			self.image = self.images[self.index]			

			# elif collide:
				# now_speed_x = 0
				# now_speed_y = 0
	

				# self.rect.x = self.rect.x
				# self.rect.y = self.rect.y

			self.rect.x += now_speed_x
			self.rect.y += now_speed_y
			# print(SLIP_TIMER["now"])
			# print(SLIP_TIMER["all"])



			if self.lvl_tank == '1':
				if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:
					self.rect.right = WIDTH_POLE+SPAWN_POLE[0]
			elif self.lvl_tank == '2':
				if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:
					self.rect.right = WIDTH_POLE+SPAWN_POLE[0]
			elif self.lvl_tank == '3':
				if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:
					self.rect.right = WIDTH_POLE+SPAWN_POLE[0]
			elif self.lvl_tank == '4':
				if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:
					self.rect.right = WIDTH_POLE+SPAWN_POLE[0]


			if self.rect.left < SPAWN_POLE[0]:
				self.rect.left = SPAWN_POLE[0]

			if self.rect.top < SPAWN_POLE[1]:
				self.rect.top = SPAWN_POLE[1]

			if self.lvl_tank == '1':
				if self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:
					self.rect.bottom = HEIGHT_POLE+SPAWN_POLE[1]
			elif self.lvl_tank == '2':
				if self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:
					self.rect.bottom = HEIGHT_POLE+SPAWN_POLE[1]
			elif self.lvl_tank == '3':
				if self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:
					self.rect.bottom = HEIGHT_POLE+SPAWN_POLE[1]
			elif self.lvl_tank == '4':
				if self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:
					self.rect.bottom = HEIGHT_POLE+SPAWN_POLE[1]


			hits_wall = pygame.sprite.spritecollide(self, walls_sprites, False)
			if hits_wall:
				self.rect.x -= now_speed_x
				self.rect.y -= now_speed_y

			hits_wall = pygame.sprite.spritecollide(self, water_sprites, False)
			if hits_wall:
				self.rect.x -= now_speed_x
				self.rect.y -= now_speed_y

			hits_wall = pygame.sprite.spritecollide(self, beton_sprites, False)
			if hits_wall:
				self.rect.x -= now_speed_x
				self.rect.y -= now_speed_y

			hits_base = pygame.sprite.spritecollide(self, base_sprites, False)
			if hits_base:
				self.rect.x -= now_speed_x
				self.rect.y -= now_speed_y




			











			


		elif self.type_player == 'enemy':
			"""Здесь будет код автоматического движения врагов"""

			self.counter += 1
			self.counter_ai += 1

			if len(enemys_sprites.sprites()) != 0:
				CHANNEL_enemy_move.play(MUSIC_move_enemy, loops=-1)
				CHANNEL_enemy_move.set_volume(set_volume)
			elif len(enemys_sprites.sprites()) == 0:
				CHANNEL_enemy_move.stop()
			

			if dict_PAUSE_GAME["g"] == False and PLAYER1_NOW_BONUS["stoptime"] == False:

				if self.ENEMY_now_speed_x == 0 or self.ENEMY_now_speed_y == 0:	
					self.border_animation, self.index, self.index_border_animation = 0, self.index, self.index_border_animation
				
				

				#### START BOT SCRIPT####


				# now_enemy_event = self.random_anchor

				if self.random_anchor == 'up':
					self.border_animation = 1
					self.index = 0
					self.index_border_animation = 0
					self.ENEMY_now_speed_y = -self.speed
					self.ENEMY_now_speed_x = 0


				elif self.random_anchor == 'down':
					self.border_animation = 5
					self.index = 4
					self.index_border_animation = 4
					self.ENEMY_now_speed_y = self.speed
					self.ENEMY_now_speed_x = 0


				elif self.random_anchor == 'right':
					self.border_animation = 7
					self.index = 6
					self.index_border_animation = 6
					self.ENEMY_now_speed_x = self.speed
					self.ENEMY_now_speed_y = 0

				elif self.random_anchor == 'left':
					self.border_animation = 3
					self.index = 2
					self.index_border_animation = 2
					self.ENEMY_now_speed_x = -self.speed
					self.ENEMY_now_speed_y = 0

				elif self.random_anchor == 'do_shoting':
					shot_doing = True
				else:
					shot_doing = False


				lst_sprites = player_sprites.sprites()

				for i in range(len(lst_sprites)):
					if pygame.sprite.collide_rect(self, lst_sprites[i]) == True:
						delete_sprite = lst_sprites[i]


				self.rect.x += self.ENEMY_now_speed_x
				self.rect.y += self.ENEMY_now_speed_y
				
			else:
				CHANNEL_enemy_move.stop()
				self.border_animation, self.index, self.index_border_animation = 0, self.index, self.index_border_animation



			#### END BOT SCRIPT ####

			if self.shim_tank == False:
				if self.counter >= 3:
					self.index += 1
					self.counter = 0
					if self.index > self.border_animation:
						self.index = self.index_border_animation

			elif self.shim_tank == True and dict_PAUSE_GAME["g"]==False and self.lvl_start != 4 and PLAYER1_NOW_BONUS["stoptime"] == False:
				self.counter_shim += 1
				if self.counter >= 3:
					self.index += 1
					self.counter = 0

				if self.counter_shim >= 8:
					self.index += 8
				if self.counter_shim >= 16:
					self.counter_shim = 0
			elif dict_PAUSE_GAME["g"]==False and self.lvl_start != 4 and PLAYER1_NOW_BONUS["stoptime"] == False:
				self.border_animation, self.index, self.index_border_animation = 0, self.index, self.index_border_animation

			


			if self.lvl_start == 4 and dict_PAUSE_GAME["g"]==False and PLAYER1_NOW_BONUS["stoptime"] == False:
				if self.hp == HP_ENEMY_LVL4 and self.shim_tank == True:
					self.counter_shim += 1
					if self.counter >= 3:
						self.index += 1
						self.counter = 0

					if self.counter_shim >= 8:
						self.index += 8*3
					if self.counter_shim >= 16:
						self.counter_shim = 0

				if self.hp == HP_ENEMY_LVL4 - 100: # 200
					self.counter_shim += 1
					if self.counter >= 3:
						self.index += 1
						self.counter = 0

					if self.counter_shim >= 8:
						self.index += 8
					if self.counter_shim >= 16:
						self.counter_shim = 0

				if self.hp == HP_ENEMY_LVL4 - 200: # 100
					self.counter_shim += 1
					if self.counter >= 3:
						self.index += 1
						self.counter = 0

					if self.counter_shim >= 8:
						self.index += 8*2
					if self.counter_shim >= 16:
						self.counter_shim = 0
			else:
				self.border_animation, self.index, self.index_border_animation = 0, self.index, self.index_border_animation





			if PLAYER1_NOW_BONUS["stoptime"] == False:
				if (self.rect.center[0] == player.rect.center[0] or self.rect.x == player.rect.x) or (self.rect.center[1] == player.rect.center[1] or self.rect.y == player.rect.y):
					self.shot()

				fault_for_shot = 4
				if (self.rect.center[0]+fault_for_shot == player.rect.center[0]+fault_for_shot or self.rect.x+fault_for_shot == player.rect.x+fault_for_shot) or (self.rect.center[1]+fault_for_shot == player.rect.center[1]+fault_for_shot or self.rect.y+fault_for_shot == player.rect.y+fault_for_shot):
					self.shot()

				if (self.rect.center[0]-fault_for_shot == player.rect.center[0]-fault_for_shot or self.rect.x-fault_for_shot == player.rect.x-fault_for_shot) or (self.rect.center[1]-fault_for_shot == player.rect.center[1]-fault_for_shot or self.rect.y-fault_for_shot == player.rect.y-fault_for_shot):
					self.shot()

				if (self.rect.y == SPAWN_BASE[1]+24+2) or (self.rect.y == SPAWN_BASE[1]+24-2) or (self.rect.x == SPAWN_BASE[0]+24+2) or (self.rect.x == SPAWN_BASE[0]+24-2):
					self.shot()
					self.shot()
			




			if self.lvl_tank == '1':
				if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:

					self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
					if self.now_enemy_event != self.random_anchor:
						self.random_anchor = self.now_enemy_event

					self.rect.right = WIDTH_POLE+SPAWN_POLE[0]
			elif self.lvl_tank == '2':
				if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:
					
					self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
					if self.now_enemy_event != self.random_anchor:
						self.random_anchor = self.now_enemy_event

					self.rect.right = WIDTH_POLE+SPAWN_POLE[0]
			elif self.lvl_tank == '3':
				if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:
					
					self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
					if self.now_enemy_event != self.random_anchor:
						self.random_anchor = self.now_enemy_event

					self.rect.right = WIDTH_POLE+SPAWN_POLE[0]
			elif self.lvl_tank == '4':
				if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:
					
					self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
					if self.now_enemy_event != self.random_anchor:
						self.random_anchor = self.now_enemy_event

					self.rect.right = WIDTH_POLE+SPAWN_POLE[0]

			if self.rect.left < SPAWN_POLE[0]:
				
				self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
				if self.now_enemy_event != self.random_anchor:
					self.random_anchor = self.now_enemy_event

				self.rect.left = SPAWN_POLE[0]

			if self.rect.top < SPAWN_POLE[1]:
			
				self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
				if self.now_enemy_event != self.random_anchor:
					self.random_anchor = self.now_enemy_event

				self.rect.top = SPAWN_POLE[1]

			if self.lvl_tank == '1':
				if self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:
					
					self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
					if self.now_enemy_event != self.random_anchor:
						self.random_anchor = self.now_enemy_event

					self.rect.bottom = HEIGHT_POLE+SPAWN_POLE[1]
			elif self.lvl_tank == '2':
				if self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:
					
					self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
					if self.now_enemy_event != self.random_anchor:
						self.random_anchor = self.now_enemy_event
				
					self.rect.bottom = HEIGHT_POLE+SPAWN_POLE[1]
			elif self.lvl_tank == '3':
				if self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:
					
					self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
					if self.now_enemy_event != self.random_anchor:
						self.random_anchor = self.now_enemy_event

					self.rect.bottom = HEIGHT_POLE+SPAWN_POLE[1]
			elif self.lvl_tank == '4':
				if self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:
					
					self.now_enemy_event = random.choice(LIST_RANDOM_EVENT_ENEMY)
					if self.now_enemy_event != self.random_anchor:
						self.random_anchor = self.now_enemy_event

					self.rect.bottom = HEIGHT_POLE+SPAWN_POLE[1]




			hits_water = pygame.sprite.spritecollide(self, water_sprites, False)
			if hits_water:
				self.rect.x -= self.ENEMY_now_speed_x
				self.rect.y -= self.ENEMY_now_speed_y

				random_list_event_wall = ['right', 'left', 'up', 'down', 'shot']
				now_event = random.choice(random_list_event_wall)

				if now_event == 'shot':
					self.shot()
				else:
					self.random_anchor = now_event









			if PLAYER1_NOW_BONUS["stoptime"] == False and dict_PAUSE_GAME["g"] == False:				
				if self.counter_ai > self.random_timer_for_counter_ai:
					self.rect.x -= self.ENEMY_now_speed_x
					self.rect.y -= self.ENEMY_now_speed_y

					random_list_event_wall = ['right', 'left', 'up', 'down',] # 'shot']
					now_event = random.choice(random_list_event_wall)

					if now_event == 'shot':
						self.shot()
					else:
						self.random_anchor = now_event

					self.counter_ai = 0
					self.random_timer_for_counter_ai = random.randint(0, TIMER_AI_MAKE_ONE)



			# hits_enemys = pygame.sprite.spritecollideany(self, enemys_sprites, False)
			# if hits_enemys:
			# 	# self.rect.x -= self.ENEMY_now_speed_x
			# 	# self.rect.y -= self.ENEMY_now_speed_y

			# 	random_list_event_wall = ['right', 'left', 'up', 'down', 'shot']
			# 	now_event = random.choice(random_list_event_wall)

			# 	if now_event == 'shot':
			# 		self.shot()
			# 	else:
			# 		self.random_anchor = now_event


			hits_beton = pygame.sprite.spritecollide(self, beton_sprites, False)
			if hits_beton:
				self.rect.x -= self.ENEMY_now_speed_x
				self.rect.y -= self.ENEMY_now_speed_y
				random_list_speed = [0, self.speed]
				random_speed_x = random.choice(random_list_speed)
				random_speed_y = random.choice(random_list_speed)
				if random_speed_x == self.speed and random_speed_y == 0:
					self.random_anchor = 'right'
				elif random_speed_x == 0 and random_speed_y == self.speed:
					self.random_anchor = 'left'

			hits_wall = pygame.sprite.spritecollide(self, walls_sprites, False)
			if hits_wall:
				self.rect.x -= self.ENEMY_now_speed_x
				self.rect.y -= self.ENEMY_now_speed_y

				random_list_event_wall = ['right', 'left', 'up', 'down', 'shot', ]

				for i in range(Difficulty_of_enemies):
					random_list_event_wall.append('shot')

				now_event = random.choice(random_list_event_wall)

				if now_event == 'shot':
					self.shot()
				else:
					self.random_anchor = now_event
					


			hits_base = pygame.sprite.spritecollide(self, base_sprites, False)
			if hits_base:
				self.rect.x -= self.ENEMY_now_speed_x
				self.rect.y -= self.ENEMY_now_speed_y

				random_list_event_wall = ['right', 'left', 'up', 'down', 'shot']
				now_event = random.choice(random_list_event_wall)

				if now_event == 'shot':
					self.shot()
				else:
					self.random_anchor = now_event



			hits_player = pygame.sprite.spritecollide(self, player_sprites, False)
			if hits_player and PLAYER1_NOW_BONUS["stoptime"]==False:
				self.shot()
				



			# self.rect = self.image.get_rect()
			self.image = self.images[self.index]

			# print(self.random_anchor)



class SpawnEnemyAnimation(pygame.sprite.Sprite):
	def __init__(self, pos, enemy_tank, timer=2):
		pygame.sprite.Sprite.__init__(self)

		self.pos = pos
		self.timer = timer

		self.enemy_tank = enemy_tank

		self.images = []

		try:
			self.images.append(image.load(f'{LOAD_TEXTURES}/tanks/enemy/spawn_a1.png'))
		except Exception:
			self.images.append(image.load(f'{DEFAULT_TEXTURES}/tanks/enemy/spawn_a1.png'))

		try:
			self.images.append(image.load(f'{LOAD_TEXTURES}/tanks/enemy/spawn_a2.png'))
		except Exception:
			self.images.append(image.load(f'{DEFAULT_TEXTURES}/tanks/enemy/spawn_a2.png'))

		try:
			self.images.append(image.load(f'{LOAD_TEXTURES}/tanks/enemy/spawn_a3.png'))
		except Exception:
			self.images.append(image.load(f'{DEFAULT_TEXTURES}/tanks/enemy/spawn_a3.png'))

		try:
			self.images.append(image.load(f'{LOAD_TEXTURES}/tanks/enemy/spawn_a4.png'))
		except Exception:
			self.images.append(image.load(f'{DEFAULT_TEXTURES}/tanks/enemy/spawn_a4.png'))


		self.index = 0

		self.image = self.images[self.index]

		self.rect = self.image.get_rect()
		self.rect.center = self.pos

		self.type_player = self.enemy_tank.type_player

		# self.pos_player = (self.enemy_tank.rect.x, self.enemy_tank.rect.y)
		self.pos_player = (self.enemy_tank.rect.center)


		self.counter = 0

		self.k = 0


	def update(self):
		self.counter += 1

		if self.counter > 4:
			self.index += 1
			self.counter = 0

			if self.index > 3:
				self.index = 0
				self.k += 1

			if self.k >= self.timer:
				self.kill()
				
				if self.type_player == 'enemy':
					enemys_sprites.add(self.enemy_tank)

				elif self.type_player == 'player':
					player_sprites.add(self.enemy_tank)
					if len(player_bonuses_sprites.sprites()) == 0:
						player_bonuses_sprites.add(BONUS_immortality(pos=(self.enemy_tank.rect.center[0]-24, self.enemy_tank.rect.center[1]-24), tank_sprite=self.enemy_tank))

		self.image = self.images[self.index]









class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, tank_sprite, killed_tank=False, killed_eagle=False):
		pygame.sprite.Sprite.__init__(self)

		self.tank_sprite = tank_sprite
		if killed_eagle == False:
			self.tank_level = self.tank_sprite.lvl_tank
			


		self.x = x
		self.y = y


		self.explosions_images = []
		# for i in range(1, 6):
		try:
			self.explosions_images.append(image.load(f'{LOAD_TEXTURES}/map_objects/explosions/explosion_a1.png'))
		except Exception:
			self.explosions_images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/explosions/explosion_a1.png'))

		try:
			self.explosions_images.append(image.load(f'{LOAD_TEXTURES}/map_objects/explosions/explosion_a2.png'))
		except Exception:
			self.explosions_images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/explosions/explosion_a2.png'))

		try:
			self.explosions_images.append(image.load(f'{LOAD_TEXTURES}/map_objects/explosions/explosion_a3.png'))
		except Exception:
			self.explosions_images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/explosions/explosion_a3.png'))

		try:
			self.explosions_images.append(image.load(f'{LOAD_TEXTURES}/map_objects/explosions/explosion_a4.png'))
		except Exception:
			self.explosions_images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/explosions/explosion_a4.png'))

		try:
			self.explosions_images.append(image.load(f'{LOAD_TEXTURES}/map_objects/explosions/explosion_a5.png'))
		except Exception:
			self.explosions_images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/explosions/explosion_a5.png'))

		try:
			self.explosions_images.append(image.load(f'{LOAD_TEXTURES}/map_objects/explosions/explosion_a6.png'))
		except Exception:
			self.explosions_images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/explosions/explosion_a6.png'))

		try:
			self.explosions_images.append(image.load(f'{LOAD_TEXTURES}/map_objects/explosions/explosion_a7.png'))
		except Exception:
			self.explosions_images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/explosions/explosion_a7.png'))

		try:
			self.explosions_images.append(image.load(f'{LOAD_TEXTURES}/map_objects/explosions/explosion_a8.png'))
		except Exception:
			self.explosions_images.append(image.load(f'{DEFAULT_TEXTURES}/map_objects/explosions/explosion_a8.png'))




		
		self.explosion_index = 0
		self.image = self.explosions_images[self.explosion_index]

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.killed_tank = killed_tank


		# if self.killed_tank == False:

		self.killed_eagle = killed_eagle

		self.rect.center = (self.x, self.y)

		self.counter = 0

	def update(self):
		if self.killed_tank == False:			
			self.counter += 1
			if self.counter >= 3:
				self.counter = 0
				self.explosion_index += 1

				if self.explosion_index >= 3:
					self.kill()

			self.image = self.explosions_images[self.explosion_index]

		elif self.killed_tank == True:

			self.counter += 1
			if self.counter >= 3:
				self.counter = 0
				self.explosion_index += 1

				if self.explosion_index >=3:
					if self.killed_eagle == True:
						self.rect.center = (335, 600)
					else:
						self.rect.center = (self.x-20, self.y-20)

				if self.explosion_index >= 6:
					self.rect.center = (self.x, self.y)

			try:
				self.image = self.explosions_images[self.explosion_index]				
			except Exception:
				self.kill()
				





class Bullet(pygame.sprite.Sprite):
	def __init__(self, p, tank_sprite, count_destroyed_walls, image_path='%s/tanks/bullet/bullet_r'):
		pygame.sprite.Sprite.__init__(self)

		self.bullet_type = "bullet"

		self.tank_sprite = tank_sprite
		self.p = p

		self.lvl_tank = str(p["lvl_start"])
		self.type_player = p[f"LVL{self.lvl_tank}"]["type_player"]

		self.count_destroyed_walls = count_destroyed_walls

		self.damage = p[f"LVL{self.lvl_tank}"]["damage"]
		self.bullet_speed = p[f"LVL{self.lvl_tank}"]["bullet_speed"]

		self.images = []
		self.index = tank_sprite.index
		for i in range(1, 5):
			try:
				self.images.append(image.load(image_path % (LOAD_TEXTURES)+f'{i}.png'))
			except Exception:
				self.images.append(image.load(image_path % (DEFAULT_TEXTURES)+f'{i}.png'))



		self.bullet_index_now = self.index
		self.now_bullet_speed_x = 0
		self.now_bullet_speed_y = 0
		self.tank_level = self.p["lvl_start"]	

		self.tank_hp = p[f"LVL{self.lvl_tank}"]["hp"]




		if self.index == 0 or self.index == 1 or self.index == 0+8 or self.index == 1+8  or self.index == 0+8*2 or self.index == 1+8*2 or self.index == 0+8*3 or self.index == 1+8*3: # ВВЕРХ
			self.now_bullet_speed_y = -self.bullet_speed
			self.image = self.images[0]
			self.index = 0
		elif self.index == 2 or self.index == 3 or self.index == 2+8 or self.index == 3+8 or self.index == 2+8*2 or self.index == 3+8*2 or self.index == 2+8*3 or self.index == 3+8*3: # ВЛЕВО
			self.now_bullet_speed_x = -self.bullet_speed
			self.image = self.images[1]
			self.index = 1
		elif self.index == 4 or self.index == 5 or self.index == 4+8 or self.index == 5+8 or self.index == 4+8*2 or self.index == 5+8*2 or self.index == 4+8*3 or self.index == 5+8*3: # ВНИЗ
			self.now_bullet_speed_y = self.bullet_speed
			self.image = self.images[2]
			self.index = 2
		elif self.index == 6 or self.index == 7 or self.index == 6+8 or self.index == 7+8 or self.index == 6+8*2 or self.index == 7+8*2 or self.index == 6+8*3 or self.index == 7+8*3: # ВПРАВО
			self.now_bullet_speed_x = self.bullet_speed
			self.image = self.images[3]
			self.index = 3


		
		# self.image = self.images[0]
		self.count = 0
		self.counter_count_kill = 0

		self.rect = self.image.get_rect()

		self.rect.center =  tank_sprite.rect.center

		self.counter_bonuses_lvl4 = 0


	def update(self):

		if dict_PAUSE_GAME["g"] == False:
			self.rect.x += self.now_bullet_speed_x
			self.rect.y += self.now_bullet_speed_y
		else:
			self.rect.x = self.rect.x
			self.rect.y = self.rect.y



		if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:

			explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
			all_sprites.add(explosion)
			explosions.add(explosion)
			if self.tank_sprite.type_player == 'player':
				MUSIC_bullet_collide.play()
			self.kill()

		elif self.rect.left < SPAWN_POLE[0]:

			explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
			all_sprites.add(explosion)
			explosions.add(explosion)
			if self.tank_sprite.type_player == 'player':
				MUSIC_bullet_collide.play()
			
			self.kill()

		elif self.rect.top < SPAWN_POLE[1]:

			explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
			all_sprites.add(explosion)
			explosions.add(explosion)

			if self.tank_sprite.type_player == 'player':
				MUSIC_bullet_collide.play()
			self.kill()

		elif self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:

			explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
			all_sprites.add(explosion)
			explosions.add(explosion)

			if self.tank_sprite.type_player == 'player':
				MUSIC_bullet_collide.play()
			self.kill()

		else:
			self.image = self.images[self.index]


		# показывать ли большой взрыв после убийства танка
		end_big_animation_kill = True

		# Счетчик бонусов для танков 4 лвл

		
		



		if self.tank_sprite.type_player == 'player':
			# когда стреляет игрок
			check_hp = False
			delete_sprite = None

			lst_sprites = enemys_sprites.sprites()

			for i in range(len(lst_sprites)):
				if pygame.sprite.collide_rect(self, lst_sprites[i]) == True:
					delete_sprite = lst_sprites[i]

			hits = pygame.sprite.spritecollide(self, enemys_sprites, check_hp)
			if hits:
				self.kill()
				if delete_sprite.hp <= self.damage:
					check_hp = True

					# расчитываем кооржинаты появления взрыва
					exp_x = self.rect.x
					exp_y = self.rect.y
					if self.index == 0 or self.index == 1: # ВВЕРХ
						exp_y -= 20
						exp_x = self.rect.x

					# MUSIC_kill_enemy.play()
					CHANNEL_kill_enemy.set_volume(set_volume)
					CHANNEL_kill_enemy.play(MUSIC_kill_enemy)
					explosion = Explosion(delete_sprite.rect.center[0], delete_sprite.rect.center[1], self.tank_sprite, end_big_animation_kill)
					all_sprites.add(explosion)

					count_kill = CountKillEnemy(tank_level=delete_sprite.lvl_tank, pos=(delete_sprite.rect.center[0]-19, delete_sprite.rect.center[1]-10))
					count_kill_enemy_sprites.add(count_kill)
					ROUND_COUNTS[str(delete_sprite.lvl_tank)] += int(COUNTER_RULES[str(delete_sprite.lvl_tank)])


					# print(delete_sprite.lvl_tank)

					if delete_sprite.shim_tank == True and delete_sprite.lvl_tank != 4 and self.counter_bonuses_lvl4 == 0:
						self.counter_bonuses_lvl4 = 5

					if delete_sprite.shim_tank == True and delete_sprite.lvl_tank != 4 and self.counter_bonuses_lvl4 == 5: #and len(bonuses_sprites.sprites()) == 0:
						# MUSIC_get_bonus.play()
						bonuses_sprites.empty()

						CHANNEL_get_bonus.play(MUSIC_get_bonus)
						random_bonus_now = random.choice(LIST_FOR_RANDOM_BONUS)
						if random_bonus_now == "immortality":
							bonuses_sprites.add(SPRITE_BONUS(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player, name_image='helmet_bonus.png', bonus_on=BONUS_immortality(pos=(self.tank_sprite.rect.x, self.tank_sprite.rect.y), tank_sprite=self.tank_sprite, now_use="timer_bonus")))
						
						elif random_bonus_now == "star":
							# bonuses_sprites.add(SPRITE_BONUS(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player, name_image='star_bonus.png', bonus_on=lambda: BONUS_star(player)))
							bonuses_sprites.add(SPRITE_BONUS_star(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))

						elif random_bonus_now == "grenade":
							bonuses_sprites.add(SPRITE_BONUS_grenade(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))

						elif random_bonus_now == "stoptime":
							bonuses_sprites.add(SPRITE_BONUS_stoptime(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))

						elif random_bonus_now == "tank":
							bonuses_sprites.add(SPRITE_BONUS_tank(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))

						elif random_bonus_now == "shovel":
							bonuses_sprites.add(SPRITE_BONUS_shovel(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))



					enemys_sprites.remove(delete_sprite)
					delete_sprite.kill()


				elif delete_sprite.hp > self.damage:
					check_hp = False
					# MUSIC_bullet_collide_tank.play()
					CHANNEL_bullet_collide_tank.play(MUSIC_bullet_collide_tank)

					 
					# if delete_sprite.shim_tank == True:
					# 	MUSIC_get_bonus.play()
					# 	bonuses_sprites.add(SPRITE_BONUS(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player, name_image='helmet_bonus.png', bonus_on=BONUS_immortality(pos=(self.tank_sprite.rect.x, self.tank_sprite.rect.y), tank_sprite=self.tank_sprite, now_use="timer_bonus")))
					if delete_sprite.shim_tank == True and delete_sprite.hp == HP_ENEMY_LVL4 and self.counter_bonuses_lvl4 == 0:
						# MUSIC_get_bonus.play()
						CHANNEL_get_bonus.play(MUSIC_get_bonus)
						bonuses_sprites.empty()
						

						random_bonus_now = random.choice(LIST_FOR_RANDOM_BONUS)
						if random_bonus_now == "immortality":
							bonuses_sprites.add(SPRITE_BONUS(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player, name_image='helmet_bonus.png', bonus_on=BONUS_immortality(pos=(self.tank_sprite.rect.x, self.tank_sprite.rect.y), tank_sprite=self.tank_sprite, now_use="timer_bonus")))
						elif random_bonus_now == "star":
							bonuses_sprites.add(SPRITE_BONUS_star(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))
						elif random_bonus_now == "grenade":
							bonuses_sprites.add(SPRITE_BONUS_grenade(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))
						elif random_bonus_now == "stoptime":
							bonuses_sprites.add(SPRITE_BONUS_stoptime(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))
						elif random_bonus_now == "tank":
							bonuses_sprites.add(SPRITE_BONUS_tank(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))
						elif random_bonus_now == "shovel":
							bonuses_sprites.add(SPRITE_BONUS_shovel(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))


						self.counter_bonuses_lvl4 += 1
					delete_sprite.hp -= self.damage


			

			


		elif self.tank_sprite.type_player == 'enemy':
			# когда стреляет враг
			# hits = pygame.sprite.collide_rect(self, player)
			hits = pygame.sprite.spritecollide(self, player_sprites, False)
			if hits:
				self.kill()

				if PLAYER1_NOW_BONUS["immortality"]==False and CHEAT_MODE == False:
					if player.hp <= self.damage:
						# расчитываем кооржинаты появления взрыва
						exp_x = self.rect.x
						exp_y = self.rect.y
						if self.index == 0 or self.index == 1: # ВВЕРХ
							exp_y -= 20
							exp_x = self.rect.x

						# MUSIC_kill_enemy.play()
						MUSIC_move_player.stop()

						MUSIC_kill_player.play()
						explosion = Explosion(exp_x, exp_y, self.tank_sprite, end_big_animation_kill)
						all_sprites.add(explosion)

						player.kill()
						player_sprites.remove(player)
						player_sprites.empty()
						player.hp = 0
						player.lvl_tank = 1



					elif player.hp > self.damage:
						CHANNEL_bullet_collide_tank.play(MUSIC_bullet_collide_tank)
						player.hp -= self.damage

				elif CHEAT_MODE == True:
					CHANNEL_bullet_collide_tank.play(MUSIC_bullet_collide_tank)



		# if PLAYER[f"lvl_start"] in LEVEL_TANKS_MAY_KILL_BETON_PLAYER:
		if int(self.lvl_tank) in LEVEL_TANKS_MAY_KILL_BETON_PLAYER and self.type_player=='player':
			kill_beton_status = True
		else:
			kill_beton_status = False

		


		lst_sprites = walls_sprites.sprites()
		
		for i in range(len(lst_sprites)):
			if pygame.sprite.collide_rect(self, lst_sprites[i]) == True:
				delete_sprite = lst_sprites[i]

		# not PLAYER1_NOW_BONUS["shovel"]

		if int(self.lvl_tank) in LEVEL_TANKS_MAY_KILL_BETON_PLAYER and self.type_player=='player':		
			destroy_beton_bricks = True
		else:
			destroy_beton_bricks = False




		hits_base_beton = pygame.sprite.spritecollide(self, beton_shovel_sprites, destroy_beton_bricks)
		if hits_base_beton:
			# if self.tank_sprite.lvl_tank not in LEVEL_TANKS_MAY_KILL_BETON_PLAYER:
			destroy_wall_bricks = False
			if self.tank_sprite.type_player == "player":
				CHANNEL_bullet_collide_wall.play(MUSIC_bullet_collide_beton)				
		else:
			destroy_wall_bricks = True
		






		hits_wall = pygame.sprite.spritecollide(self, walls_sprites, destroy_wall_bricks)	

		if hits_wall:
			if self.tank_sprite.type_player == "player":
				CHANNEL_bullet_collide_wall.play(MUSIC_bullet_collide_wall)
			if kill_beton_status == False:
				self.kill()
				AddExplosion(pos=(self.rect.center[0], self.rect.center[1]), sprite=self, big=False)

			elif kill_beton_status == True:
				self.count_destroyed_walls += 1

		

		if self.count_destroyed_walls >= HIGH_LEVEL_TANK_MAY_DESTROY_WALLBRICKS:
			self.kill()
			AddExplosion(pos=(self.rect.center[0], self.rect.center[1]), sprite=self, big=False)





		lst_sprites_beton = beton_sprites.sprites()
		
		for i in range(len(lst_sprites_beton)):
			if pygame.sprite.collide_rect(self, lst_sprites_beton[i]) == True:
				delete_sprite = lst_sprites_beton[i]



		hits_wall_betons = pygame.sprite.spritecollide(self, beton_sprites, kill_beton_status)
		

		if hits_wall_betons:
			if self.tank_sprite.type_player == "player":
				CHANNEL_bullet_collide_wall.play(MUSIC_bullet_collide_beton)
			AddExplosion(pos=(self.rect.center[0], self.rect.center[1]), sprite=self, big=False)
			self.kill()
				







class Rocket(pygame.sprite.Sprite):
	def __init__(self, p, tank_sprite, count_destroyed_walls, image_path='%s/tanks/bullet/rocket_r'):
		pygame.sprite.Sprite.__init__(self)

		self.bullet_type = "rocket"

		self.tank_sprite = tank_sprite
		self.p = p

		self.lvl_tank = str(p["lvl_start"])
		self.type_player = p[f"LVL{self.lvl_tank}"]["type_player"]

		self.count_destroyed_walls = count_destroyed_walls

		self.damage = p[f"LVL{self.lvl_tank}"]["damage"]
		# self.bullet_speed = p[f"LVL{self.lvl_tank}"]["bullet_speed"]
		self.bullet_speed = int(p[f"LVL{self.lvl_tank}"]["bullet_speed"])+int(ROCKET_BUST_SPEED)


		self.images = []
		self.index = tank_sprite.index
		for i in range(1, 5):
			try:
				self.images.append(image.load(image_path % (LOAD_TEXTURES)+f'{i}.png'))
			except Exception:
				self.images.append(image.load(image_path % (DEFAULT_TEXTURES)+f'{i}.png'))



		self.bullet_index_now = self.index
		self.now_bullet_speed_x = 0
		self.now_bullet_speed_y = 0
		self.tank_level = self.p["lvl_start"]	

		self.tank_hp = p[f"LVL{self.lvl_tank}"]["hp"]




		if self.index == 0 or self.index == 1 or self.index == 0+8 or self.index == 1+8  or self.index == 0+8*2 or self.index == 1+8*2 or self.index == 0+8*3 or self.index == 1+8*3: # ВВЕРХ
			self.now_bullet_speed_y = -self.bullet_speed
			self.image = self.images[0]
			self.index = 0
		elif self.index == 2 or self.index == 3 or self.index == 2+8 or self.index == 3+8 or self.index == 2+8*2 or self.index == 3+8*2 or self.index == 2+8*3 or self.index == 3+8*3: # ВЛЕВО
			self.now_bullet_speed_x = -self.bullet_speed
			self.image = self.images[1]
			self.index = 1
		elif self.index == 4 or self.index == 5 or self.index == 4+8 or self.index == 5+8 or self.index == 4+8*2 or self.index == 5+8*2 or self.index == 4+8*3 or self.index == 5+8*3: # ВНИЗ
			self.now_bullet_speed_y = self.bullet_speed
			self.image = self.images[2]
			self.index = 2
		elif self.index == 6 or self.index == 7 or self.index == 6+8 or self.index == 7+8 or self.index == 6+8*2 or self.index == 7+8*2 or self.index == 6+8*3 or self.index == 7+8*3: # ВПРАВО
			self.now_bullet_speed_x = self.bullet_speed
			self.image = self.images[3]
			self.index = 3


		
		# self.image = self.images[0]
		self.count = 0
		self.counter_count_kill = 0

		self.rect = self.image.get_rect()

		self.rect.center =  tank_sprite.rect.center

		self.counter_bonuses_lvl4 = 0

		self.counter_collide = 0


	def update(self):

		if dict_PAUSE_GAME["g"] == False:
			self.rect.x += self.now_bullet_speed_x
			self.rect.y += self.now_bullet_speed_y
		else:
			self.rect.x = self.rect.x
			self.rect.y = self.rect.y


		if ROCKET_LOGIC == 1:
			if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:

				# explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				# all_sprites.add(explosion)
				# explosions.add(explosion)
				
				self.now_bullet_speed_x = 0
				self.now_bullet_speed_y = -self.bullet_speed
				self.index = 0
				self.image = self.images[self.index]

				self.counter_collide += 1
				self.rect.x -= 18
				# self.kill()

			elif self.rect.left < SPAWN_POLE[0]:

				# explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				# all_sprites.add(explosion)
				# explosions.add(explosion)
				
				self.now_bullet_speed_x = 0
				self.now_bullet_speed_y = self.bullet_speed
				self.index = 2
				self.image = self.images[self.index]

				self.counter_collide += 1
				self.rect.x += 18
				
				# self.kill()

			elif self.rect.top < SPAWN_POLE[1]:

				# explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				# all_sprites.add(explosion)
				# explosions.add(explosion)

				# self.index = 2

				self.now_bullet_speed_x = -self.bullet_speed
				self.now_bullet_speed_y = 0
				self.image = self.images[1]
				self.index = 1

				self.counter_collide += 1

				self.rect.y = self.rect.y + 18
				

				# self.kill()

			elif self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:

				explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				all_sprites.add(explosion)
				explosions.add(explosion)

				self.kill()

			else:
				self.image = self.images[self.index]

		


			destroy_rocket_list = [1, 0, 3, 4, 5]
			if self.rect.right > WIDTH_POLE+SPAWN_POLE[0] and self.counter_collide in destroy_rocket_list:
				explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				all_sprites.add(explosion)
				explosions.add(explosion)
				self.kill()

			elif self.rect.left < SPAWN_POLE[0] and self.counter_collide in destroy_rocket_list:
				explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				all_sprites.add(explosion)
				explosions.add(explosion)
				self.kill()


			elif self.rect.top < SPAWN_POLE[1] and self.counter_collide in destroy_rocket_list:
				explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				all_sprites.add(explosion)
				explosions.add(explosion)
				self.kill()

			elif self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1] and self.counter_collide in destroy_rocket_list:
				explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				all_sprites.add(explosion)
				explosions.add(explosion)
				self.kill()





		elif ROCKET_LOGIC == 2:

			if self.rect.right > WIDTH_POLE+SPAWN_POLE[0]:
				explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				all_sprites.add(explosion)
				explosions.add(explosion)
				

				self.kill()

			elif self.rect.left < SPAWN_POLE[0]:

				explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				all_sprites.add(explosion)
				explosions.add(explosion)
				

				
				self.kill()

			elif self.rect.top < SPAWN_POLE[1]:

				explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				all_sprites.add(explosion)
				explosions.add(explosion)				

				self.kill()

			elif self.rect.bottom > HEIGHT_POLE+SPAWN_POLE[1]:

				explosion = Explosion(self.rect.center[0], self.rect.center[1], self.tank_sprite)
				all_sprites.add(explosion)
				explosions.add(explosion)

				

				self.kill()

			else:
				self.image = self.images[self.index]






		# показывать ли большой взрыв после убийства танка
		end_big_animation_kill = True

		# Счетчик бонусов для танков 4 лвл

			
		



		if self.tank_sprite.type_player == 'player':
			# когда стреляет игрок
			check_hp = False
			delete_sprite = None

			lst_sprites = enemys_sprites.sprites()

			for i in range(len(lst_sprites)):
				if pygame.sprite.collide_rect(self, lst_sprites[i]) == True:
					delete_sprite = lst_sprites[i]

			hits = pygame.sprite.spritecollide(self, enemys_sprites, check_hp)
			if hits:
				self.kill()
				if delete_sprite.hp <= self.damage:
					check_hp = True

					# расчитываем кооржинаты появления взрыва
					exp_x = self.rect.x
					exp_y = self.rect.y
					if self.index == 0 or self.index == 1: # ВВЕРХ
						exp_y -= 20
						exp_x = self.rect.x

					# MUSIC_kill_enemy.play()
					CHANNEL_kill_enemy.set_volume(set_volume)
					CHANNEL_kill_enemy.play(MUSIC_kill_enemy)
					explosion = Explosion(delete_sprite.rect.center[0], delete_sprite.rect.center[1], self.tank_sprite, end_big_animation_kill)
					all_sprites.add(explosion)

					count_kill = CountKillEnemy(tank_level=delete_sprite.lvl_tank, pos=(delete_sprite.rect.center[0]-19, delete_sprite.rect.center[1]-10))
					count_kill_enemy_sprites.add(count_kill)
					ROUND_COUNTS[str(delete_sprite.lvl_tank)] += int(COUNTER_RULES[str(delete_sprite.lvl_tank)])


					# print(delete_sprite.lvl_tank)

					if delete_sprite.shim_tank == True and delete_sprite.lvl_tank != 4 and self.counter_bonuses_lvl4 == 0:
						self.counter_bonuses_lvl4 = 5

					if delete_sprite.shim_tank == True and delete_sprite.lvl_tank != 4 and self.counter_bonuses_lvl4 == 5: #and len(bonuses_sprites.sprites()) == 0:
						# MUSIC_get_bonus.play()
						bonuses_sprites.empty()

						CHANNEL_get_bonus.play(MUSIC_get_bonus)
						random_bonus_now = random.choice(LIST_FOR_RANDOM_BONUS)
						if random_bonus_now == "immortality":
							bonuses_sprites.add(SPRITE_BONUS(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player, name_image='helmet_bonus.png', bonus_on=BONUS_immortality(pos=(self.tank_sprite.rect.x, self.tank_sprite.rect.y), tank_sprite=self.tank_sprite, now_use="timer_bonus")))
						
						elif random_bonus_now == "star":
							# bonuses_sprites.add(SPRITE_BONUS(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player, name_image='star_bonus.png', bonus_on=lambda: BONUS_star(player)))
							bonuses_sprites.add(SPRITE_BONUS_star(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))

						elif random_bonus_now == "grenade":
							bonuses_sprites.add(SPRITE_BONUS_grenade(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))

						elif random_bonus_now == "stoptime":
							bonuses_sprites.add(SPRITE_BONUS_stoptime(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))

						elif random_bonus_now == "tank":
							bonuses_sprites.add(SPRITE_BONUS_tank(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))

						elif random_bonus_now == "shovel":
							bonuses_sprites.add(SPRITE_BONUS_shovel(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))



					enemys_sprites.remove(delete_sprite)
					delete_sprite.kill()


				elif delete_sprite.hp > self.damage:
					check_hp = False
					# MUSIC_bullet_collide_tank.play()
					CHANNEL_bullet_collide_tank.play(MUSIC_bullet_collide_tank)

					 
					# if delete_sprite.shim_tank == True:
					# 	MUSIC_get_bonus.play()
					# 	bonuses_sprites.add(SPRITE_BONUS(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player, name_image='helmet_bonus.png', bonus_on=BONUS_immortality(pos=(self.tank_sprite.rect.x, self.tank_sprite.rect.y), tank_sprite=self.tank_sprite, now_use="timer_bonus")))
					if delete_sprite.shim_tank == True and delete_sprite.hp == HP_ENEMY_LVL4 and self.counter_bonuses_lvl4 == 0:
						# MUSIC_get_bonus.play()
						CHANNEL_get_bonus.play(MUSIC_get_bonus)
						bonuses_sprites.empty()
						

						random_bonus_now = random.choice(LIST_FOR_RANDOM_BONUS)
						if random_bonus_now == "immortality":
							bonuses_sprites.add(SPRITE_BONUS(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player, name_image='helmet_bonus.png', bonus_on=BONUS_immortality(pos=(self.tank_sprite.rect.x, self.tank_sprite.rect.y), tank_sprite=self.tank_sprite, now_use="timer_bonus")))
						elif random_bonus_now == "star":
							bonuses_sprites.add(SPRITE_BONUS_star(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))
						elif random_bonus_now == "grenade":
							bonuses_sprites.add(SPRITE_BONUS_grenade(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))
						elif random_bonus_now == "stoptime":
							bonuses_sprites.add(SPRITE_BONUS_stoptime(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))
						elif random_bonus_now == "tank":
							bonuses_sprites.add(SPRITE_BONUS_tank(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))
						elif random_bonus_now == "shovel":
							bonuses_sprites.add(SPRITE_BONUS_shovel(pos=(random.randint(SPAWN_POLE[0], WIDTH_POLE), random.randint(SPAWN_POLE[1], HEIGHT_POLE)), tank_sprite=player))


						self.counter_bonuses_lvl4 += 1
					delete_sprite.hp -= self.damage


			



				


class LevelParser:
	def __init__(self, path_file_level='data/configs/levels/01.bslvl', coords=(SPAWN_POLE[0], SPAWN_POLE[1])):
		self.path_file_level = path_file_level

		f = open(self.path_file_level, 'r', encoding='utf-8')
		self.level = f.readlines()
		f.close()

		###### self.h_line = SPAWN_POLE[1]+48

		# self.h_line = BATTLE_POLE.y

		# self.v_line = BATTLE_POLE.x

		self.h_line = coords[1]

		self.v_line = coords[0]
		self.num_e = 0

	def draw(self):
		n = 12 # ширина уровня
		# print(self.level[len(self.level)-1])
		for e in self.level:
			self.num_e += 1
			# print(e)
			# print(self.level[len(self.level)-1])
			try:
				if self.num_e in [12, 11, 13]: # or e == self.level[len(self.level)-2]:
					self.level[self.num_e] = self.level[self.num_e][0:4] + 5*' ' + self.level[self.num_e][9:len(self.level[self.num_e])]
				# self.level[len(self.level)-2] = self.level[len(self.level)-2][0:4] + 4*' ' + self.level[len(self.level)-2][9:len(self.level[len(self.level)-2])]
			except Exception:
				pass

			for simvol in e:
				if simvol == '=':
					wall = Wall(WALL_BRICKS, (self.v_line + 12, self.h_line))
					walls_sprites.add(wall)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == ' ':
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == '-':
					wall = Wall(WALL_BRICKS_24, (self.v_line + 12, self.h_line))
					walls_sprites.add(wall)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == '\\':
					wall = Wall(WALL_BRICKS_24_R2, (self.v_line + 12, self.h_line))
					walls_sprites.add(wall)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == '/':
					wall = Wall(WALL_BRICKS_24_R3, (self.v_line+24 - 24 + 12, self.h_line))
					walls_sprites.add(wall)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == '_':
					wall = Wall(WALL_BRICKS_24_R4, (self.v_line + 12, self.h_line+24))
					walls_sprites.add(wall)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == '*':
					bush = Bush(WALL_BUSH, (self.v_line, self.h_line))
					bush_sprites.add(bush)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == 'w':
					water = Water(WATER, (self.v_line, self.h_line))
					water_sprites.add(water)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == '#':
					beton = WallBeton(WALL_BETON, (self.v_line, self.h_line))
					beton_sprites.add(beton)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == "'":
					beton = WallBeton(WALL_BETON_24UP, (self.v_line, self.h_line))
					beton_sprites.add(beton)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == ",":
					beton = WallBeton(WALL_BETON_24DOWN, (self.v_line, self.h_line+24))
					beton_sprites.add(beton)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == "[":
					beton = WallBeton(WALL_BETON_24LEFT, (self.v_line, self.h_line))
					beton_sprites.add(beton)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == "]":
					beton = WallBeton(WALL_BETON_24RIGHT, (self.v_line+24, self.h_line))
					beton_sprites.add(beton)
					if self.v_line <= 48*n:
						self.v_line += 48

				elif simvol == ';':
					self.h_line -= 48
					break

				elif simvol == "i":
					ice = Ice(WALL_BUSH, (self.v_line, self.h_line))
					ice_sprites.add(ice)
					if self.v_line <= 48*n:
						self.v_line += 48

			if self.h_line <= 12*48:
				self.h_line += 48
			self.v_line = SPAWN_POLE[0]



# 699, 285
class Respawn_Player1_CountPanel(pygame.sprite.Sprite):
	def __init__(self, count, pos=(699, 395), path_image_panel='%s/gui/battle/1_player.png'):
		pygame.sprite.Sprite.__init__(self)

		self.count = count

		try:
			self.image = image.load(path_image_panel % LOAD_TEXTURES)
		except Exception:
			self.image = image.load(path_image_panel % DEFAULT_TEXTURES)
		self.rect = self.image.get_rect()


		if TYPE_RIGHT_INTERFACE == 1:
			self.pos_x = pos[0]
			self.pos_y = pos[1]

			self.rect.x = self.pos_x
			self.rect.y = self.pos_y
		elif TYPE_RIGHT_INTERFACE in [2, 3]:
			self.rect.x = 696
			self.rect.y = 121
		


class EnemyRightList(pygame.sprite.Sprite):
	def __init__(self, count_enemy, pos=(696, 49), path_image_panel='%s/gui/battle/panel_tank.png'):
		pygame.sprite.Sprite.__init__(self)
		# (702, 49) = для сокращенного
		# (696, 49) = для полного

		self.count_enemy = count_enemy
		self.pos_x = pos[0]
		self.pos_y = pos[1]

		try:
			self.image = image.load(path_image_panel % LOAD_TEXTURES)
		except Exception:
			self.image = image.load(path_image_panel % DEFAULT_TEXTURES)
		self.rect = self.image.get_rect()

		self.rect.x = self.pos_x
		self.rect.y = self.pos_y


	def update(self):
		pass





class RocketPanel(pygame.sprite.Sprite):
	def __init__(self, pos=(696, 169), path_image_panel='%s/gui/battle/rocket_counter_panel.png'):
		pygame.sprite.Sprite.__init__(self)
		
		self.pos_x = 696
		self.pos_y = 174-5

		try:
			self.image = image.load(path_image_panel % LOAD_TEXTURES)
		except Exception:
			self.image = image.load(path_image_panel % DEFAULT_TEXTURES)
		self.rect = self.image.get_rect()

		self.rect.x = self.pos_x
		self.rect.y = self.pos_y

	def update(self):

		
		self.rect.x = self.pos_x
		self.rect.y = self.pos_y

		






class FlagPanel(pygame.sprite.Sprite):
	def __init__(self, pos=(696, 529), path_image_panel='%s/gui/battle/panel_flag.png'):
		pygame.sprite.Sprite.__init__(self)

		
		self.pos_x = pos[0]
		self.pos_y = pos[1]

		try:
			self.image = image.load(path_image_panel % LOAD_TEXTURES)
		except Exception:
			self.image = image.load(path_image_panel % DEFAULT_TEXTURES)

		self.rect = self.image.get_rect()

		self.rect.x = self.pos_x
		self.rect.y = self.pos_y







def draw_level_number(lvl_num=level_number["g"]):
	text = battlecity_font.render(str(lvl_num), 0, BLACK, BATTLE_BG_COLOR)

	if lvl_num <= 9:
		(screen).blit(text, (696+24, 574))
	else:
		(screen).blit(text, (696, 574))




class GAMEOVER(pygame.sprite.Sprite):
	def __init__(self, pos=(WIDTH_POLE/2, HEIGHT_POLE), path_panel='%s/gui/battle/game_over.png'):
		pygame.sprite.Sprite.__init__(self)


		try:
			self.image = image.load(path_panel % LOAD_TEXTURES)
		except Exception:
			self.image = image.load(path_panel % DEFAULT_TEXTURES)

		self.rect = self.image.get_rect()

		self.rect.x = pos[0]
		self.rect.y = pos[1]


	def update(self):
		if self.rect.y >= HEIGHT_POLE/2-35:
			self.rect.y -= SPEED_MOVE_GAMEOVER
		else:
			self.rect.y = self.rect.y

			



class PAUSE(pygame.sprite.Sprite):
	def __init__(self, pos=(WIDTH//2-22, HEIGHT//2), path_panel='%s/gui/battle/pause.png'):
		pygame.sprite.Sprite.__init__(self)


		try:
			self.image = image.load(path_panel % LOAD_TEXTURES)
		except Exception:
			self.image = image.load(path_panel % DEFAULT_TEXTURES)

		self.rect = self.image.get_rect()
		self.pos = pos

		self.rect.center = self.pos

		self.count = 0

	def update(self):
		self.count += 1
		if self.count == 20:
			self.rect.center = (-100, -100)

		elif self.count == 37:
			self.rect.center = self.pos
			self.count = 0
		




		






class CountKillEnemy(pygame.sprite.Sprite):
	def __init__(self, tank_level, pos, counter_rules=COUNTER_RULES):
		pygame.sprite.Sprite.__init__(self)

		self.tank_level = str(tank_level)
		self.pos = pos

		self.pos_x = self.pos[0]
		self.pos_y = self.pos[1]

		self.rules = counter_rules

		self.add_exp = self.rules[self.tank_level]
		self.timer = self.rules["timer"]

		try:
			self.image = image.load(f'{LOAD_TEXTURES}/gui/battle/counter/'+self.add_exp+'.png')
		except Exception:
			self.image = image.load(f'{DEFAULT_TEXTURES}/gui/battle/counter/'+self.add_exp+'.png')
		self.rect = self.image.get_rect()

		self.rect.x = self.pos_x
		self.rect.y = self.pos_y

		self.counter = 0

	def update(self):
		self.counter += 1
		if self.counter > self.timer:
			self.kill()
			self.counter = 0






##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################




class SPRITE_BONUS_shovel(pygame.sprite.Sprite):
	def __init__(self, pos, tank_sprite, name_image='shovel_bonus.png', path_images='%s/map_objects/bonuses/'):
		pygame.sprite.Sprite.__init__(self)
		# player_bonuses_sprites.add(BONUS_immortality(pos=(self.enemy_tank.rect.center[0]-24, self.enemy_tank.rect.center[1]-24), tank_sprite=self.enemy_tank))
		self.pos = pos

		self.pos_x = self.pos[0]
		self.pos_y = self.pos[1]
		self.tank_sprite = tank_sprite
		

		try:
			self.image = image.load(path_images % (LOAD_TEXTURES)+name_image)
		except Exception:
			self.image = image.load(path_images % (DEFAULT_TEXTURES)+name_image)

		self.rect = self.image.get_rect()
		self.rect.center = (self.pos_x, self.pos_y)
		# self.pos_center = self.rect.center

		

		self.counter = 0
		self.k = 20

		self.timer = 0

		self.timer_stoptime = 0
		self.count_timer = False



	def update(self):

		if dict_PAUSE_GAME["g"] == False:
			
			self.timer += 1
			

			if self.timer <= TIMER_LIVE_BONUS:
				self.counter += 1
				if self.counter >= self.k:
					# self.index = 1
					self.rect.center = (-100, -100)

				if self.counter >= self.k*2:
					self.rect.center = (self.pos_x, self.pos_y)		
					self.counter = 0


				hits_player = pygame.sprite.spritecollide(self, player_sprites, False)
				if hits_player:
					MUSIC_use_bonus.set_volume(set_volume)
					MUSIC_use_bonus.play()
					self.kill()

					bonuses_sprites.remove(self)
					count_kill = CountKillEnemy(tank_level="bonus_get", pos=(self.rect.center[0]-19, self.rect.center[1]-10))
					count_kill_enemy_sprites.add(count_kill)
					ROUND_COUNTS["other"] += int(COUNTER_RULES["bonus_get"])

					######### ######## ####### ######

					PLAYER1_NOW_BONUS["shovel"] = True

					

			else:
				self.kill()






class SPRITE_BONUS_tank(pygame.sprite.Sprite):
	def __init__(self, pos, tank_sprite, name_image='tank_bonus.png', path_images='%s/map_objects/bonuses/'):
		pygame.sprite.Sprite.__init__(self)
		# player_bonuses_sprites.add(BONUS_immortality(pos=(self.enemy_tank.rect.center[0]-24, self.enemy_tank.rect.center[1]-24), tank_sprite=self.enemy_tank))
		self.pos = pos

		self.pos_x = self.pos[0]
		self.pos_y = self.pos[1]
		self.tank_sprite = tank_sprite
		

		try:
			self.image = image.load(path_images % (LOAD_TEXTURES)+name_image)
		except Exception:
			self.image = image.load(path_images % (DEFAULT_TEXTURES)+name_image)

		self.rect = self.image.get_rect()
		self.rect.center = (self.pos_x, self.pos_y)
		# self.pos_center = self.rect.center

		

		self.counter = 0
		self.k = 20

		self.timer = 0

		self.timer_stoptime = 0
		self.count_timer = False



	def update(self):

		if dict_PAUSE_GAME["g"] == False:
			
			self.timer += 1
			

			if self.timer <= TIMER_LIVE_BONUS:
				self.counter += 1
				if self.counter >= self.k:
					# self.index = 1
					self.rect.center = (-100, -100)

				if self.counter >= self.k*2:
					self.rect.center = (self.pos_x, self.pos_y)		
					self.counter = 0


				hits_player = pygame.sprite.spritecollide(self, player_sprites, False)
				if hits_player:
					MUSIC_bonus_life.set_volume(set_volume)
					MUSIC_bonus_life.play()
					self.kill()

					bonuses_sprites.remove(self)
					count_kill = CountKillEnemy(tank_level="bonus_get", pos=(self.rect.center[0]-19, self.rect.center[1]-10))
					count_kill_enemy_sprites.add(count_kill)
					ROUND_COUNTS["other"] += int(COUNTER_RULES["bonus_get"])

					PLAYER_1_HP["now"] += 1

					######### ######## ####### ######

					

					
			

					

			else:
				self.kill()






timer_stoptime = 0
class SPRITE_BONUS_stoptime(pygame.sprite.Sprite):
	def __init__(self, pos, tank_sprite, name_image='stoptime_bonus.png', path_images='%s/map_objects/bonuses/'):
		pygame.sprite.Sprite.__init__(self)
		# player_bonuses_sprites.add(BONUS_immortality(pos=(self.enemy_tank.rect.center[0]-24, self.enemy_tank.rect.center[1]-24), tank_sprite=self.enemy_tank))
		self.pos = pos

		self.pos_x = self.pos[0]
		self.pos_y = self.pos[1]
		self.tank_sprite = tank_sprite
		

		try:
			self.image = image.load(path_images % (LOAD_TEXTURES)+name_image)
		except Exception:
			self.image = image.load(path_images % (DEFAULT_TEXTURES)+name_image)

		self.rect = self.image.get_rect()
		self.rect.center = (self.pos_x, self.pos_y)
		# self.pos_center = self.rect.center

		self.counter = 0
		self.k = 20

		self.timer = 0

		self.timer_stoptime = 0
		self.count_timer = False



	def update(self):
		
		if dict_PAUSE_GAME["g"] == False:

			self.timer += 1

			# print(self.timer)
			if self.timer >= 500 and PLAYER1_NOW_BONUS["stoptime"] == True:
				PLAYER1_NOW_BONUS["stoptime"] = False
			

			if self.timer <= TIMER_LIVE_BONUS:
				self.counter += 1
				if self.counter >= self.k:
					# self.index = 1
					self.rect.center = (-100, -100)

				if self.counter >= self.k*2:
					self.rect.center = (self.pos_x, self.pos_y)		
					self.counter = 0


				hits_player = pygame.sprite.spritecollide(self, player_sprites, False)
				if hits_player:
					MUSIC_use_bonus.set_volume(set_volume)
					MUSIC_use_bonus.play()
					self.kill()

					bonuses_sprites.remove(self)
					count_kill = CountKillEnemy(tank_level="bonus_get", pos=(self.rect.center[0]-19, self.rect.center[1]-10))
					count_kill_enemy_sprites.add(count_kill)
					ROUND_COUNTS["other"] += int(COUNTER_RULES["bonus_get"])

					######### ######## ####### ######
								
					PLAYER1_NOW_BONUS["stoptime"] = True

					# BONUS_stoptime()

			else:
				self.kill()








# Количество танков, убитых гранатой
grenade_destroyed_enemys = {"g": 0}
# grenade_destroyed_enemys["g"]

class SPRITE_BONUS_grenade(pygame.sprite.Sprite):
	def __init__(self, pos, tank_sprite, name_image='grenade_bonus.png', path_images='%s/map_objects/bonuses/'):
		pygame.sprite.Sprite.__init__(self)
		# player_bonuses_sprites.add(BONUS_immortality(pos=(self.enemy_tank.rect.center[0]-24, self.enemy_tank.rect.center[1]-24), tank_sprite=self.enemy_tank))
		self.pos = pos

		self.pos_x = self.pos[0]
		self.pos_y = self.pos[1]
		self.tank_sprite = tank_sprite
		

		try:
			self.image = image.load(path_images % (LOAD_TEXTURES)+name_image)
		except Exception:
			self.image = image.load(path_images % (DEFAULT_TEXTURES)+name_image)

		self.rect = self.image.get_rect()
		self.rect.center = (self.pos_x, self.pos_y)
		# self.pos_center = self.rect.center

		self.counter = 0
		self.k = 20

		self.timer = 0



	def update(self):

		if dict_PAUSE_GAME["g"] == False:
		
			self.timer += 1
			

			if self.timer <= TIMER_LIVE_BONUS:
				self.counter += 1
				if self.counter >= self.k:
					# self.index = 1
					self.rect.center = (-100, -100)

				if self.counter >= self.k*2:
					self.rect.center = (self.pos_x, self.pos_y)		
					self.counter = 0


				hits_player = pygame.sprite.spritecollide(self, player_sprites, False)
				if hits_player:
					MUSIC_use_bonus.set_volume(set_volume)
					MUSIC_use_bonus.play()
					self.kill()

					bonuses_sprites.remove(self)
					count_kill = CountKillEnemy(tank_level="bonus_get", pos=(self.rect.center[0]-19, self.rect.center[1]-10))
					count_kill_enemy_sprites.add(count_kill)
					ROUND_COUNTS["other"] += int(COUNTER_RULES["bonus_get"])

					######### ######## ####### ######

					for sprite in enemys_sprites.sprites():
						AddExplosion(pos=sprite.rect.center, sprite=sprite, big=True)
						sprite.kill()
						grenade_destroyed_enemys["g"] += 1

					CHANNEL_kill_enemy.play(MUSIC_kill_enemy)




						

			else:
				self.kill()







class SPRITE_BONUS(pygame.sprite.Sprite):
	def __init__(self, pos, tank_sprite, name_image, bonus_on, path_images='%s/map_objects/bonuses/'):
		pygame.sprite.Sprite.__init__(self)
		# player_bonuses_sprites.add(BONUS_immortality(pos=(self.enemy_tank.rect.center[0]-24, self.enemy_tank.rect.center[1]-24), tank_sprite=self.enemy_tank))

		self.pos_x = pos[0]
		self.pos_y = pos[1]
		self.tank_sprite = tank_sprite
		self.bonus_on = bonus_on

		try:
			self.image = image.load(path_images % (LOAD_TEXTURES)+name_image)
		except Exception:
			self.image = image.load(path_images % (DEFAULT_TEXTURES)+name_image)

		self.rect = self.image.get_rect()
		self.rect.center = (self.pos_x, self.pos_y)
		# self.pos_center = self.rect.center

		self.counter = 0
		self.k = 20

		self.timer = 0



	def update(self):
		if dict_PAUSE_GAME["g"] == False:

			self.timer += 1
			if self.timer <= TIMER_LIVE_BONUS:
				
				self.counter += 1
				if self.counter >= self.k:
					# self.index = 1
					self.rect.center = (-100, -100)

				if self.counter >= self.k*2:
					self.rect.center = (self.pos_x, self.pos_y)		
					self.counter = 0


				hits_player = pygame.sprite.spritecollide(self, player_sprites, False)
				if hits_player:		
					MUSIC_use_bonus.set_volume(set_volume)
					MUSIC_use_bonus.play()
					self.kill()
					bonuses_sprites.remove(self)
					count_kill = CountKillEnemy(tank_level="bonus_get", pos=(self.rect.center[0]-19, self.rect.center[1]-10))
					count_kill_enemy_sprites.add(count_kill)
					ROUND_COUNTS["other"] += int(COUNTER_RULES["bonus_get"])

					try:
						player_bonuses_sprites.add(self.bonus_on)
					except Exception:
						self.bonus_on()
			else:
				self.kill()

	def sprite(self):
		return self




class SPRITE_BONUS_star(pygame.sprite.Sprite):
	def __init__(self, pos, tank_sprite, name_image='star_bonus.png', path_images='%s/map_objects/bonuses/'):
		pygame.sprite.Sprite.__init__(self)
		# player_bonuses_sprites.add(BONUS_immortality(pos=(self.enemy_tank.rect.center[0]-24, self.enemy_tank.rect.center[1]-24), tank_sprite=self.enemy_tank))
		self.pos = pos

		self.pos_x = self.pos[0]
		self.pos_y = self.pos[1]
		self.tank_sprite = tank_sprite
		

		try:
			self.image = image.load(path_images % (LOAD_TEXTURES)+name_image)
		except Exception:
			self.image = image.load(path_images % (DEFAULT_TEXTURES)+name_image)
		self.rect = self.image.get_rect()
		self.rect.center = (self.pos_x, self.pos_y)
		# self.pos_center = self.rect.center

		self.counter = 0
		self.k = 20

		self.timer = 0



	def update(self):

		if dict_PAUSE_GAME["g"] == False:
			
			self.timer += 1
			

			if self.timer <= TIMER_LIVE_BONUS:
				self.counter += 1
				if self.counter >= self.k:
					# self.index = 1
					self.rect.center = (-100, -100)

				if self.counter >= self.k*2:
					self.rect.center = (self.pos_x, self.pos_y)		
					self.counter = 0


				hits_player = pygame.sprite.spritecollide(self, player_sprites, False)
				if hits_player:
					MUSIC_use_bonus.set_volume(set_volume)
					MUSIC_use_bonus.play()
					self.kill()

					bonuses_sprites.remove(self)

					lvl_tank_now = int(self.tank_sprite.lvl_tank)

					if lvl_tank_now < 4:
						lvl_tank_now += 1
					else:
						lvl_tank_now = 4

					self.tank_sprite.lvl_tank = lvl_tank_now


					PLAYER["lvl_start"] = lvl_tank_now
					pos_x_tank = player_sprites.sprites()[len(player_sprites.sprites())-1].rect.x
					pos_y_tank = player_sprites.sprites()[len(player_sprites.sprites())-1].rect.y


					player = Tank(PLAYER, pos_spawn=(pos_x_tank, pos_y_tank))
					player_sprites.empty()
					# player_sprites.sprites()[len(player_sprites.sprites())-1].kill()

					player_sprites.add(player)
					count_kill = CountKillEnemy(tank_level="bonus_get", pos=(self.rect.center[0]-19, self.rect.center[1]-10))
					count_kill_enemy_sprites.add(count_kill)
					ROUND_COUNTS["other"] += int(COUNTER_RULES["bonus_get"])





					if PLAYER1_NOW_BONUS["immortality"] == True:					
						# player_bonuses_sprites.sprites()[len(player_bonuses_sprites.sprites())-1].kill()
						# player_sprites.empty()
						PLAYER1_NOW_BONUS["immortality"] = False
						

			else:
				self.kill()
			





class BONUS_immortality(pygame.sprite.Sprite):
	def __init__(self, pos, tank_sprite, now_use="timer_respawn", p=BONUSCONFIG_immortality, path_images='%s/gui/battle/tank_effects/'):
		pygame.sprite.Sprite.__init__(self)

		self.pos_x = pos[0]
		self.pos_y = pos[1]
		self.tank_sprite = tank_sprite

		self.p = p

		self.timer_respawn = self.p["timer_respawn"]
		self.timer_bonus = self.p["timer_bonus"]
		self.now_use = now_use
		

		self.images = []

		try:
			self.images.append(image.load(path_images % (LOAD_TEXTURES)+'immortality_a1.png'))
		except Exception:
			self.images.append(image.load(path_images % (DEFAULT_TEXTURES)+'immortality_a1.png'))

		try:
			self.images.append(image.load(path_images % (LOAD_TEXTURES)+'immortality_a2.png'))
		except Exception:
			self.images.append(image.load(path_images % (DEFAULT_TEXTURES)+'immortality_a2.png'))
		

		self.index = 0

		self.image = self.images[self.index]
		self.rect = self.image.get_rect()

		self.rect.x = self.pos_x
		self.rect.y = self.pos_y

		# self.rect.x = self.tank_sprite.rect.x
		# self.rect.y = self.tank_sprite.rect.y


		self.counter = 0
		self.counter_shim = 0
		self.timer = 0

		

		self.k = 2


	def update(self):
		if len(player_sprites.sprites()) == 1:
			if dict_PAUSE_GAME["g"] == False:
				self.timer += 1
				if self.timer <= self.p[self.now_use]:
					self.counter += 1
					

					if self.counter >= self.k:
						self.index = 1

					if self.counter >= self.k*2:
						self.index = 0
						self.counter = 0
					

					PLAYER1_NOW_BONUS["immortality"] = True
					
					self.image = self.images[self.index]
					self.rect.center = (self.tank_sprite.rect.center)


				else:
					self.rect.center = (self.tank_sprite.rect.center)
					self.kill()
					PLAYER1_NOW_BONUS["immortality"] = False
					self.timer = 0








##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################










#### ДОБАВЛЕНИЕ СПРАЙТОВ ОБЪЕКТОВ В ГРУППУ СПРАЙТОВ ####
all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()


# CountKillEnemy
count_kill_enemy_sprites = pygame.sprite.Group()


player_bonuses_sprites = pygame.sprite.Group()




flag_panel_sprites = pygame.sprite.Group()
flag_panel_sprites.add(FlagPanel())

rocket_counter_panel_sprites = pygame.sprite.Group()
if TYPE_RIGHT_INTERFACE == 2:
	rocket_counter_panel_sprites.add(RocketPanel())




gameover_sprites = pygame.sprite.Group()
gameover_label = GAMEOVER()
gameover_sprites.add(gameover_label)


pause_sprites = pygame.sprite.Group()
pause_label = PAUSE()
pause_sprites.add(pause_label)




level_panel_sprites = pygame.sprite.Group()


respawn_count_sprites = pygame.sprite.Group()
respawn_count_panel = Respawn_Player1_CountPanel(count=0)
respawn_count_sprites.add(respawn_count_panel)



enemys_spawn_animation_sprites = pygame.sprite.Group()


# player_sprites.add(player)

enemys_sprites = pygame.sprite.Group()

# enemy = [Tank(ENEMY), Tank(ENEMY), Tank(ENEMY)]
# for i in range(len(enemy)):
# 	enemys_sprites.add(enemy[i])



sysinfo_game_sprites = pygame.sprite.Group()


walls_sprites = pygame.sprite.Group()
beton_sprites = pygame.sprite.Group()
bush_sprites = pygame.sprite.Group()
water_sprites = pygame.sprite.Group()
base_sprites = pygame.sprite.Group()


bonuses_sprites = pygame.sprite.Group()
# SPRITE_BONUS_immortality

ice_sprites = pygame.sprite.Group()





#### ГРУППА СПРАЙТОВ ДЛЯ БЕТОННЫХ СТЕН ОТ БОНУСА ЛОПАТА ####
beton_shovel_sprites = pygame.sprite.Group()
# ПРОЧИЕ ПЕРЕМЕННЫЕ
timer_shovel = 0


counter_shovel = 0
count_shovel_animations = 0




# КОНФИГ ВСЕХ 35 УРОВНЕЙ ДЛЯ ИГРЫ НА ПЕРВОЙ СТАДИИ ИГРЫ
LEVELS_CONFIG = dict()
# Для первого круга
for i in range(1, 37):
	if i <= 9:
		str_lvl = "0"+str(i)
	else:
		str_lvl = str(i)
	LEVELS_CONFIG[str_lvl] = CONFIG_ROUND1_LEVELS



# ЧЕТВЕРТЫЙ, 11 и 18 ТАНКИ МЕРАЦЮЩИЕ

class EnemyList:
	def __init__(self, LEVELS_CONFIG=LEVELS_CONFIG, lvl_now=str(level_number["g"]), counter_shim_tanks=-1, lvl_counts=[]):
		self.LEVELS_CONFIG = LEVELS_CONFIG
		self.lvl_now = lvl_now

		if int(lvl_now) < 10:		
			lvl_now = "0" + str(lvl_now)
		else:
			lvl_now = str(level_number["g"])


		now_lvl_config = LEVELS_CONFIG[f"{lvl_now}"]
		# print(now_lvl_config)


		# lvl_counts = []

		for i in range(1, 5):
			lvl_counts.append(now_lvl_config[f"lvl{i}"])

		lvl1_count = now_lvl_config["lvl1"]
		lvl2_count = now_lvl_config["lvl2"]
		lvl3_count = now_lvl_config["lvl3"]
		lvl4_count = now_lvl_config["lvl4"]

		self.count_all_tanks = lvl1_count + lvl2_count + lvl3_count + lvl4_count

		# Список врагов для конкретно этого уровня
		self.enemys_list_for_now_level = []

		# Счетчик для спавна мерцающих танков
		# counter_shim_tanks = -1

		for i in range(lvl1_count):
			counter_shim_tanks += 1
			if counter_shim_tanks == 3 or counter_shim_tanks == 10 or counter_shim_tanks == 17:
				bonuses_sprites.empty()
				self.enemys_list_for_now_level.append(Tank(ENEMY, shim_tank=True))
			else:
				self.enemys_list_for_now_level.append(Tank(ENEMY))


		for i in range(lvl2_count):
			counter_shim_tanks += 1
			if counter_shim_tanks == 3 or counter_shim_tanks == 10 or counter_shim_tanks == 17:
				bonuses_sprites.empty()
				self.enemys_list_for_now_level.append(Tank(ENEMY_LVL2, shim_tank=True))
			else:
				self.enemys_list_for_now_level.append(Tank(ENEMY_LVL2))

		for i in range(lvl3_count):
			counter_shim_tanks += 1
			if counter_shim_tanks == 3 or counter_shim_tanks == 10 or counter_shim_tanks == 17:
				bonuses_sprites.empty()	
				self.enemys_list_for_now_level.append(Tank(ENEMY_LVL3, shim_tank=True))
			else:
				self.enemys_list_for_now_level.append(Tank(ENEMY_LVL3))


		for i in range(lvl4_count):
			counter_shim_tanks += 1
			if counter_shim_tanks == 3 or counter_shim_tanks == 10 or counter_shim_tanks == 17:
				bonuses_sprites.empty()
				self.enemys_list_for_now_level.append(Tank(ENEMY_LVL4, shim_tank=True))
			else:
				self.enemys_list_for_now_level.append(Tank(ENEMY_LVL4))

		# counter_shim_tanks = -1
		# print(counter_shim_tanks)


	def get_list(self):
		"""Функция возращает список танков для конкретного уровня. Спавнер будет спавнить подряд каждый танк пока они не закончатся"""
		return self.enemys_list_for_now_level

	def get_count(self):
		"""Возращает количество танков противника"""
		return self.count_all_tanks


ENEMYLIST = EnemyList(LEVELS_CONFIG, level_number["g"])



panel_tanks_sprites = pygame.sprite.Group()

if TYPE_RIGHT_INTERFACE == 1:
	posx, posy = 696, 49
	startx, starty = posx, posy

	panel_tanks = EnemyRightList(count_enemy=ENEMYLIST.get_count(), pos=[posx, posy])
	panel_tanks_sprites.add(panel_tanks)

	for i in range(EnemyList(LEVELS_CONFIG, level_number["g"]).get_count()-1):
		if posx >= 696+24:
			posx = startx
			posy += 24
		else:
			posx += 24

		panel_tanks = EnemyRightList(count_enemy=ENEMYLIST.get_count(), pos=[posx, posy])
		panel_tanks_sprites.add(panel_tanks)


elif TYPE_RIGHT_INTERFACE in [2, 3]:
	posx, posy = 702, 49
	startx, starty = posx, posy

	# enemy_counter_right = battlecity_font.


	enemy_counter_right = battlecity_font.render(str(len(panel_tanks_sprites.sprites())), 0, BLACK, BATTLE_BG_COLOR)



# ЗАПОЛНЯЕМ СПИСОК ПРОТИВНИКОВ ДЛЯ ДАННОГО УРОВНЯ
# random_level_list = ListEnemyForLEVEL(LEVELS_CONFIG, level_number)




# КАК ЧАСТО БУДЕТ ПОЯВЛЯТСЯ ПРОТИВНИК ПОСЛЕ УБИЙСТВА ПОСЛЕДНЕГО
TIMER_RESPAWN_ENEMYS = CONFIG_ROUND1_LEVELS["timer_respawn"]


# СКОЛЬКО ПРОТИВНИКОВ МОЖЕТ БЫТЬ ОДНОВРЕМЕННО НА ПОЛЕ БОЯ
ENEMYS_COUNT_IN_BATTLE = CONFIG_ROUND1_LEVELS["all_enemys_count_in_battle"]


# level_number = 5
if level_number["g"] <= 9:
	level_map = LevelParser(f'data/configs/levels/0{level_number["g"]}.bslvl')
else:
	level_map = LevelParser(f'data/configs/levels/{level_number["g"]}.bslvl')

level_map.draw()


wall_base_1 = Wall(WALL_BRICKS_24, (SPAWN_BASE[0]+12, SPAWN_BASE[1]))
walls_sprites.add(wall_base_1)
wall_base_2 = Wall(WALL_BRICKS_24, (SPAWN_BASE[0]+48+12, SPAWN_BASE[1]))
walls_sprites.add(wall_base_2)
wall_base_3 = Wall(WALL_BRICKS_24_R2, (SPAWN_BASE[0]+12, SPAWN_BASE[1]+24))
walls_sprites.add(wall_base_3)
wall_base_4 = Wall(WALL_BRICKS_24_R3, (SPAWN_BASE[0]+48+12, SPAWN_BASE[1]+24))
walls_sprites.add(wall_base_4)

eagle = BaseEagle(pos=(SPAWN_BASE[0]+24, SPAWN_BASE[1]+24))
base_sprites.add(eagle)

	
player = Tank(PLAYER)
animation_spawn = SpawnEnemyAnimation(pos=(player.rect.center), enemy_tank=player)			
enemys_spawn_animation_sprites.add(animation_spawn)



bullets = pygame.sprite.Group()
bullets_enemy = pygame.sprite.Group()

rockets_sprites = pygame.sprite.Group()


explosions = pygame.sprite.Group()

k_full = False
counter = 0

counter_respawn_player = 0
counter_respawn_enemy = 0


# Какой эелемент списка будет заспавнен следующим
count_spawn = 0

FILL_BLACK = False


# next_window_mode = pygame.FULLSCREEN
next_window_mode = 1



enemys_list_for_spawner = {"list": ENEMYLIST.get_list()}




def ReloadBattle(next_level=level_number["g"], custom=False, config_rules_enemy=CONFIG_ROUND1_LEVELS):
	"""Функция обновляет параметры сражения под номер следующего уровня"""
	


	all_sprites.empty()
	player_sprites.empty()
	count_kill_enemy_sprites.empty()
	player_bonuses_sprites.empty()
	flag_panel_sprites.empty()
	gameover_sprites.empty()
	pause_sprites.empty()
	level_panel_sprites.empty()
	respawn_count_sprites.empty()
	enemys_spawn_animation_sprites.empty()
	enemys_sprites.empty()
	sysinfo_game_sprites.empty()
	walls_sprites.empty()
	beton_sprites.empty()
	bush_sprites.empty()
	water_sprites.empty()
	base_sprites.empty()
	bonuses_sprites.empty()
	beton_shovel_sprites.empty()
	panel_tanks_sprites.empty()
	walls_sprites.empty()
	bullets.empty()
	bullets_enemy.empty()
	explosions.empty()
	ice_sprites.empty()
	rockets_sprites.empty()

	
	rocket_counter_panel_sprites.empty()

	CHANNEL_enemy_move.stop()
	CHANNEL_player_move.stop()
	CHANNEL_bullet_collide_tank.stop()
	CHANNEL_bullet_collide_wall.stop()
	CHANNEL_shot_tanks.stop()
	CHANNEL_kill_enemy.stop()
	CHANNEL_bullet_collide_wall.stop()



	flag_panel_sprites.add(FlagPanel())
	gameover_label = GAMEOVER()
	gameover_sprites.add(gameover_label)
	pause_label = PAUSE()
	pause_sprites.add(pause_label)
	respawn_count_panel = Respawn_Player1_CountPanel(count=0)
	respawn_count_sprites.add(respawn_count_panel)

	posx, posy = 696, 49
	startx, starty = posx, posy


	level_number["g"] = next_level
	LEVELS_CONFIG["36"] = config_rules_enemy

	ENEMYLIST_local = EnemyList(LEVELS_CONFIG, level_number["g"])	
	panel_tanks = EnemyRightList(count_enemy=ENEMYLIST_local.get_count(), pos=[posx, posy])
	panel_tanks_sprites.add(panel_tanks)
	for i in range(EnemyList(LEVELS_CONFIG, level_number["g"]).get_count()-1):
		if posx >= 696+24:
			posx = startx
			posy += 24
		else:
			posx += 24

		panel_tanks = EnemyRightList(count_enemy=ENEMYLIST_local.get_count(), pos=[posx, posy])
		panel_tanks_sprites.add(panel_tanks)
	# КАК ЧАСТО БУДЕТ ПОЯВЛЯТСЯ ПРОТИВНИК ПОСЛЕ УБИЙСТВА ПОСЛЕДНЕГО
	TIMER_RESPAWN_ENEMYS = config_rules_enemy["timer_respawn"]


	# СКОЛЬКО ПРОТИВНИКОВ МОЖЕТ БЫТЬ ОДНОВРЕМЕННО НА ПОЛЕ БОЯ
	ENEMYS_COUNT_IN_BATTLE = config_rules_enemy["all_enemys_count_in_battle"]


	# level_number = 5
	if level_number["g"] <= 9:
		level_map = LevelParser(f'data/configs/levels/0{level_number["g"]}.bslvl')
	else:
		level_map = LevelParser(f'data/configs/levels/{level_number["g"]}.bslvl')



	level_map.draw()


	wall_base_1 = Wall(WALL_BRICKS_24, (SPAWN_BASE[0]+12, SPAWN_BASE[1]))
	walls_sprites.add(wall_base_1)
	wall_base_2 = Wall(WALL_BRICKS_24, (SPAWN_BASE[0]+48+12, SPAWN_BASE[1]))
	walls_sprites.add(wall_base_2)
	wall_base_3 = Wall(WALL_BRICKS_24_R2, (SPAWN_BASE[0]+12, SPAWN_BASE[1]+24))
	walls_sprites.add(wall_base_3)
	wall_base_4 = Wall(WALL_BRICKS_24_R3, (SPAWN_BASE[0]+48+12, SPAWN_BASE[1]+24))
	walls_sprites.add(wall_base_4)

	eagle = BaseEagle(pos=(SPAWN_BASE[0]+24, SPAWN_BASE[1]+24))
	base_sprites.add(eagle)

	if TYPE_RIGHT_INTERFACE == 2:
		rocket_counter_panel_sprites.add(RocketPanel())

	player_sprites.empty()
	enemys_spawn_animation_sprites.empty()

	
	

	player = Tank(PLAYER)
	animation_spawn = SpawnEnemyAnimation(pos=(player.rect.center), enemy_tank=player)			
	enemys_spawn_animation_sprites.add(animation_spawn)
	k_full = False
	counter = 0

	counter_respawn_player = 0
	counter_respawn_enemy = 0


	# Какой эелемент списка будет заспавнен следующим
	count_spawn = 0

	FILL_BLACK = False


	next_window_mode = pygame.FULLSCREEN

	# dict_RUN_SLIDE_NOW["g"] = 1

	dict_PAUSE_GAME["g"] = False

	# screen.fill(GREY)
	# SysText(level=level_number).draw()
	# BATTLE_POLE = draw.rect(screen, BLACK, (SPAWN_POLE[0], SPAWN_POLE[1], WIDTH_POLE, HEIGHT_POLE))
	enemys_list_for_spawner["list"] = ENEMYLIST_local.get_list()
	# return ENEMYLIST.get_list()

	# return enemys_list_for_spawner["list"]
	return level_number["g"]



NEXT_TIME = False



# Скорость движения серого экрана
SPEED_MOVE_GREY_SCREENS = 17

grey_screens_sprites = pygame.sprite.Group()


class GreyScreen(pygame.sprite.Sprite):
	def __init__(self, pos, state, move_type, img_path='%s/gui/battle/grey_screen.png'):
		pygame.sprite.Sprite.__init__(self)
		if BATTLE_BG_COLOR == GREY:
			img_path = "%s/gui/battle/grey_screen_default.png"
		try:
			self.image = image.load(img_path % (LOAD_TEXTURES))
		except Exception:
			self.image = image.load(img_path % (DEFAULT_TEXTURES))

		self.move_type = move_type

		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]

		self.state = state

		self.speed_now = SPEED_MOVE_GREY_SCREENS
		self.speed_now_back = SPEED_MOVE_GREY_SCREENS

	def update(self):
		if self.move_type == 1:
			if self.state == "top":
				self.rect.y += self.speed_now

				if self.rect.y > -50: # -50:
					self.speed_now = 0

			if self.state == "down":
				self.rect.y -= self.speed_now

				if self.rect.y < HEIGHT//2: # HEIGHT//2:
					self.speed_now = 0

		if self.move_type == 2:
			# print('LLL')
			if self.state == "top":
				self.rect.y -= self.speed_now_back

				if self.rect.y < -400: 
					self.speed_now_back = 0

			if self.state == "down":
				self.rect.y += self.speed_now_back

				if self.rect.y >= HEIGHT:
					self.speed_now_back = 0


	def return_true_for_end_move2(self):
		"""Возвращает True если спрайты закончили движение"""
		if self.speed_now_back == 0:
			return True
		else:
			return False


			
				



def CreateGreyScreens():
	grey_screen_top = GreyScreen((0, -400), "top", 1)
	grey_screen_down = GreyScreen((0, HEIGHT), "down", 1)


	grey_screens_sprites.add(grey_screen_top)
	grey_screens_sprites.add(grey_screen_down)

	return grey_screen_top, grey_screen_down


grey_screen_top, grey_screen_down = CreateGreyScreens()

TIMER_REPLACE_MOVETYPE_GREYS = 230
timer_replace_movetype_greys = 0









######## СПРАЙТЫ ДЛЯ ГЛАВНОГО МЕНЮ #########

def EMPTY_ALL_SPRITES():	
	all_sprites.empty()
	player_sprites.empty()
	count_kill_enemy_sprites.empty()
	player_bonuses_sprites.empty()
	flag_panel_sprites.empty()
	gameover_sprites.empty()
	pause_sprites.empty()
	level_panel_sprites.empty()
	respawn_count_sprites.empty()
	enemys_spawn_animation_sprites.empty()
	enemys_sprites.empty()
	sysinfo_game_sprites.empty()
	walls_sprites.empty()
	beton_sprites.empty()
	bush_sprites.empty()
	water_sprites.empty()
	base_sprites.empty()
	bonuses_sprites.empty()
	beton_shovel_sprites.empty()
	panel_tanks_sprites.empty()
	walls_sprites.empty()
	bullets.empty()
	bullets_enemy.empty()
	explosions.empty()
	ice_sprites.empty()
	rockets_sprites.empty()
	# menu_content_sprites.empty()

	# if TYPE_RIGHT_INTERFACE == 2:
	rocket_counter_panel_sprites.empty()

	CHANNEL_enemy_move.stop()
	CHANNEL_player_move.stop()
	CHANNEL_bullet_collide_tank.stop()
	CHANNEL_bullet_collide_wall.stop()
	CHANNEL_shot_tanks.stop()
	CHANNEL_kill_enemy.stop()
	CHANNEL_bullet_collide_wall.stop()
	# MUSIC_pause_get.stop()



class Button(pygame.sprite.Sprite):
	def __init__(self, pos, text="Test", font_name="2003.ttf", font_size=29, fg=BLACK, font=battlecity_font, fon_image='%s/gui/menu/test_btn.png', press_fon_image='%s/gui/menu/test_btn_press.png', focus_fon_image='%s/gui/menu/test_btn_focus.png'):
		pygame.sprite.Sprite.__init__(self)

		self.images = []

		try:
			self.images.append((image.load(fon_image % (LOAD_TEXTURES))))
		except Exception:
			self.images.append((image.load(fon_image % (DEFAULT_TEXTURES))))

		try:
			self.images.append((image.load(press_fon_image % (LOAD_TEXTURES))))
		except Exception:
			self.images.append((image.load(press_fon_image % (DEFAULT_TEXTURES))))

		try:
			self.images.append((image.load(focus_fon_image % (LOAD_TEXTURES))))
		except Exception:
			self.images.append((image.load(focus_fon_image % (DEFAULT_TEXTURES))))

		self.index = 0
		self.image = self.images[self.index]

		self.rect = self.image.get_rect()

		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.font = pygame.font.Font('data\\fonts\\'+font_name, font_size)
		self.font_size = font_size
		self.text = text
		self.fg = fg

	def update(self):
		pressed = pygame.mouse.get_pressed()
		pos = pygame.mouse.get_pos()
		
		if pressed[0] and (self.rect.x < pos[0] < self.rect.x+self.image.get_width()) and (self.rect.y < pos[1] < self.rect.y+self.image.get_height()):
			# print(pos)
			self.index = 1
		elif (self.rect.x < pos[0] < self.rect.x+self.image.get_width()) and (self.rect.y < pos[1] < self.rect.y+self.image.get_height()):
			self.index = 2
		else:
			self.index = 0

		FON_TEXT = self.image.get_at((15, 15))

		
		text_screen = self.font.render(self.text, 0, self.fg, FON_TEXT)

		# (screen).blit(text_screen, (self.rect.x+4, self.rect.y+4))
		(screen).blit(text_screen, (self.rect.center[0]-text_screen.get_width()//2, self.rect.center[1]-text_screen.get_height()//2))


		self.image = self.images[self.index]






class SmallTankMenu(pygame.sprite.Sprite):
	def __init__(self, pos, lvl_tank=1):
		pygame.sprite.Sprite.__init__(self)

		self.images = []
		self.type_player = "player"
		self.lvl_tank = lvl_tank

		try:			
			self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))
		except Exception:
			self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a1_r4.png'))

		try:			
			self.images.append(image.load(ALL_TEXTURES_TANKS+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))
		except Exception:
			self.images.append(image.load(DEFAULT_TEXTURES+"tanks/"+self.type_player+f'/lvl{self.lvl_tank}_a2_r4.png'))

		self.index = 0

		self.image = self.images[self.index]

		self.rect = self.image.get_rect()

		self.rect.x = pos[0]
		self.rect.y = pos[1]

		self.counter = 0
		
		self.border_animation = 1
		self.index_border_animation = 0

	def update(self):
		# if self.index == 0:
		# 	self.index = 1
		# else:
		# 	self.index = 0
		self.counter += 1


		if self.counter >= 3:
				self.index += 1
				self.counter = 0
				if self.index > self.border_animation:
					self.index = self.index_border_animation


		self.image = self.images[self.index]


class LinkTextButton:
	def __init__(self, pos, text="www.example.com", link="www.example.com", font=pygame.font.Font('data\\fonts\\calibri.ttf', 22), font_name="2003.ttf", fg_focus=(0, 143, 255), bg_focus=BLACK, bg=BLACK, fg=(0, 100, 220)):

		self.font = font
		self.link = link
		self.text = text
		self.fg = fg
		self.bg = bg

		self.font_name = font_name

		self.fg_focus = fg_focus
		self.bg_focus = bg_focus

		self.fg_default = self.fg
		self.bg_default = self.bg
		
		self.pos = pos




		self.button_state = 0	

		self.text_screen = self.font.render(self.text, 0, self.fg, self.bg)
		self.text_screen.set_colorkey((0, 0, 0))

		if self.pos[0] == "cx":
			self.pos[0] = WIDTH//2 - self.text_screen.get_width()//2

		if self.pos[1] == "cy":
			self.pos[1] = HEIGHT//2 - self.text_screen.get_height()//2


		self.posx = pos[0]
		self.posy = pos[1]

		self.start_x = self.posx
		self.start_y = self.posy


		self.counter_click = 0




	def draw(self):
		pressed = pygame.mouse.get_pressed()
		pos = pygame.mouse.get_pos()

		
		if pressed[0] and (self.posx < pos[0] < self.posx+self.text_screen.get_width()) and (self.posy < pos[1] < self.posy+self.text_screen.get_height()):
			self.button_state = 1
		elif (self.posx < pos[0] < self.posx+self.text_screen.get_width()) and (self.posy < pos[1] < self.posy+self.text_screen.get_height()):
			self.button_state = 2
		else:	
			self.button_state = 0

		
		# print(self.button_state)
		if self.button_state == 1:
			self.posx += 1
			self.posy += 1
			if self.counter_click == 0:
				webbrowser.open_new_tab(self.link)
			self.counter_click = 1
		
		# if self.button_state in [0, 2]:
		# 	self.counter_click = 0


		if self.button_state == 2:
			# menu_tank.rect.y = self.posy - 3	
			self.fg = self.fg_focus
			self.bg = self.bg_focus
			self.counter_click = 0

		
		if self.button_state == 0:
			self.fg = self.fg_default
			self.bg = self.bg_default
			self.counter_click = 0


		self.text_screen = self.font.render(self.text, 0, self.fg, self.bg)
		self.text_screen.set_colorkey((0, 0, 0))

		(screen).blit(self.text_screen, (self.posx, self.posy))

		self.posx = self.start_x
		self.posy = self.start_y

	def get_height(self):
		return self.text_screen.get_height()

	def get_width(self):
		return self.text_screen.get_width()

	def update_pos(self, new_pos): ############# ДОБАВЬ ОБРАБОТКУ КООРДИНАТ №№№№№№№№№№№№№№№
		# self.label = self.font.render(self.text, 0, self.fg, self.bg)

		self.pos = new_pos
		
		self.text_screen = self.font.render(self.text, 0, self.fg, self.bg)
		self.text_screen.set_colorkey((0, 0, 0))

		if self.pos[0] == "cx":
			self.pos[0] = WIDTH//2 - self.text_screen.get_width()//2

		if self.pos[1] == "cy":
			self.pos[1] = HEIGHT//2 - self.text_screen.get_height()//2


		self.posx = self.pos[0]
		self.posy = self.pos[1]

		self.start_x = self.posx
		self.start_y = self.posy

		# (screen).blit(self.text_screen, (self.posx, self.posy))

	def update_coords(self):
		"""Обновляет координаты кнопки в соответствии с новым текстом"""
		self.text_screen = self.font.render(self.text, 0, self.fg, self.bg)
		self.text_screen.set_colorkey((0, 0, 0))

		if self.pos[0] == "cx":
			self.pos[0] = WIDTH//2 - self.text_screen.get_width()//2

		if self.pos[1] == "cy":
			self.pos[1] = HEIGHT//2 - self.text_screen.get_height()//2


		self.posx = self.pos[0]
		self.posy = self.pos[1]

		self.start_x = self.posx
		self.start_y = self.posy






class TextButton:
	def __init__(self, pos, text="Test", font_name="2003.ttf", font_size=29, fg_focus=WHITE, bg_focus=YELLOW_COUNT, bg=BLACK, fg=WHITE, font=battlecity_font, command=lambda: print("Test"), set_small_tank=False):

		self.font = pygame.font.Font('data\\fonts\\'+font_name, font_size)
		self.font_size = font_size
		self.text = text
		self.fg = fg
		self.bg = bg

		self.font_name = font_name

		self.fg_focus = fg_focus
		self.bg_focus = bg_focus

		self.fg_default = self.fg
		self.bg_default = self.bg
		
		self.pos = pos




		self.button_state = 0


		self.command = command
		self.set_small_tank = set_small_tank

		

		self.text_screen = self.font.render(self.text, 0, self.fg, self.bg)
		self.text_screen.set_colorkey((0, 0, 0))

		if self.pos[0] == "cx":
			self.pos[0] = WIDTH//2 - self.text_screen.get_width()//2

		if self.pos[1] == "cy":
			self.pos[1] = HEIGHT//2 - self.text_screen.get_height()//2


		self.posx = pos[0]
		self.posy = pos[1]

		self.start_x = self.posx
		self.start_y = self.posy


		self.counter_click = 0

	def draw(self):
		pressed = pygame.mouse.get_pressed()
		pos = pygame.mouse.get_pos()

		
		if pressed[0] and (self.posx < pos[0] < self.posx+self.text_screen.get_width()) and (self.posy < pos[1] < self.posy+self.text_screen.get_height()):
			self.button_state = 1
		elif (self.posx < pos[0] < self.posx+self.text_screen.get_width()) and (self.posy < pos[1] < self.posy+self.text_screen.get_height()):
			self.button_state = 2
		else:	
			self.button_state = 0

		
		# print(self.button_state)
		if self.button_state == 1:
			self.posx += 1
			self.posy += 1
			if self.counter_click == 0:
				self.command()				
			self.counter_click = 1
		
		# if self.button_state in [0, 2]:
		# 	self.counter_click = 0


		if self.button_state == 2:
			# menu_tank.rect.y = self.posy - 3	
			self.fg = self.fg_focus
			self.bg = self.bg_focus
			self.counter_click = 0

		
		if self.button_state == 0:
			self.fg = self.fg_default
			self.bg = self.bg_default
			self.counter_click = 0


		self.text_screen = self.font.render(self.text, 0, self.fg, self.bg)
		self.text_screen.set_colorkey((0, 0, 0))

		(screen).blit(self.text_screen, (self.posx, self.posy))

		self.posx = self.start_x
		self.posy = self.start_y


	def update(self):
		pressed = pygame.mouse.get_pressed()
		pos = pygame.mouse.get_pos()

		
		if pressed[0] and (self.posx < pos[0] < self.posx+self.text_screen.get_width()) and (self.posy < pos[1] < self.posy+self.text_screen.get_height()):
			self.button_state = 1
		elif (self.posx < pos[0] < self.posx+self.text_screen.get_width()) and (self.posy < pos[1] < self.posy+self.text_screen.get_height()):
			self.button_state = 2
		else:	
			self.button_state = 0

		
		# print(self.button_state)
		if self.button_state == 1:
			self.posx += 1
			self.posy += 1
			if self.counter_click == 0:
				self.command()
			self.counter_click = 1
		
		# if self.button_state in [0, 2]:
		# 	self.counter_click = 0

		if self.button_state == 2 and self.set_small_tank==True:
			menu_tank.rect.y = self.posy - 3
			# self.fg = YELLOW
			self.counter_click = 0

		if self.button_state == 2 and self.set_small_tank==False:
			# menu_tank.rect.y = self.posy - 3	
			self.fg = self.fg_focus
			self.bg = self.bg_focus
			self.counter_click = 0

		
		if self.button_state == 0 and self.set_small_tank==False:
			self.fg = self.fg_default
			self.bg = self.bg_default
			self.counter_click = 0


		self.text_screen = self.font.render(self.text, 0, self.fg, self.bg)
		self.text_screen.set_colorkey((0, 0, 0))

		(screen).blit(self.text_screen, (self.posx, self.posy))

		self.posx = self.start_x
		self.posy = self.start_y

	def get_height(self):
		return self.text_screen.get_height()

	def get_width(self):
		return self.text_screen.get_width()

	def update_coords(self):
		"""Обновляет координаты кнопки в соответствии с новым текстом"""
		self.text_screen = self.font.render(self.text, 0, self.fg, self.bg)
		self.text_screen.set_colorkey((0, 0, 0))

		if self.pos[0] == "cx":
			self.pos[0] = WIDTH//2 - self.text_screen.get_width()//2

		if self.pos[1] == "cy":
			self.pos[1] = HEIGHT//2 - self.text_screen.get_height()//2


		self.posx = self.pos[0]
		self.posy = self.pos[1]

		self.start_x = self.posx
		self.start_y = self.posy

	def update_pos(self, new_pos): ############# ДОБАВЬ ОБРАБОТКУ КООРДИНАТ №№№№№№№№№№№№№№№
		# self.label = self.font.render(self.text, 0, self.fg, self.bg)

		self.pos = new_pos
		
		self.text_screen = self.font.render(self.text, 0, self.fg, self.bg)
		self.text_screen.set_colorkey((0, 0, 0))

		if self.pos[0] == "cx":
			self.pos[0] = WIDTH//2 - self.text_screen.get_width()//2

		if self.pos[1] == "cy":
			self.pos[1] = HEIGHT//2 - self.text_screen.get_height()//2


		self.posx = self.pos[0]
		self.posy = self.pos[1]

		self.start_x = self.posx
		self.start_y = self.posy

		# (screen).blit(self.text_screen, (self.posx, self.posy))

	def update_all_params(self):
		"""Обновляет ВСЕ параметры кнопки"""
		pass

	def check_focus(self):
		"""Возвращает True если курсор наведен на эту кнопку"""
		if self.button_state in [1, 2]:
			return True
		else:
			return False








class TITLE_MENU(pygame.sprite.Sprite):
	def __init__(self, pos=(84, 120), path_image='%s/gui/title_menu.png'):
		pygame.sprite.Sprite.__init__(self)

		try:
			self.image = (image.load(path_image % (LOAD_TEXTURES))).convert()
		except Exception:
			self.image = (image.load(path_image % (DEFAULT_TEXTURES))).convert()

		self.rect = self.image.get_rect()

		# self.rect.center = pos
		self.end_coord = pos

		# self.rect.x = 84
		# self.rect.y = HEIGHT+5

		# self.rect.x = pos[0]
		# self.rect.y = pos[1]

		self.rect.x = WIDTH//2 - self.image.get_width()//2
		self.rect.y = pos[1]

	def update(self):
		pass
		# if self.rect.y >= self.end_coord[1]:
		# 	self.rect.y -= SPEED_MOVE_GAMEOVER*2
		# else:
		# 	self.rect.y = self.rect.y








class BG_MENU(pygame.sprite.Sprite):
	def __init__(self, pos=(0, 0), path_image='%s/gui/2MenuBG.png'):
		pygame.sprite.Sprite.__init__(self)

		try:
			self.image = (image.load(path_image % (LOAD_TEXTURES))).convert()
		except Exception:
			self.image = (image.load(path_image % (DEFAULT_TEXTURES))).convert()

		self.rect = self.image.get_rect()

		# self.rect.center = pos
		self.end_coord = pos

		# self.rect.x = 84
		# self.rect.y = HEIGHT+5

		self.rect.x = pos[0]
		self.rect.y = pos[1]

	def update(self):
		pass
		# if self.rect.y >= self.end_coord[1]:
		# 	self.rect.y -= SPEED_MOVE_GAMEOVER*2
		# else:
		# 	self.rect.y = self.rect.y






def set_slide_battle():
	player_sprites.empty()
	dict_RUN_SLIDE_NOW["g"]=5
	zero_counts()
	clear_player1_bonus()
	# ReloadBattle(level_number)

buttons_list = []
def update_buttons():
	for e in buttons_list:
		e.update()


def set_center_btn(sprite):
	"""Oстановить кнопку по центру"""
	# sprite.posx = WIDTH-sprite.get_width()//2
	pass


def set_slide_number(num):
	player_sprites.empty()
	dict_RUN_SLIDE_NOW["g"]=num
	zero_counts()
	clear_player1_bonus()
	# CLEAR_ALL()



menu_content_sprites = pygame.sprite.Group()
title_menu_sprite = TITLE_MENU((84, 80))

# try:
# 	bg_image = (image.load('%s/gui/3MenuBG.png' % (LOAD_TEXTURES)))
# except Exception:
# 	bg_image = (image.load('%s/gui/3MenuBG.png' % (DEFAULT_TEXTURES)))

x2020 = 265
y2020 = 176



# background_menu = BG_MENU()

# menu_content_sprites.add(background_menu)






menu_content_sprites.add(title_menu_sprite)
# Откуда начинать расстановку кнопочек
menu_start_y = 360

# Размер отступа между кнопками
intedent_btn = 15

# Шрифт надписи на кнопке
font_size_btn = 29

menu_tank = SmallTankMenu((230, menu_start_y-3), lvl_tank=1)
menu_content_sprites.add(menu_tank)

# MENU_BUTTONS BUTTONS_MENU

# player1 = TextButton(pos=(280, menu_start_y), text="play"+24*" ", font_size=font_size_btn, command=lambda: set_slide_battle(), fg=YELLOW, set_small_tank=True)
player1 = TextButton(pos=(280, menu_start_y), text="play"+24*" ", font_size=font_size_btn, command=lambda: set_slide_number(8), fg=YELLOW, set_small_tank=True)
set_center_btn(player1)
buttons_list.append(player1)


# menu_start_y += player1.get_height() + intedent_btn
# shop = TextButton(pos=(280, menu_start_y), text="shop"+24*" ", font_size=font_size_btn, set_small_tank=True) #, fg=(107,63,127))
# set_center_btn(shop)
# buttons_list.append(shop)


menu_start_y += player1.get_height() + intedent_btn
construction = TextButton(pos=(280, menu_start_y), text="construction"+24*" ", font_size=font_size_btn, fg=GREEN2, command=lambda: set_slide_number(6), set_small_tank=True)
set_center_btn(construction)
buttons_list.append(construction)

menu_start_y += player1.get_height() + intedent_btn
settings = TextButton(pos=(280, menu_start_y), text="about project"+24*" ", font_size=font_size_btn, set_small_tank=True, command=lambda: set_slide_number(10))
set_center_btn(settings)
buttons_list.append(settings)


menu_start_y += player1.get_height() + intedent_btn
quit_windows = TextButton(pos=(280, menu_start_y), text="Exit Windows"+24*" ", font_size=font_size_btn, command=lambda: sys.exit(), fg=RED_COUNT, set_small_tank=True)
set_center_btn(quit_windows)
buttons_list.append(quit_windows)


menu_start_y += player1.get_height() + intedent_btn*3
place_author_x = 160
author_text = battlecity_font.render("© tankalxat34 - 2021", 0, WHITE, BLACK)
author_text.set_colorkey((0, 0, 0))


battlecity_font2 = pygame.font.Font('data\\fonts\\2003.ttf', 70)
text2020 = battlecity_font2.render("20.20", 0, WHITE, BLACK)
text2020.set_colorkey((0, 0, 0))




c_now_x = SPAWN_POLE[0]
list_normal_coords_x = []

list_normal_coords_x.append(c_now_x)


c_now_y = SPAWN_POLE[1]
list_normal_coords_y = []

list_normal_coords_y.append(c_now_y)

how_much_sum = 48

for i in range(13):
	c_now_x += how_much_sum
	list_normal_coords_x.append(c_now_x)

for i in range(13):
	c_now_y += how_much_sum
	list_normal_coords_y.append(c_now_y)








class MapObjectButton:
	def __init__(self, pos=(0, 0), type=1):
		self.pos = pos
		self.posx = pos[0]
		self.posy = pos[1]


		self.type = type
		self.blit_in_mouse = False

		# self.list_parts_block = []
		# self.index = 0
		self.simvol = ""

		if self.type == 1:	
			try:
				self.block = image.load(LOAD_TEXTURES + "/map_objects/blocks/const/brick_full.png")
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(LOAD_TEXTURES + "/map_objects/blocks/const/brick_full.png")


			except Exception:
				self.block = image.load(DEFAULT_TEXTURES + "/map_objects/blocks/const/brick_full.png")
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(DEFAULT_TEXTURES + "/map_objects/blocks/const/brick_full.png")

		elif self.type in [2, 3, 4, 5]:	
			

			try:
				self.block = image.load(LOAD_TEXTURES + "/map_objects/blocks/const/brick%s.png" % str(self.type-1))
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(LOAD_TEXTURES + "/map_objects/blocks/const/brick%s.png" % str(self.type-1))

			except Exception:
				self.block = image.load(DEFAULT_TEXTURES + "/map_objects/blocks/const/brick%s.png" % str(self.type-1))
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(DEFAULT_TEXTURES + "/map_objects/blocks/const/brick%s.png" % str(self.type-1))

		# ("=", "\\", "-", "_", "/", "#", "[", "'", ",", "]", "*", "w")
		elif self.type == 6:	
			try:
				self.block = image.load(LOAD_TEXTURES + "/map_objects/blocks/const/beton_full.png")
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(LOAD_TEXTURES + "/map_objects/blocks/const/beton_full.png")

			except Exception:
				self.block = image.load(DEFAULT_TEXTURES + "/map_objects/blocks/const/beton_full.png")
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(DEFAULT_TEXTURES + "/map_objects/blocks/const/beton_full.png")

		elif self.type in [7, 8, 9, 10]:	
			try:
				self.block = image.load(LOAD_TEXTURES + "/map_objects/blocks/const/beton%s.png" % str(self.type-6))
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(LOAD_TEXTURES + "/map_objects/blocks/const/beton%s.png" % str(self.type-6))

			except Exception:
				self.block = image.load(DEFAULT_TEXTURES + "/map_objects/blocks/const/beton%s.png" % str(self.type-6))
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(DEFAULT_TEXTURES + "/map_objects/blocks/const/beton%s.png" % str(self.type-6))

		elif self.type == 11:	
			try:
				self.block = image.load(LOAD_TEXTURES + "/map_objects/bush.png")
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(LOAD_TEXTURES + "/map_objects/bush.png")

			except Exception:
				self.block = image.load(DEFAULT_TEXTURES + "/map_objects/bush.png")
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(DEFAULT_TEXTURES + "/map_objects/bush.png")

		elif self.type == 12:	
			try:
				self.block = image.load(LOAD_TEXTURES + "/map_objects/water_a2.png")
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(LOAD_TEXTURES + "/map_objects/water_a2.png")

			except Exception:
				self.block = image.load(DEFAULT_TEXTURES + "/map_objects/water_a2.png")
				# self.list_parts_block.append(first_brick)
				self.block_mouse = image.load(DEFAULT_TEXTURES + "/map_objects/water_a2.png")




		self.list_coord = []

		self.set_x_coord = 0
		self.set_y_coord = 0

		

		


	def update(self):
		screen.blit(self.block, self.pos)

		pressed = pygame.mouse.get_pressed()
		pos_mouse = pygame.mouse.get_pos()



		if pressed[0] and (self.posx < pos_mouse[0] < self.posx+self.block.get_width()) and (self.posy < pos_mouse[1] < self.posy+self.block.get_height()):
			self.button_state = 1
		elif (self.posx < pos_mouse[0] < self.posx+self.block.get_width()) and (self.posy < pos_mouse[1] < self.posy+self.block.get_height()):
			self.button_state = 2
		else:	
			self.button_state = 0

		# print(self.button_state)

		if self.button_state == 2:
			self.block.set_alpha(190)
			if get_mouse_any_block():
				self.blit_in_mouse = False

		elif self.button_state == 0:
			self.block.set_alpha(255)

		elif self.button_state == 1:
			self.blit_in_mouse = True
		
		if self.blit_in_mouse:
			self.block_mouse.set_alpha(180)
			screen.blit(self.block_mouse, (pos_mouse[0]-24, pos_mouse[1]-24))

		
		#  (250, 665, 320, 75)
		if PARAMS_RECT_DESTROY_MOUSE_CONST[0] < pos_mouse[0] < PARAMS_RECT_DESTROY_MOUSE_CONST[0]+PARAMS_RECT_DESTROY_MOUSE_CONST[2] and PARAMS_RECT_DESTROY_MOUSE_CONST[1] < pos_mouse[1] < PARAMS_RECT_DESTROY_MOUSE_CONST[1]+PARAMS_RECT_DESTROY_MOUSE_CONST[3]:
			# screen.blit(self.block_mouse, [-100, -100])
			self.blit_in_mouse = False


		if pressed[2] or pressed[0]:
			if SPAWN_POLE[0] < pos_mouse[0] < SPAWN_POLE[0]+WIDTH_POLE and SPAWN_POLE[1] < pos_mouse[1] < SPAWN_POLE[1]+HEIGHT_POLE and len(self.list_coord)<=GET_LIST_LEN() and GET_LIST_LEN()<=13**2:
				# self.list_coord.append((pos_mouse[0]-24, pos_mouse[1]-24))
				
				# высчитываем координату по x
				for i in range(len(list_normal_coords_x)-1):
					if list_normal_coords_x[i] <= pos_mouse[0] <= list_normal_coords_x[i+1]:
						# set_block_coord.append(list_normal_coords_x[i])
						self.set_x_coord = list_normal_coords_x[i]

				# высчитываем координату по y
				for i in range(len(list_normal_coords_y)-1):
					if list_normal_coords_y[i] <= pos_mouse[1] <= list_normal_coords_y[i+1]:
						# set_block_coord.append(list_normal_coords_y[i])
						self.set_y_coord = list_normal_coords_y[i]

				try:
					self.list_coord.remove((self.set_x_coord, self.set_y_coord))

					brick_full_list = brick_full_button.get_list_coord_block()
					brick_list = brick_button.get_list_coord_block()
					brick_list2 = brick_button2.get_list_coord_block()
					brick_list3 = brick_button3.get_list_coord_block()
					brick_list4 = brick_button4.get_list_coord_block()
					beton_list = beton_button.get_list_coord_block()
					beton_list1 = beton_button1.get_list_coord_block()
					beton_list2 = beton_button2.get_list_coord_block()
					beton_list3 = beton_button3.get_list_coord_block()
					beton_list4 = beton_button4.get_list_coord_block()
					bush_list = bush_button.get_list_coord_block()
					water_list = water_button.get_list_coord_block()

					brick_full_list.sort()
					brick_list.sort()
					brick_list2.sort()
					brick_list3.sort()
					brick_list4.sort()
					beton_list.sort()
					beton_list1.sort()
					beton_list2.sort()
					beton_list3.sort()
					beton_list4.sort()
					bush_list.sort()
					water_list.sort()

					brick_full_list.remove((self.set_x_coord, self.set_y_coord))
					brick_list.remove((self.set_x_coord, self.set_y_coord))
					brick_list2.remove((self.set_x_coord, self.set_y_coord))
					brick_list3.remove((self.set_x_coord, self.set_y_coord))
					brick_list4.remove((self.set_x_coord, self.set_y_coord))
					beton_list.remove((self.set_x_coord, self.set_y_coord))
					beton_list1.remove((self.set_x_coord, self.set_y_coord))
					beton_list2.remove((self.set_x_coord, self.set_y_coord))
					beton_list3.remove((self.set_x_coord, self.set_y_coord))
					beton_list4.remove((self.set_x_coord, self.set_y_coord))
					bush_list.remove((self.set_x_coord, self.set_y_coord))
					water_list.remove((self.set_x_coord, self.set_y_coord))

				except Exception:
					pass



		if pressed[0] and self.blit_in_mouse:
			if SPAWN_POLE[0] < pos_mouse[0] < SPAWN_POLE[0]+WIDTH_POLE and SPAWN_POLE[1] < pos_mouse[1] < SPAWN_POLE[1]+HEIGHT_POLE and len(self.list_coord)<=GET_LIST_LEN() and GET_LIST_LEN()<=13**2:
					

				# высчитываем координату по x
				for i in range(len(list_normal_coords_x)-1):
					if list_normal_coords_x[i] <= pos_mouse[0] <= list_normal_coords_x[i+1]:
						# set_block_coord.append(list_normal_coords_x[i])
						self.set_x_coord = list_normal_coords_x[i]

				# высчитываем координату по y
				for i in range(len(list_normal_coords_y)-1):
					if list_normal_coords_y[i] <= pos_mouse[1] <= list_normal_coords_y[i+1]:
						# set_block_coord.append(list_normal_coords_y[i])
						self.set_y_coord = list_normal_coords_y[i]

				if (self.set_x_coord, self.set_y_coord) not in self.list_coord and (self.set_x_coord, self.set_y_coord) not in CONST_COORD_EXCEPTIONS:
					self.list_coord.append((self.set_x_coord, self.set_y_coord))




		


		for e in self.list_coord:
			self.block_mouse.set_alpha(255)
			screen.blit(self.block_mouse, e)

		self.set_x_coord = 0
		self.set_y_coord = 0


	def set_block(self, pos):
		"""Установить блок данного типа на позицию pos. Возвращает True если установлен успешно, иначе False"""
		try:
			self.list_coord.append(pos)
			return True
		except Exception:
			return False
		


	def set_mouse_block(self):
		"""Устанавливает на курсор данный блок"""
		self.blit_in_mouse = True

	def del_mouse_block(self):
		"""Удалает на курсоре данный блок"""
		self.blit_in_mouse = False

	def get_mouse_block(self):
		"""Возращает True если на курсоре есть данный блок. False если блока нет"""
		return self.blit_in_mouse




	def clear_coords(self):
		"""Очищает все блоки данного типа на карте"""
		return self.list_coord.clear()

	def get_list_len(self):
		"""Возвращает количество блоков данного типа на карте"""
		return len(self.list_coord)

	def get_check_block_in_coord(self):
		"""Возвращает True если блок данного типа уже находится в этих координатах"""
		my_list = (self.set_x_coord, self.set_y_coord)
		if my_list in self.list_coord:
			return 1
		else:
			return 0

	def get_list_coord_block(self):
		"""Возвращает список координат, где находится данный блок. Возвращаются координаты левого верхнего угла."""
		return self.list_coord




def CHECK_BLOCK_IN_COORD():
	"""Есть ли какой нибудь блок в данных координатах"""
	if brick_full_button.get_check_block_in_coord() + brick_button.get_check_block_in_coord() + brick_button2.get_check_block_in_coord() + brick_button3.get_check_block_in_coord() + brick_button4.get_check_block_in_coord() +	beton_button.get_check_block_in_coord() +	beton_button1.get_check_block_in_coord() + beton_button2.get_check_block_in_coord() + beton_button3.get_check_block_in_coord() + beton_button4.get_check_block_in_coord() + bush_button.get_check_block_in_coord() + water_button.get_check_block_in_coord() >= 1:
		return True
	elif brick_full_button.get_check_block_in_coord() + brick_button.get_check_block_in_coord() + brick_button2.get_check_block_in_coord() + brick_button3.get_check_block_in_coord() + brick_button4.get_check_block_in_coord() +	beton_button.get_check_block_in_coord() +	beton_button1.get_check_block_in_coord() + beton_button2.get_check_block_in_coord() + beton_button3.get_check_block_in_coord() + beton_button4.get_check_block_in_coord() + bush_button.get_check_block_in_coord() + water_button.get_check_block_in_coord() == 0:
		return False


		
def GET_LIST_LEN():
	all_len = brick_full_button.get_list_len()+brick_button.get_list_len()+brick_button2.get_list_len()+brick_button3.get_list_len()+brick_button4.get_list_len()+beton_button.get_list_len()+beton_button1.get_list_len()+beton_button2.get_list_len()+beton_button3.get_list_len()+beton_button4.get_list_len()+bush_button.get_list_len()+water_button.get_list_len()
	return all_len



dict_RANDOM_MOUSE_BLOCK = dict()
dict_RANDOM_MOUSE_BLOCK["g"] = False
dict_RANDOM_MOUSE_BLOCK["counter"] = 0

def VIEW_RANDOM_BLOCK():
	# if dict_RANDOM_MOUSE_BLOCK["g"]:
	RANDOM_BLOCK()

	

def RANDOM_BLOCK():
	a = []
	a.append(brick_full_button)
	a.append(brick_button)
	a.append(brick_button2)
	a.append(brick_button3)
	a.append(brick_button4)
	a.append(beton_button)
	a.append(beton_button1)
	a.append(beton_button2)
	a.append(beton_button3)
	a.append(beton_button4)
	a.append(bush_button)
	a.append(water_button)

	for e in a:
		e.del_mouse_block()

	random.choice(a).set_mouse_block()


















def CLEAR_ALL():
	brick_full_button.clear_coords()
	brick_button.clear_coords()
	brick_button2.clear_coords()
	brick_button3.clear_coords()
	brick_button4.clear_coords()
	beton_button.clear_coords()
	beton_button1.clear_coords()
	beton_button2.clear_coords()
	beton_button3.clear_coords()
	beton_button4.clear_coords()
	bush_button.clear_coords()
	water_button.clear_coords()
	dict_level_loaded_status["g"] = False



## Я НАКОНЕЦ ТО СДЕЛАЛ КЛАСС ДЛЯ НАДПИСИ
class Label:
	def __init__(self, pos, text="test", font=pygame.font.Font('data\\fonts\\2003.ttf', 45), bg=BLACK, fg=WHITE, colorkey_fg=True):

		self.font = font
		self.text = text
		self.pos = pos
		self.bg = bg
		self.fg = fg
		self.colorkey_fg = colorkey_fg

		self.label = self.font.render(self.text, 0, self.fg, self.bg)
		if self.pos[1] == "cy":
			self.pos[1] = HEIGHT//2 - self.label.get_height()//2

		if self.pos[0] == "cx":
			self.pos[0] = WIDTH//2 - self.label.get_width()//2
		
		if self.colorkey_fg:
			self.label.set_colorkey(self.bg)



	def draw(self):
		(screen).blit(self.label, self.pos)

	def get_surface(self):
		return self.label

	def set_text(self, new_text):
		self.text = new_text
		self.label = self.font.render(self.text, 0, self.fg, self.bg)
		if self.colorkey_fg:
			self.label.set_colorkey(self.bg)

	def update_pos(self, new_pos): ############# ДОБАВЬ ОБРАБОТКУ КООРДИНАТ №№№№№№№№№№№№№№№
		self.label = self.font.render(self.text, 0, self.fg, self.bg)

		self.pos = new_pos

		if self.pos[1] == "cy":
			self.pos[1] = HEIGHT//2 - self.label.get_height()//2

		if self.pos[0] == "cx":
			self.pos[0] = WIDTH//2 - self.label.get_width()//2


	def set_fg(self, new_fg):
		self.fg = new_fg
		self.label = self.font.render(self.text, 0, self.fg, self.bg)







class ImageButton:
	def __init__(self, pos, img_path, command=lambda: print("Test"), focus_image_path=False, second_image=False, text_coord=False, text_in_image=False, font_size=30):
		self.pos = pos

		self.command = command
		self.focus_image_path = focus_image_path
		self.second_image = second_image

		self.counter_click = 0
		self.text_coord = text_coord
		self.text_in_image = text_in_image
		self.font_size = font_size
		

		if img_path.split("/")[0] != "dlc":
			try:
				self.img = image.load(LOAD_TEXTURES + img_path)
			except Exception:
				self.img = image.load(DEFAULT_TEXTURES + img_path)
		else:
			try:
				self.img = image.load(img_path)
			except Exception:
				self.img = image.load(campaign_no_icon)



		if self.focus_image_path:
			try:
				self.img_focus = image.load(LOAD_TEXTURES + self.focus_image_path)
			except Exception:
				self.img_focus = image.load(DEFAULT_TEXTURES + self.focus_image_path)

		if self.second_image:
			try:
				self.img_second = image.load(LOAD_TEXTURES + self.second_image)
			except Exception:
				self.img_second = image.load(DEFAULT_TEXTURES + self.second_image)

		if self.text_in_image:
			if self.text_coord: 
				if "c" in self.text_coord:
					self.text_in_image = self.text_in_image.replace(".bslvl", "")
					self.text_in_image = self.text_in_image.replace("0", "")
					self.label = Label(pos=(self.pos[0] + self.img.get_width()//2, self.pos[1] + self.img.get_height()//4), text=self.text_in_image, font=pygame.font.Font('data\\fonts\\2003.ttf', 45), bg=BLACK, fg=WHITE, colorkey_fg=True)


		if self.pos[0] == "cx":
			self.pos[0] = WIDTH//2 - self.img.get_width()//2

		if self.pos[1] == "cy":
			self.pos[1] = HEIGHT//2 - self.img.get_height()//2

		self.posx = self.pos[0]
		self.posy = self.pos[1]

		self.start_x = self.posx
		self.start_y = self.posy




	def update(self):
		# screen.blit(self.img, self.pos)

		pressed = pygame.mouse.get_pressed()
		pos = pygame.mouse.get_pos()

		
		if pressed[0] and (self.posx < pos[0] < self.posx+self.img.get_width()) and (self.posy < pos[1] < self.posy+self.img.get_height()):
			self.button_state = 1
		elif (self.posx < pos[0] < self.posx+self.img.get_width()) and (self.posy < pos[1] < self.posy+self.img.get_height()):
			self.button_state = 2
		else:	
			self.button_state = 0

		
		# print(self.button_state)
		if self.button_state == 1:
			self.posx += 1
			self.posy += 1
			if self.counter_click == 0:
				self.command()
			self.counter_click = 1

		(screen).blit(self.img, (self.posx, self.posy))
		try:
			(screen).blit(self.img_second, (self.posx, self.posy))
		except Exception:
			pass

		if self.button_state == 2:
			if self.focus_image_path:
				(screen).blit(self.img_focus, (self.posx, self.posy))


		if self.button_state in [0, 2]:
			self.counter_click = 0

		self.posx = self.start_x
		self.posy = self.start_y

		try:
			self.label.draw()
		except Exception:
			pass

	def get_width(self):
		"""Возвращает длину кнопки"""
		return self.img.get_width()

	def get_height(self):
		"""Возвращает длину кнопки"""
		return self.img.get_height()

	def set_focus(self):
		"""Устанавливает фокус, если наведен курсор"""
		self.button_state = 2

	def check_focus(self):
		"""Возвращает True если курсор наведен на эту кнопку"""
		if self.button_state in [1, 2]:
			return True
		else:
			return False






# ⟸
f_size_construction = 24
list_construction_button = []
# button_clear_all = TextButton(pos=(5, 670), text="  X      "+17*" ", font_name='calibri.ttf', font_size=f_size_construction, command=lambda: CLEAR_ALL(), fg=WHITE, bg=(48,48,48))
# list_construction_button.append(button_clear_all)

# button_clear_all_text = TextButton(pos=(0, 670), text="  clear  ", font_name='2003.ttf', font_size=f_size_construction, command=lambda: CLEAR_ALL(), fg=WHITE, bg=(48,48,48))
# list_construction_button.append(button_clear_all_text)


# button_back = TextButton(pos=(5, 700), text="  ←        "+17*" ", font_name='calibri.ttf', font_size=f_size_construction, command=lambda: set_slide_number(4), fg=WHITE, bg=RED_COUNT)
# list_construction_button.append(button_back)

# button_back_text = TextButton(pos=(0, 700), text="  back   ", font_name='2003.ttf', font_size=f_size_construction, command=lambda: set_slide_number(4), fg=WHITE, bg=RED_COUNT)
# list_construction_button.append(button_back_text)

button_back = ImageButton(pos=(15,55), img_path="gui/menu/buttons/back_button.png", focus_image_path="gui/menu/buttons/back_button_focus.png", command=lambda: set_slide_number(4))
button_back_construction = ImageButton(pos=(15,670), img_path="gui/menu/buttons/back_button.png", focus_image_path="gui/menu/buttons/back_button_focus.png", command=lambda: set_slide_number(4))

button_clear_all = ImageButton(pos=(218,670), img_path="map_objects/blocks/const/clear_all.png", command=lambda: CLEAR_ALL())


list_construction_button.append(button_back_construction)
list_construction_button.append(button_clear_all)







def set_level_dif(type_dif):
	LevelCompiler("start_game", type_dif).start_work()
	LOAD_ENEMY_CONFIG["g"] = type_dif



#### lambda: LevelCompiler("start_game").start_work()

list_buttons_choise_difficult = []
# button_back_to_const_text = TextButton(pos=(WIDTH//2-174//2, 650), text=" back ", font_name='2003.ttf', font_size=40, command=lambda: set_slide_number(6), fg=WHITE, bg_focus=RED, bg=RED_COUNT)
font_difficult = 38

y_difficult_buttons = 110
# button_back_to_const_text = TextButton(pos=(120, y_difficult_buttons), text=" back ", font_name='2003.ttf', font_size=font_difficult, command=lambda: set_slide_number(6), fg=WHITE, bg_focus=RED, bg=RED_COUNT)
# list_buttons_choise_difficult.append(button_back_to_const_text)

# button_play_to_const_text = TextButton(pos=(WIDTH//2-button_back_to_const_text.get_width()//2, y_difficult_buttons), text=" play ", font_name='2003.ttf', font_size=font_difficult, command=lambda: set_slide_number(6), fg=WHITE, bg_focus=RED, bg=RED_COUNT)
# list_buttons_choise_difficult.append(button_play_to_const_text)


try:
	enemy_tank_lvl1 = image.load(LOAD_TEXTURES + "tanks/enemy/lvl1_a1_r1.png")
except Exception:
	enemy_tank_lvl1 = image.load(DEFAULT_TEXTURES + "tanks/enemy/lvl1_a1_r1.png")

try:
	enemy_tank_lvl2 = image.load(LOAD_TEXTURES + "tanks/enemy/lvl2_a1_r1.png")
except Exception:
	enemy_tank_lvl2 = image.load(DEFAULT_TEXTURES + "tanks/enemy/lvl2_a1_r1.png")

try:
	enemy_tank_lvl3 = image.load(LOAD_TEXTURES + "tanks/enemy/lvl3_a1_r1.png")
except Exception:
	enemy_tank_lvl3 = image.load(DEFAULT_TEXTURES + "tanks/enemy/lvl3_a1_r1.png")

try:
	enemy_tank_lvl4 = image.load(LOAD_TEXTURES + "tanks/enemy/lvl4_a1_r1.png")
except Exception:
	enemy_tank_lvl4 = image.load(DEFAULT_TEXTURES + "tanks/enemy/lvl4_a1_r1.png")











button_bg_level_difficult_lvl1_CLASS = ImageButton(pos=(0,0), img_path="gui/menu/buttons/level_dif.png", command=lambda: print("Test"))
button_bg_level_difficult_lvl1 = ImageButton(pos=(WIDTH//2-button_bg_level_difficult_lvl1_CLASS.get_width()//2, y_difficult_buttons), img_path="gui/menu/buttons/level_dif.png", command=lambda: set_level_dif(CONFIG_ROUND1_LEVELS), focus_image_path="gui/menu/buttons/level_dif_focus.png")

list_buttons_choise_difficult.append(button_bg_level_difficult_lvl1)

try:
	black_arrow = image.load(LOAD_TEXTURES + "/gui/arrow_black.png")
except Exception:
	black_arrow = image.load(DEFAULT_TEXTURES + "/gui/arrow_black.png")

battlecity_font6 = pygame.font.Font('data\\fonts\\2003.ttf', 34)
text_level_dif_lvl1 = battlecity_font6.render("easy", 0, BLACK, WHITE)
text_level_dif_lvl1.set_colorkey(WHITE)

"""

CONFIG_ROUND1_LEVELS = { # Всего 20


		"lvl1": 18,
		"lvl2": 2,
		"lvl3": 0,
		"lvl4": 0,

		# КАК ЧАСТО БУДЕТ ПОЯВЛЯТСЯ ПРОТИВНИК ПОСЛЕ УБИЙСТВА ПОСЛЕДНЕГО (меньше - быстрее)
		"timer_respawn": 70, #70,

		# СКОЛЬКО ПРОТИВНИКОВ МОЖЕТ БЫТЬ ОДНОВРЕМЕННО НА ПОЛЕ БОЯ
		"all_enemys_count_in_battle": 4,
		}
"""

battlecity_font7_count_enemy_dif = pygame.font.Font('data\\fonts\\2003.ttf', 30)
text_count_dif_lvl1 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND1_LEVELS["lvl1"]), 0, BLACK, WHITE)
text_count_dif_lvl1.set_colorkey(WHITE)

text_count_dif_lvl2 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND1_LEVELS["lvl2"]), 0, BLACK, WHITE)
text_count_dif_lvl2.set_colorkey(WHITE)

text_count_dif_lvl3 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND1_LEVELS["lvl3"]), 0, BLACK, WHITE)
text_count_dif_lvl3.set_colorkey(WHITE)

text_count_dif_lvl4 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND1_LEVELS["lvl4"]), 0, BLACK, WHITE)
text_count_dif_lvl4.set_colorkey(WHITE)









button_bg_level_difficult_lvl2 = ImageButton(pos=(WIDTH//2-button_bg_level_difficult_lvl1_CLASS.get_width()//2, y_difficult_buttons + button_bg_level_difficult_lvl1_CLASS.get_height() + 22), img_path="gui/menu/buttons/level_dif.png", command=lambda: set_level_dif(CONFIG_ROUND2_LEVELS), focus_image_path="gui/menu/buttons/level_dif_focus.png")

list_buttons_choise_difficult.append(button_bg_level_difficult_lvl2)

text_level_dif_lvl2 = battlecity_font6.render("medium", 0, BLACK, WHITE)
text_level_dif_lvl2.set_colorkey(WHITE)

# battlecity_font7_count_enemy_dif = pygame.font.Font('data\\fonts\\2003.ttf', 30)
text_count_medium_dif_lvl1 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND2_LEVELS["lvl1"]), 0, BLACK, WHITE)
text_count_medium_dif_lvl1.set_colorkey(WHITE)

text_count_medium_dif_lvl2 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND2_LEVELS["lvl2"]), 0, BLACK, WHITE)
text_count_medium_dif_lvl2.set_colorkey(WHITE)

text_count_medium_dif_lvl3 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND2_LEVELS["lvl3"]), 0, BLACK, WHITE)
text_count_medium_dif_lvl3.set_colorkey(WHITE)

text_count_medium_dif_lvl4 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND2_LEVELS["lvl4"]), 0, BLACK, WHITE)
text_count_medium_dif_lvl4.set_colorkey(WHITE)












button_bg_level_difficult_lvl3 = ImageButton(pos=(WIDTH//2-button_bg_level_difficult_lvl1_CLASS.get_width()//2, y_difficult_buttons + 2*button_bg_level_difficult_lvl1_CLASS.get_height() + 2*22), img_path="gui/menu/buttons/level_dif.png", command=lambda: set_level_dif(CONFIG_ROUND3_LEVELS), focus_image_path="gui/menu/buttons/level_dif_focus.png")

list_buttons_choise_difficult.append(button_bg_level_difficult_lvl3)

text_level_dif_lvl3 = battlecity_font6.render("hard", 0, BLACK, WHITE)
text_level_dif_lvl3.set_colorkey(WHITE)

# battlecity_font7_count_enemy_dif = pygame.font.Font('data\\fonts\\2003.ttf', 30)
text_count_hard_dif_lvl1 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND3_LEVELS["lvl1"]), 0, BLACK, WHITE)
text_count_hard_dif_lvl1.set_colorkey(WHITE)

text_count_hard_dif_lvl2 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND3_LEVELS["lvl2"]), 0, BLACK, WHITE)
text_count_hard_dif_lvl2.set_colorkey(WHITE)

text_count_hard_dif_lvl3 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND3_LEVELS["lvl3"]), 0, BLACK, WHITE)
text_count_hard_dif_lvl3.set_colorkey(WHITE)

text_count_hard_dif_lvl4 = battlecity_font7_count_enemy_dif.render(str(CONFIG_ROUND3_LEVELS["lvl4"]), 0, BLACK, WHITE)
text_count_hard_dif_lvl4.set_colorkey(WHITE)



# button_play = TextButton(pos=(700+15, 700), text="  →   ", font_name='calibri.ttf', font_size=f_size_construction, command=lambda: set_slide_number(4), fg=GREEN, bg=(48,48,48))
# list_construction_button.append(button_play)


# button_play_text = TextButton(pos=(625, 700), text=" play ", font_name='2003.ttf', font_size=f_size_construction, command=lambda: set_slide_number(4), fg=BLACK, bg=GREEN2)#(48,48,48))
# list_construction_button.append(button_play_text)





# button_save_level = TextButton(pos=(700+15, 670), text="  →   ", font_name='calibri.ttf', font_size=f_size_construction, command=lambda: set_slide_number(4), fg=WHITE, bg=(48,48,48))
# list_construction_button.append(button_save_level)


# button_save_level_text = TextButton(pos=(625, 670), text=" save ", font_name='2003.ttf', font_size=f_size_construction, command=lambda: set_slide_number(4), fg=WHITE, bg=(48,48,48))
# list_construction_button.append(button_save_level_text)

start_x_line = SPAWN_POLE[0]
start_y_line = SPAWN_POLE[1]


def VIEW_GRID_F_FOR_BTN():
	if VIEW_GRID["g"] == True:
		VIEW_GRID["g"] = False
	else:
		VIEW_GRID["g"] = True


def VIEW_BASE_F_FOR_BTN():
	if VIEW_BASE["g"] == True:
		VIEW_BASE["g"] = False
	else:
		VIEW_BASE["g"] = True



# pygame.draw.line(screen, WHITE, (start_x_line, start_y_line), (start_x_line, 448), 1)

battlecity_font3 = pygame.font.Font('data\\fonts\\calibri.ttf', 18)
# text_destroy_mouse = battlecity_font3.render("Move block in this rectangle for destroy...", 0, RED_COUNT, BLACK)
# text_destroy_mouse.set_colorkey((0, 0, 0))

# button_kill_block = TextButton(pos=(PARAMS_RECT_DESTROY_MOUSE_CONST[0]+5, PARAMS_RECT_DESTROY_MOUSE_CONST[1]+25), text="Move block in this rectangle for destroy...", font_name='calibri.ttf', font_size=18, fg=RED_COUNT)
# list_construction_button.append(button_kill_block)


x_objects = 720
y_objects = SPAWN_POLE[1] # 73

brick_full_button = MapObjectButton(pos=(x_objects, y_objects), type=1)
brick_button = MapObjectButton(pos=(x_objects, y_objects+48), type=2)
brick_button2 = MapObjectButton(pos=(x_objects, y_objects+48+48), type=3)
brick_button3 = MapObjectButton(pos=(x_objects, y_objects+48+48+48), type=4)
brick_button4 = MapObjectButton(pos=(x_objects, y_objects+48+48+48+48), type=5)
beton_button = MapObjectButton(pos=(x_objects, y_objects+48+48+48+48+48), type=6)
beton_button1 = MapObjectButton(pos=(x_objects, y_objects+48+48+48+48+48+48), type=7)
beton_button2 = MapObjectButton(pos=(x_objects, y_objects+48+48+48+48+48+48+48), type=8)
beton_button3 = MapObjectButton(pos=(x_objects, y_objects+48+48+48+48+48+48+48+48), type=9)
beton_button4 = MapObjectButton(pos=(x_objects, y_objects+48+48+48+48+48+48+48+48+48), type=10)
bush_button = MapObjectButton(pos=(x_objects, y_objects+48+48+48+48+48+48+48+48+48+48), type=11)
water_button = MapObjectButton(pos=(x_objects, y_objects+48+48+48+48+48+48+48+48+48+48+48), type=12)






# button_play = TextButton(pos=(700+15, 700), text="  →   ", font_name='calibri.ttf', font_size=f_size_construction, command=lambda: set_slide_number(4), fg=GREEN, bg=(48,48,48))
# list_construction_button.append(button_play)



# button_play_text = TextButton(pos=(WIDTH//2-105, 670), text=" play ", fg_focus=WHITE, bg_focus=RED, fg=WHITE, bg=RED_COUNT, font_name='2003.ttf', font_size=50, command=lambda: set_slide_number(4))#(48,48,48))
# list_construction_button.append(button_play_text)

# button_save_level = TextButton(pos=(WIDTH//2-103, 670+53), text="   save map   ", fg_focus=WHITE, bg_focus=YELLOW, fg=WHITE, bg=YELLOW_COUNT, font_name='2003.ttf', font_size=21, command=lambda: set_slide_number(4))#(48,48,48))
# list_construction_button.append(button_save_level)



# ²
# button_play_text = TextButton(pos=(WIDTH//2-105, 670), text=" play ", fg_focus=WHITE, bg_focus=RED, fg=WHITE, bg=RED_COUNT, font_name='2003.ttf', font_size=50, command=lambda: LevelCompiler("start_game").start_work())#(48,48,48))
# button_play_text = TextButton(pos=(WIDTH//2-105, 670), text=" play ", fg_focus=WHITE, bg_focus=RED, fg=WHITE, bg=RED_COUNT, font_name='2003.ttf', font_size=50, command=lambda: set_slide_number(7))#(48,48,48))
# button_play_text = TextButton(pos=(WIDTH//2-105, 670), text=" play ", fg_focus=WHITE, bg_focus=GREEN, fg=WHITE, bg=GREEN2, font_name='2003.ttf', font_size=50, command=lambda: set_slide_number(7))#(48,48,48))
button_play_text = TextButton(pos=(WIDTH//2-105, 670), text=" play ", fg_focus=WHITE, bg_focus=RED, fg=WHITE, bg=RED_COUNT, font_name='2003.ttf', font_size=50, command=lambda: set_slide_number(7))#(48,48,48))
list_construction_button.append(button_play_text)

button_save_level = TextButton(pos=(WIDTH//2-103, 670+53), text=" save ", fg_focus=GREY_BLACK, bg_focus=YELLOW, fg=WHITE, bg=YELLOW_COUNT, font_name='2003.ttf', font_size=21, command=lambda: LevelCompiler("save").start_work())#(48,48,48))
list_construction_button.append(button_save_level)

button_load_level = TextButton(pos=(WIDTH//2-103+92, 670+53), text="  load  ", fg_focus=GREY_BLACK, bg_focus=YELLOW, fg=WHITE, bg=YELLOW_COUNT, font_name='2003.ttf', font_size=21, command=lambda: LevelCompiler("load").start_work())#(48,48,48))
list_construction_button.append(button_load_level)





list_special_buttons = []
btn_grig_view = ImageButton(pos=(540, 670), img_path="/map_objects/blocks/const/view_grid_btn.png", command=lambda: VIEW_GRID_F_FOR_BTN())
list_special_buttons.append(btn_grig_view)

btn_base_view = ImageButton(pos=(540+48+12, 670), img_path="/map_objects/base.png", command=lambda: VIEW_BASE_F_FOR_BTN())
list_special_buttons.append(btn_base_view)

# btn_random_block = ImageButton(pos=(540+48+12+48+12, 670), img_path="/map_objects/blocks/const/random.png", command=lambda: VIEW_RANDOM_BLOCK())
# list_special_buttons.append(btn_random_block)





try:
	const_img_base = image.load(LOAD_TEXTURES + "/map_objects/base.png")
except Exception:
	const_img_base = image.load(DEFAULT_TEXTURES + "/map_objects/base.png")

try:
	const_brick_base = image.load(LOAD_TEXTURES + "/map_objects/blocks/const/brick_base.png")
except Exception:
	const_brick_base = image.load(DEFAULT_TEXTURES + "/map_objects/blocks/const/brick_base.png")


try:
	const_p1_base = image.load(LOAD_TEXTURES + "/tanks/player/lvl1_a1_r1.png")
except Exception:
	const_p1_base = image.load(DEFAULT_TEXTURES + "/tanks/player/lvl1_a1_r1.png")

try:
	const_p2_base = image.load(LOAD_TEXTURES + "/tanks/player2/lvl1_a1_r1.png")
except Exception:
	const_p2_base = image.load(DEFAULT_TEXTURES + "/tanks/player2/lvl1_a1_r1.png")

try:
	const_e1_base = image.load(LOAD_TEXTURES + "/tanks/enemy/lvl1_a1_r3.png")
except Exception:
	const_e1_base = image.load(DEFAULT_TEXTURES + "/tanks/enemy/lvl1_a1_r3.png")










class LevelCompiler:
	""" Класс предназначен для работы конструктора. Может сохранять, открывать и запускать уровни. """
	def __init__(self, type_work="save", type_dif=CONFIG_ROUND1_LEVELS):
		"""
		:type_work: принимает строки "save", "open" или "start"
		Если получена строка "start" то уровень запустится

		"""
		self.level_string = ""
		self.symvol = "="

		self.type_work = type_work
		# self.k_x = SPAWN_POLE[0]
		# self.k_y = SPAWN_POLE[1]

		self.k_x = 0
		self.k_y = 0
		self.type_dif = type_dif
		

	def start_work(self):
		if self.type_work == "save":
			# saved_file_level = fd.asksaveasfile(title=win_name + " - cохранить уровень...", initialdir=os.getcwd()+"\\data\\configs\\levels\\", filetypes=(("BattleCity 20.20 files", "*.bslvl"), ("BattleCity 20.20 files", "*.bslvl")))	

			brick_full_list = brick_full_button.get_list_coord_block()
			brick_list = brick_button.get_list_coord_block()
			brick_list2 = brick_button2.get_list_coord_block()
			brick_list3 = brick_button3.get_list_coord_block()
			brick_list4 = brick_button4.get_list_coord_block()
			beton_list = beton_button.get_list_coord_block()
			beton_list1 = beton_button1.get_list_coord_block()
			beton_list2 = beton_button2.get_list_coord_block()
			beton_list3 = beton_button3.get_list_coord_block()
			beton_list4 = beton_button4.get_list_coord_block()
			bush_list = bush_button.get_list_coord_block()
			water_list = water_button.get_list_coord_block()

			brick_full_list.sort()
			brick_list.sort()
			brick_list2.sort()
			brick_list3.sort()
			brick_list4.sort()
			beton_list.sort()
			beton_list1.sort()
			beton_list2.sort()
			beton_list3.sort()
			beton_list4.sort()
			bush_list.sort()
			water_list.sort()
			# всего 12
			a = []
			a.append(brick_full_list)
			a.append(brick_list)
			a.append(brick_list2)
			a.append(brick_list3)
			a.append(brick_list4)
			a.append(beton_list)
			a.append(beton_list1)
			a.append(beton_list2)
			a.append(beton_list3)
			a.append(beton_list4)
			a.append(bush_list)
			a.append(water_list)

			simvols = ("=", "\\", "-", "_", "/", "#", "[", "'", ",", "]", "*", "w")
			simvol_now = 0
			counter_x_coord = 0

			# if False:
			# 	try:
			# 		for i in range(13):
			# 			print((list_normal_coords_x[i], list_normal_coords_y[self.k_y]))
			# 			print(f"brick_full_list[{i}] == {brick_full_list[i]}")
			# 			print("----------------------")
			# 	except Exception:
			# 		pass

			
			
			true_in_el = 0
			for y in range(13):
				for i in range(13):
					for el in a:			
						if (list_normal_coords_x[i], list_normal_coords_y[y]) in el:
							self.level_string += simvols[simvol_now]
							true_in_el = 0
						else:
							true_in_el += 1

						if true_in_el == len(a):
							self.level_string += " "
							true_in_el = 0

						simvol_now += 1
					simvol_now = 0
					true_in_el = 0

				self.level_string += "\n"
				true_in_el = 0

			







			

			# f = open("data/configs/levels/custom/custom.bslvl", "w")
			f = open("data/configs/levels/36.bslvl", "w")
			f.write(self.level_string)
			f.close()

			
			# print("Level Saved!")
			# print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
			# print(self.level_string)
			# print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')





		if self.type_work == "start_game":
			self.type_work = "save"
			self.start_work()
			level_number["g"] = 36
			ReloadBattle(next_level=36, custom=True, config_rules_enemy=self.type_dif)
			# dict_RUN_SLIDE_NOW["g"] = 5
			
			set_slide_battle()



		if self.type_work == "load":
			if dict_level_loaded_status["g"] == False:
				CLEAR_ALL()
				try:
					f = open("data/configs/levels/36.bslvl", "r")
				except Exception:
					f = open("data/configs/levels/36.bslvl", "w")
					f.close()
					f = open("data/configs/levels/36.bslvl", "r")


				self.level_string = f.read()
				f.close()

				dict_level_loaded_status["g"] = True

				string_for_len = len((self.level_string.replace(" ", "")).replace("\n", ""))
				clone_string_for_len = string_for_len

				simvols = ("=", "\\", "-", "_", "/", "#", "[", "'", ",", "]", "*", "w")
				simvol_now = 0

				a = []
				a.append(brick_full_button)
				a.append(brick_button)
				a.append(brick_button2)
				a.append(brick_button3)
				a.append(brick_button4)
				a.append(beton_button)
				a.append(beton_button1)
				a.append(beton_button2)
				a.append(beton_button3)
				a.append(beton_button4)
				a.append(bush_button)
				a.append(water_button)
				# brick_full_button.set_block((list_normal_coords_x[0], list_normal_coords_y[3]))
				x = 0
				y = 0



				if string_for_len <= 13**2:
					string_for_len += string_for_len
					for i in range(len(self.level_string)):
						if self.level_string[i] != "\n":
							for k in range(len(a)):
								if self.level_string[i] == simvols[k]:
									a[k].set_block((list_normal_coords_x[x], list_normal_coords_y[y]))
							if x < 12:
								x += 1
							else:
								x = 0
						else:
							y += 1
					


def get_mouse_any_block():
	"""Возвращает True, если на курсоре есть любой блок"""
	if water_button.get_mouse_block() or bush_button.get_mouse_block() or beton_button4.get_mouse_block() or beton_button3.get_mouse_block() or beton_button2.get_mouse_block() or beton_button1.get_mouse_block() or beton_button.get_mouse_block() or brick_full_button.get_mouse_block() or brick_button.get_mouse_block() or brick_button2.get_mouse_block() or brick_button3.get_mouse_block() or brick_button4.get_mouse_block():
		return True
	else:
		return False




############# БЛОК КОДА ДЛЯ ВЫБОРА КАМПАНИИ #############






		

# draw_count
# (699+1, 395-6)
# label_counter_respawn_player1 = Label(pos=[721, 418-5], text=str(dict_respawn_count["now"]), font=battlecity_font, bg=BATTLE_BG_COLOR, fg=BLACK)


label_select_campaign = Label(pos=["cx", 50], text="select campaign")




dlc_buttons_x = 20


list_string_campaigns_description = []
classic_description = "standard battles in format BattleCity from 80's years"



list_campaign_buttons = []

# button_classic_campaign = ImageButton(pos=[dlc_buttons_x, "cy"], img_path="gui/menu/buttons/campaign/classic.png", command=lambda: set_slide_battle(), focus_image_path="gui/menu/buttons/campaign_button_focus.png")
button_classic_campaign = ImageButton(pos=[dlc_buttons_x, "cy"], img_path="gui/menu/buttons/campaign/classic.png", command=lambda: set_slide_number(9), focus_image_path="gui/menu/buttons/campaign_button_focus.png")

list_campaign_buttons.append(TextButton(pos=[button_classic_campaign.pos[0]+(10*len(' '+"classic"+" "))//2, 505], text=' '+"classic"+" ", font_name="2003.ttf", font_size=23, fg_focus=GREY, bg_focus=BLACK, bg=BLACK, fg=WHITE, font=battlecity_font, command=lambda: set_slide_number(9)))
list_campaign_buttons.append(button_classic_campaign)

list_string_campaigns_description.append(classic_description)
list_string_campaigns_description.append(classic_description)


# rect_bg_campaign_buttons = pygame.draw.rect(screen, GREY_BLACK, (0, 200, WIDTH, 330))





def REPLACE_DLC_BUTTON_TEXT():
	if vidget_campaigns_dlc_btn.text.replace(" ", "") == "campaigns" and vidget_campaigns_dlc_btn.button_state == 1:
		vidget_campaigns_dlc_btn.text = "    dlc    "
		# vidget_campaigns_dlc_btn.bg_focus = GREEN3
		vidget_campaigns_dlc_btn.fg = WHITE
		vidget_campaigns_dlc_btn.fg_focus = WHITE


	else:
		vidget_campaigns_dlc_btn.text = " campaigns "
		vidget_campaigns_dlc_btn.bg = YELLOW_COUNT
		vidget_campaigns_dlc_btn.bg_focus = YELLOW_COUNT
		vidget_campaigns_dlc_btn.fg = WHITE
		# vidget_campaigns_dlc_btn.fg_focus = WHITE

	vidget_campaigns_dlc_btn.bg = GREEN3
	vidget_campaigns_dlc_btn.bg_focus = GREEN3

	vidget_campaigns_dlc_btn.pos = ["cx", 115]
	vidget_campaigns_dlc_btn.update_coords()

	text_description_descr_dlc.set_text(default_text_description)
	text_description_descr_dlc.set_fg(GREY)
	text_description_descr_dlc.update_pos(["cx", 607])
	text_author_dlc.set_text(" ")
	text_version_dlc.set_text(" ")


	




#####################################################################

# class DLC_INI_READER:
# 	def __init__(self, dlc_name):
# 		self.dlc_name = dlc_name

#####################################################################





list_vidget_campaigns_dlc = []
vidget_campaigns_dlc_btn = TextButton(pos=["cx", 115], text=" campaigns ", font_name="2003.ttf", font_size=29, fg_focus=GREY_BLACK, bg_focus=YELLOW_COUNT, bg=YELLOW_COUNT, fg=WHITE, font=battlecity_font, command=lambda: REPLACE_DLC_BUTTON_TEXT(), set_small_tank=False)
list_vidget_campaigns_dlc.append(vidget_campaigns_dlc_btn)




####### ЗДЕСЬ Я ОПИСЫВАЮ ВСЕ, ЧТО КАСАЕТСЯ DLC ДОПОЛНЕНИЙ ######

# список подтвержденных DLC Дополнений от разработчика (на них будет лента бирюзового цвета из файла official_dlc.png)
OFFICIAL_DLC_LIST = ["newyear", ]

# список легендарных DLC (самые редкие и крутые)
LEGEND_DLC_LIST = ["grey_player", ]

# список золотых DLC (почти самые крутые)
GOLD_DLC_LIST = ["enemy_player", ]


# Для уменьшения объема кода засунул все в такой список. 
LIST_ALL_DLC_TYPE = [OFFICIAL_DLC_LIST, LEGEND_DLC_LIST, GOLD_DLC_LIST]
LIST_DLC_TYPE_LINE = ["official_dlc.png", "legend.png", "gold.png"]



list_dlc_buttons = []
# button_dlc_campaign = ImageButton(pos=[40, "cy"], img_path="gui/menu/buttons/campaign/classic.png", command=lambda: print("Test"), focus_image_path="gui/menu/buttons/campaign_button_focus.png")
# list_dlc_buttons.append(button_classic_campaign)








# ОСУЩЕСТВЛЯЕМ ОБРАБОТКУ DLC ДЛЯ ОТОБРАЖЕНИЯ

# исключаем "закомментированные" DLC
try:
	dlc_folder_list = os.listdir(os.getcwd()+"/dlc/")
	# dlc_folder_list.remove("__old")
	for e in dlc_folder_list:
		if e[0] == "-" or e[0] == "_":
			dlc_folder_list.remove(e)
except Exception:
	os.mkdir(os.getcwd()+"/dlc/")
	dlc_folder_list = os.listdir(os.getcwd()+"/dlc/")
	# dlc_folder_list.remove("__old")
	for e in dlc_folder_list:
		if e[0] == "-" or e[0] == "_":
			dlc_folder_list.remove(e)

intedent_dlc_buttons_x = button_classic_campaign.get_width() + 15
# .pos[0]+(10*len(' '+"classic"+" "))//2

dlc_text_now = ""
max_len_string_dlc_text = 10

config = configparser.ConfigParser()

list_string_dlc_description = []
list_string_dlc_author = []
list_string_dlc_version = []


def UPDATE_TEXTUREPACK(TYPE_LOADER=TYPE_LOADER["g"]):
	if TYPE_LOADER == "classic":
		# Откуда загружать текстуры (закинул удочку на обработку dlc)
		LOAD_TEXTURES = "data/textures/"
		LOAD_LEVELS = "data/configs/levels/"
	else:
		try:
			LOAD_TEXTURES = f"dlc/{TYPE_LOADER}/textures/"
			LOAD_LEVELS = f"dlc/{TYPE_LOADER}/configs/levels/"
		except Exception:
			LOAD_TEXTURES = "data/textures/"
			LOAD_LEVELS = "data/configs/levels/"
		# LOAD_TEXTURES = "dlc/enemy_player/textures/"


	# Если какой то текстуры не обнаруживается, загружается ее базовый аналог из этой папки
	DEFAULT_TEXTURES = "data/textures/"

	# Конструктор и обработчик dlc файлов
	ALL_TEXTURES_TANKS = f'{LOAD_TEXTURES}tanks/'
	ALL_BUTTONS_FOLDER = '%s/gui/menu/buttons/'

	return DEFAULT_TEXTURES, ALL_TEXTURES_TANKS, ALL_BUTTONS_FOLDER


if len(dlc_folder_list) != 0:
	for e in dlc_folder_list:
		list_dlc_buttons.append(ImageButton(pos=[dlc_buttons_x, "cy"], img_path="dlc/"+e+"/dlc_icon.png", focus_image_path="gui/menu/buttons/campaign_button_focus.png", command=lambda: UPDATE_TEXTUREPACK(TYPE_LOADER="newyear")))
		# list_dlc_buttons.append(TextButton(pos=[list_dlc_buttons[len(list_dlc_buttons)-1].pos[0], 511], text=' '+e+" ", font_name="2003.ttf", font_size=23, fg_focus=GREY, bg_focus=BLACK, bg=BLACK, fg=WHITE, font=battlecity_font, command=lambda: print("Test")))
		
		config.read("dlc/"+e+"/dlc.ini")

		# обработка ошибки если нет имени
		try:
			dlc_text_now = config["information"]["dlc_name"]
		except Exception:
			dlc_text_now = e

		# обработка автора DLC
		for i in range(2):
			try:
				list_string_dlc_author.append(config["information"]["author"])
			except Exception:
				list_string_dlc_author.append("none")

		# обработка версии DLC
		for i in range(2):
			try:
				list_string_dlc_version.append(config["information"]["version"])
			except Exception:
				list_string_dlc_version.append("none")
			

		# обработка описания. Если нет, то ставится фраза "No description"
		try:
			list_string_dlc_description.append(config["information"]["dlc_info"])
		except Exception:
			list_string_dlc_description.append("no description")


		if len(dlc_text_now) >= max_len_string_dlc_text:
			dlc_text_now = dlc_text_now[0:max_len_string_dlc_text]
		list_dlc_buttons.append(TextButton(pos=[dlc_buttons_x+(10*len(dlc_text_now))//2, 505], text=dlc_text_now, font_name="2003.ttf", font_size=23, fg_focus=GREY, bg_focus=BLACK, bg=BLACK, fg=WHITE, font=battlecity_font, command=lambda: print("Test")))

		# ДЕЛАЕМ ЕЩЕ РАЗ, ЧТО БЫ НЕ БЫЛО ОШИБКИ ИНДЕКСА ЭЛЕМЕНТА обработка описания. Если нет, то ставится фраза "No description"
		try:
			list_string_dlc_description.append(config["information"]["dlc_info"])
		except Exception:
			list_string_dlc_description.append("no description")


		dlc_buttons_x += intedent_dlc_buttons_x
else:
	text_no_dlc = "You do not have DLC add-ons installed"
	text_you_have_not_dlc = Label(pos=["cx", "cy"], text=text_no_dlc, font=pygame.font.Font('data\\fonts\\2003.ttf', 25))



list_text_content_dlc_description = []


FG_COLOR_DLC_TEXT = (0, 255, 4)




text_description_dlc = Label(pos=["cx", 565], text="description", font=pygame.font.Font('data\\fonts\\2003.ttf', 30), fg=FG_COLOR_DLC_TEXT)
list_text_content_dlc_description.append(text_description_dlc)


author_dlc_start_y = 640
text_label_author_dlc = Label(pos=[46, author_dlc_start_y], text="author:", font=pygame.font.Font('data\\fonts\\2003.ttf', 25), fg=FG_COLOR_DLC_TEXT)
list_text_content_dlc_description.append(text_label_author_dlc)

text_author_dlc = Label(pos=[170, author_dlc_start_y+2], text=" ", font=pygame.font.Font('data\\fonts\\2003.ttf', 20), fg=WHITE)
list_text_content_dlc_description.append(text_author_dlc)


text_label_version_dlc = Label(pos=[46, 667], text="version:", font=pygame.font.Font('data\\fonts\\2003.ttf', 25), fg=FG_COLOR_DLC_TEXT)
list_text_content_dlc_description.append(text_label_version_dlc)

text_version_dlc = Label(pos=[170+20, 667+2], text=" ", font=pygame.font.Font('data\\fonts\\2003.ttf', 20), fg=WHITE)
list_text_content_dlc_description.append(text_version_dlc)


default_text_description = "Hover over the DLC map to see more"
text_description_descr_dlc = Label(pos=["cx", 607], text=default_text_description, font=pygame.font.Font('data\\fonts\\2003.ttf', 20), fg=GREY)
list_text_content_dlc_description.append(text_description_descr_dlc)









# ВЫБОР УРОВНЯ LEVEL SELECTION



levels_folder_list = os.listdir(os.getcwd()+"/"+LOAD_LEVELS)
for e in levels_folder_list:
	if e[0] == "-" or e[0] == "_":
		levels_folder_list.remove(e)
	try:
		int(e.replace(".bslvl", ""))
	except Exception:
		pass
		# levels_folder_list.remove(e)
		# print(e)
		# print("HI")


levels_folder_list.sort()


start_x_levels_cards = 70
start_y_levels_cards = 180

x_levels_cards = start_x_levels_cards
y_levels_cards = start_y_levels_cards

max_count_how_many_level_cards_in_line = 5
count_how_many_level_cards_in_line = 0

levels_imagebuttons_list = []
for i in range(len(levels_folder_list)-1):
	if count_how_many_level_cards_in_line < max_count_how_many_level_cards_in_line:
		levels_imagebuttons_list.append(ImageButton(pos=(x_levels_cards, y_levels_cards), img_path="gui/menu/buttons/level_button.png", command=lambda: print(levels_folder_list[i]), focus_image_path="gui/menu/buttons/level_button_focus.png", text_coord=("c"), text_in_image=levels_folder_list[i], font_size=30))
		count_how_many_level_cards_in_line += 1
		x_levels_cards += levels_imagebuttons_list[len(levels_imagebuttons_list)-1].get_width() + 30
	else:
		count_how_many_level_cards_in_line = 0;
		x_levels_cards = start_x_levels_cards
		# y_levels_cards += levels_imagebuttons_list[len(levels_imagebuttons_list)-1].get_height() + 20
		y_levels_cards += levels_imagebuttons_list[0].get_height() + 20






label_select_level = Label(pos=["cx", 50], text="select level")


LABEL_VERSION_TITLE = Label(pos=["cx", HEIGHT-30], text="0.1beta", font=pygame.font.Font('data\\fonts\\2003.ttf', 20), fg=GREY)










PLAYER_1_HP = dict()
PLAYER_1_HP["all"] = 2
PLAYER_1_HP["now"] = PLAYER_1_HP["all"]


PLAYER_1_HP_LABEL = Label(pos=[723, 419-5], text=str(PLAYER_1_HP["now"]), font=pygame.font.Font('data\\fonts\\2003.ttf', 34), bg=WHITE, fg=BLACK, colorkey_fg=True)


group_project_label = []

CREDITS_PROJECT = Label(pos=[20, 20], text=__doc__, font=pygame.font.Font('data\\fonts\\9303.ttf', 34))
# group_project_label.append(CREDITS_PROJECT)

CREDITS_PROJECT2 = (Label(pos=[20, 57], text="             Автор: Подстречный Александр, 11А класс, МБОУ Гимназия №6", fg=RED_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

# BG_CREDITS_PROGECT_TITLE = draw.rect(screen, YELLOW_COUNT, (0, 0, WIDTH, 70))

project_label_start_y = dict()
project_label_start_y["g"] = 120
project_label_start_y["rotate_speed"] = 24


group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Проект «BattleCity 20.20» реализован на языке программирования", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))


group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30], text="Python. Использовались библиотеки pygame, random, sys, os, math,", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*2], text="time, pyperclip, WebBrowser и configparcer.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))


group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*3], text=" ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*4], text="О ПРОЕКТЕ", fg=YELLOW_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*5], text="BattleCity 20.20 - игра, написанная на языке программирования Python.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*6], text="Создана по мотивам известной каждому игры Battle City на приставках", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*7], text="Nintendo Entertainment System (также известная как NES) начала 80-х", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*8], text="годов.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

NES_IMAGE = image.load("data/textures/gui/nes.png")


for i in range(10):
	group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*8], text=" ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text=" ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="ИНФОРМАЦИЯ О ПРОЕКТЕ", fg=YELLOW_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Деятельность: Исследовательская, творческая;", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Количество участников: Индивидуальный (1 человек);", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Место проведения: Внеурочный;", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Тема: Свободная;", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Продолжительность: Долгосрочный (7 месяцев);", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))


group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text=" ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))


group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*9], text="ВНУТРЕНИЕ ВЫВОДЫ", fg=YELLOW_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="При создании игры я получил большой опыт в работе с большими", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="проектами в сфере IT. Узнал много нового про работу программиста,", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="геймдизайнера, художника, звукорежжисера и других профессиях.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text=" ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*9], text="ВНЕШНИЕ ВЫВОДЫ", fg=YELLOW_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Своей целью ставил разработать максимально приближенную к", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="оригиналу игру, но с некоторыми изменениями.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Так как это еще далеко не финальная версия, в ней реализованы", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="еще не все особенности. Планируются различные механики,", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="в числе которых система хранения данных о пользователях, ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="механизм Боевого Пропуска и многие другие «фишки» современных", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="проектов.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text=" ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*9], text="РЕЗУЛЬТАТЫ ПРОЕКТА", fg=YELLOW_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Основная цель реализации механики сражений Battle City на", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="языке программирования Python успешно достигнута.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text=" ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*9], text="ДАЛЬНЕЙШИЕ ЦЕЛИ", fg=YELLOW_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="Поддержка проекта, его модернизация, увеличение количества", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text="пользователей, реализация новых механик.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text=" ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*9], text="ИСТОЧНИКИ ИНФОРМАЦИИ", fg=YELLOW_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(LinkTextButton(pos=[20, project_label_start_y["g"]+30*15], text="PromoDJ - https://promodj.com/x/blog/1012328/Battle_City_Super_Tank_1990_Tank_1991_Missile_Tank_1994_Missile_Tank_1995", link="https://promodj.com/x/blog/1012328/Battle_City_Super_Tank_1990_Tank_1991_Missile_Tank_1994_Missile_Tank_1995"))
group_project_label.append(LinkTextButton(pos=[20, project_label_start_y["g"]+30*15], text="Библиотека Pygame - https://www.pygame.org/docs/", link="https://www.pygame.org/docs/"))
group_project_label.append(LinkTextButton(pos=[20, project_label_start_y["g"]+30*15], text="Библиотека Pygame-Widgets - https://pypi.org/project/pygame-widgets/", link="https://pypi.org/project/pygame-widgets/"))
group_project_label.append(LinkTextButton(pos=[20, project_label_start_y["g"]+30*15], text="Библиотека WebBrowser - https://habr.com/ru/post/470938/", link="https://habr.com/ru/post/470938/"))
group_project_label.append(LinkTextButton(pos=[20, project_label_start_y["g"]+30*15], text="Этапы работы над проектом - https://infourok.ru/material.html?mid=51665", link="https://infourok.ru/material.html?mid=51665"))
group_project_label.append(LinkTextButton(pos=[20, project_label_start_y["g"]+30*15], text="Научня библиотека ТГУ - http://www.lib.tsu.ru/win/produkzija/metodichka/6_6.html", link="http://www.lib.tsu.ru/win/produkzija/metodichka/6_6.html"))
group_project_label.append(LinkTextButton(pos=[20, project_label_start_y["g"]+30*15], text="Оформление списка литературы АГТУ - https://narfu.ru/agtu/www.agtu.ru/fad08f5ab5ca9486942a52596ba6582elit.html", link="https://narfu.ru/agtu/www.agtu.ru/fad08f5ab5ca9486942a52596ba6582elit.html"))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]], text=" ", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))

group_project_label.append(Label(pos=[20, project_label_start_y["g"]+30*9], text="ПОРТФОЛИО ПРОЕКТА", fg=YELLOW_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
group_project_label.append(TextButton(pos=[20, project_label_start_y["g"]], text=f"Архив версий: {os.getcwd()}\\_git\\", font_name="calibri.ttf", font_size=25, fg_focus=GREY, bg_focus=BLACK, bg=BLACK, fg=WHITE, command=lambda: os.system(f"explorer.exe {os.getcwd()}\\_git\\")))




# group_project_label.append(Label(pos=[20, 150+30*3], text="ВЫВОДЫ О ПРОЕКТЕ", fg=YELLOW_COUNT, font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
# group_project_label.append(Label(pos=[20, 150+30*4], text="Внутренние выводы: Я приобрел навыки работы с различными библио-", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
# group_project_label.append(Label(pos=[20, 150+30*5], text="теками, получил ценный опыт в работе над большими проектами.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))
# group_project_label.append(Label(pos=[20, 150+30*6], text="Испытал себя в роли разработчика компьютерных игр.", font=pygame.font.Font('data\\fonts\\calibri.ttf', 25)))



"""import pygame
from pygame import *
import sys, random, math, time
import os, os.path, pyperclip
import configparser"""

IMAGE_PROJECT_ICON = image.load("data/textures/gui/icon.png")


CLOSE_PROJECT_LABEL = TextButton(pos=["cx", HEIGHT-40], text=" Закрыть ", font_name="2003.ttf", font_size=28, fg_focus=WHITE, bg_focus=RED, bg=RED_COUNT, fg=WHITE, font=battlecity_font, command=lambda: set_slide_number(4))





















































while 1:
	fpsClock.tick(FPS) # define frame rate

	# print(brick_button4.get_mouse_block())

	# print(enemys_list_for_spawner["list"])

	# screen.fill(BLACK)
	# print(fpsClock.tick(FPS))



	for e in event.get():
		if e.type == QUIT:
			quit()
			sys.exit()

		# if e.type == pygame.MOUSEBUTTONDOWN and dict_RUN_SLIDE_NOW["g"]==6 or win_name == "BattleCity 20.20 - Construction":
		if e.type == pygame.MOUSEBUTTONDOWN and dict_RUN_SLIDE_NOW["g"]==10:
			if e.button == 4:
				project_label_start_y["g"] += project_label_start_y["rotate_speed"]
			elif e.button == 5:
				project_label_start_y["g"] -= project_label_start_y["rotate_speed"]

			for el in group_project_label:
				el.update_pos([20, project_label_start_y["g"]+30*group_project_label.index(el)])
			


		if e.type == MOUSEBUTTONDOWN and dict_RUN_SLIDE_NOW["g"]==6:
			# if counter_click_rotate_block <= 1:
			# print("PRESSED", e.button)
			if e.button == 4:
				if brick_button.get_mouse_block()==True:
					brick_button.del_mouse_block()
					brick_button2.set_mouse_block()

				elif brick_button2.get_mouse_block()==True:
					brick_button2.del_mouse_block()
					brick_button3.set_mouse_block()

				elif brick_button3.get_mouse_block() == True:
					brick_button3.del_mouse_block()
					brick_button4.set_mouse_block()

				elif brick_button4.get_mouse_block() == True:
					brick_button4.del_mouse_block()
					brick_button.set_mouse_block()



				elif beton_button1.get_mouse_block() == True:
					beton_button1.del_mouse_block()
					beton_button2.set_mouse_block()

				elif beton_button2.get_mouse_block() == True:
					beton_button2.del_mouse_block()
					beton_button3.set_mouse_block()

				elif beton_button3.get_mouse_block() == True:
					beton_button3.del_mouse_block()
					beton_button4.set_mouse_block()

				elif beton_button4.get_mouse_block() == True:
					beton_button4.del_mouse_block()
					beton_button1.set_mouse_block()

			elif e.button == 5:
				if brick_button4.get_mouse_block() == True:
					brick_button4.del_mouse_block()
					brick_button.set_mouse_block()

				elif brick_button3.get_mouse_block() == True:
					brick_button3.del_mouse_block()
					brick_button4.set_mouse_block()

				elif brick_button2.get_mouse_block()==True:
					brick_button2.del_mouse_block()
					brick_button3.set_mouse_block()

				elif brick_button.get_mouse_block()==True:
					brick_button.del_mouse_block()
					brick_button2.set_mouse_block()


				if beton_button4.get_mouse_block() == True:
					beton_button4.del_mouse_block()
					beton_button3.set_mouse_block()

				elif beton_button3.get_mouse_block() == True:
					beton_button3.del_mouse_block()
					beton_button2.set_mouse_block()

				elif beton_button2.get_mouse_block() == True:
					beton_button2.del_mouse_block()
					beton_button1.set_mouse_block()

				elif beton_button1.get_mouse_block() == True:
					beton_button1.del_mouse_block()
					beton_button4.set_mouse_block()






		if e.type == KEYDOWN and e.key == K_ESCAPE and dict_RUN_SLIDE_NOW["g"] not in [2, 3, 5] and GAME_OVER != True and GAME_WIN != True:
			# quit()
			# sys.exit()
			# ESC_PRESSED()

			MUSIC_INTRO.stop()

			vidget_campaigns_dlc_btn.text = " campaigns "
			text_description_descr_dlc.set_text(default_text_description)
			text_description_descr_dlc.set_fg(GREY)
			text_description_descr_dlc.update_pos(["cx", 607])
			text_author_dlc.set_text(" ")
			text_version_dlc.set_text(" ")
			

			PLAYER = {
				"LVL1": {
					"hp": 100,
					"damage": 100,
					"speed": TANK_SPEED,
					"bullet_speed": BULLET_SPEED,
					"type_player": "player", 
				},

				"LVL2": {
					"hp": 100,
					"damage": 100,
					"speed": TANK_SPEED,
					"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
					"type_player": "player",
				},

				"LVL3": {
					"hp": 100,
					"damage": 100,
					"speed": TANK_SPEED,
					"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
					"type_player": "player",
				},

				"LVL4": {
					"hp": 100,
					"damage": 100,
					"speed": TANK_SPEED,
					"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
					"type_player": "player",
				},

				"lvl_start": PLAYER_LEVEL_START,
			}



			dict_RUN_SLIDE_NOW["g"] = 4
			count_spawn = 0
			level_number["g"] = 1

			
			player_sprites.empty()

			if TYPE_RIGHT_INTERFACE == 1:
				ROCKET_COLUMN["now"] = -1
			elif TYPE_RIGHT_INTERFACE == 2:
				if CHEAT_MODE == False:
					ROCKET_COLUMN["now"] = 3
				else:
					ROCKET_COLUMN["now"] = 999

			title_menu_sprite = TITLE_MENU((84, 80))
			menu_content_sprites.add(title_menu_sprite)
			if len(grey_screens_sprites.sprites()) != 2:
				grey_screens_sprites.empty()
				grey_screen_top, grey_screen_down = CreateGreyScreens()

		if e.type == KEYDOWN and e.key == K_PRINT:
			ScreenshotsWorker(saved_name=f'screenshot{round(time.time())}').save_screen()
			MUSIC_screenshot.play()

		if e.type == KEYDOWN and e.key == K_RETURN and dict_RUN_SLIDE_NOW["g"] not in [5, 4]:
			if dict_PAUSE_GAME["g"] == False:
				dict_PAUSE_GAME["g"] = True
				MUSIC_pause_get.play()			
			else:
				dict_PAUSE_GAME["g"] = False


		if e.type == KEYDOWN and e.key == K_x and dict_RUN_SLIDE_NOW["g"] == 6:
			CLEAR_ALL()


		if e.type == KEYDOWN and e.key == K_F11 and False:	
			dict_PAUSE_GAME["g"] = True
		
			if next_window_mode == pygame.FULLSCREEN:
				next_window_mode = 1
				true_res = win_size

			else:
				next_window_mode = pygame.FULLSCREEN		
				windll.user32.SetProcessDPIAware()
				true_res = (windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1)) 
				

			pygame.display.set_mode(true_res,next_window_mode)

		



		





		# ЧИТ ФУНКЦИИ

		if CHEAT_MODE:
			# нажатие клавиши Num 0 перезагружает уровень 
			if e.type == KEYDOWN and e.key == K_KP0:
				walls_sprites.empty()
				beton_sprites.empty()
				water_sprites.empty()
				base_sprites.empty()
				base_sprites.empty()
				bush_sprites.empty()

				if level_number["g"] <= 9:
					level_map = LevelParser(f'data/configs/levels/0{level_number["g"]}.bslvl')
				else:
					level_map = LevelParser(f'data/configs/levels/{level_number["g"]}.bslvl')
				level_map.draw()

				wall_base_1 = Wall(WALL_BRICKS_24, (SPAWN_BASE[0]+12, SPAWN_BASE[1]))
				walls_sprites.add(wall_base_1)
				wall_base_2 = Wall(WALL_BRICKS_24, (SPAWN_BASE[0]+48+12, SPAWN_BASE[1]))
				walls_sprites.add(wall_base_2)
				wall_base_3 = Wall(WALL_BRICKS_24_R2, (SPAWN_BASE[0]+12, SPAWN_BASE[1]+24))
				walls_sprites.add(wall_base_3)
				wall_base_4 = Wall(WALL_BRICKS_24_R3, (SPAWN_BASE[0]+48+12, SPAWN_BASE[1]+24))
				walls_sprites.add(wall_base_4)

				eagle = BaseEagle(pos=(SPAWN_BASE[0]+24, SPAWN_BASE[1]+24))
				base_sprites.add(eagle)

			# увеличиваем уровень танка
			if e.type == KEYDOWN and e.key == K_KP_PLUS and dict_RUN_SLIDE_NOW["g"] != 4:
				lvl_tank_now = int(player_sprites.sprites()[len(player_sprites.sprites())-1].lvl_tank)

				if lvl_tank_now < 4:
					lvl_tank_now += 1
				else:
					lvl_tank_now = 1

				player_sprites.sprites()[len(player_sprites.sprites())-1].lvl_tank = lvl_tank_now


				PLAYER["lvl_start"] = lvl_tank_now
				pos_x_tank = player_sprites.sprites()[len(player_sprites.sprites())-1].rect.x
				pos_y_tank = player_sprites.sprites()[len(player_sprites.sprites())-1].rect.y


				player = Tank(PLAYER, pos_spawn=(pos_x_tank, pos_y_tank))
				player_sprites.empty()
				player_sprites.add(player)

			# уменьшаем уровень танка
			if e.type == KEYDOWN and e.key == K_KP_MINUS and dict_RUN_SLIDE_NOW["g"] != 4:
				lvl_tank_now = int(player_sprites.sprites()[len(player_sprites.sprites())-1].lvl_tank)

				if lvl_tank_now > 1:
					lvl_tank_now -= 1
				else:
					lvl_tank_now = 4

				player_sprites.sprites()[len(player_sprites.sprites())-1].lvl_tank = lvl_tank_now


				PLAYER["lvl_start"] = lvl_tank_now
				pos_x_tank = player_sprites.sprites()[len(player_sprites.sprites())-1].rect.x
				pos_y_tank = player_sprites.sprites()[len(player_sprites.sprites())-1].rect.y


				player = Tank(PLAYER, pos_spawn=(pos_x_tank, pos_y_tank))
				player_sprites.empty()
				player_sprites.add(player)

			# убить всех врагов
			if e.type == KEYDOWN and e.key == K_KP2:
				for sprite in enemys_sprites.sprites():
					AddExplosion(pos=sprite.rect.center, sprite=sprite, big=True)
					sprite.kill()
				CHANNEL_kill_enemy.play(MUSIC_kill_enemy)

			# добавить очень много жизней
			if e.type == KEYDOWN and e.key == K_KP5:
				pass
				

			# включить/отключить действие бонуса лопаты
			if e.type == KEYDOWN and e.key == K_KP8:
				if PLAYER1_NOW_BONUS["shovel"] == True:
					PLAYER1_NOW_BONUS["shovel"] = False
				else:
					PLAYER1_NOW_BONUS["shovel"] = True







	if dict_RUN_SLIDE_NOW["g"] == 1:

		# win_name = "BattleCity 20.20 - stage"+str(level_number)
		# display.set_caption(win_name)

		screen.fill(BATTLE_BG_COLOR)
		# screen.fill(GREY)		
		# screen.fill(BLACK)

		SysText(level=level_number["g"]).draw()
		# if next_window_mode == 1:
		BATTLE_POLE = draw.rect(screen, BLACK, (SPAWN_POLE[0], SPAWN_POLE[1], WIDTH_POLE, HEIGHT_POLE))
		# else:
			# BATTLE_POLE = draw.rect(screen, BLACK, (windll.user32.GetSystemMetrics(0)//2 - WIDTH_POLE // 2, windll.user32.GetSystemMetrics(1)//2 - HEIGHT_POLE // 2, WIDTH_POLE, HEIGHT_POLE))
			
			# pygame.transform.scale(player_sprites.sprites()[0].image, (16, 16))
			# BATTLE_POLE = draw.rect(screen, BLACK, (SPAWN_POLE[0], SPAWN_POLE[1], WIDTH_POLE*BUST_BIGGER_SPRITES_ALL_SCREEN, HEIGHT_POLE*BUST_BIGGER_SPRITES_ALL_SCREEN))

			# player_sprites.sprites()[0].image = pygame.transform.scale(player_sprites.sprites()[0].image, (player_sprites.sprites()[0].image.get_width()*BUST_BIGGER_SPRITES_ALL_SCREEN, player_sprites.sprites()[0].image.get_height()*BUST_BIGGER_SPRITES_ALL_SCREEN))

			# screen = pygame.transform.scale(screen, (506, 506))



		all_sprites.update()
		# Отрисовка
		walls_sprites.draw(screen)
		walls_sprites.update()

		beton_sprites.draw(screen)
		beton_sprites.update()

		ice_sprites.draw(screen)


		water_sprites.draw(screen)

		draw_level_number(level_number["g"])
		


		flag_panel_sprites.draw(screen)


		level_panel_sprites.draw(screen)
		level_panel_sprites.update()


		base_sprites.draw(screen)
		base_sprites.update()

		
			


		



		count_kill_enemy_sprites.draw(screen)
		count_kill_enemy_sprites.update()





		if dict_PAUSE_GAME["g"] == False:
			if PLAYER1_NOW_BONUS["stoptime"] == True:
				timer_stoptime += 1
				if timer_stoptime >= TIMER_STOPTIME:
					PLAYER1_NOW_BONUS["stoptime"] = False
					timer_stoptime = 0


			if PLAYER1_NOW_BONUS["shovel"] == True:
				if timer_shovel == 0:

					beton_shovel_sprites.add(WallBetonBricks(1, (SPAWN_BASE[0], SPAWN_BASE[1])))
					beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24, SPAWN_BASE[1])))
					beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24*2, SPAWN_BASE[1])))
					beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24*3, SPAWN_BASE[1])))
					beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24*3, SPAWN_BASE[1]+24)))
					beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24*3, SPAWN_BASE[1]+24*2)))
					beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0], SPAWN_BASE[1]+24*1)))
					beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0], SPAWN_BASE[1]+24*2)))


				timer_shovel += 1

				beton_shovel_sprites.draw(screen)


				if timer_shovel >= TIMER_SHOVEL:

					counter_shovel += 1

					if counter_shovel >= 17:
						beton_shovel_sprites.empty()

					if counter_shovel >= 34:
						beton_shovel_sprites.empty()

						beton_shovel_sprites.add(WallBetonBricks(1, (SPAWN_BASE[0], SPAWN_BASE[1])))
						beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24, SPAWN_BASE[1])))
						beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24*2, SPAWN_BASE[1])))
						beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24*3, SPAWN_BASE[1])))
						beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24*3, SPAWN_BASE[1]+24)))
						beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0]+24*3, SPAWN_BASE[1]+24*2)))
						beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0], SPAWN_BASE[1]+24*1)))
						beton_shovel_sprites.add(WallBetonBricks(2, (SPAWN_BASE[0], SPAWN_BASE[1]+24*2)))
						counter_shovel = 0
						count_shovel_animations += 1

					if count_shovel_animations >= SHIM_SHOVEL_ANIMATION_COUNT: # SHIM_SHOVEL_ANIMATION_COUNT 
						PLAYER1_NOW_BONUS["shovel"] = False
						beton_shovel_sprites.empty()
						timer_shovel = 0


					


			if PLAYER1_NOW_BONUS["shovel"] == False:
				beton_shovel_sprites.empty()
				timer_shovel = 0




		water_sprites.update()
		enemys_sprites.update()
		enemys_sprites.draw(screen)
		player_sprites.draw(screen)
		player_sprites.update()

		player_bonuses_sprites.draw(screen)
		player_bonuses_sprites.update()

		all_sprites.draw(screen)
		bush_sprites.draw(screen)

		enemys_spawn_animation_sprites.draw(screen)
		enemys_spawn_animation_sprites.update()


		if TYPE_RIGHT_INTERFACE == 1:
			panel_tanks_sprites.draw(screen)
		elif TYPE_RIGHT_INTERFACE in [2, 3]:
			# enemy_counter_right.text = str(len(panel_tanks_sprites.sprites()))
			enemy_counter_right = battlecity_font.render(str(len(panel_tanks_sprites.sprites())), 0, BLACK, BATTLE_BG_COLOR)
			screen.blit(enemy_counter_right, (startx, starty))


		'''696
		174'''

		if TYPE_RIGHT_INTERFACE in [2, 3]:
			text_rocket_counter = battlecity_font.render(str(ROCKET_COLUMN["now"]), 0, BLACK, BATTLE_BG_COLOR)
			if ROCKET_COLUMN["now"] != -1:
				if len(str(ROCKET_COLUMN["now"])) <= 9:
					(screen).blit(text_rocket_counter, (696+24+2, 174+24-7-5))
				else:
					(screen).blit(text_rocket_counter, (696, 174+24-7-5))

		
		respawn_count_sprites.draw(screen)

		rocket_counter_panel_sprites.draw(screen)
		rocket_counter_panel_sprites.update()



		bonuses_sprites.draw(screen)
		bonuses_sprites.update()
		# SPRITE_BONUS_immortality

		if dict_PAUSE_GAME["g"] == True:
			pause_sprites.draw(screen)
			pause_sprites.update()








		# ГЛАВНОЕ УСЛОВИЕ ДЛЯ ЗАВЕРШЕНИЯ ИГРЫ
		if GAME_OVER == True or GAME_WIN == True:
			timer_wait_end_game += 1

			if timer_wait_end_game >= TIMER_WAIT_END_GAME:
				timer_wait_end_game = 0
				# print('END_GAME')
				FILL_BLACK = True
		
		# УСЛОВИЕ ДЛЯ ЗАВЕРШЕНИЯ ИГРЫ
		# if len(panel_tanks_sprites.sprites()) == 0 and len(enemys_sprites.sprites()) == 0 and get_sum_desrtoyed_enemy() == ENEMYLIST.get_count():
		if len(enemys_sprites.sprites()) == 0 and get_sum_desrtoyed_enemy()+grenade_destroyed_enemys["g"] == ENEMYLIST.get_count():
			GAME_WIN = True
			grenade_destroyed_enemys["g"] = 0
			






		if SPAWN_ENEMY_STATUS==True and dict_PAUSE_GAME["g"] == False:
			# print('SPAWN_WORK')
			counter += 1

			if len(enemys_sprites.sprites()) < ENEMYS_COUNT_IN_BATTLE and counter > TIMER_RESPAWN_ENEMYS: # 45
				
				# random_level_list = ListEnemyForLEVEL(LEVELS_CONFIG, level_number)
				random_level_list = enemys_list_for_spawner["list"] #ENEMYLIST.get_list()
				
				

				counter_respawn_enemy += 1
				# if counter_respawn_enemy > RESPAWN_TIMER_ENEMY:


				try:
					enemy_tank = random_level_list[count_spawn]
					animation_spawn = SpawnEnemyAnimation(pos=(enemy_tank.rect.center), enemy_tank=enemy_tank)			
					enemys_spawn_animation_sprites.add(animation_spawn)
					count_spawn += 1

					list_sprites = panel_tanks_sprites.sprites()
					list_sprites[len(list_sprites)-1].kill()
				except Exception:
					pass
					# counter_respawn_enemy = 0


				counter = 0

			elif len(enemys_sprites.sprites()) == 0:
				CHANNEL_enemy_move.stop()
				
		

			# ВО ИЗБЕЖАНИЕ ПЕРЕГРУЗКИ ПРОГРАММЫ ОБНУЛЯЕМ СЧЕТЧИК КАЖДЫЕ 5000 ТАКТОВ
			if counter > 5000:
				counter = 0

		if player.hp <= 0:
			counter_respawn_player += 1
			if counter_respawn_player > RESPAWN_TIMER_PLAYER:	

				PLAYER_1_HP["now"] -= 1

				if PLAYER_1_HP["now"]>0:
					PLAYER["LVL1"]["hp"]=100
					PLAYER["lvl_start"]=1

					player = Tank(PLAYER)
					animation_spawn = SpawnEnemyAnimation(pos=(player.rect.center), enemy_tank=player)			
					enemys_spawn_animation_sprites.add(animation_spawn)
					counter_respawn_player = 0


		if PLAYER_1_HP["now"] <= 0:
			# GAME_OVER = True
			gameover_sprites.draw(screen)
			gameover_sprites.update()
			GAME_OVER = True
			CHANNEL_player_move.stop()


		# print(PLAYER_1_HP["now"])


		# Label(pos=[723, 419], text=str(PLAYER_1_HP["now"])).draw()
		if PLAYER_1_HP["now"]>0:
			PLAYER_1_HP_LABEL.set_text(str(PLAYER_1_HP["now"]))
			PLAYER_1_HP_LABEL.draw()
		else:
			PLAYER_1_HP_LABEL.set_text(str(0))
			PLAYER_1_HP_LABEL.draw()


		if counter_respawn_player > 5000:
			counter_respawn_player = 0

		try:
			if (base_sprites.sprites())[len(base_sprites.sprites())-1].index == 1:
				counter_respawn_player += 1
				if counter_respawn_player > RESPAWN_TIMER_PLAYER+5:
					gameover_sprites.draw(screen)
					gameover_sprites.update()
					GAME_OVER = True
					CHANNEL_player_move.stop()
		except Exception:
			pass


		
		

		
		if FILL_BLACK == True:
			# DISPLAY_COUNTSCORE.count_score()
			dict_RUN_SLIDE_NOW["g"] = 2
			# print('FILL_BLACK')
			FILL_BLACK = False
			NEXT_TIME = False



		
		# label_counter_respawn_player1.draw()

	elif dict_RUN_SLIDE_NOW["g"] == 10:
		# win_name = "BattleCity 20.20 - stage"+str(level_number)
		# display.set_caption(win_name)

		screen.fill(BLACK)
		# screen.fill(GREY)		
		# screen.fill(BLACK)


		# BG_CREDITS_PROGECT_TITLE.draw()


		for e in group_project_label:
			e.draw()


		screen.blit(NES_IMAGE, (50, project_label_start_y["g"]+30*10))
		draw.rect(screen, GREY_BLACK_DLC, (0, 0, WIDTH, 100))
		screen.blit(IMAGE_PROJECT_ICON, (20, 20))
		CREDITS_PROJECT.draw()
		CREDITS_PROJECT2.draw()

		draw.rect(screen, GREY_BLACK_DLC, (0, HEIGHT-55, WIDTH, 100))	
		CLOSE_PROJECT_LABEL.update()
			
		SysText(level=level_number["g"]).draw()





			





	elif dict_RUN_SLIDE_NOW["g"] == 2:
		

		# DISPLAY_COUNTSCORE.count_score()
		if NEXT_TIME == True:
			dict_RUN_SLIDE_NOW["g"] = 1
			# print('DICT_UPDATE')
		elif NEXT_TIME == False:
			screen.fill(BLACK)


			CHANNEL_enemy_move.stop()
			CHANNEL_player_move.stop()
			CHANNEL_bullet_collide_tank.stop()
			CHANNEL_bullet_collide_wall.stop()
			CHANNEL_shot_tanks.stop()
			CHANNEL_kill_enemy.stop()
			CHANNEL_bullet_collide_wall.stop()

			dict_PAUSE_GAME["g"] = True

			PLAYER_1_HP["now"] = PLAYER_1_HP["all"]
			
			#### MUSIC_pause_get.stop()

			text = battlecity_font.render("HI-score", 0, RED_COUNT, BLACK)
			(screen).blit(text, (195, 48))

			if level_number["g"] != 36:
				stage = battlecity_font.render("stage  "+str(level_number["g"]), 0, WHITE, BLACK)
			else:
				stage = battlecity_font.render("stage  custom", 0, WHITE, BLACK)

			(screen).blit(stage, (291, 96))

			i_player = battlecity_font.render("i-player", 0, RED_COUNT, BLACK)
			(screen).blit(i_player, (78, 144))

			# Сумма очков за пройденный уровень
			count_player_1 = str(get_sum_counts())
			# count_player_1 = "3000"
			end_str_count_player_1 = ""	
			end_str_count_player_1 += (5-len(count_player_1))*' '+count_player_1
		
			i_player_count = battlecity_font.render(end_str_count_player_1, 0, YELLOW_COUNT, BLACK)
			(screen).blit(i_player_count, (150, 192))


			# 285
			posy = 264
			posy2 = 255

			
			# i = 1
			TIMER_TOTAL_COUNTER["now"] += 1

			for i in range(1, 5):
				if TIMER_TOTAL_COUNTER["now"]  >= TIMER_TOTAL_COUNTER["all"] and COUNT_LVL[str(i)] < ROUND_COUNTS[str(i)]:
					MUSIC_total_tick.play()
					COUNT_LVL[str(i)] += int(COUNTER_RULES[str(i)])
					COUNT_DEMONSTRATION_LVL[str(i)] = str(COUNT_LVL[str(i)])

					COUNT_DEMONSTRATION_KILLS_LVL[str(i)] = str(COUNT_LVL[str(i)] // int(COUNTER_RULES[str(i)]))
					
					if COUNT_DEMONSTRATION_KILLS_LVL[str(i)] == "0":
						COUNT_DEMONSTRATION_KILLS_LVL[str(i)] = ' '

					if COUNT_DEMONSTRATION_LVL[str(i)] == "0":
						COUNT_DEMONSTRATION_LVL[str(i)] = ' '

					TIMER_TOTAL_COUNTER["now"] = 0



				end_str = (4-len(str(COUNT_DEMONSTRATION_LVL[str(i)])))*" "+str(COUNT_DEMONSTRATION_LVL[str(i)])		

				i_player_count_lvl1 = battlecity_font.render(end_str+' PTS '+((2-len(COUNT_DEMONSTRATION_KILLS_LVL[str(i)]))*' ')+COUNT_DEMONSTRATION_KILLS_LVL[str(i)], 0, WHITE, BLACK)
				(screen).blit(i_player_count_lvl1, (75, posy))

				try:
					screen.blit(image.load(f'{LOAD_TEXTURES}/gui/arrow.png'), (340, posy+7))
				except Exception:
					screen.blit(image.load(f'{DEFAULT_TEXTURES}/gui/arrow.png'), (340, posy+7))

				try:
					screen.blit(image.load(f'{LOAD_TEXTURES}/tanks/enemy/lvl{str(i)}_a1_r1.png'), (367, posy2+7))
				except Exception:
					screen.blit(image.load(f'{DEFAULT_TEXTURES}/tanks/enemy/lvl{str(i)}_a1_r1.png'), (367, posy2+7))
				posy += 72
				posy2 += 72





			# line = battlecity_font.render("-------", 0, WHITE, BLACK)


			for i in range(1, 5):
				if TIMER_TOTAL_COUNTER["now"]  >= TIMER_TOTAL_COUNTER["all"]:
					if COUNT_DEMONSTRATION_KILLS_LVL[str(i)] == " ":
						COUNT_DEMONSTRATION_KILLS_LVL[str(i)] = '0'
						TIMER_TOTAL_COUNTER["now"] = 0


					if COUNT_DEMONSTRATION_LVL[str(i)] == " ":
						COUNT_DEMONSTRATION_LVL[str(i)] = '0'
						TIMER_TOTAL_COUNTER["now"] = 0





			total = battlecity_font.render("total", 0, WHITE, BLACK)
			(screen).blit(total, (150, 528))



			sum_destroyed = 0
			for i in range(1, 5):
				sum_destroyed += int(ROUND_COUNTS[str(i)] // int(COUNTER_RULES[str(i)]))
			
			if TIMER_TOTAL_COUNTER["now"]  >= TIMER_TOTAL_COUNTER["all"]:
				total_sum_destroyed = battlecity_font.render((2-len(str(sum_destroyed)))*" "+str(sum_destroyed), 0, WHITE, BLACK)
				(screen).blit(total_sum_destroyed, (294, 528))


			try:
				(screen).blit(image.load(f'{LOAD_TEXTURES}/gui/line.png'), (288, 519+7))
			except Exception:
				(screen).blit(image.load(f'{DEFAULT_TEXTURES}/gui/line.png'), (288, 519+7))


			if TIMER_TOTAL_COUNTER["now"]  >= TIMER_TOTAL_COUNTER["all"]*BUST_TIMER_DEMONSTRATION_COUNT_LVL and GAME_WIN == True:
				GAME_WIN = False

				level_number["g"] += 1
				count_spawn = 0

				# enemys_list_for_spawner["list"] = ReloadBattle(level_number)
				# NEXT_TIME = True
				dict_RUN_SLIDE_NOW["g"] = 5
				zero_counts()
				clear_player1_bonus()

				grey_screen_top = GreyScreen((0, -400), "top", 1)
				grey_screen_down = GreyScreen((0, HEIGHT), "down", 1)

				grey_screens_sprites.add(grey_screen_top)
				grey_screens_sprites.add(grey_screen_down)




			if TIMER_TOTAL_COUNTER["now"]  >= TIMER_TOTAL_COUNTER["all"]*BUST_TIMER_DEMONSTRATION_COUNT_LVL and GAME_OVER == True:
				# DISPLAY_GAMEOVER.CLEAR_ALL_DISPLAY()
				dict_RUN_SLIDE_NOW["g"] = 3
			




	elif dict_RUN_SLIDE_NOW["g"] == 3:
		win_name = "BattleCity 20.20 - Game over"

		
		screen.fill(BLACK)

		if GAME_OVER == True and GAME_INTERFACE_DICT["game_over_bricks_sound"]==0:
			# CHANNEL_gui_music.play(MUSIC_game_over)
			EMPTY_ALL_SPRITES()
			MUSIC_game_over.play()
			GAME_INTERFACE_DICT["game_over_bricks_sound"]=1
			# dict_RUN_SLIDE_NOW["g"]=4


		if GAME_INTERFACE_DICT["game_over_bricks_sound"]==1:
			TIMER_EXIT_MENU_GAMEOVER["now"] += 1

		if TIMER_EXIT_MENU_GAMEOVER["now"] >= TIMER_EXIT_MENU_GAMEOVER["all"]:
			# print('i am here')
			TIMER_EXIT_MENU_GAMEOVER["now"] = 0
			# dict_RUN_SLIDE_NOW["g"] = 4

			count_spawn = 0
			level_number["g"] = 1
			

			if TYPE_RIGHT_INTERFACE == 1:
				ROCKET_COLUMN["now"] = -1
			elif TYPE_RIGHT_INTERFACE == 2:
				ROCKET_COLUMN["now"] = RC
				

			title_menu_sprite = TITLE_MENU((84, 80))
			menu_content_sprites.add(title_menu_sprite)
			if len(grey_screens_sprites.sprites()) != 2:
				grey_screens_sprites.empty()
				grey_screen_top, grey_screen_down = CreateGreyScreens()

			dict_PAUSE_GAME["g"] = False
			GAME_OVER = False
			GAME_INTERFACE_DICT["game_over_bricks_sound"] = 0
			# lvl_start = 1
			PLAYER_LEVEL_START = 1

			PLAYER["lvl_start"] = PLAYER_LEVEL_START
			player_sprites.empty()
			zero_counts()
			clear_player1_bonus()

			
			

			# quit()
			# sys.exit()
			# ESC_PRESSED()
			PLAYER = {
				"LVL1": {
					"hp": 100,
					"damage": 100,
					"speed": TANK_SPEED,
					"bullet_speed": BULLET_SPEED,
					"type_player": "player", 
				},

				"LVL2": {
					"hp": 100,
					"damage": 100,
					"speed": TANK_SPEED,
					"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
					"type_player": "player",
				},

				"LVL3": {
					"hp": 100,
					"damage": 100,
					"speed": TANK_SPEED,
					"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
					"type_player": "player",
				},

				"LVL4": {
					"hp": 100,
					"damage": 100,
					"speed": TANK_SPEED,
					"bullet_speed": BULLET_SPEED+BUST_BULLET_SPEED,
					"type_player": "player",
				},

				"lvl_start": PLAYER_LEVEL_START,
			}



			dict_RUN_SLIDE_NOW["g"] = 4
			count_spawn = 0
			level_number["g"] = 1
			# clone_START_RESPAWN_COUNT = START_RESPAWN_COUNT


			
			player_sprites.empty()

			if TYPE_RIGHT_INTERFACE == 1:
				ROCKET_COLUMN["now"] = -1
			elif TYPE_RIGHT_INTERFACE == 2:
				if CHEAT_MODE == False:
					ROCKET_COLUMN["now"] = 3
				else:
					ROCKET_COLUMN["now"] = 999

			title_menu_sprite = TITLE_MENU((84, 80))
			menu_content_sprites.add(title_menu_sprite)
			if len(grey_screens_sprites.sprites()) != 2:
				grey_screens_sprites.empty()
				grey_screen_top, grey_screen_down = CreateGreyScreens()





		



		gameover_bricks_sprites.draw(screen)



	elif dict_RUN_SLIDE_NOW["g"] == 5:
		if level_number["g"] <= 36:
			if level_number["g"] != 36:
				win_name = "BattleCity 20.20 - Stage "+str(level_number["g"])
			else:
				win_name = "BattleCity 20.20 - Stage custom"
		else:
			level_number["g"] = 1
			win_name = "BattleCity 20.20 - Stage "+str(level_number["g"])
			count_spawn = 0
			# clone_START_RESPAWN_COUNT = START_RESPAWN_COUNT
			
			



		screen.fill(BLACK)

		EMPTY_ALL_SPRITES()
		player_sprites.empty()

		grey_screens_sprites.draw(screen)
		grey_screens_sprites.update()


		SysText(level=level_number["g"]).draw()


		collide_greys = pygame.sprite.collide_rect(grey_screen_top, grey_screen_down)
		if collide_greys:
			# print('OK')

			if level_number["g"] != 36:
				stage_label = battlecity_font_stage.render("STAGE "+str(level_number["g"]), 0, BLACK, BATTLE_BG_COLOR)
			else:
				stage_label = battlecity_font_stage.render("STAGE CUSTOM", 0, BLACK, BATTLE_BG_COLOR)

			screen.blit(stage_label, [(WIDTH)//2-stage_label.get_width()//2, (HEIGHT)//2-20])

			
			timer_replace_movetype_greys += 1

			if timer_replace_movetype_greys == TIMER_REPLACE_MOVETYPE_GREYS//2-20:
				# MUSIC_INTRO.set_volume(set_volume)
				MUSIC_INTRO.play()


			if timer_replace_movetype_greys == TIMER_REPLACE_MOVETYPE_GREYS:
				grey_screen_top.move_type = 2
				grey_screen_down.move_type = 2
				k = 1


		if grey_screen_top.return_true_for_end_move2() == True and grey_screen_down.return_true_for_end_move2() == True and k == 1:
			k = 0
			grey_screens_sprites.empty()



			dict_RUN_SLIDE_NOW["g"] = 1
			timer_replace_movetype_greys = 0



			if level_number["g"] <= 36:
				if level_number["g"] != 36:
					ReloadBattle(level_number["g"])
				else:
					ReloadBattle(level_number["g"], True, LOAD_ENEMY_CONFIG["g"])
			else:
				set_slide_number(4)
				set_slide_battle()
	



			player_sprites.empty()
			
			# print('EMPTY')







	elif dict_RUN_SLIDE_NOW["g"] == 4:
		###### ГЛАВНОЕ МЕНЮ ######
		
		win_name = "BattleCity 20.20"

		project_label_start_y["g"] = 120
		for el in group_project_label:
			el.update_pos([20, project_label_start_y["g"]+30*group_project_label.index(el)])
		
		screen.fill(BLACK)

		EMPTY_ALL_SPRITES()
		player_sprites.empty()

		vidget_campaigns_dlc_btn.text = " campaigns "
		text_description_descr_dlc.set_text(default_text_description)
		text_description_descr_dlc.set_fg(GREY)
		text_description_descr_dlc.update_pos(["cx", 607])
		text_author_dlc.set_text(" ")
		text_version_dlc.set_text(" ")


		SysText(level=level_number["g"], bg=BLACK).draw()


		menu_content_sprites.draw(screen)
		menu_content_sprites.update()
		try:
			screen.blit(bg_image, (x2020, y2020))
		except Exception:
			pass
		(screen).blit(author_text, (place_author_x, menu_start_y))

		update_buttons()

		# respawn_count_panel.count = START_RESPAWN_COUNT
		

		screen.blit(text2020, (WIDTH//2-text2020.get_width()//2, 168))
		# display.set_caption(win_name + " - MENU")
		flag_minus_restart = False

		LABEL_VERSION_TITLE.draw()
		

		

	elif dict_RUN_SLIDE_NOW["g"] == 6:
		win_name = "BattleCity 20.20 - Construction"


		screen.fill(CONSTRUCTION_BG_COLOR)

		EMPTY_ALL_SPRITES()
		player_sprites.empty()


		SysText(level=level_number["g"], bg=()).draw()


		BATTLE_POLE = draw.rect(screen, BLACK, (SPAWN_POLE[0], SPAWN_POLE[1], WIDTH_POLE, HEIGHT_POLE))





		counter_click_rotate_block = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_r]:
			counter_click_rotate_block += 1
			if counter_click_rotate_block <= 1:
				if brick_button.get_mouse_block()==True:
					brick_button.del_mouse_block()
					brick_button2.set_mouse_block()

				elif brick_button2.get_mouse_block()==True:
					brick_button2.del_mouse_block()
					brick_button3.set_mouse_block()

				elif brick_button3.get_mouse_block() == True:
					brick_button3.del_mouse_block()
					brick_button4.set_mouse_block()

				elif brick_button4.get_mouse_block() == True:
					brick_button4.del_mouse_block()
					brick_button.set_mouse_block()



				elif beton_button1.get_mouse_block() == True:
					beton_button1.del_mouse_block()
					beton_button2.set_mouse_block()

				elif beton_button2.get_mouse_block() == True:
					beton_button2.del_mouse_block()
					beton_button3.set_mouse_block()

				elif beton_button3.get_mouse_block() == True:
					beton_button3.del_mouse_block()
					beton_button4.set_mouse_block()

				elif beton_button4.get_mouse_block() == True:
					beton_button4.del_mouse_block()
					beton_button1.set_mouse_block()

				counter_click_rotate_block = 0
			else:
				counter_click_rotate_block = 0




		# button_back.update()
		# button_back_text.update()
		for e in list_construction_button:
			e.update()


		if VIEW_BASE["g"]:
			screen.blit(const_img_base, (336, 601))
			# const_brick_base
			screen.blit(const_brick_base, (312, 601-24))
			screen.blit(const_brick_base, (312, 601))
			screen.blit(const_brick_base, (312, 601+24))
			screen.blit(const_brick_base, (312+24, 601-24))
			screen.blit(const_brick_base, (312+24*2, 601-24))
			screen.blit(const_brick_base, (312+24*3, 601-24))
			screen.blit(const_brick_base, (312+24*3, 601))
			screen.blit(const_brick_base, (312+24*3, 601+24))
			# const_p1_base
			screen.blit(const_p1_base, (243, 610))
			screen.blit(const_p2_base, (441-3, 610))
			# const_e1_base
			screen.blit(const_e1_base, (48+3, 25+3))
			screen.blit(const_e1_base, (339, 28))
			screen.blit(const_e1_base, (628, 28))





		for e in list_special_buttons:
			e.update()

		brick_full_button.update()
		brick_button.update()
		brick_button2.update()
		brick_button3.update()
		brick_button4.update()
		beton_button.update()
		beton_button1.update()
		beton_button2.update()
		beton_button3.update()
		beton_button4.update()
		bush_button.update()
		water_button.update()

		if VIEW_GRID["g"]:
			for i in range(14):
				pygame.draw.line(screen, WHITE, (start_x_line, start_y_line), (start_x_line, HEIGHT_POLE+SPAWN_POLE[1]-1), 1)
				start_x_line += 48
			
			start_x_line = SPAWN_POLE[0]

			for i in range(14):
				pygame.draw.line(screen, WHITE, (start_x_line, start_y_line), (start_x_line+WIDTH_POLE, start_y_line), 1)
				start_y_line += 48

		start_y_line = SPAWN_POLE[1]

		pygame.draw.line(screen, GREY, (720, SPAWN_POLE[1]), (720, 12*48+24), 1)
		pygame.draw.line(screen, GREY, (720+48, SPAWN_POLE[1]), (720+48, 12*48+24), 1)

		for i in range(13):
			pygame.draw.line(screen, GREY, (720, start_y_line), (720+48, start_y_line), 1)
			start_y_line += 48


		start_y_line = SPAWN_POLE[1]















	elif dict_RUN_SLIDE_NOW["g"] == 7:
		"""Выбор сложности уровня"""
		win_name = "BattleCity 20.20 - Select difficulty"


		screen.fill(BLACK)

		EMPTY_ALL_SPRITES()
		player_sprites.empty()


		SysText(level=level_number["g"], bg=()).draw()

		# battlecity_font.render((0,0), BLACK, WHITE, "text")
		battlecity_font5 = pygame.font.Font('data\\fonts\\2003.ttf', 45)
		text = battlecity_font5.render("Select difficulty", 0, WHITE, BLACK)
		(screen).blit(text, (WIDTH//2-text.get_width()//2, 50))

		# button_back_to_const_text.update()
		# pygame.draw.rect(screen, CONSTRUCTION_BG_COLOR, (0, 580, WIDTH, HEIGHT), 2)


		for e in list_buttons_choise_difficult:
			e.update()


		# WIDTH//2-button_bg_level_difficult_lvl1_CLASS.get_width()//2, y_difficult_buttons

		# LOAD_ENEMY_CONFIG["g"]
		# print(y_difficult_buttons)

		### EASY BUTTON ###
		screen.blit(text_level_dif_lvl1, (WIDTH//2-text_level_dif_lvl1.get_width()//2, y_difficult_buttons+15))
		screen.blit(enemy_tank_lvl1, (254, 165))
		screen.blit(black_arrow, (254+48, 165+12))
		screen.blit(text_count_dif_lvl1, (254+48+25, 165+7))

		screen.blit(enemy_tank_lvl2, (254, 165+48+10))
		screen.blit(black_arrow, (254+48, 165++48+10+12))
		screen.blit(text_count_dif_lvl2, (254+48+25, 165+48+10+7))

		screen.blit(enemy_tank_lvl3, (420, 165))
		screen.blit(black_arrow, (420+48, 165+12))
		screen.blit(text_count_dif_lvl3, (420+48+25, 165+7))


		screen.blit(enemy_tank_lvl4, (420, 165+48+10))
		screen.blit(black_arrow, (420+48, 165++48+10+12))
		screen.blit(text_count_dif_lvl4, (420+48+25, 165+48+10+7))

		


		### MEDIUM BUTTON ###
		screen.blit(text_level_dif_lvl2, (WIDTH//2-text_level_dif_lvl2.get_width()//2, 320))
		screen.blit(enemy_tank_lvl1, (254, 326+33))
		screen.blit(black_arrow, (254+48, 326+33+12))
		screen.blit(text_count_medium_dif_lvl1, (254+48+25, 326+33+7))

		screen.blit(enemy_tank_lvl2, (254, 326+33+58))
		screen.blit(black_arrow, (254+48, 326+33+12+58))
		screen.blit(text_count_medium_dif_lvl2, (254+48+25, 326+33+7+58))

		screen.blit(enemy_tank_lvl3, (254+166, 326+33))
		screen.blit(black_arrow, (254+48+166, 326+33+12))
		screen.blit(text_count_medium_dif_lvl3, (254+48+25+166, 326+33+7))

		screen.blit(enemy_tank_lvl4, (254+166, 326+33+58))
		screen.blit(black_arrow, (254+48+166, 326+33+12+58))
		screen.blit(text_count_medium_dif_lvl4, (254+48+25+166, 326+33+7+58))



		### HARD BUTTON ###
		screen.blit(text_level_dif_lvl3, (WIDTH//2-text_level_dif_lvl3.get_width()//2, 514))
		screen.blit(enemy_tank_lvl1, (254, 520+33))
		screen.blit(black_arrow, (254+48, 520+33+12))
		screen.blit(text_count_hard_dif_lvl1, (254+48+25, 520+33+7))

		screen.blit(enemy_tank_lvl2, (254, 520+33+58))
		screen.blit(black_arrow, (254+48, 520+33+12+58))
		screen.blit(text_count_hard_dif_lvl2, (254+48+25, 520+33+7+58))

		screen.blit(enemy_tank_lvl3, (254+166, 520+33))
		screen.blit(black_arrow, (254+48+166, 520+33+12))
		screen.blit(text_count_hard_dif_lvl3, (254+48+25+166, 520+33+7))

		screen.blit(enemy_tank_lvl4, (254+166, 520+33+58))
		screen.blit(black_arrow, (254+48+166, 520+33+12+58))
		screen.blit(text_count_hard_dif_lvl4, (254+48+25+166, 520+33+7+58))













	elif dict_RUN_SLIDE_NOW["g"] == 8:
		"""Выбор кампании/dlc. Открывается после нажатия на кнопку PLAY в главном меню"""
		win_name = "BattleCity 20.20 - Select Campaign"
		button_back.command = (lambda: set_slide_number(4))



		screen.fill(BLACK)

		EMPTY_ALL_SPRITES()
		player_sprites.empty()


		SysText(level=level_number["g"], bg=()).draw()

		button_back.update()

		label_select_campaign.draw()

		# pygame.draw.rect(screen, (20,20,20), (0, HEIGHT//6, WIDTH, HEIGHT//2+HEIGHT//4))
		pygame.draw.rect(screen, GREY_BLACK_DLC, (0, 200, WIDTH, 335+19))
		# pygame.draw.rect(screen, (20,20,20), (0, 200, WIDTH, HEIGHT//2+HEIGHT//6))

		if vidget_campaigns_dlc_btn.text.replace(" ", "") == "campaigns":
			for e in list_campaign_buttons:
				e.update()

				if e.check_focus() == True:
					if list_string_campaigns_description[list_campaign_buttons.index(e)] != "no description":
						text_description_descr_dlc.set_text(list_string_campaigns_description[list_campaign_buttons.index(e)])
						text_description_descr_dlc.set_fg(WHITE)
					else:
						text_description_descr_dlc.set_text(list_string_campaigns_description[list_campaign_buttons.index(e)])
						text_description_descr_dlc.set_fg(RED_COUNT)

					text_author_dlc.set_text("battlecity 20.20")
					text_version_dlc.set_text("none")
					text_description_descr_dlc.update_pos(["cx", 607])

		else:
			try:
				text_you_have_not_dlc.draw()
			except Exception:
				pass

			for e in list_dlc_buttons:
				e.update()

			for e in list_dlc_buttons:
				if e.check_focus() == True:
					if list_string_dlc_description[list_dlc_buttons.index(e)] != "no description":
						text_description_descr_dlc.set_text(list_string_dlc_description[list_dlc_buttons.index(e)])
						text_description_descr_dlc.set_fg(WHITE)
					else:
						text_description_descr_dlc.set_text(list_string_dlc_description[list_dlc_buttons.index(e)])
						text_description_descr_dlc.set_fg(RED_COUNT)

					text_author_dlc.set_text(list_string_dlc_author[list_dlc_buttons.index(e)])
					# list_string_dlc_version 
					text_version_dlc.set_text(list_string_dlc_version[list_dlc_buttons.index(e)])
					text_description_descr_dlc.update_pos(["cx", 607])

		for e in list_vidget_campaigns_dlc:
			e.update()


		
		for e in list_text_content_dlc_description:
			e.draw()


	elif dict_RUN_SLIDE_NOW["g"] == 9:
		"""Меню выбора уровня. Будут распологаться квадратики со скругленными углами с миникартами, внутри. Если уровень закрыт, миникарта будет затемнена"""
		set_slide_battle()
		# win_name = "BattleCity 20.20 - Select level"


		# screen.fill(BLACK)

		# EMPTY_ALL_SPRITES()
		# player_sprites.empty()


		# SysText(level=level_number["g"], bg=()).draw()

		# button_back.update()
		# button_back.command = (lambda: set_slide_number(8))

		# label_select_level.draw()

		# for e in levels_imagebuttons_list:
		# 	e.update()






	if len(player_sprites.sprites()) >= 2:
		player_sprites.sprites()[1].kill()

	if next_window_mode == pygame.FULLSCREEN:
		screen.blit(IMAGE_FULLSCREEN_BORDER, (0,0))
		# screen.fill(BLACK)

	display.update()
	display.flip()
	display.set_caption(win_name)
