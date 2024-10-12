import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups, collision_sprites, enemy_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(r'Tiny Swords (Update 010)\Factions\Knights\Troops\Warrior\Blue\tile000.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        # hitbox_height = 50
        self.hitbox_rect = self.rect.inflate(-120, -175)
        # self.attack_rect = self.rect.inflate(-30,0)
        # self.hitbox_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, hitbox_height)
        self.state, self.frame_index = 'right', 0
        self.frames = {'left': [], 'right': [], 'still' : [], 'still_left': [], 'attack':[], 'attack_left':[]}
        self.load_images()
        self.last_direction = 'still'
        self.is_attacking = False
        self.attack_complete = True

        self.password = [3,8,2]
        self.current_completed = []
        self.enemy_alive = []

        # movement
        self.direction = pygame.Vector2()
        self.speed = 400
        self.attack_duration = 500
        self.collision_sprites = collision_sprites
        self.enemy_sprites = enemy_sprites
        self.attack_time = 0

    def load_images(self):

        for i in range(6, 12):  # range from 006 to 011
            frame_path = f'Tiny Swords (Update 010)/Factions/Knights/Troops/Warrior/Blue/tile{i:03}.png'
            frame_image = pygame.image.load(frame_path).convert_alpha()  # Assuming you're using pygame for loading images
            self.frames['right'].append(frame_image)

        # Reverse the right-facing frames for left-facing animation
        self.frames['left'] = [pygame.transform.flip(frame, True, False) for frame in self.frames['right']]

        for i in range(6):  # range from tile000 to tile005
            frame_path = f'Tiny Swords (Update 010)/Factions/Knights/Troops/Warrior/Blue/tile{i:03}.png'
            frame_image = pygame.image.load(frame_path).convert_alpha()
            self.frames['still'].append(frame_image)

        self.frames['still_left'] = [pygame.transform.flip(frame, True, False) for frame in self.frames['still']]

        for i in range(12, 18):  # range from 006 to 011
                frame_path = f'Tiny Swords (Update 010)/Factions/Knights/Troops/Warrior/Blue/tile{i:03}.png'
                frame_image = pygame.image.load(frame_path).convert_alpha()  # Assuming you're using pygame for loading images
                self.frames['attack'].append(frame_image)

        # Reverse the right-facing frames for left-facing animation
        self.frames['attack_left'] = [pygame.transform.flip(frame, True, False) for frame in self.frames['attack']]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.is_attacking:  # Only allow movement input when not attacking
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
            self.direction = self.direction.normalize() if self.direction else self.direction

        if keys[pygame.K_SPACE] and not self.is_attacking and self.attack_complete:  # Start attack if not already attacking
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()  # Record attack start time
            self.frame_index = 0  # Reset the frame index to 0 to start attack animation
            self.state = "attack" if self.last_direction == "right" else "attack_left"

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def animate(self, dt):
        # get state 
        if self.is_attacking:
            # Increment frame index for attack animation
            self.frame_index += 15 * dt
            # Check if attack animation is complete
            if self.frame_index >= len(self.frames[self.state]):
                self.is_attacking = False  # End the attack state
                self.attack_complete = True  # Mark attack as complete
                self.frame_index = len(self.frames[self.state]) - 1  # Stop on the last frame

            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

        else:
            # Normal movement animations
            if self.direction and self.attack_complete:
                if self.direction.x != 0:
                    self.state = 'right' if self.direction.x > 0 else 'left'
                    self.last_direction = self.state
                if self.direction.y != 0:
                    self.state = 'right' if self.last_direction == 'right' else 'left'
            else:
                self.state = 'still' if self.last_direction == 'right' else 'still_left'

            self.frame_index += 15 * dt
            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top 

        for sprite in self.enemy_sprites:
            # print(sprite.hitbox_rec.x, self.attack_rect.)
            if sprite.hitbox_rect.colliderect(self.rect) and self.is_attacking == True:
                sprite.destroy()
                # self.current_completed.append(sprite.id)
                # print(self.current_completed)
                # dx = (sprite.hitbox_rect.centerx - self.rect.centerx)
                # if dx > 0:
                #     print('left')  # rect1 is to the right of rect2
                # else:
                #     print('right')
            if sprite.hitbox_rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.hitbox_rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.hitbox_rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.hitbox_rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.hitbox_rect.top 


    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)