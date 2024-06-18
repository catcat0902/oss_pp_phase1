import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("톰을 피해라!!!")
clock = pygame.time.Clock()
FPS = 60

# 이미지 로드 및 최적화
background = pygame.image.load(r"이미지경로/oss_pp_phase1/images/background.png").convert()
character = pygame.image.load(r"이미지경로/oss_pp_phase1/images/character.png").convert_alpha()
angry_jerry = pygame.image.load(r"이미지경로/oss_pp_phase1/images/angry_jerry.png").convert_alpha()
tom_images = [
    pygame.image.load(r"이미지경로/oss_pp_phase1/images/tom1.png").convert_alpha(),
    pygame.image.load(r"이미지경로/oss_pp_phase1/images/tom2.png").convert_alpha(),
    pygame.image.load(r"이미지경로/oss_pp_phase1/images/tom3.png").convert_alpha()
]

# 아이템 이미지 로드 및 크기 조절
heart_item = pygame.image.load(r"이미지경로/oss_pp_phase1/images/heart.png").convert_alpha()
heart_item = pygame.transform.scale(heart_item, (40, 40))  # 크기 조절

shield_item = pygame.image.load(r"이미지경로/oss_pp_phase1/images/shield.png").convert_alpha()
shield_item = pygame.transform.scale(shield_item, (40, 40))  # 크기 조절

slow_item = pygame.image.load(r"이미지경로/oss_pp_phase1/images/slow.png").convert_alpha()
slow_item = pygame.transform.scale(slow_item, (40, 40))  # 크기 조절

double_score_item = pygame.image.load(r"이미지경로/oss_pp_phase1/images/double_score.png").convert_alpha()
double_score_item = pygame.transform.scale(double_score_item, (40, 40))  # 크기 조절

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

# 아이템 설정
item_list = []  # 아이템 정보를 담을 리스트
item_speed = 5

# 폰트 설정
game_font = pygame.font.Font(None, 40)

# 게임 시간 설정
total_time = 50
start_ticks = pygame.time.get_ticks()

# #################################################
# #################### PHASE 2 ####################
# #################################################
# 플레이어 생명 설정
player_lives = 3

# 무적 상태 변수
is_invincible = False
invincibility_duration = 5  # 무적 상태 지속 시간 (초)
invincibility_start_time = 0

# 점수 설정
score = 0
double_score = False
double_score_duration = 5  # 점수 두 배 지속 시간 (초)
double_score_start_time = 0

# 생명 표시 함수
def display_lives(screen, lives):
    lives_text = game_font.render(f'Lives: {lives}', True, (255, 255, 255))
    screen.blit(lives_text, (screen_width - 100, 10))

# 점수 표시 함수
def display_score(screen, score):
    score_text = game_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (screen_width - 100, 50))

# 무적 상태 표시 함수
def display_invincibility(screen):
    invincibility_text = game_font.render("Invincible!", True, (255, 0, 0))
    screen.blit(invincibility_text, (screen_width // 2 - 60, 10))
# #################################################
# #################### PHASE 2 ####################
# #################################################

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
        print(f"톰 생성: 위치=({tom_x_pos}, {tom_y_pos})")  # 디버깅 메시지 추가

    for tom in tom_list:
        tom[1] += tom_speed  # 톰 떨어뜨리기
        if tom[1] > screen_height:  # 톰이 화면 밖으로 나가면 제거
            tom_list.remove(tom)

        # 충돌 처리 (Rect 사용)
        character_rect = character.get_rect(topleft=(character_x_pos, character_y_pos))
        tom_rect = tom[2].get_rect(topleft=(tom[0], tom[1]))
        if character_rect.colliderect(tom_rect):
            if not is_invincible:
                player_lives -= 1
                if player_lives <= 0:
                    running = False
                is_invincible = True
                invincibility_start_time = pygame.time.get_ticks() / 1000
                tom_list.remove(tom)

# #################################################
# #################### PHASE 2 ####################
# #################################################
    # 아이템 생성 및 이동 처리
    if random.randint(0, 500) == 0:  # 500분의 1 확률로 아이템 생성
        item_type = random.choice(['heart', 'shield', 'slow', 'double_score'])
        item_x_pos = random.randint(0, screen_width - heart_item.get_width())
        item_y_pos = 0
        if item_type == 'heart':
            item_image = heart_item
        elif item_type == 'shield':
            item_image = shield_item
        elif item_type == 'slow':
            item_image = slow_item
        elif item_type == 'double_score':
            item_image = double_score_item
        item_list.append([item_x_pos, item_y_pos, item_image, item_type])
        print(f"아이템 생성: 유형={item_type}, 위치=({item_x_pos}, {item_y_pos})")  # 디버깅 메시지 추가

    for item in item_list:
        item[1] += item_speed
        if item[1] > screen_height:
            item_list.remove(item)

        # 아이템 충돌 처리
        item_rect = item[2].get_rect(topleft=(item[0], item[1]))
        if character_rect.colliderect(item_rect):
            if item[3] == 'heart':
                player_lives += 1
            elif item[3] == 'shield':
                is_invincible = True
                invincibility_start_time = pygame.time.get_ticks() / 1000
            elif item[3] == 'slow':
                tom_speed = max(1, tom_speed - 2)
            elif item[3] == 'double_score':
                double_score = True
                double_score_start_time = pygame.time.get_ticks() / 1000
            item_list.remove(item)
    
    # 무적 상태 지속 시간 확인
    if is_invincible and (pygame.time.get_ticks() / 1000 - invincibility_start_time > invincibility_duration):
        is_invincible = False
    
    # 점수 두 배 지속 시간 확인
    if double_score and (pygame.time.get_ticks() / 1000 - double_score_start_time > double_score_duration):
        double_score = False
# #################################################
# #################### PHASE 2 ####################
# #################################################

    # 점수 증가
    score += 1 if not double_score else 2

    # 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    for tom in tom_list:
        screen.blit(tom[2], (tom[0], tom[1]))  # 각 톰 이미지 그리기
    for item in item_list:
        screen.blit(item[2], (item[0], item[1]))  # 각 아이템 이미지 그리기

    # 타이머 표시
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render(f"Time: {int(total_time - elapsed_time)}", True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 생명, 점수 및 무적 상태 표시
    display_lives(screen, player_lives)
    display_score(screen, score)
    if is_invincible:
        display_invincibility(screen)

    if total_time - elapsed_time <= 0:
        running = False 

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

# Pygame 종료
pygame.quit()