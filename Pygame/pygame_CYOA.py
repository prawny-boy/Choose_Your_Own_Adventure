# TO MAKE THIS WORK
# pip install pygame
# change the filenames for the fonts and images

# NOTICES
# This code is written by Aaron, please do not redistribute, claim, sell, or otherwise distribute this code. 
# Do not modify it without permission.
# Please read the pygame_readme.md file for more information

import pygame
import sys

# PYGAME START ------------------------------------------------------------------------------------------------------

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Base Template")

# Screen colour
screen.fill((0, 0, 0)) # clear the display

# START ---------------------------------------------------------------------------------------------------------

# Colours
## Basic colouts
colour_white = (255, 255, 255)
colour_black = (0, 0, 0)
colour_blue = (0, 0, 255)
## Colour palette 1, style: playful
colour1_cambridge_blue = (131, 182, 146)
colour1_melon = (249, 173, 160)
colour1_bright_pink_crayola = (249, 98, 125)
colour1_blush = (198, 91, 124)
colour1_violet_jtc = (91, 55, 88)

try:
    _ =  pygame.font.Font("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsRegular.ttf", 32)
    file_path_type = "Choose_Your_Own_Adventure/"
except:
    file_path_type = ""

def pConvertFileName(filepath:str):
    return file_path_type + filepath

# Fonts
## Poppins
font_poppins =  pygame.font.Font(pConvertFileName("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsRegular.ttf"), 32)
font_poppins_bold =  pygame.font.Font(pConvertFileName("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsBold.ttf"), 48)
font_poppins_small =  pygame.font.Font(pConvertFileName("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsRegular.ttf"), 12)
font_poppins_bold_small =  pygame.font.Font(pConvertFileName("Choose_Your_Own_Adventure/Pygame/Fonts/PoppinsBold.ttf"), 18)
    # POPPINS FONT CREDITS
        # Poppins
        # Designed by Indian Type Foundry, Jonny Pinhorn, Ninad Kale 

# Settings
game_state = "main_menu" # The game state, which is for choosing which screen to load
frame_rate = 30 # The frame rate of the game, recommended to be 30
button_cooldown = 500 # The cooldown of the button, in miliseconds, which makes a cooldown for the button after it is pressed
button_cooldown_end = 0 # The cooldown end of the button, keep this at zero, unless you want to make a cooldown at the start of the game

# CLASSES ------------------------------------------------------------------------------------------------------

# FUNCTIONS ------------------------------------------------------------------------------------------------------

# Function to quit Pygame
def pygame_quit():
    """
    Quit Pygame.

    Returns
    -------
    None
    """
    pygame.quit()
    sys.exit()

# Display text on the screen
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
    font : font, optional
        The font of the text. Default is Poppins.

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

# Create buttons for choices
def create_button(x=10, y=120, w=200, h=75, 
                  text_padding=10,
                  heading_text="Button", heading_text_colour=colour_black, heading_text_font=font_poppins_bold_small, 
                  body_text="Body text", body_text_offset=30, body_text_colour=colour_black, body_text_font=font_poppins_small, 
                  button_colour=colour1_melon, hover_colour=colour1_bright_pink_crayola):
    """
    Create a button for choices in the game.

    Parameters
    ----------
    x : int
        The x-coordinate of the button.
    y : int
        The y-coordinate of the button.
    w : int
        The width of the button.
    h : int
        The height of the button.
    heading_text : str, optional
        The heading text of the button. Default is "Button".
    heading_text_colour : tuple, optional
        The colour of the heading text. Default is black.
    heading_text_font : pygame.font.Font, optional
        The font of the heading text. Default is font_poppins_bold_small.
    body_text : str, optional
        The body text of the button. Default is "Body text".
    body_text_offset : int, optional
        The offset of the body text from the top of the button. Default is 30.
    body_text_colour : tuple, optional
        The colour of the body text. Default is black.
    body_text_font : pygame.font.Font, optional
        The font of the body text. Default is font_poppins_small.
    button_colour : tuple, optional
        The colour of the button. Default is melon.
    hover_colour : tuple, optional
        The colour of the button when hovered over. Default is bright pink crayola.

    Returns
    -------
    bool
        True if the button is clicked, False otherwise.
    """
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

    draw_text(text=heading_text, x=x+text_padding, y=y+text_padding, colour=heading_text_colour, font=heading_text_font)
    draw_text(text=body_text, x=x+text_padding, y=y+text_padding+body_text_offset, colour=body_text_colour, font=body_text_font)
    return False

