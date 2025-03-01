import pygame
import sys
import random
import os

# 게임 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("피카추 배구")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 프레임 설정
clock = pygame.time.Clock()
FPS = 60

# 중력 설정
GRAVITY = 0.6  # 중력 약간 감소하여 공중에 더 오래 머물게 함

# 게임 상수
BOUNCE_SOUND_COOLDOWN = 10  # 소리가 너무 자주 나지 않게

# 이미지 로드 함수
def load_image(name, scale=1):
    """이미지를 로드하고 크기를 조정하는 함수"""
    # 파일이 존재하는지 먼저 확인
    if os.path.exists(name):
        try:
            image = pygame.image.load(name)
            image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
            return image
        except pygame.error as e:
            print(f"이미지를 로드할 수 없습니다: {name}")
            print(f"에러: {e}")
    else:
        print(f"이미지 파일을 찾을 수 없습니다: {name}, 대체 이미지를 생성합니다.")
    
    # 이미지가 없을 경우 간단한 도형으로 대체
    if "pikachu" in name:
        surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(surf, YELLOW, (0, 0, 100, 100))
        # 얼굴 특징 추가
        pygame.draw.circle(surf, BLACK, (30, 30), 10)  # 왼쪽 눈
        pygame.draw.circle(surf, BLACK, (70, 30), 10)  # 오른쪽 눈
        pygame.draw.arc(surf, BLACK, (25, 40, 50, 40), 0, 3.14, 3)  # 입
    elif "ball" in name:
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(surf, RED, (25, 25), 25)
    elif "net" in name:
        surf = pygame.Surface((20, 150), pygame.SRCALPHA)
        # 네트 격자 패턴 만들기
        for y in range(0, 150, 10):
            pygame.draw.line(surf, BLACK, (0, y), (20, y), 2)
        pygame.draw.line(surf, BLACK, (10, 0), (10, 150), 2)
    elif "background" in name:
        surf = pygame.Surface((WIDTH, HEIGHT))
        # 하늘색 배경에 구름 몇 개 추가
        surf.fill((135, 206, 235))  # 하늘색
        for _ in range(5):
            cloud_x = random.randint(0, WIDTH)
            cloud_y = random.randint(0, HEIGHT // 2)
            pygame.draw.circle(surf, WHITE, (cloud_x, cloud_y), random.randint(20, 40))
    else:
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        surf.fill((255, 0, 255))  # 디폴트 매젠타 색상
    
    return surf

# 게임 리소스 로드
# 리소스가 없으면 기본 도형으로 대체됩니다
try:
    os.makedirs("assets", exist_ok=True)
except:
    pass

pikachu1_img = load_image("assets/pikachu1.png", 0.2)
pikachu2_img = load_image("assets/pikachu2.png", 0.2)
ball_img = load_image("assets/ball.png", 0.1)
background_img = load_image("assets/background.png", 1)
net_img = load_image("assets/net.png", 0.5)

# 피카추 클래스
class Pikachu(pygame.sprite.Sprite):
    def __init__(self, x, y, player_num):
        super().__init__()
        self.player_num = player_num
        if player_num == 1:
            self.image = pikachu1_img
        else:
            self.image = pikachu2_img
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.vel_x = 0
        self.jump = False
        self.score = 0
    
    def update(self):
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        
        # 플레이어 1 (왼쪽) 조작
        if self.player_num == 1:
            if keys[pygame.K_a]:
                self.vel_x = -7  # 속도 증가
            elif keys[pygame.K_d]:
                self.vel_x = 7  # 속도 증가
            else:
                # 점차 속도 감소
                if abs(self.vel_x) > 0.5:
                    self.vel_x *= 0.9
                else:
                    self.vel_x = 0
                
            # 점프 (공중에서도 일정 시간마다 추가 점프 가능)
            if keys[pygame.K_w]:
                if not self.jump:
                    self.vel_y = -15
                    self.jump = True
                # 이미 점프 중일 때 작은 부스트 (공중에서 추가 조작)
                elif self.vel_y > 0 and self.rect.bottom < HEIGHT - 50:
                    self.vel_y -= 0.4  # 낙하 속도 감소
        
        # 플레이어 2 (오른쪽) 조작
        else:
            if keys[pygame.K_LEFT]:
                self.vel_x = -7  # 속도 증가
            elif keys[pygame.K_RIGHT]:
                self.vel_x = 7  # 속도 증가
            else:
                # 점차 속도 감소
                if abs(self.vel_x) > 0.5:
                    self.vel_x *= 0.9
                else:
                    self.vel_x = 0
                
            # 점프 (공중에서도 일정 시간마다 추가 점프 가능)
            if keys[pygame.K_UP]:
                if not self.jump:
                    self.vel_y = -15
                    self.jump = True
                # 이미 점프 중일 때 작은 부스트 (공중에서 추가 조작)
                elif self.vel_y > 0 and self.rect.bottom < HEIGHT - 50:
                    self.vel_y -= 0.4  # 낙하 속도 감소
        
        # 점프 키를 계속 누르지 않으면 빨리 낙하
        if self.player_num == 1 and not keys[pygame.K_w] and self.vel_y < 0:
            self.vel_y *= 0.9  # 상승 중 점프 키를 놓으면 빨리 떨어짐
        elif self.player_num == 2 and not keys[pygame.K_UP] and self.vel_y < 0:
            self.vel_y *= 0.9  # 상승 중 점프 키를 놓으면 빨리 떨어짐
        
        # 중력 적용
        self.vel_y += GRAVITY
        
        # 공중에서 최대 낙하 속도 제한
        if self.vel_y > 12:
            self.vel_y = 12
        
        # 위치 업데이트
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # 바닥 충돌 확인
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.jump = False
        
        # 좌우 경계 확인
        if self.player_num == 1:
            # 플레이어 1은 코트 왼쪽 절반에만 있을 수 있음
            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right >= WIDTH // 2 - 10:
                self.rect.right = WIDTH // 2 - 10
        else:
            # 플레이어 2는 코트 오른쪽 절반에만 있을 수 있음
            if self.rect.left <= WIDTH // 2 + 10:
                self.rect.left = WIDTH // 2 + 10
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH

# 볼 클래스
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ball_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = random.choice([-3, 3])
        self.vel_y = -5
        self.last_hit_by = 0  # 마지막으로 공을 친 플레이어
        self.consecutive_hits = 0  # 연속 히트 카운트
        self.sound_cooldown = 0  # 소리 쿨다운
    
    def update(self, pikachu1, pikachu2, net_rect):
        # 소리 쿨다운 감소
        if self.sound_cooldown > 0:
            self.sound_cooldown -= 1
            
        # 중력 적용 - 속도 제한 추가
        self.vel_y += GRAVITY * 0.5
        
        # 공중에서 최대 속도 제한
        if self.vel_y > 14:
            self.vel_y = 14
        if abs(self.vel_x) > 12:
            self.vel_x = 12 * (1 if self.vel_x > 0 else -1)
        
        # 위치 업데이트
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # 바닥 충돌
        if self.rect.bottom >= HEIGHT - 50:
            # 득점 처리
            if self.rect.centerx < WIDTH // 2:
                pikachu2.score += 1
                self.reset(2)  # 플레이어 2가 득점하여 서브권 획득
            else:
                pikachu1.score += 1
                self.reset(1)  # 플레이어 1이 득점하여 서브권 획득
            
            # 연속 히트 카운트 리셋
            self.consecutive_hits = 0
        
        # 천장 충돌 - 튕김 감소
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vel_y = abs(self.vel_y) * 0.8
            
            # 소리 처리 (나중에 추가)
            if self.sound_cooldown == 0:
                self.sound_cooldown = BOUNCE_SOUND_COOLDOWN
        
        # 좌우 벽 충돌 - 튕김 감소
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vel_x = abs(self.vel_x) * 0.9
            
            # 소리 처리 (나중에 추가)
            if self.sound_cooldown == 0:
                self.sound_cooldown = BOUNCE_SOUND_COOLDOWN
        
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.vel_x = -abs(self.vel_x) * 0.9
            
            # 소리 처리 (나중에 추가)
            if self.sound_cooldown == 0:
                self.sound_cooldown = BOUNCE_SOUND_COOLDOWN
        
        # 네트 충돌
        if self.rect.colliderect(net_rect):
            # 왼쪽에서 오른쪽으로 가는 경우
            if self.vel_x > 0 and self.rect.centerx < net_rect.centerx:
                self.rect.right = net_rect.left
                self.vel_x = -abs(self.vel_x) * 0.9
            # 오른쪽에서 왼쪽으로 가는 경우
            elif self.vel_x < 0 and self.rect.centerx > net_rect.centerx:
                self.rect.left = net_rect.right
                self.vel_x = abs(self.vel_x) * 0.9
            # 위에서 아래로 가는 경우
            elif self.vel_y > 0 and self.rect.centery < net_rect.top:
                self.rect.bottom = net_rect.top
                self.vel_y = -abs(self.vel_y) * 0.7  # 반발력 감소
            # 아래에서 위로 가는 경우 (거의 발생하지 않음)
            elif self.vel_y < 0 and self.rect.centery > net_rect.bottom:
                self.rect.top = net_rect.bottom
                self.vel_y = abs(self.vel_y) * 0.7  # 반발력 감소
                
            # 소리 처리 (나중에 추가)
            if self.sound_cooldown == 0:
                self.sound_cooldown = BOUNCE_SOUND_COOLDOWN
        
        # 피카추와 충돌
        if pygame.sprite.collide_rect(self, pikachu1):
            self.handle_pikachu_collision(pikachu1)
            
            # 연속 히트 시스템 - 공이 더 빨라지고 더 높이 튀게 됨
            if self.last_hit_by == 1:
                self.consecutive_hits += 1
            else:
                self.consecutive_hits = 1
                
            self.last_hit_by = 1
        
        if pygame.sprite.collide_rect(self, pikachu2):
            self.handle_pikachu_collision(pikachu2)
            
            # 연속 히트 시스템 - 공이 더 빨라지고 더 높이 튀게 됨
            if self.last_hit_by == 2:
                self.consecutive_hits += 1
            else:
                self.consecutive_hits = 1
                
            self.last_hit_by = 2
            
        # 연속 히트에 따른 속도 보너스 (최대 3회)
        bonus = min(self.consecutive_hits, 3) * 0.2
        if self.consecutive_hits > 1:
            # 속도 증가 (최대 제한 내에서)
            max_x_vel = 12 * (1 + bonus)
            if abs(self.vel_x) > max_x_vel:
                self.vel_x = max_x_vel * (1 if self.vel_x > 0 else -1)
                
            # 점프 높이 증가 (최대 제한 내에서)
            if self.vel_y < 0:  # 올라가는 중일 때만
                self.vel_y *= (1 + bonus * 0.3)  # 높이 약간 증가
    
    def handle_pikachu_collision(self, pikachu):
        # 충돌이 일어나면 주로 위로 튀기게 하되, 방향별 처리도 개선
        
        # 공을 친 횟수에 따른 보너스 효과
        combo_bonus = min(self.consecutive_hits, 3) * 0.2
        
        # 위에서 아래로 충돌 (피카추 머리 위에서 충돌)
        if self.rect.bottom >= pikachu.rect.top and self.rect.top < pikachu.rect.top:
            # 위쪽 충돌 - 항상 위로 튕기게 함
            self.rect.bottom = pikachu.rect.top
            
            # 점프 키를 누르고 있으면 더 강하게 튀기게 함
            keys = pygame.key.get_pressed()
            jump_pressed = False
            
            if pikachu.player_num == 1 and keys[pygame.K_w]:
                jump_pressed = True
            elif pikachu.player_num == 2 and keys[pygame.K_UP]:
                jump_pressed = True
                
            if jump_pressed:
                self.vel_y = -18 * (1 + combo_bonus)  # 강한 반발력 + 콤보 보너스
            else:
                self.vel_y = -12 * (1 + combo_bonus)  # 일반 반발력 + 콤보 보너스
                
            # 플레이어 움직임에 따라 공의 수평 속도 조정
            if pikachu.vel_x != 0:
                self.vel_x = pikachu.vel_x * 1.8  # 더 강하게 플레이어 방향으로 움직임
            
        # 측면 충돌 (왼쪽, 오른쪽)
        elif abs(self.rect.right - pikachu.rect.left) < 15:
            # 오른쪽에서 왼쪽으로 충돌
            self.rect.right = pikachu.rect.left
            self.vel_x = -abs(self.vel_x) - 2 * (1 + combo_bonus)  # 더 빠르게 반대 방향으로
            self.vel_y = -8 * (1 + combo_bonus * 0.5)  # 약간 위로도 튀기게 함
            
        elif abs(self.rect.left - pikachu.rect.right) < 15:
            # 왼쪽에서 오른쪽으로 충돌
            self.rect.left = pikachu.rect.right
            self.vel_x = abs(self.vel_x) + 2 * (1 + combo_bonus)  # 더 빠르게 반대 방향으로
            self.vel_y = -8 * (1 + combo_bonus * 0.5)  # 약간 위로도 튀기게 함
            
        # 아래에서 위로 충돌 (피카추 아래에서 충돌 - 거의 발생 안함)
        elif self.rect.top <= pikachu.rect.bottom and self.rect.bottom > pikachu.rect.bottom:
            # 아래에서 위로 충돌 - 살짝 아래로 내려감
            self.rect.top = pikachu.rect.bottom
            self.vel_y = 4
            
        # 다른 모든 경우 - 일반적인 상향 반발
        else:
            # 기본 반응 - 항상 어느 정도 위로 튀기게 함
            if self.vel_y > 0:  # 아래로 떨어지는 중이었다면
                self.vel_y = -10 * (1 + combo_bonus * 0.5)
            else:
                self.vel_y -= 2 * (1 + combo_bonus)  # 더 높이 올라가게 함
                
            # 수평 속도에 영향
            if abs(pikachu.vel_x) > 0:
                self.vel_x = pikachu.vel_x * 1.2 * (1 + combo_bonus * 0.3)
        
        # 소리 처리 (나중에 추가)
        if self.sound_cooldown == 0:
            self.sound_cooldown = BOUNCE_SOUND_COOLDOWN
    
    def reset(self, server):
        """득점 후 공을 재배치하는 함수"""
        self.vel_y = -5
        
        if server == 1:
            self.rect.x = WIDTH // 4
            self.vel_x = random.choice([-3, 3])
        else:
            self.rect.x = 3 * WIDTH // 4
            self.vel_x = random.choice([-3, 3])
        
        self.rect.y = HEIGHT // 3
        self.last_hit_by = 0

# 게임 요소 초기화
pikachu1 = Pikachu(WIDTH // 4, HEIGHT - 150, 1)
pikachu2 = Pikachu(3 * WIDTH // 4, HEIGHT - 150, 2)
ball = Ball(WIDTH // 2, HEIGHT // 3)

# 네트 설정
net_rect = pygame.Rect(WIDTH // 2 - 5, HEIGHT - 200, 10, 150)

# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 게임 상태
game_active = True
winner = None
MAX_SCORE = 15

# 게임 메인 루프
def main():
    global game_active, winner
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # 게임이 끝났을 때 스페이스바로 재시작
                if not game_active and event.key == pygame.K_SPACE:
                    reset_game()
        
        # 배경 그리기
        screen.blit(background_img, (0, 0))
        
        # 바닥 그리기
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - 50, WIDTH, 50))
        
        # 네트 그리기
        screen.blit(net_img, (WIDTH // 2 - net_img.get_width() // 2, HEIGHT - 50 - net_img.get_height()))
        
        # 점수 표시
        score_text = font.render(f"{pikachu1.score} - {pikachu2.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        
        if game_active:
            # 게임 요소 업데이트
            pikachu1.update()
            pikachu2.update()
            ball.update(pikachu1, pikachu2, net_rect)
            
            # 연속 히트 카운트 표시
            if ball.consecutive_hits > 1:
                combo_color = (255, 255 - min(ball.consecutive_hits * 30, 255), 0)  # 노란색에서 점점 붉은색으로
                combo_text = font.render(f"콤보: {ball.consecutive_hits}x", True, combo_color)
                screen.blit(combo_text, (WIDTH // 2 - combo_text.get_width() // 2, 60))
                
                # 히트 횟수에 따라 공의 색상 변경 효과
                if ball.consecutive_hits >= 3:
                    glow_radius = 30 + (ball.consecutive_hits - 3) * 5
                    glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surf, (*combo_color, 100), (glow_radius, glow_radius), glow_radius)
                    screen.blit(glow_surf, (ball.rect.centerx - glow_radius, ball.rect.centery - glow_radius))
            
            # 승자 확인
            if pikachu1.score >= MAX_SCORE:
                game_active = False
                winner = "피카추 1"
            elif pikachu2.score >= MAX_SCORE:
                game_active = False
                winner = "피카추 2"
        else:
            # 게임 종료 화면
            winner_text = font.render(f"{winner} 승리!", True, WHITE)
            restart_text = font.render("다시 시작하려면 스페이스바를 누르세요", True, WHITE)
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
        
        # 요소 그리기
        screen.blit(pikachu1.image, pikachu1.rect)
        screen.blit(pikachu2.image, pikachu2.rect)
        screen.blit(ball.image, ball.rect)
        
        # 화면 업데이트
        pygame.display.flip()
        clock.tick(FPS)

def reset_game():
    """게임을 초기 상태로 재설정하는 함수"""
    global game_active, winner
    
    pikachu1.score = 0
    pikachu2.score = 0
    pikachu1.rect.x = WIDTH // 4
    pikachu1.rect.y = HEIGHT - 150
    pikachu2.rect.x = 3 * WIDTH // 4
    pikachu2.rect.y = HEIGHT - 150
    ball.reset(random.choice([1, 2]))
    
    game_active = True
    winner = None

# 게임 시작
if __name__ == "__main__":
    main()
