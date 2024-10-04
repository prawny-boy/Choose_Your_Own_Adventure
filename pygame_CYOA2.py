import pygame
import sys

# PYGAME START ------------------------------------------------------------------------------------------------------

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("CYOA Pygame")

# Screen colour
screen.fill((0, 0, 0))

# START ---------------------------------------------------------------------------------------------------------

# Colours
colour_white = (255, 255, 255)
colour_black = (0, 0, 0)
colour_blue = (0, 0, 255)
colour1_cambridge_blue = (131, 182, 146)
colour1_melon = (249, 173, 160)
colour1_bright_pink_crayola = (249, 98, 125)
colour1_blush = (198, 91, 124)
colour1_violet_jtc = (91, 55, 88)

# Fonts
font_poppins =  pygame.font.Font("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsRegular.ttf", 32)
font_poppins_bold =  pygame.font.Font("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsBold.ttf", 32)
    # POPPINS FONT CREDITS
        # Poppins
        # Designed by Indian Type Foundry, Jonny Pinhorn, Ninad Kale 

# Settings
game_state = "main_menu"

# CLASSES ------------------------------------------------------------------------------------------------------

# FUNCTIONS ------------------------------------------------------------------------------------------------------

# Helper function to display text on the screen
def draw_text(text, x, y, colour=colour_black, font=font_poppins):
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
    colour : tuple, optional
        The colour of the text. Default is black.

    Returns
    -------
    None
    """

    try:
        text_surface = pygame.font.Font.render(font, text, True, colour)
    except:
        text_surface = font_poppins.render(text, True, colour)
    screen.blit(text_surface, (x, y))

# Helper function to create buttons for choices
def create_button(text, x, y, w, h, text_colour=colour_black, text_font=font_poppins, button_colour=colour1_melon, hover_colour=colour1_bright_pink_crayola):
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
    colour : tuple
        The colour of the button.
    hover_colour : tuple
        The colour of the button when the mouse hovers over it.

    Returns
    -------
    bool
        True if the button is clicked, False otherwise.
    """

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y: # Check if mouse is hovering over button
        pygame.draw.rect(screen, hover_colour, (x, y, w, h))
        if click[0] == 1:
            return True  # Button is clicked
    else:
        pygame.draw.rect(screen, button_colour, (x, y, w, h))

    draw_text(text, x + 10, y + 10, colour=text_colour, font=text_font)
    return False

# MAIN LOOP --------------------------------------------------------------------------------------------------------

while True:
    # EVENTS ------------------------------------------------------------------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # GAME --------------------------------------------------------------------------------------------------------

    if game_state == "main_menu":
        pass

    # DRAW AND UPDATE --------------------------------------------------------------------------------------------------------

    pygame.display.update()

# END OF GAME ------------------------------------------------------------------------------------------------------

pygame.quit()