# Create multiple buttons
def create_multiple_buttons(button_text_list=[("Button 1 Heading", "Button 1 Subheading"), ("Button 2 Heading", "Button 2 Subheading")], x=0, y=0, w=200, h=50, 
                            text_padding=10,
                            x_offset=0, y_offset=0, 
                            heading_text_colour=colour_black, heading_text_font=font_poppins_bold_small, 
                            body_text_colour=colour_black, body_text_font=font_poppins_small, 
                            button_colour=colour1_melon, hover_colour=colour1_bright_pink_crayola):
    
    """
    Create multiple buttons with headings and subheadings.

    Parameters
    ----------
    button_text_list : list of tuple of str, optional
        A list of tuples containing the heading and subheading for each button. Default is [("Button 1 Heading", "Button 1 Subheading"), ("Button 2 Heading", "Button 2 Subheading")].
    x : int, optional
        The x-coordinate of the first button. Default is 0.
    y : int, optional
        The y-coordinate of the first button. Default is 0.
    w : int, optional
        The width of each button. Default is 200.
    h : int, optional
        The height of each button. Default is 50.
    text_padding : int, optional
        The padding from the edge of the button to the text. Default is 10.
    x_offset : int, optional
        The offset from the previous button's x-coordinate to the next button's x-coordinate. Default is 0.
    y_offset : int, optional
        The offset from the previous button's y-coordinate to the next button's y-coordinate. Default is 0.
    heading_text_colour : tuple, optional
        The colour of the heading text. Default is black.
    heading_text_font : pygame.font.Font, optional
        The font of the heading text. Default is font_poppins_bold_small.
    body_text_colour : tuple, optional
        The colour of the body text. Default is black.
    body_text_font : pygame.font.Font, optional
        The font of the body text. Default is font_poppins_small.
    button_colour : tuple, optional
        The colour of the button. Default is melon.
    hover_colour : tuple, optional
        The colour of the button when hovered over. Default is bright pink crayola.

    Returns
    -------
    int
        The index (starting from 1) of the button that was clicked, or -1 if no button was clicked.
    """

    global button_cooldown_end
    for index, (heading_text, body_text) in enumerate(button_text_list):
        # Calculate position for each button based on index and offsets
        button_x = x + index * x_offset # Start from x and add index * x_offset
        button_y = y + index * y_offset # Start from y and add index * y_offset
        
        # Call create_button function for each button
        clicked = create_button(button_x, button_y, w, h, 
                                text_padding=text_padding,
                                heading_text=heading_text, heading_text_colour=heading_text_colour, heading_text_font=heading_text_font,
                                body_text=body_text, body_text_offset=30, body_text_colour=body_text_colour, body_text_font=body_text_font,
                                button_colour=button_colour, hover_colour=hover_colour)
        
        if clicked:
            return index + 1 # Return the index (starting from 1) of the clicked button
    return False  # Return False if no button was clicked

# Display heading function
def display_heading(title="Title", title_colour=colour_white, title_pos=(10, 10), title_font=font_poppins_bold, subtext="Subtext", subtext_colour=colour_white, subtext_pos=(10, 60), subtext_font=font_poppins):
    """
    Display the heading of the game.

    Parameters
    ----------
    title : str, optional
        The title of the game. Default is "Title".
    title_colour : tuple, optional
        The colour of the title. Default is white.
    title_pos : tuple, optional
        The position of the title. Default is (10, 10).
    title_font : pygame.font.Font, optional
        The font of the title. Default is font_poppins_bold.
    subtext : str, optional
        The subtitle of the game. Default is "Subtext".
    subtext_colour : tuple, optional
        The colour of the subtitle. Default is white.
    subtext_pos : tuple, optional
        The position of the subtitle. Default is (10, 60).
    subtext_font : pygame.font.Font, optional
        The font of the subtitle. Default is font_poppins.

    Returns
    -------
    None
    """    
    # Render title using bold font
    draw_text(title, title_pos[0], title_pos[1], colour=title_colour, font=title_font)
    
    # Render subtext using regular font
    draw_text(subtext, subtext_pos[0], subtext_pos[1], colour=subtext_colour, font=subtext_font)

# MAIN LOOP --------------------------------------------------------------------------------------------------------

while True:
    # EVENTS ------------------------------------------------------------------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame_quit()
    
    # GAME --------------------------------------------------------------------------------------------------------

    if game_state == "main_menu": # Main menu
        screen.fill(colour_black) # clear the display

        display_heading(title="Choose Your Own Adventure", subtext="This code is written by Aaron. WARNING: UNFINISHED")
        start_story = create_button(x=10, y=120, w=200, h=75, heading_text="Start", body_text="Start the adventure")
        if start_story:
            game_state = "story"
        
        go_to_multi_buttons = create_button(x=10, y=240, w=200, h=75, heading_text="Multi buttons", body_text="Test multiple buttons")
        if go_to_multi_buttons:
            game_state = "multi buttons"
    
    elif game_state == "story": # Sample page, stored as a story
        screen.fill(colour_black) # clear the display

        display_heading(title="Story", subtext="Just a test screen")
        exit_story = create_button(x=10, y=120, w=200, h=75, heading_text="Exit", body_text="Back to menu")
        if exit_story:
            game_state = "main_menu"
    
    elif game_state == "multi buttons":
        screen.fill(colour_black) # clear the display

        # Example button list
        button_texts = [("Start", "Begin your adventure"), ("Menu", "Go to the main menu"), ("Exit", "Quit the game")]

        # Inside the game loop
        clicked_button = create_multiple_buttons(button_text_list=button_texts, x=10, y=10, w=600, h=75, x_offset=0, y_offset=120)
        
        if clicked_button == 1:
            game_state = "story"
        elif clicked_button == 2:
            game_state = "main_menu"
        elif clicked_button == 3:
            pygame_quit()

    # DRAW AND UPDATE --------------------------------------------------------------------------------------------------------

    pygame.display.update() # Update the display

    pygame.time.Clock().tick(frame_rate) # Wait for the next frame

# END OF GAME ------------------------------------------------------------------------------------------------------

pygame_quit()