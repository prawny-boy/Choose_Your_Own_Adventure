import pygame
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Time Travel Adventure")

# Screen colour
screen.fill((0, 0, 0))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CAMBRIDGE_BLUE = (131, 182, 146)
MELON = (249, 173, 160)
BRIGHT_PINK_CRAYOLA = (249, 98, 125)
BLUSH = (198, 91, 124)
VIOLET_JTC = (91, 55, 88)

# Fonts
fontBasic = pygame.font.Font(None, 32)
fontPoppins =  pygame.font.Font("Choose_Your_Own_Adventure/Pygame/Fonts/Poppins Regular 400.ttf", 32)
fontPoppinsBold =  pygame.font.Font("Choose_Your_Own_Adventure/Pygame/Fonts/Poppins Bold 700.ttf", 32)
# POPPINS FONT CREDITS
# Poppins
# Designed by Indian Type Foundry, Jonny Pinhorn, Ninad Kale 

# Helper function to display text on the screen
def draw_text(text, x, y, color=BLACK, font=fontPoppins):
    """
    Draw text on the screen.

    Parameters
    ----------
    text : str
        The text to display.
    x : int
        The x-coordinate of the text.
    y : int
        The y-coordinate of the text.
    color : tuple, optional
        The color of the text. Default is black.

    Returns
    -------
    None
    """

    try:
        text_surface = pygame.font.Font.render(font, text, True, color)
    except:
        text_surface = fontPoppins.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Helper function to create buttons for choices
def create_button(text, x, y, w, h, text_color=BLACK, text_font=fontPoppins, button_color=MELON, hover_color=BRIGHT_PINK_CRAYOLA):
    """
    Create buttons for choices.

    Parameters
    ----------
    text : str
        The text to display on the button.
    x : int
        The x-coordinate of the button.
    y : int
        The y-coordinate of the button.
    w : int
        The width of the button.
    h : int
        The height of the button.
    color : tuple
        The color of the button.
    hover_color : tuple
        The color of the button when the mouse hovers over it.

    Returns
    -------
    bool
        True if the button is clicked, False otherwise.
    """

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y: # Check if mouse is hovering over button
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True  # Button is clicked
    else:
        pygame.draw.rect(screen, button_color, (x, y, w, h))

    draw_text(text, x + 10, y + 10, color=text_color, font=text_font)
    return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    clicked = create_button("BUTTON text", 60, 60, 240, 60, button_color=MELON, hover_color=BRIGHT_PINK_CRAYOLA)

    if clicked:
        print("BUTTON CLICKED")
        break

    pygame.display.update()

pygame.quit()