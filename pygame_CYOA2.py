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
font_poppins_bold =  pygame.font.Font("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsBold.ttf", 48)
font_poppins_small =  pygame.font.Font("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsRegular.ttf", 12)
font_poppins_bold_small =  pygame.font.Font("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsBold.ttf", 18)
    # POPPINS FONT CREDITS
        # Poppins
        # Designed by Indian Type Foundry, Jonny Pinhorn, Ninad Kale 

# Settings
game_state = "main_menu"
frame_rate = 30
button_cooldown = 500
button_cooldown_end = 0

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
    text_rect = text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)

# Helper function to create buttons for choices
def create_button(x, y, w, h, heading_text="Button", heading_text_colour=colour_black, heading_text_font=font_poppins_bold_small, body_text="Body text", body_text_offset=30, body_text_colour=colour_black, body_text_font=font_poppins_small, button_colour=colour1_melon, hover_colour=colour1_bright_pink_crayola):
    global button_cooldown_end
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y: # Check if mouse is hovering over button
        pygame.draw.rect(screen, hover_colour, (x, y, w, h))
        if click[0] == 1 and button_cooldown_end < pygame.time.get_ticks():
            button_cooldown_end = pygame.time.get_ticks() + button_cooldown
            return True
    else:
        pygame.draw.rect(screen, button_colour, (x, y, w, h))

    draw_text(text=heading_text, x=x+10, y=y+10, colour=heading_text_colour, font=heading_text_font)
    draw_text(text=body_text, x=x+10, y=y+10+body_text_offset, colour=body_text_colour, font=body_text_font)
    return False

# Display heading function
def display_heading(title="Title", title_colour=colour_white, title_pos=(10, 10), title_font=font_poppins_bold, subtext="Subtext", subtext_colour=colour_white, subtext_pos=(10, 60), subtext_font=font_poppins):
    screen.fill((0, 0, 0))  # Clear screen with black background
    
    # Render title using bold font
    draw_text(title, title_pos[0], title_pos[1], colour=title_colour, font=title_font)
    
    # Render subtext using regular font
    draw_text(subtext, subtext_pos[0], subtext_pos[1], colour=subtext_colour, font=subtext_font)

# MAIN LOOP --------------------------------------------------------------------------------------------------------

while True:
    # EVENTS ------------------------------------------------------------------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # GAME --------------------------------------------------------------------------------------------------------

    if game_state == "main_menu":
        display_heading(title="Choose Your Own Adventure", subtext="This code is written by Aaron")
        main_menu = create_button(x=10, y=120, w=200, h=75, heading_text="Start", body_text="Start the adventure")
        if main_menu:
            game_state = "story"
    
    elif game_state == "story":
        display_heading(title="Story", subtext="Just a test screen")
        exit_story = create_button(x=10, y=120, w=200, h=75, heading_text="Exit", body_text="Back to menu")
        if exit_story:
            game_state = "main_menu"

    # DRAW AND UPDATE --------------------------------------------------------------------------------------------------------

    pygame.display.update()

    pygame.time.Clock().tick(frame_rate)

# END OF GAME ------------------------------------------------------------------------------------------------------

pygame.quit()
