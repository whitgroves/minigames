const canvas = document.getElementById("mainCanvas");
const ctx = canvas.getContext("2d");

// start (1/10): https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Create_the_Canvas_and_draw_on_it

// ctx.beginPath();
// ctx.rect(20, 40, 50, 50);
// ctx.fillStyle = "#FF0000";
// ctx.fill();
// ctx.closePath();

// ctx.beginPath();
// ctx.arc(240, 160, 20, 0, Math.PI * 2);
// ctx.fillStyle = "green";
// ctx.fill();
// ctx.closePath();

// ctx.beginPath();
// ctx.rect(160, 10, 100, 40);
// ctx.strokeStyle = "rgba(0, 0, 255, 0.5)";
// ctx.stroke();
// ctx.closePath();

// checkpoint (2/10): https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Move_the_ball

let x = canvas.width / 2;
let y = canvas.height - 30;

let dx = 2;
let dy = -2;

// function drawBall() {
//     ctx.clearRect(0, 0, canvas.width, canvas.height);
//     ctx.beginPath();
//     ctx.arc(x, y, 10, 0, Math.PI * 2);
//     ctx.fillStyle = "#0095DD";
//     ctx.fill();
//     ctx.closePath();
// }

// function draw() {
//     drawBall();
//     x += dx;
//     y += dy;
// }
// setInterval(draw, 10);

// checkpoint (3/10): https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Bounce_off_the_walls

const ballRadius = 10;

// function drawBall() {
//     ctx.clearRect(0, 0, canvas.width, canvas.height);
//     ctx.beginPath();
//     ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
//     ctx.fillStyle = "#0095DD";
//     ctx.fill();
//     ctx.closePath();
// }

// function draw() {
//     drawBall();
//     if (x + dx < ballRadius || x + dx > canvas.width - ballRadius) {
//         dx = -dx;
//     }
//     if (y + dy < ballRadius || y + dy > canvas.height - ballRadius) {
//         dy = -dy;
//     }
//     x += dx;
//     y += dy;
// }
// setInterval(draw, 10);

// checkpoint (4/10): https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Paddle_and_keyboard_controls

const paddleHeight = 10;
const paddleWidth = 75;
let paddleX = (canvas.width - paddleWidth) / 2;
let defaultColor = "#0095DD"

let rightPressed = false;
let leftPressed = false;
let paddleSpeed = 7;

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

function keyDownHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = true;
    }
    if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = false;
    }
    if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = false;
    }
}

function drawCircle() {
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = defaultColor;
    ctx.fill();
    ctx.closePath();
}

function drawPaddle() {
    ctx.beginPath();
    ctx.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
    ctx.fillStyle = defaultColor;
    ctx.fill();
    ctx.closePath();
}

// function draw() {
//     ctx.clearRect(0, 0, canvas.width, canvas.height);

//     drawPaddle();
//     drawBall();

//     if (rightPressed) {
//         paddleX = Math.min(paddleX + paddleSpeed, canvas.width - paddleWidth);
//     } else if (leftPressed) {
//         paddleX = Math.max(paddleX - paddleSpeed, 0);
//     }

//     if (x + dx < ballRadius || x + dx > canvas.width - ballRadius) {
//         dx = -dx;
//     }

//     if (y + dy < ballRadius || y + dy > canvas.height - ballRadius) {
//         dy = -dy;
//     }

//     x += dx;
//     y += dy;
// }
// setInterval(draw, 10);

// checkpoint (5/10): https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Game_over

const interval = setInterval(run, 10);

// function draw() {
//     ctx.clearRect(0, 0, canvas.width, canvas.height);

//     drawPaddle();
//     drawBall();

//     if (rightPressed) {
//         paddleX = Math.min(paddleX + paddleSpeed, canvas.width - paddleWidth);
//     } else if (leftPressed) {
//         paddleX = Math.max(paddleX - paddleSpeed, 0);
//     }

//     if (x + dx < ballRadius || x + dx > canvas.width - ballRadius) {
//         dx = -dx;
//     }

//     if (y + dy < ballRadius) {
//         dy = -dy;
//     } else if (y + dy > canvas.height - ballRadius) {
//         if (x > paddleX && x < paddleX + paddleWidth) {
//             dy = -dy;
//             dx *= 1.1;
//             dy *= 1.1;
//         } else {
//             alert("Game over, man, game over!")
//             document.location.reload();
//             clearInterval(interval); // ends game in chrome
//         }
//     }

//     x += dx;
//     y += dy;
// }

// checkpoint(6/10): https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Build_the_brick_field

const brickRowCount = 4;
const brickColCount = 5;
const brickWidth = 75;
const brickHeight = 20;
const brickPadding = 10;
const brickOffsetTop = 20;
const brickOffsetLeft = 30;

const bricks = [];
for (let col = 0; col < brickColCount; col++) {
    bricks[col] = [];
    for (let row = 0; row < brickRowCount; row++) {
        bricks[col][row] = { x: 0, y: 0 };
    }
}

function drawBricks() {
    for (let col = 0; col < brickColCount; col++) {
        for (let row = 0; row < brickRowCount; row++) {
            const brickX = col * (brickWidth + brickPadding) + brickOffsetLeft;
            const brickY = row * (brickHeight + brickPadding) + brickOffsetTop;
            bricks[col][row].x = 0;
            bricks[col][row].y = 0;
            ctx.beginPath();
            ctx.rect(brickX, brickY, brickWidth, brickHeight);
            ctx.fillStyle = defaultColor;
            ctx.fill();
            ctx.closePath();
        }
    }
}

function run() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawBricks();
    drawPaddle();
    drawCircle();

    if (rightPressed) {
        paddleX = Math.min(paddleX + paddleSpeed, canvas.width - paddleWidth);
    } else if (leftPressed) {
        paddleX = Math.max(paddleX - paddleSpeed, 0);
    }

    if (x + dx < ballRadius || x + dx > canvas.width - ballRadius) {
        dx = -dx;
    }

    if (y + dy < ballRadius) {
        dy = -dy;
    } else if (y + dy > canvas.height - ballRadius) {
        if (x > paddleX && x < paddleX + paddleWidth) {
            dy = -dy;
            dx *= 1.1;
            dy *= 1.1;
        } else {
            alert("Game over, man, game over!")
            document.location.reload();
            clearInterval(interval); // ends game in chrome
        }
    }

    x += dx;
    y += dy;
}

// checkpoint (7/10): https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Collision_detection
