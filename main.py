import sys, pygame
from pygame import gfxdraw
from pygame.locals import *
from KenKen import *
random.seed(102)

red = (255, 15, 86)
blue = (67, 181, 238)
white = (255, 255, 255)
dark_blue = (14, 26, 37)
dark_white = (180, 180, 180)
width = 1280
height = 720

# ken ken stuff
available_operators = ["+", "x", "-", "÷"]
max_cage_size = 3
current_size = 4
current_kenken = KenKen(current_size, available_operators, max_cage_size) # default kenken

# main loop
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("KenKen Generator")
font = pygame.font.Font('freesansbold.ttf', 30)

screen = pygame.display.set_mode((1280, 720))
pygame.mouse.set_cursor(*pygame.cursors.diamond)
default_font = pygame.font.get_default_font()
font_renderer = pygame.font.Font(default_font, 15)
operator_colors = [white, white, white, white]
solution_color = dark_white
show_solution = False

def get_cage(box, current_kenken):
    for cage in current_kenken.cages:
        if (cage.is_in_cage(box)):
            return cage

while True:
    clock.tick(30)
    # quit condition
    # print(available_operators)
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if event.type == MOUSEBUTTONUP:
            if mouseX > 210 and mouseX < 210 + 50 and mouseY > 180 and mouseY < 180 + 20 and current_size > 2:
                current_size -= 1
                pygame.time.wait(100)
            elif mouseX > 210 and mouseX < 210 + 50 and mouseY > 150 and mouseY < 150 + 20:
                current_size += 1
                pygame.time.wait(100)
            elif mouseX > 50 and mouseX < 100 and mouseY > 210 and mouseY < 210 + 50:
                if operator_colors[0][0] == 255:
                    available_operators[0] = ''
                    operator_colors[0] = dark_white
                else:
                    available_operators[0] = '+'
                    operator_colors[0] = white
            elif mouseX > 110 and mouseX < 110 + 50 and mouseY > 210 and mouseY < 210 + 50:
                if operator_colors[1][1] == 255:
                    available_operators[1] = ''
                    operator_colors[1] = dark_white
                else:
                    available_operators[1] = 'x'
                    operator_colors[1] = white
            elif mouseX > 50 and mouseX < 50 + 50 and mouseY > 270 and mouseY < 270 + 50:
                if operator_colors[2][2] == 255:
                    available_operators[2] = ''
                    operator_colors[2] = dark_white
                else:
                    available_operators[2] = '-'
                    operator_colors[2] = white
            elif mouseX > 110 and mouseX < 110 + 50 and mouseY > 270 and mouseY < 270 + 50:
                if operator_colors[3][2] == 255:
                    available_operators[3] = ''
                    operator_colors[3] = dark_white
                else:
                    available_operators[3] = '÷'
                    operator_colors[3] = white
            elif mouseX > 50 and mouseX < 50 + 260 and mouseY > 380 and mouseY < 380 + 50:
                if solution_color == white:
                    solution_color = dark_white
                    show_solution = False
                else:
                    solution_color = white
                    show_solution = True
            elif mouseX > 50 and mouseX < (50 + 375) and mouseY > 90 and mouseY < (90 + 50):
                current_kenken = KenKen(current_size, available_operators, max_cage_size)
                show_solution = False
                solution_color = dark_white

    # clear screen
    screen.fill(dark_blue)
    # get mouse position
    mouseX, mouseY = pygame.mouse.get_pos()
    # print(f"{mouseX} {mouseY}")
    # draw buttons
    pygame.draw.rect(screen, white, (50, 90, 375, 50))
    tText = font.render("Generate New KenKen", True, dark_blue)
    screen.blit(tText, (70, 100))
    # print(f"{mouseX} and {mouseY}")

    pygame.draw.rect(screen, white, (50, 150, 150, 50))
    tText = font.render(f"Size:  {str(current_size)}", True, dark_blue)
    screen.blit(tText, (70, 160))

    pygame.draw.rect(screen, white, (210, 150, 50, 20))
    tText = font.render("^", True, dark_blue)
    screen.blit(tText, (225, 150))

    pygame.draw.rect(screen, white, (210, 180, 50, 20))
    tText = font.render("v", True, dark_blue)
    screen.blit(tText, (225, 175))

    pygame.draw.rect(screen, operator_colors[0], (50, 210, 50, 50))
    tText = font.render("+", True, dark_blue)
    screen.blit(tText, (66, 218))

    pygame.draw.rect(screen, operator_colors[1], (110, 210, 50, 50))
    tText = font.render("x", True, dark_blue)
    screen.blit(tText, (130, 218))

    pygame.draw.rect(screen, operator_colors[2], (50, 270, 50, 50))
    tText = font.render("-", True, dark_blue)
    screen.blit(tText, (69, 287))

    pygame.draw.rect(screen, operator_colors[3], (110, 270, 50, 50))
    tText = font.render("÷", True, dark_blue)
    screen.blit(tText, (130, 280))

    pygame.draw.rect(screen, solution_color, (50, 380, 260, 50))
    tText = font.render("Show Solution", True, dark_blue)
    screen.blit(tText, (70, 390))







    line_size = 600 / current_kenken.size
    for i in range(len(current_kenken.board)):
        for j in range(len(current_kenken.board[0])):
            wid = 10
            # find current cage
            current_cage = get_cage(current_kenken.boxes[i * current_kenken.size + j], current_kenken)
            # top
            wid = 10
            if i != 0 and j < current_kenken.size and i < current_kenken.size and current_cage == get_cage(current_kenken.boxes[(i - 1) * current_kenken.size + j], current_kenken):
                wid = 1
            pygame.draw.line(screen, white, (500 + line_size * j, 90 + line_size * i),
                             (500 + line_size * j + line_size, 90 + line_size * i), width=wid)

            # left
            wid = 10
            if j != 0 and j < current_kenken.size and i < current_kenken.size and current_cage == get_cage(current_kenken.boxes[i * current_kenken.size + (j - 1)], current_kenken):
                wid = 2
            pygame.draw.line(screen, white, (500 + line_size * j, 90 + line_size * i),
                         ((500 + line_size * j), 90 + line_size * (i + 1)), width=wid)

            # down
            wid = 10
            if j < current_kenken.size and i < current_kenken.size - 1 and current_cage == get_cage(current_kenken.boxes[(i + 1) * current_kenken.size + j], current_kenken):
                wid = 1
            pygame.draw.line(screen, white, (500 + line_size * j, 90 + line_size * (i + 1)),
                             (500 + line_size * j + line_size, 90 + line_size * (i + 1)), width=wid)

            # right
            wid = 10
            if j < current_kenken.size - 1 and i < current_kenken.size and current_cage == get_cage(current_kenken.boxes[i * current_kenken.size + (j + 1)], current_kenken):
                wid = 1
            pygame.draw.line(screen, white, (500 + line_size * (j + 1), 90 + line_size * i),
                             ((500 + line_size * (j + 1)), 90 + line_size * (i + 1)), width=wid)

            if show_solution:
                tText = font.render(f"{current_kenken.board[i][j]}", True, white)
                screen.blit(tText, (500 + (line_size / 2) + line_size * j, 90 + (line_size / 2) + line_size * i))

            if current_cage.cage_size == 1:
                tText = font.render(f"{current_kenken.board[i][j]}", True, white)
                screen.blit(tText, (500 + (line_size / 2) + line_size * j, 90 + (line_size / 2) + line_size * i))

            if current_kenken.boxes[i * current_kenken.size + j] == current_cage.boxes[0] and current_cage.cage_size != 1:
                tText = font.render(f"{current_cage.target_num}{current_cage.operator}", True, white)
                screen.blit(tText, (500 + (line_size / 5) + line_size * j, 90 + (line_size / 5) + line_size * i))


    pygame.display.flip()