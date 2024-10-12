import pygame

class AllSprites(pygame.sprite.Group):
    def __init__(self, map_width, map_height):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
        self.map_width = map_width
        self.map_height = map_height
    
    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - 1280 / 2)
        self.offset.y = -(target_pos[1] - 720 / 2)

        # ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')] 
        # object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')] 
        
        # for layer in [ground_sprites,object_sprites]:
        #     for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
        #         self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        self.offset.x = max(min(self.offset.x, 0), -(self.map_width - 1280))
        self.offset.y = max(min(self.offset.y, 0), -(self.map_height - 720))

        sorted_sprites = sorted(self, key=lambda sprite: sprite.rect.bottom)

        # Draw all sprites in the correct order
        for sprite in sorted_sprites:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)