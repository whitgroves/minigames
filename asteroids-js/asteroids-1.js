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
const PLAYER_V = 12 // player max vel
const T_OFFSET = Math.PI / 2; // theta offset for player rotations; consequence of triangle pointing along y-axis

const PROJ_V = 1; // projectile speed

const OCTAGON = [0, (Math.PI / 4), (Math.PI / 2), (3 * Math.PI / 4), Math.PI, (5 * Math.PI / 4), (3 * Math.PI / 2), (7 * Math.PI / 4)];
const ROCK_R = 32; // asteroid radius
const ROCK_V = 0.3; // asteroid speed

const LINE_COLOR = '#FFF' 

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
  copy = () => { return new Vector2(this.x, this.y) } // TIL JS is sometimes pass by reference
}

tracePoints = (points, enclose=true) => {
  ctx.beginPath();
  ctx.strokeStyle = LINE_COLOR;
  if (enclose) ctx.moveTo(points[points.length-1].x, points[points.length-1].y);
  points.forEach(point => { ctx.lineTo(point.x, point.y) });
  ctx.stroke();
  ctx.closePath();
}

class GameObject {
  constructor(game, loc=null, vel=null) {
    this.game = game;
    this.loc = loc ? loc.copy() : new Vector2();
    this.vel = vel ? vel.copy() : new Vector2();
    this.objId = this.game.register(this);
  }
  inBounds = () => { return 0 < this.loc.x && this.loc.x < canvas.width && 0 < this.loc.y && this.loc.y < canvas.height }
  update = () => {} // virtual
  render = () => {} // virtual
  destroy = () => { this.game.deregister(this.objId) }
}

class Projectile extends GameObject {
  constructor(game, loc, theta) { super(game, loc, new Vector2(Math.cos(theta), Math.sin(theta), PROJ_V)) }
  update = () => {
    if (this.inBounds() && !this.game.checkAsteroidCollision(this)) {
      this.loc.add(this.vel.x, this.vel.y, this.game.deltaTime);
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
    this.registerInputs();
  }

  // generally, event sets an update flag, then response is handled during update() loop
  // done this way so we aren't trying to do trig every time the mouse moves or a key is pressed
  registerInputs = () => {
    document.addEventListener('mousemove', this._acquireTarget);
    document.addEventListener('keydown', this._boostOn);
    document.addEventListener('keyup', this._boostOff);
    document.addEventListener('mousedown', this._fireProjectile);
  }

  deregisterInputs = () => {
    document.removeEventListener('mousemove', this._acquireTarget);
    document.removeEventListener('keydown', this._boostOn);
    document.removeEventListener('keyup', this._boostOff);
    document.removeEventListener('mousedown', this._fireProjectile);
  }

  _acquireTarget = (event) => { this.target = new Vector2(event.x, event.y) }
  _boostOn = (event) => { this.boosting = event.key === ' ' }
  _boostOff = (event) => { this.boosting = !event.key === ' ' }
  _fireProjectile = (event) => { if (event.button === 0) new Projectile(this.game, this.loc, this.theta-T_OFFSET) }

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
    if (this.game.checkAsteroidCollision(this)) {
      this.game.gameOver = true;
      this.destroy();
      this.deregisterInputs();
      console.log('GAME OVER');
    }
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

class Asteroid extends GameObject {
  constructor(game, loc, theta=null) {
    super(game, loc);
    this.theta = theta ? theta % 2 * Math.PI : Math.atan2(loc.y-game.player.loc.y, loc.x-game.player.loc.x); // by default, head towards player
    this.vel.set(Math.cos(this.theta), Math.sin(this.theta), ROCK_V);
    this.isAsteroid = true; // in reality this can be anything so long as the property exists
  }
  update = () => {
    if (this.inBounds()) {
      this.loc.add(this.vel.x, this.vel.y, -this.game.deltaTime);
    } else {
      this.destroy();
    }
  }
  render = () => {
    var points = [];
    OCTAGON.forEach(point => {
      var x = this.loc.x + ROCK_R * Math.cos(point + this.theta);
      var y = this.loc.y + ROCK_R * Math.sin(point + this.theta);
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
    this.nextObjectId = -1; // will increment to 0 on first registration
    this.cleanupIds = [];
    this.newGame();
    this.paused = false;
    document.addEventListener('keydown', (event) => this.paused = event.key === 'Escape' && !this.paused);
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
      this.gameObjects.delete(objId);
    });
    this.cleanupIds = [];
  }

  newGame = () => {
    this.gameOver = false;
    this.score = 0;
    this.player = new Player(this);
    this.asteroidTimer = 2500;
    this.spawnAsteroid(0);
  }

  reset = () => { // loop through game objects and destroy them
    this.newGame();
  }

  spawnAsteroid = (size) => { // spawns a new asteroid on a decreasing timer
    if (!this.gameOver) {
      switch (size) {
        case 0: new Asteroid(this, new Vector2(1000, 400));
        // case 1: new BigAsteroid(this, loc, theta);
      }
      if (this.asteroidTimer > 250) this.asteroidTimer -= 25;
      setTimeout(this.spawnAsteroid, this.asteroidTimer, 0);
    }
  }

  checkAsteroidCollision = (collisionObj) => {
    // for (let i = 0; i < this.gameObjects.size; i++) { // https://stackoverflow.com/a/34653650/3178898
    for (const k of this.gameObjects.keys()) {
      let gameObj = this.gameObjects.get(k);
      if ('isAsteroid' in gameObj && Math.abs(collisionObj.loc.x-gameObj.loc.x) < ROCK_R && Math.abs(collisionObj.loc.y-gameObj.loc.y) < ROCK_R) {
        gameObj.destroy();
        this.score++;
        return true;
      }
    }
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
    if (!this.paused) {
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
      this.cleanup();
    // } else {
    //   console.log('paused');
    }
    requestAnimationFrame(this.run);
  }
}

var game = new Game();
requestAnimationFrame(game.run);