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
const PROJ_SPD = 1; // projectile speed

const DEF_COLOR = '#FFF'

// I know libraries for this exist but sometimes you want a scoop of vanilla
class Vector2 {
  constructor(x=0, y=0, scale=1) {
    this.set(x, y, scale);
  }

  set = (x, y, scale=1) => {
    this.x = x * scale;
    this.y = y * scale;
  }

  add = (x, y, scale=1) => {
    this.x += x * scale;
    this.y += y * scale;
  }

  apply = (func) => {
    this.x = func(this.x);
    this.y = func(this.y);
  }
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

class GameObject {
  constructor(game, loc=new Vector2(), vel=new Vector2()) {
    this.game = game;
    this.loc = loc;
    this.vel = vel;
    this.objId = this.game.register(this);
  }
  inBounds() { return 0 <= this.loc.x <= canvas.width && 0 <= this.loc.y <= canvas.height }
  update() {} // virtual
  render() {} // virtual
  destroy() { this.game.deregister(this.objId) }
}

class Projectile extends GameObject {
  constructor(game, loc, theta) { super(game, loc, new Vector2(Math.cos(theta), Math.sin(theta), PROJ_SPD)) }
  update = () => {
    if (this.inBounds()) {
      this.loc.add(this.vel.x, this.vel.y, this.game.deltaTime);
      // TODO check asteroid collision
    } else {
      this.destroy();
    }
  }
  render = () => { tracePoints([this.loc, new Vector2(this.loc.x-this.vel.x, this.loc.y-this.vel.y)], false) }
}

class Player extends GameObject {
  constructor(game) {
    super(game, new Vector2(HALF_W, HALF_H));
    this.accel = 0.02;
    this.frict = 0.02;
    this.theta = 0;
    this.target = null;
    this.boosting = false;
    this.registerEvents();
  }

  // generally, event sets an update flag, then response is handled during update() loop
  // done this way so we aren't trying to do trig every time the mouse moves or a key is pressed
  registerEvents = () => {
    document.addEventListener('mousemove', (event) => this.target = new Vector2(event.x, event.y));
    document.addEventListener('keydown', (event) => this.boosting = event.key === ' ');
    document.addEventListener('keyup', (event) => this.boosting = !event.key === ' ');
    document.addEventListener('mousedown', this._fireProjectile);
  }

  _fireProjectile = (event) => {
    this.game.register(new Projectile(this.game, new Vector2(this.loc.x, this.loc.y), this.theta-T_OFFSET)); // TIL JS is sometimes pass by reference
  }

  _safeUpdateVelocity = (v) => {
    v *= (1 - this.frict)
    v = Math.max(-PLAYER_V, Math.min(v, PLAYER_V));            
    if (Math.abs(v) < 0.001) v = 0;
    return v;
  }

  update = () => {
    if (this.target) { 
      this.theta = Math.atan2(this.target.y-this.loc.y, this.target.x-this.loc.x) + T_OFFSET;
      this.theta %= 2 * Math.PI; // radians
      this.target = null;
    }
    if (this.boosting) this.vel.add(Math.cos(this.theta-T_OFFSET), Math.sin(this.theta-T_OFFSET), this.accel * this.game.deltaTime);
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
    tracePoints(points);
  }
}

class Game {
  constructor() {
    this.lastTick = 0; // last time run() was executed
    this.deltaTime = 0;
    this.gameObjects = new Map();
    this.nextObjectId = 0;
    this.cleanupIds = [];
    this.newGame();
    // TODO: set font for UI
  }

  register = (gameObj) => {
    this.gameObjects.set(++this.nextObjectId, gameObj);
    return this.nextObjectId;
  }

  deregister = (objId) => {
    this.cleanupIds.push(objId);
  }

  cleanup = () => {
    this.cleanupIds.forEach((objId) => {
      delete this.gameObjects[objId];
    });
    this.cleanupIds = [];
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
    this.gameObjects.forEach((gameObj) => {
      gameObj.update();
    });
  }

  render = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    this.gameObjects.forEach((gameObj) => {
      gameObj.render(); 
    });
  } 

  // https://isaacsukin.com/news/2015/01/detailed-explanation-javascript-game-loops-and-timing
  run = (timestamp) => {
    this.deltaTime += timestamp - this.lastTick;
    this.lastTick = timestamp;
    var updatesThisLoop = 0;
    while (this.deltaTime >= TIME_STEP) {
      this.update();
      this.deltaTime -= TIME_STEP;
      if (++updatesThisLoop > 251) { // if updates are taking too long, panic and bail
        console.log('...at the disco')
        this.deltaTime = 0;
        break;
      }
    }
    this.render();
    requestAnimationFrame(this.run);
    this.cleanup();
  }
}

var game = new Game();
requestAnimationFrame(game.run);