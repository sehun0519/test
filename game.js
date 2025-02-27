// 게임 캔버스와 컨텍스트 설정
const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');
const playerScoreDisplay = document.getElementById('player-score');
const aiScoreDisplay = document.getElementById('ai-score');

// 게임 상수
const GRAVITY = 0.5;
const JUMP_FORCE = -12;
const PLAYER_SPEED = 5;
const AI_SPEED = 4;
const BALL_SPEED_X = 5;
const BALL_SPEED_Y = -8;

// 게임 변수
let gameRunning = false;
let playerScore = 0;
let aiScore = 0;
let gameLoopStarted = false; // 게임 루프 시작 여부 확인용 변수 추가

// 피카츄 이미지 로딩
const playerPikachu = new Image();
playerPikachu.src = 'https://i.imgur.com/HHQ0Kgm.png'; // 적절한 피카츄 이미지 URL 필요

const aiPikachu = new Image();
aiPikachu.src = 'https://i.imgur.com/HHQ0Kgm.png'; // 적절한 피카츄 이미지 URL 필요

// 배구 이미지 로딩
const ballImg = new Image();
ballImg.src = 'https://i.imgur.com/4GpAdRn.png'; // 적절한 공 이미지 URL 필요

// 게임 객체
const player = {
    x: 150,
    y: canvas.height - 100,
    width: 80,
    height: 80,
    velocityY: 0,
    score: 0,
    isJumping: false,
    moveLeft: false,
    moveRight: false
};

const ai = {
    x: canvas.width - 150 - 80,
    y: canvas.height - 100,
    width: 80,
    height: 80,
    velocityY: 0,
    score: 0,
    isJumping: false
};

const ball = {
    x: canvas.width / 2,
    y: 50,
    radius: 20,
    velocityX: BALL_SPEED_X,
    velocityY: 0
};

const net = {
    x: canvas.width / 2 - 2,
    y: canvas.height - 100,
    width: 4,
    height: 100
};

// 키보드 조작
const keys = {};

document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// 게임 초기화
function resetGame() {
    player.x = 150;
    player.y = canvas.height - 100;
    player.velocityY = 0;
    player.isJumping = false;

    ai.x = canvas.width - 150 - 80;
    ai.y = canvas.height - 100;
    ai.velocityY = 0;
    ai.isJumping = false;

    ball.x = canvas.width / 2;
    ball.y = 50;
    ball.velocityX = BALL_SPEED_X * (Math.random() > 0.5 ? 1 : -1);
    ball.velocityY = 0;
}

// 충돌 감지
function collision(ball, player) {
    // 공의 중심과 플레이어 사각형 사이의 최단 거리 계산
    let closestX = Math.max(player.x, Math.min(ball.x, player.x + player.width));
    let closestY = Math.max(player.y, Math.min(ball.y, player.y + player.height));
    
    // 최단 거리 계산
    const dx = ball.x - closestX;
    const dy = ball.y - closestY;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    return distance < ball.radius;
}

// 게임 업데이트
function update() {
    // 게임 실행 중이 아니어도 키 입력은 처리 (준비 상태)
    handlePlayerInput();
    
    if (!gameRunning) return;

    // 플레이어 중력
    player.velocityY += GRAVITY;
    player.y += player.velocityY;
    if (player.y > canvas.height - player.height) {
        player.y = canvas.height - player.height;
        player.velocityY = 0;
        player.isJumping = false;
    }

    // AI 움직임
    updateAI();

    // 공 움직임
    ball.x += ball.velocityX;
    ball.y += ball.velocityY;
    ball.velocityY += GRAVITY;

    // 공이 바닥에 닿았을 때
    if (ball.y > canvas.height - ball.radius) {
        // 점수 계산
        if (ball.x < canvas.width / 2) {
            aiScore++;
            aiScoreDisplay.textContent = aiScore;
        } else {
            playerScore++;
            playerScoreDisplay.textContent = playerScore;
        }
        resetGame();
    }

    // 공과 벽의 충돌
    if (ball.x - ball.radius < 0 || ball.x + ball.radius > canvas.width) {
        ball.velocityX = -ball.velocityX;
    }

    // 공이 천장에 닿았을 때
    if (ball.y - ball.radius < 0) {
        ball.velocityY = -ball.velocityY;
    }

    // 공과 네트의 충돌
    if (ball.x + ball.radius > net.x && ball.x - ball.radius < net.x + net.width &&
        ball.y + ball.radius > net.y) {
        ball.velocityX = -ball.velocityX;
    }

    // 공과 플레이어의 충돌
    if (collision(ball, player)) {
        // 튕겨나가는 방향 조정
        ball.velocityY = BALL_SPEED_Y;
        // 충돌 각도에 따라 X 속도 조정
        const playerCenterX = player.x + player.width / 2;
        let angle = (ball.x - playerCenterX) / (player.width / 2);
        ball.velocityX = BALL_SPEED_X * angle;
    }

    // 공과 AI의 충돌
    if (collision(ball, ai)) {
        // 튕겨나가는 방향 조정
        ball.velocityY = BALL_SPEED_Y;
        // 충돌 각도에 따라 X 속도 조정
        const aiCenterX = ai.x + ai.width / 2;
        let angle = (ball.x - aiCenterX) / (ai.width / 2);
        ball.velocityX = BALL_SPEED_X * angle;
    }
}

