import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups,map, animated_frames=None):
        super().__init__(groups)
        self.pos = pos
        self.image = surf
        self.rect = self.image.get_rect(topleft=self.pos)
        self.animated_frames = animated_frames  # List of frames for animated tiles or objects
        self.current_frame = 0
        self.animation_time = 0  # Accumulator for frame duration
        self.map = map

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
                self.image = self.map.get_tile_image_by_gid(new_gid)
                self.rect = self.image.get_rect(topleft=self.pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, enemy_id):
        super().__init__(groups)

        self.image = pygame.image.load(r'Tiny Swords (Update 010)\Factions\Knights\Troops\Warrior\Blue\tile000.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.player = player
        self.frames = {'still': [], 'die': []}
        self.load_images()

        # Animation control
        self.frame_index = 0
        self.animation_speed = 6
        self.dying = False  # Flag to track if the enemy is dying
        self.id = enemy_id

        # rect
        self.hitbox_rect = self.rect.inflate(-120, -120)

    def load_images(self):
        for i in range(7):  # range from tile000 to tile006 for 'still' animation
            frame_path = f'Tiny Swords (Update 010)/Factions/Goblins/Troops/Torch/Blue/tile{i:03}.png'
            frame_image = pygame.image.load(frame_path).convert_alpha()
            self.frames['still'].append(frame_image)

        for i in range(14):  # range for 'die' animation frames
            frame_path = f'Tiny Swords (Update 010)/Factions/Knights/Troops/Dead/tile{i:03}.png'
            frame_image = pygame.image.load(frame_path).convert_alpha()
            self.frames['die'].append(frame_image)

    def destroy(self):
        """Play the die animation once and then kill the sprite."""
        self.dying = True  # Set flag to play die animation

    def animate(self, dt):
        if self.dying:
            # Play the 'die' animation
            self.frame_index += self.animation_speed * dt
            if int(self.frame_index) >= len(self.frames['die']):
                # Animation finished, kill the sprite
                self.kill()
                self.player.current_completed.append(int(self.id))
                self.player.enemy_alive.remove(self.id)

            else:
                self.image = self.frames['die'][int(self.frame_index)]

                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            # Play the 'still' animation
            self.frame_index += self.animation_speed * dt
            self.image = self.frames['still'][int(self.frame_index) % len(self.frames['still'])]

    def update(self, dt):
        # Update sprite animations
        self.animate(dt)