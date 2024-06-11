import pygame
import random
import os

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("톰을 피해라!!!")
clock = pygame.time.Clock()
FPS = 60

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# 이미지 로드 및 최적화
background = pygame.image.load(os.path.join(image_path, "background.png")).convert()
character = pygame.image.load(os.path.join(image_path, "character.png")).convert_alpha()
angry_jerry = pygame.image.load(os.path.join(image_path, "angry_jerry.png")).convert_alpha()
tom_images = [
    pygame.image.load(os.path.join(image_path, "tom1.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path, "tom2.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path, "tom3.png")).convert_alpha()
]   ############### 이미지를 상대 경로로 변경했습니다 #####################

# 캐릭터 크기 및 위치 설정
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) / 2
character_y_pos = screen_height - character_height

# 캐릭터 이동 설정
to_x = 0
speed = 5

# 톰(tom) 설정
tom_list = []  # 톰 정보를 담을 리스트
tom_speed = 5

# 폰트 설정 ddd
game_font = pygame.font.Font(None, 40)

#####################################
######### PHASE 2 ###################
score = 0        ## 점수 추가
#####################################
#####################################


# 게임 시간 설정
total_time = 50
start_ticks = pygame.time.get_ticks()

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= speed
            elif event.key == pygame.K_RIGHT:
                to_x += speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    # 캐릭터 이동 처리
    character_x_pos += to_x

    # 캐릭터 화면 밖으로 나가지 않도록 설정
    character_x_pos = max(0, min(character_x_pos, screen_width - character_width))

    # 톰(tom) 생성 및 이동 처리
    if random.randint(0, 130) == 0:  # 150분의 1 확률로 톰 생성
        tom_x_pos = random.randint(0, screen_width - tom_images[0].get_width())
        tom_y_pos = 0
        current_tom_image = random.choice(tom_images)
        tom_list.append([tom_x_pos, tom_y_pos, current_tom_image])

    for tom in tom_list:
        tom[1] += tom_speed  # 톰 떨어뜨리기
        if tom[1] > screen_height:  # 톰이 화면 밖으로 나가면 제거
            tom_list.remove(tom)
            #####################################
            ######### PHASE 2 ###################
            score += 1  # 톰을 피할 때마다 점수 증가
            #####################################
            #####################################



        # 충돌 처리 (Rect 사용)
        character_rect = character.get_rect(topleft=(character_x_pos, character_y_pos))
        tom_rect = tom[2].get_rect(topleft=(tom[0], tom[1]))
        if character_rect.colliderect(tom_rect):
            character = angry_jerry
            character_y_pos -= 90
            pygame.display.update()
            pygame.time.delay(2000)
            running = False

    # 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    for tom in tom_list:
        screen.blit(tom[2], (tom[0], tom[1]))  # 각 톰 이미지 그리기

    #####################################
    ######### PHASE 2 ###################
    score_display = game_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_display, (10, 40))   # 점수 표시
    #####################################
    #####################################

    # 타이머 표시
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 
    timer = game_font.render(f"Time: {int(total_time - elapsed_time)}", True, (255, 255, 255))
    screen.blit(timer, (10, 10))
    
    if total_time - elapsed_time <= 0:
        running = False 

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

# Pygame 종료
pygame.quit()
