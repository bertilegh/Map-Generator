import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 16  # Size of each tile
SCREEN_WIDTH = 1600  # Width of the screen
SCREEN_HEIGHT = 1200  # Height of the screen
BACKGROUND_COLOR = (0, 230, 0)

# Paths to tile images
WATER_IMAGE_PATH = 'water_image.png'  # Replace with your water tile image path
OUTER_TILE_IMAGE_PATH = 'edgegrasstexture.png'  # Replace with your outer tile image path
INNER_TILE_IMAGE_PATH = 'grasstexture.png'  # Replace with your inner tile image path

# Load tile images
water_image = pygame.image.load(WATER_IMAGE_PATH)
outer_tile_image = pygame.image.load(OUTER_TILE_IMAGE_PATH)
inner_tile_image = pygame.image.load(INNER_TILE_IMAGE_PATH)

# Resize images to TILE_SIZE
water_image = pygame.transform.scale(water_image, (TILE_SIZE, TILE_SIZE))
outer_tile_image = pygame.transform.scale(outer_tile_image, (TILE_SIZE, TILE_SIZE))
inner_tile_image = pygame.transform.scale(inner_tile_image, (TILE_SIZE, TILE_SIZE))

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Map Renderer")

# Function to load map data from a file
def load_map_data(filename):
    map_data = []
    with open(filename, 'r') as file:
        for line in file:
            x, y, render = map(int, line.strip().split(','))
            if render == 1:  # Only add tiles that should be rendered
                map_data.append((x, y))
    return map_data

# Load the map data
map_data = load_map_data('segments')

# Create a set for quick lookup
map_data_set = set(map_data)

# Define the relative positions of neighboring tiles
neighbors = [
    (0, -TILE_SIZE),  # Above
    (0, TILE_SIZE),   # Below
    (-TILE_SIZE, 0),  # Left
    (TILE_SIZE, 0)    # Right
]

# Create a surface to draw the tiles on
tile_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the tile surface with the background color
    tile_surface.fill(BACKGROUND_COLOR)

    # Draw the tiles on the tile surface
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            if (x, y) in map_data_set:
                is_outer_tile = False

                # Check neighboring tiles
                for dx, dy in neighbors:
                    if (x + dx, y + dy) not in map_data_set:
                        is_outer_tile = True
                        break

                # Blit the appropriate image based on tile type
                if is_outer_tile:
                    tile_surface.blit(outer_tile_image, (x, y))
                else:
                    tile_surface.blit(inner_tile_image, (x, y))
            else:
                # Render water if the tile is not in map_data
                tile_surface.blit(water_image, (x, y))

    # Blit the tile surface onto the main screen
    screen.blit(tile_surface, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
