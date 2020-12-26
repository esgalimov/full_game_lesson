import pygame
import sys
import os


level_name = input('Введите имя файла с уровнем (map.txt, map2.txt, map3.txt, map4.txt): ')
if not os.path.isfile(os.path.join('data', level_name)):
    print(f"Файл {level_name} не найден")
    sys.exit()
pygame.init()
pygame.display.set_caption('Перемещение героя')
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
FPS = 50
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player = None


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            self.add(walls_group)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def go_up(self):
        self.rect = self.rect.move(0, -50)
        if pygame.sprite.spritecollide(self, walls_group, False):
            self.rect = self.rect.move(0, 50)

    def go_down(self):
        self.rect = self.rect.move(0, 50)
        if pygame.sprite.spritecollide(self, walls_group, False):
            self.rect = self.rect.move(0, -50)

    def go_left(self):
        self.rect = self.rect.move(-50, 0)
        if pygame.sprite.spritecollide(self, walls_group, False):
            self.rect = self.rect.move(50, 0)

    def go_right(self):
        self.rect = self.rect.move(50, 0)
        if pygame.sprite.spritecollide(self, walls_group, False):
            self.rect = self.rect.move(-50, 0)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["МАРИО", "",
                  "Правила игры",
                  "Чтобы ходить, нажимайте на стрелочки",]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


run = True
clock = pygame.time.Clock()
start_screen()
player, level_x, level_y = generate_level(load_level(level_name))
camera = Camera()
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
           if event.key == 1073741906:
               player.go_up()
           if event.key == 1073741905:
               player.go_down()
           if event.key == 1073741904:
               player.go_left()
           if event.key == 1073741903:
               player.go_right()
    screen.fill(pygame.Color([0, 0, 0]))
    # изменяем ракурс камеры
    camera.update(player);
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    player_group.update()
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
terminate()
