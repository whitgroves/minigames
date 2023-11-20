// https://stackoverflow.com/questions/4037212/html-canvas-full-screen
const canvas = document.getElementById('mainCanvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// in python this is stored on the game object, but this isn't python
const ctx = canvas.getContext('2d');

// constants (SETTINGS)
const HALF_W = canvas.width / 2;
const HALF_H = canvas.height / 2;
const FPS = 60
const TIME_STEP = 1000 / FPS;

const TRIANGLE = [(3 * Math.PI / 2), (Math.PI / 4), (3 * Math.PI / 4)];
const PLAYER_R = 16 // player radius (reminder: this is only HALF the player size)
const PLAYER_V = 8 // player max vel
const T_OFFSET = Math.PI / 2; // theta offset for player rotations; consequence of triangle pointing along y-axis

const DEF_COLOR = '#FFF'

// I know libraries for this exist but sometimes you want a scoop of vanilla
class Vector2 {
  constructor(x=0, y=0) {
    this.set(x, y);
  }

  set(x, y) {
    this.x = x;
    this.y = y;
  }

  add(x, y, scale=1) {
    this.x += x * scale;
    this.y += y * scale;
  }

  apply(func) {
    this.x = func(this.x);
    this.y = func(this.y);
  }
}

class GameObject {
  constructor(game, loc=new Vector2()) {
    this.game = game;
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
  constructor(game) {
    super(game, new Vector2(HALF_W, HALF_H));
    this.vel = new Vector2();
    this.accel = 0.02;
    this.frict = 0.015;
    this.theta = 0;
    this.target = null;
    this.boosting = false;
    this.registerEvents();
  }

  // generally, event sets an update flag, then response is handled during update() loop
  // done this way so we aren't trying to do trig every time the mouse moves or a key is pressed
  registerEvents = () => {
    document.addEventListener('mousemove', (event) => this.target = new Vector2(event.x, event.y));
    document.addEventListener('keydown', (event) => this.boosting = true);
  }

  _safeUpdateVelocity = (v) => {
    v *= (1 - this.frict);
    v = Math.max(-PLAYER_V, Math.min(v, PLAYER_V));
    if (Math.abs(v) < 0.0001) v = 0;
    return v;
  }

  update = () => {
    if (this.target) { 
      this.theta = Math.atan2(this.target.y-this.loc.y, this.target.x-this.loc.x) + T_OFFSET;
      this.theta %= 2 * Math.PI; // radians
      this.target = null;
    }
    if (this.boosting) {
      this.vel.add(Math.cos(this.theta-T_OFFSET), Math.sin(this.theta-T_OFFSET), this.accel * this.game.deltaTime);
      this.boosting = false;
    }
    this.vel.apply(this._safeUpdateVelocity);
    this.loc.x = Math.max(0, Math.min(this.loc.x + this.vel.x, canvas.width));
    this.loc.y = Math.max(0, Math.min(this.loc.y + this.vel.y, canvas.height));
    // TODO: check for asteroid collisions and initiate game over if so
  }

  render = () => {
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
    this.lastTick = 0; // last time run() was executed
    this.deltaTime = 0; 
    this.newGame();
    // TODO: set font for UI
  }

  newGame = () => {
    this.gameOver = false;
    this.score = 0;
    this.player = new Player(this);
    // TODO set timer for the next asteroid to spawn
  }

  reset = () => {
    // loop through game objects and destroy them
    this.newGame();
  }

  spawnAsteroid = (x, y, size, angle) => {} // TODO spawn in asteroids (use JS approach for spawn event)

  getAsteroids = () => {} // TODO get all of the asteroids being tracked by the game

  checkAsteroidCollision = (gameObj) => {
    // loop through asteroids in this object and see if any overlap with gameObj
    // if they do, the asteroid is destroyed, score is increased and returns true.
    // returns false otherwise.
    return false;
  }

  update = () => {
    this.player.update();
  }

  render = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    this.player.render();
  } 

  // https://isaacsukin.com/news/2015/01/detailed-explanation-javascript-game-loops-and-timing
  run = (timestamp) => {
    this.deltaTime += timestamp - this.lastTick;
    this.lastTick = timestamp;
    var updatesThisLoop = 0;
    while (this.deltaTime >= TIME_STEP) {
      this.update();
      this.deltaTime -= TIME_STEP;
      if (++updatesThisLoop > 300) { // if updates are taking too long, panic and bail
        console.log('...at the disco')
        this.deltaTime = 0;
        break;
      }
    }
    this.render();
    requestAnimationFrame(this.run);
  }
}

var game = new Game();
requestAnimationFrame(game.run);