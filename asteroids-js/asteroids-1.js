// https://stackoverflow.com/questions/4037212/html-canvas-full-screen
const canvas = document.getElementById('mainCanvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// in python this is stored on the game object, but this isn't python
const ctx = canvas.getContext('2d');

// constants (SETTINGS)
const HALF_W = canvas.width / 2;
const HALF_H = canvas.height / 2;

const TRIANGLE = [(3 * Math.PI / 2), (Math.PI / 4), (3 * Math.PI / 4)];
const PLAYER_R = 16 // player radius (reminder: this is only HALF the player size)
const PLAYER_V = 4 // player max vel
const T_OFFSET = Math.PI / 2; // theta offset for player rotations; consequence of triangle pointing along y-axis

const DEF_COLOR = '#FFF'

// I know libraries for this exist but sometimes you want a scoop of vanilla
class Vector2 {
  constructor(x=0, y=0) {
    this.update(x, y);
  }

  update(x, y, scale=1) {
    this.x = x * scale;
    this.y = y * scale;
  }

  apply(func) {
    this.x = func(this.x);
    this.y = func(this.y);
  }
}

class GameObject {
  constructor(loc=new Vector2()) {
    this.loc = loc;
  }

  tracePoints = (points, enclose=true) => {
    ctx.beginPath();
    ctx.strokeStyle = DEF_COLOR;
    if (enclose) ctx.moveTo(points[points.length-1].x, points[points.length-1].y);
    points.forEach(point => {
      ctx.lineTo(point.x, point.y);
    });
    ctx.stroke();
    ctx.closePath();
  }
}

class Player extends GameObject {
  constructor() {
    super(new Vector2(HALF_W, HALF_H));
    this.vel = new Vector2();
    this.accel = 5; //0.02;
    this.frict = 0.05; //0.02;
    this.theta = 0;
    document.addEventListener('mousemove', this.onMouseMove);
    document.addEventListener('keydown', this.onKeyDown);
  }

  onMouseMove = (event) => {
    this.theta = Math.atan2(event.y-this.loc.y, event.x-this.loc.x) + T_OFFSET;
    this.theta %= 2 * Math.PI; // radians
  }

  onKeyDown = (event) => {
    if (event.key === ' ') {
      this.vel.update(Math.cos(this.theta-T_OFFSET), Math.sin(this.theta-T_OFFSET), this.accel);
    }
    // elif ... projectile keybinding
  }

  _safeUpdateVelocity = (v) => {
    v *= (1 - this.frict);
    v = Math.max(-PLAYER_V, Math.min(v, PLAYER_V));
    if (Math.abs(v) < 0.0001) v = 0;
    return v;
  }

  update() {
    this.vel.apply(this._safeUpdateVelocity);
    this.loc.x = Math.max(0, Math.min(this.loc.x + this.vel.x, canvas.width));
    this.loc.y = Math.max(0, Math.min(this.loc.y + this.vel.y, canvas.height));
    // check for asteroid collisions and initiate game over if so
  }

  render() {
    var points = [];
    TRIANGLE.forEach(point => {
      var x = this.loc.x + PLAYER_R * Math.cos(point + this.theta);
      var y = this.loc.y + PLAYER_R * Math.sin(point + this.theta);
      points.push(new Vector2(x, y));
    });
    this.tracePoints(points);
  }
}

class Game {
  constructor() {
    // screen setup (see top of file)
    // setup clock object for game loop
    this.deltaTime = 1;
    this.newGame();
    // set font for UI
    this.run = this.run.bind(this); // https://stackoverflow.com/q/4011793/3178898
  }

  newGame() {
    this.gameOver = false;
    this.score = 0;
    this.player = new Player(this);
    // set timer for the next asteroid to spawn
  }

  reset() {
    // loop through game objects and destroy them
    this.newGame();
  }

  // spawn asteroid event object (may not exist for JS)

  spawnAsteroid(x, y, size, angle) {} // spawn in asteroids

  getAsteroids() {} // get all of the asteroids being tracked by the game

  checkAsteroidCollision(gameObj) {
    // loop through asteroids in this object and see if any overlap with gameObj
    // if they do, the asteroid is destroyed, score is increased and returns true.
    // returns false otherwise.
    return false;
  }

  events() {} // event loop for handling inputs. may not be needed for JS

  update() {
    this.player.update();
  }

  render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    this.player.render();
  } 

  run() {
    this.events();
    this.update();
    this.render();
    // cleanup deregistered gameObjects
    requestAnimationFrame(this.run); // https://isaacsukin.com/news/2015/01/detailed-explanation-javascript-game-loops-and-timing
  }
}

var game = new Game();
requestAnimationFrame(game.run);