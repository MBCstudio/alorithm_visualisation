import math
import pygame
import random

pygame.init()


class Info_visualistion():
    # static colours
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    GREYS = [
        (128, 128, 128),
        (160, 160, 160),
        (180, 180, 180)
    ]
    BG_COLOUR = WHITE
    # fonts
    FONT = pygame.font.SysFont("comicsans", 20)
    LARGE_FONT = pygame.font.SysFont("comicsans", 30)
    # static paddings
    TOP_PAD = 150
    SIDE_PAD = 100

    def __init__(self, height, width, lst):
        self.height = height
        self.width = width

        self.window = pygame.display.set_mode((width, height))  # iniial of window
        pygame.display.set_caption("Algorithm visualizer")
        self.set_lst(lst)  # creationof list

    def set_lst(self, lst):
        self.lst = lst
        self.min = min(lst)
        self.max = max(lst)

        self.bar_width = round(self.width - self.SIDE_PAD) / len(lst)  # calculation of one bar width
        self.bar_height = math.floor(self.height - self.TOP_PAD) / (self.max - self.min)  # calculation of height for 'height step'
        self.start_x = self.SIDE_PAD // 2  # starting point (first bar)


def draw(Info_visualistion, algorithm_name, ascending):
    Info_visualistion.window.fill(Info_visualistion.BG_COLOUR)  # filling background with color

    if ascending == True:
        ascending_string = "Ascending"
    else:
        ascending_string = "Decending"

    main_info = Info_visualistion.LARGE_FONT.render(f"{algorithm_name.__name__} -- {ascending_string}",1,Info_visualistion.GREEN)
    Info_visualistion.window.blit(main_info,(Info_visualistion.width/2-main_info.get_width()/2,5))

    controls = Info_visualistion.FONT.render("R - Reset | SPACE - Start sorting | A - Ascending | D - Decending", 1,
                                             Info_visualistion.BLACK)  # rendering text on our window
    Info_visualistion.window.blit(controls, (Info_visualistion.width / 2 - controls.get_width() / 2, 40))  # placing text on window in corrert place on screen

    sorting = Info_visualistion.FONT.render("B - Bubble Sort | I - Insert Sort", 1, Info_visualistion.BLACK)
    Info_visualistion.window.blit(sorting, (Info_visualistion.width / 2 - sorting.get_width() / 2, 70))

    draw_bars(Info_visualistion)
    pygame.display.update()


def draw_bars(Info_visualisation, color_position={}, bg_clear=False):
    lst = Info_visualisation.lst

    if bg_clear:
        clear_rect = (Info_visualisation.start_x, Info_visualisation.TOP_PAD, Info_visualisation.width-Info_visualisation.SIDE_PAD, Info_visualisation.height-Info_visualisation.TOP_PAD)
        pygame.draw.rect(Info_visualisation.window, Info_visualisation.BG_COLOUR, clear_rect)

    for i, val in enumerate(lst):
        x = Info_visualisation.start_x + i * Info_visualisation.bar_width  # placing each bar in a correct position
        y = Info_visualisation.height - (val- Info_visualisation.min) * Info_visualisation.bar_height  # computing height of each bar based on real height that is on the list (2 uwagi minimalne słupi są punktem odniesniea czyli nie wiadać ich na ekranie są trakotowanie jako punkt 0, 2 uwaga to że wielkosc y działa odwrotnie czyli dla wielkiści y = maksymalnej wysokości to wyskowość malowania słupka jest najmnejsza (w przypadku y=height to słupka nie ma bo jesgo wielkosc równa jest y = heihgt-height=0))

        colour = Info_visualisation.GREYS[i % 3] #bars will be in a diffrent grey color
        if i in color_position:
            colour = color_position[i]

        pygame.draw.rect(Info_visualisation.window, colour,
                         (x, y, Info_visualisation.bar_width, Info_visualisation.height))#drawing rectangle x,y - where is start point and how big is the bar after scaling

    if bg_clear:
        pygame.display.update()

def create_starting_lst(n, min, max):
    lst = []
    for i in range(n):
        val = random.randint(min, max)
        lst.append(val)

    return lst

def bubble_sorting(Info_visualisation, ascending = True):
    lst = Info_visualisation.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num_1 = lst[j]
            num_2 = lst[j+1]
            if (num_1>num_2 and ascending) or (num_1<num_2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_bars(Info_visualisation, {j: Info_visualistion.GREEN, j+1:Info_visualisation.RED}, True)
                yield True

    return lst

def insret_sorting(Info_visualisation, ascending = True):
    lst = Info_visualisation.lst

    for i in range(1,len(lst)):
        key = lst[i]
        j = i-1
        while (j>=0 and key<lst[j] and ascending == True) or (j>=0 and key>lst[j] and not ascending):
            lst[j+1] = lst[j]
            j-=1
            draw_bars(Info_visualisation, {j: Info_visualistion.GREEN, j + 1: Info_visualisation.RED}, True)
            yield True
        lst[j+1] = key

def main():
    #init and var
    flag = True
    ascending = True
    sorting = False
    clock = pygame.time.Clock()

    #current algorithm
    sorting_algorithm = bubble_sorting
    sorting_algorithm_generator = None

    #creating a list
    n = 10
    min = 10
    max = 100
    lst = create_starting_lst(n, min, max)
    visualisation = Info_visualistion(600, 800, lst)

    while flag:
        clock.tick(40)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(visualisation, sorting_algorithm, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = create_starting_lst(n, min, max)
                visualisation.set_lst(lst)
                sorting = False
                print(lst)
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(visualisation,ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sorting
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insret_sorting

    pygame.quit()

if __name__ == "__main__":
    main()