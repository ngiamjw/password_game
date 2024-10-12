import pygame
import sys
from pytmx.util_pygame import load_pygame
import time

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, animated_frames=None):
        super().__init__(groups)
        self.pos = pos
        self.image = surf
        self.rect = self.image.get_rect(topleft=self.pos)
        self.animated_frames = animated_frames  # List of frames for animated tiles or objects
        self.current_frame = 0
        self.animation_time = 0  # Accumulator for frame duration

    def update(self, dt):
        if self.animated_frames:  # Check if this tile or object has animation frames
            self.animation_time += dt * 1000  # Convert dt to milliseconds

            # Get the current frame's duration
            frame_duration = self.animated_frames[self.current_frame][1]

            # If enough time has passed, move to the next frame
            if self.animation_time > frame_duration:
                self.animation_time = 0  # Reset the timer
                self.current_frame = (self.current_frame + 1) % len(self.animated_frames)  # Cycle to next frame

                # Update the image to the new frame
                new_gid = self.animated_frames[self.current_frame][0]
                self.image = map.get_tile_image_by_gid(new_gid)
                self.rect = self.image.get_rect(topleft=self.pos)  # Update the rect to match the new image size

# Initialize pygame and load the map
pygame.init()
screen = pygame.display.set_mode((1280, 720))
map = load_pygame(r'C:\Users\ngiam\Desktop\python_projects\knight_game\data\tmx\new_world.tmx')
sprite_group = pygame.sprite.Group()

# Time tracking for animation
clock = pygame.time.Clock()

# cycle through all layers
for layer in map.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, gid in layer:
            tile_image = map.get_tile_image_by_gid(gid)

            # Ensure tile_image is not None before creating a Tile
            if tile_image:
                pos = (x * 32, y * 32)

                # Check if the tile is animated by checking if it has frames
                animated_frames = None
                tile_props = map.get_tile_properties_by_gid(gid)

                # Check if tile_props contains animation frames
                if tile_props and "frames" in tile_props:
                    # Get the frames and their duration
                    animated_frames = [(frame.gid, frame.duration) for frame in tile_props['frames']]

                # Create a Tile, passing in animated_frames if the tile has animation
                Tile(pos=pos, surf=tile_image, groups=sprite_group, animated_frames=animated_frames)

# Handle objects (which can also be animated)
for obj in map.objects:
    pos = (obj.x, obj.y)

    # Check if the object has an image and if it's animated
    if obj.image:
        animated_frames = None

        # Check if the object has animation frames in its properties
        obj_props = map.get_tile_properties_by_gid(obj.gid)
        if obj_props and "frames" in obj_props:
            # Get the frames and their duration for the object
            animated_frames = [(frame.gid, frame.duration) for frame in obj_props['frames']]

        # Create a Tile for the object, passing animated_frames if the object has animation
        Tile(pos=pos, surf=obj.image, groups=sprite_group, animated_frames=animated_frames)

# Main loop
while True:
    dt = clock.tick(60) / 1000  # Time since last frame in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')

    # Update all sprites, especially the animated ones
    sprite_group.update(dt)
    sprite_group.draw(screen)

    pygame.display.update()