// 플레이어 입력 처리 함수 분리
function handlePlayerInput() {
    if (keys['a'] || keys['A']) {
        player.x -= PLAYER_SPEED;
        if (player.x < 0) player.x = 0;
    }
    if (keys['d'] || keys['D']) {
        player.x += PLAYER_SPEED;
        if (player.x > canvas.width / 2 - player.width) player.x = canvas.width / 2 - player.width;
    }
    if ((keys['w'] || keys['W']) && !player.isJumping) {
        player.velocityY = JUMP_FORCE;
        player.isJumping = true;
    }
}

// AI 업데이트 함수 분리
function updateAI() {
    // AI 기본 움직임 - 공이 어디에 있든 공을 따라감
    const aiCenterX = ai.x + ai.width / 2;
    
    if (ball.x > aiCenterX + 10) {
        ai.x += AI_SPEED;
        // AI가 화면 오른쪽 끝을 넘지 않도록 제한
        if (ai.x > canvas.width - ai.width) ai.x = canvas.width - ai.width;
    } else if (ball.x < aiCenterX - 10) {
        ai.x -= AI_SPEED;
        // AI가 네트를 넘지 않도록 제한
        if (ai.x < canvas.width / 2) ai.x = canvas.width / 2;
    }
    
    // 공이 AI 쪽에 있고, 정해진 높이 이하로 내려오고 있을 때 점프
    if (ball.x > canvas.width / 2 && 
        ball.y > canvas.height / 2 && 
        ball.y < canvas.height - 150 && 
        ball.velocityY > 0 && 
        !ai.isJumping && 
        Math.abs(ball.x - aiCenterX) < 150) {
        ai.velocityY = JUMP_FORCE * 0.9; // 플레이어보다 조금 약하게 점프
        ai.isJumping = true;
    }
    
    // AI 중력
    ai.velocityY += GRAVITY;
    ai.y += ai.velocityY;
    if (ai.y > canvas.height - ai.height) {
        ai.y = canvas.height - ai.height;
        ai.velocityY = 0;
        ai.isJumping = false;
    }
}

// 게임 화면 그리기
function draw() {
    // 배경 지우기
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 바닥 그리기
    ctx.fillStyle = '#8B4513';
    ctx.fillRect(0, canvas.height - 20, canvas.width, 20);
    
    // 네트 그리기
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(net.x, net.y, net.width, net.height);
    
    // 플레이어 그리기
    ctx.drawImage(playerPikachu, player.x, player.y, player.width, player.height);
    
    // AI 그리기
    ctx.drawImage(aiPikachu, ai.x, ai.y, ai.width, ai.height);
    
    // 공 그리기
    ctx.drawImage(ballImg, ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2);
}

// 게임 루프
function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// 게임 시작
startBtn.addEventListener('click', () => {
    gameRunning = true;
    resetGame();
    
    // 게임 루프가 아직 시작되지 않았다면 시작
    if (!gameLoopStarted) {
        gameLoopStarted = true;
        gameLoop();
    }
});

// 게임 재시작
resetBtn.addEventListener('click', () => {
    playerScore = 0;
    aiScore = 0;
    playerScoreDisplay.textContent = playerScore;
    aiScoreDisplay.textContent = aiScore;
    gameRunning = true;  // 재시작 시 게임 실행 상태로 설정
    resetGame();
    
    // 게임 루프가 아직 시작되지 않았다면 시작
    if (!gameLoopStarted) {
        gameLoopStarted = true;
        gameLoop();
    }
});

// 이미지가 로드된 후 초기 화면 그리기
window.onload = () => {
    draw();
    
    // 이미지 로딩 오류 처리
    playerPikachu.onerror = () => {
        console.error("피카츄 이미지를 로드할 수 없습니다.");
        playerPikachu.src = ''; // 이미지 대신 직접 그리도록
    };
    
    ballImg.onerror = () => {
        console.error("공 이미지를 로드할 수 없습니다.");
        ballImg.src = ''; // 이미지 대신 직접 그리도록
    };
};
