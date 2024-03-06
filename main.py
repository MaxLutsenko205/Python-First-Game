import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player1_run1 = pygame.image.load('graphics/ArmBro_run1.png').convert_alpha()
        player1_run2 = pygame.image.load('graphics/ArmBro_run2.png').convert_alpha()
        player1_run3 = pygame.image.load('graphics/ArmBro_run3.png').convert_alpha()
        player1_run4 = pygame.image.load('graphics/ArmBro_run4.png').convert_alpha()
        self.player1_run = [player1_run1, player1_run2, player1_run3, player1_run4]
        self.player1_jump = pygame.image.load('graphics/ArmBro_jump2.png').convert_alpha()

        player2_run1 = pygame.image.load('graphics/Pivozavr_run1.png').convert_alpha()
        player2_run2 = pygame.image.load('graphics/Pivozavr_run2.png').convert_alpha()
        player2_run3 = pygame.image.load('graphics/Pivozavr_run3.png').convert_alpha()
        player2_run4 = pygame.image.load('graphics/Pivozavr_run4.png').convert_alpha()
        self.player2_jump = pygame.image.load('graphics/Pivozavr_jump2.png').convert_alpha()
        self.player2_run = [player2_run1, player2_run2, player2_run3, player2_run4]

        player3_run1 = pygame.image.load('graphics/Maxon_run1.png').convert_alpha()
        player3_run2 = pygame.image.load('graphics/Maxon_run2.png').convert_alpha()
        player3_run3 = pygame.image.load('graphics/Maxon_run3.png').convert_alpha()
        player3_run4 = pygame.image.load('graphics/Maxon_run4.png').convert_alpha()
        self.player3_jump = pygame.image.load('graphics/Maxon_jump2.png').convert_alpha()
        self.player3_run = [player3_run1, player3_run2, player3_run3, player3_run4]

        self.player_index = 0
        self.image = pygame.image.load('graphics/ArmBro_run1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/cartoon-jump-6462.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -17

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            if player_frame_rect.colliderect(player1_stand_rect):
                self.image = self.player1_jump
            if player_frame_rect.colliderect(player2_stand_rect):
                self.image = self.player2_jump
            if player_frame_rect.colliderect(player3_stand_rect):
                self.image = self.player3_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player1_run): self.player_index = 0
            if player_frame_rect.colliderect(player1_stand_rect):
                self.image = self.player1_run[int(self.player_index)]
            if player_frame_rect.colliderect(player2_stand_rect):
                self.image = self.player2_run[int(self.player_index)]
            if player_frame_rect.colliderect(player3_stand_rect):
                self.image = self.player3_run[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'package':
            package_frame1 = pygame.image.load('graphics/plastic_package.png').convert_alpha()
            package_frame2 = pygame.image.load('graphics/plastic_package2.png').convert_alpha()
            self.frames = [package_frame1, package_frame2]
            y_pos = randint(150, 200)
        elif type == 'trash':
            if randint(0, 2):
                trash_surf = pygame.image.load('graphics/trash.png').convert_alpha()
                self.frames = [trash_surf, trash_surf]
                y_pos = 300
            else:
                bush_surf = pygame.image.load('graphics/bush.png').convert_alpha()
                self.frames = [bush_surf, bush_surf]
                y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks()/900) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def sky_animation():
    global sky_rect, sky_rect2
    sky_rect.x -= 1
    sky_rect2.x -= 1
    if sky_rect.x <= -800: sky_rect.x = 800
    if sky_rect2.x <= -800: sky_rect2.x = 800


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('University Day')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/Slower-Tempo-2020-03-22_-_A_Bit_Of_Hope_-_David_Fesliyan.mp3')
bg_music.set_volume(0.2)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#  SURFACES
sky_surface = pygame.image.load('graphics/mountains1.png').convert()
sky_rect = sky_surface.get_rect(topleft=(0, 0))
sky_rect2 = sky_surface.get_rect(topleft=(800, 0))
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
player_frame = pygame.Surface((134, 210))
player_frame_rect = player_frame.get_rect(center=(400, 200))

player1_stand = pygame.image.load('graphics/ArmBro2.png').convert_alpha()
player1_stand = pygame.transform.scale2x(player1_stand)
player1_stand_rect = player1_stand.get_rect(center=(400, 200))

player2_stand = pygame.image.load('graphics/Pivozavr.png').convert_alpha()
player2_stand = pygame.transform.scale2x(player2_stand)
player2_stand_rect = player2_stand.get_rect(center=(600, 200))

player3_stand = pygame.image.load('graphics/Maxon.png').convert_alpha()
player3_stand = pygame.transform.scale2x(player3_stand)
player3_stand_rect = player3_stand.get_rect(center=(200, 200))

text_surf = test_font.render(f'Press SPASE to start', False, (64, 64, 64))
text_rect = text_surf.get_rect(center=(400, 350))

next_surf = test_font.render(f'>', False, (64, 64, 64))
next_rect = next_surf.get_rect(center=(700, 200))
prev_surf = test_font.render(f'<', False, (64, 64, 64))
prev_rect = prev_surf.get_rect(center=(100, 200))

# endgame
end_text_surf = test_font.render(f'You went to University', False, (64, 64, 64))
end_txt_rect = end_text_surf.get_rect(center=(400, 80))

# TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

# GAME CONTENT

while True:

    # EVENTS(buttons)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/900)
                bg_music.play(loops=-1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if player_frame_rect.x > 400: player_frame_rect.x -= 400
                else: player_frame_rect.x += 200
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if player_frame_rect.x < 300: player_frame_rect.x += 400
                else: player_frame_rect.x -= 200

        if event.type == obstacle_timer and game_active:
            obstacle_group.add(Obstacle(choice(['package', 'trash', 'trash', 'trash'])))


# GAME ACTIONS
    if game_active:
        sky_animation()
        screen.blit(sky_surface, sky_rect)
        screen.blit(sky_surface, sky_rect2)
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()


        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()


# INTRO & OUTRO
    else:
        bg_music.stop()
        screen.fill((94, 129, 162))

        screen.blit(player1_stand, player1_stand_rect)
        screen.blit(player2_stand, player2_stand_rect)
        screen.blit(player3_stand, player3_stand_rect)

        current_score = test_font.render(f'Your score: {score}', False, (64, 64, 64))
        current_score_rect = current_score.get_rect(center=(400, 50))
        screen.blit(current_score, current_score_rect)
        screen.blit(text_surf, text_rect)

        # Player choosing
        pygame.draw.rect(screen, (51, 102, 153), player_frame_rect, 6)
        screen.blit(next_surf, next_rect)
        screen.blit(prev_surf, prev_rect)

    pygame.display.update()
    clock.tick(60)
