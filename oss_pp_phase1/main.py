import pygame
import random

################################################################################################
#########################################  PHASE 2 #############################################
################################### Feature 1 & 3-build up #####################################
################################################################################################
def init_Game(): #- Feature 3 구현을 위해 게임 초기화를 모듈화 함.
    global screen_width, screen_height,screen, clock, FPS, background, character, angry_jerry, trap, tom_images, running
    # Pygame 초기화
    pygame.init()

    # 화면 크기 설정
    screen_width = 480
    screen_height = 640
    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption("톰을 피해라!!!")
    clock = pygame.time.Clock()
    FPS = 60
    running = True
    
    # 이미지 로드 및 최적화
    background = pygame.image.load(r'images/background.png').convert_alpha()
    character = [
        pygame.image.load(r'images/character-left.png').convert_alpha(),
        pygame.image.load(r'images/character-right.png').convert_alpha()
    ]
    angry_jerry = pygame.image.load(r'images/angry_jerry.png').convert_alpha()
    trap = pygame.image.load(r'images/trap.png').convert_alpha()
    tom_images = [
        pygame.image.load(r'images/tom-left.png').convert_alpha(),
        pygame.image.load(r'images/tom-right.png').convert_alpha()
    ] 
    # 이미지 수정 & 이미지 경로 상대 경로로 수정.
    
################################################################################################
#########################################  PHASE 2 #############################################
################################### Feature 1 & 3-build up #####################################
################################################################################################

def run_game(): #- Feature 3 구현을 위해 게임 시작을 함수로 모듈화 함.
    global screen_width, screen_height,screen, clock, FPS, background, character, angry_jerry, trap, tom_images, running
    # 캐릭터 크기 및 위치 설정
    character_size = character[0].get_rect().size 
    character_width = character_size[0]
    character_height = character_size[1]
    character_x_pos = (screen_width - character_width) / 2
    character_y_pos = screen_height - character_height

################################################################################################
#########################################  PHASE 2 #############################################
################################### Feature1 & 2-build up ######################################
################################################################################################

    # 캐릭터 이동 설정
    LEFT = 'left' # 캐릭터가 보는 방향 추가
    RIGHT = 'right' # 캐릭터가 보는 방향 추가
    direction_list = [LEFT, RIGHT]
    to_x = 0
    to_y = 0 # y축 이동 변수 추가
    direction = LEFT
    speed = 5

    # 톰(tom) 설정
    tom_list = []  # 톰 정보를 담을 리스트
    tom_speed = 3.5

    trap_list = []
    trap_speed = 3
    
################################################################################################
#########################################  PHASE 2 #############################################
################################### Feature1 & 2-build up ######################################
################################################################################################

    # 폰트 설정
    game_font = pygame.font.Font(None, 40)

    # 게임 시간 설정
    total_time = 50
    start_ticks = pygame.time.get_ticks()

    # 게임 루프
    running = True
    while running:
        
################################################################################################
#########################################  PHASE 2 #############################################
######################################### Feature1 #############################################
################################################################################################

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = LEFT
                    to_x -= speed
                elif event.key == pygame.K_RIGHT:
                    direction = RIGHT
                    to_x += speed
                elif event.key == pygame.K_UP:
                    to_y -= speed
                elif event.key == pygame.K_DOWN:
                    to_y += speed
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    to_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    to_y = 0

        # 캐릭터 이동 처리
        character_x_pos += to_x
        character_y_pos += to_y

        # 캐릭터 화면 밖으로 나가지 않도록 설정
        character_x_pos = max(0, min(character_x_pos, screen_width - character_width))
        character_y_pos = max(0, min(character_y_pos, screen_height - character_height))

################################################################################################
#########################################  PHASE 2 #############################################
######################################### Feature1 #############################################
################################################################################################



################################################################################################
#########################################  PHASE 2 #############################################
######################################### Feature2 #############################################
################################################################################################

        # 트랩(trap) 생성 (y 축으로 낙하)
        if random.randint(0, 150) == 0:  # 150분의 1 확률로 트랩 생성
            trap_x_pos = random.randint(0, screen_width- trap.get_width() )
            trap_y_pos = 0
            trap_list.append([trap_x_pos, trap_y_pos, trap])
        
        # 톰(tom) 생성 
        if random.randint(0, 300) == 0:  # 300분의 1 확률로 톰 생성
            tom_direction = direction_list[random.randint(0,1)]
            if tom_direction == LEFT:            
                tom_x_pos = screen_width 
                current_tom_image = tom_images[0]
            else:
                tom_x_pos = 0 
                current_tom_image = tom_images[1]
            tom_y_pos = random.randint(0, screen_height - tom_images[0].get_height())
            tom_list.append([tom_x_pos, tom_y_pos, current_tom_image,tom_direction])

        for tom in tom_list:
            if tom[3] == LEFT: # 톰이 좌측으로 이동
                tom[0] -= tom_speed
            else : # 톰이 우측으로 이동
                tom[0] += tom_speed  
                
            if tom[0] > screen_width or tom[0] < 0:  # 톰이 화면 밖으로 나가면 제거
                tom_list.remove(tom)

            # 충돌 처리 (Rect 사용)
            character_rect = character[0].get_rect(topleft=(character_x_pos, character_y_pos))
            tom_rect = tom_images[0].get_rect(topleft=(tom[0],tom[1]))
            if character_rect.colliderect(tom_rect):
                game_over()
        
        for traps in trap_list:
            traps[1] += trap_speed  # 트랩 떨어뜨리기
            if traps[1] > screen_height:  # 트랩이 화면 밖으로 나가면 제거
                trap_list.remove(traps)
            
            # 충돌 처리 (Rect 사용)
            character_rect = character[0].get_rect(topleft=(character_x_pos, character_y_pos))
            trap_rect = trap.get_rect(topleft=(traps[0],traps[1]))
            if character_rect.colliderect(trap_rect):
                game_over()
                            
        # 화면에 그리기
        if direction == LEFT:    
            current_character_image = character[0]
        else :
            current_character_image = character[1]
            
        screen.blit(background, (0, 0))
        screen.blit(current_character_image, (character_x_pos, character_y_pos))
        
        for traps in trap_list:
            trap_posi = (traps[0], traps[1])
            screen.blit(trap, trap_posi)  # 각 트랩 이미지 그리기
            
        for tom in tom_list:
            screen.blit(tom[2], (tom[0], tom[1]))  # 각 톰 이미지 그리기

################################################################################################
#########################################  PHASE 2 #############################################
######################################### Feature2 #############################################
################################################################################################

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

################################################################################################
#########################################  PHASE 2 #############################################
######################################### Feature3 #############################################
################################################################################################
def game_over():
    global screen, background, angry_jerry, running
    screen.blit(background, (0, 0))
    screen.blit(angry_jerry, (screen_width/2-30, screen_height/2+10))
    gofont = pygame.font.SysFont(None,80)
    gotext = gofont.render('GAME OVER',True,(0,0,0)) #go = gameover
    gotextpos = gotext.get_rect()
    gotextpos.center = (screen_width/2,screen_height/2-40)
    screen.blit(gotext,gotextpos)
    
    rsfont = pygame.font.SysFont(None,30)
    rstext = rsfont.render('Press R to restrart',True,(0,0,0))
    rstextpos = rstext.get_rect()
    rstextpos.center = (screen_width/2,screen_height/2+10)
    screen.blit(rstext,rstextpos)
    
    pygame.display.update()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
 

################################################################################################
#########################################  PHASE 2 #############################################
######################################### Feature3 #############################################
################################################################################################


####################
###### Phase2 ######
####################
init_Game()
run_game()