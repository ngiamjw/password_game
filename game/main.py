import pygame
from player import Player
import sprite
from pytmx.util_pygame import load_pygame
from groups import AllSprites

from random import choice


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280,720))
        self.clock = pygame.time.Clock()
        self.running = True


        # groups
        self.all_sprites = AllSprites(1280, 1280)
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # enemy timer 
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 5)
        self.enemy_triggered = False
        self.spawn_positions = []

        self.setup()

    def setup(self):
        map = load_pygame(r'C:\Users\ngiam\Desktop\python_projects\knight_game\data\tmx\new_world.tmx')

        # base layer
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
                        sprite.Tile(pos=pos, surf=tile_image, groups=self.all_sprites,map=map ,animated_frames=animated_frames)

        # objects
        for obj in map.get_layer_by_name('objects'):
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
                sprite.Tile(pos=pos, surf=obj.image, groups=self.all_sprites,map=map, animated_frames=animated_frames)
        for obj in map.get_layer_by_name('collisions'):
            sprite.CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('entities'):
            if obj.name == 'player':
                self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites, self.enemy_sprites)
            else:
                if (obj.x, obj.y) not in self.spawn_positions:
                    self.spawn_positions.append([(obj.x, obj.y),obj.name])
                    self.player.enemy_alive.append(obj.name)   

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event and self.enemy_triggered == False:
                    print(self.spawn_positions)
                    for pos in self.spawn_positions:
                        sprite.Enemy(pos[0],(self.all_sprites, self.enemy_sprites), self.player, pos[1])
                        pygame.time.set_timer(self.enemy_event, 0)
                        self.enemy_triggered = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                for pos in self.spawn_positions:
                    if pos[1] not in self.player.enemy_alive:
                        sprite.Enemy(pos[0],(self.all_sprites, self.enemy_sprites), self.player, pos[1])
                        self.player.enemy_alive.append(pos[1])
                        self.player.current_completed.clear()


            if self.player.password == self.player.current_completed:
                print('quit')
                self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
            