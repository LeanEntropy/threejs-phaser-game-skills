import Phaser from 'phaser';
import { Player } from '../entities/Player';
import { spawnRelays } from '../entities/Pickup';
import { InputController } from '../systems/InputController';
import { CameraRig } from '../systems/CameraRig';
import { AudioSystem } from '../systems/AudioSystem';
import { Hud } from '../systems/Hud';
import { DebugTools } from '../systems/DebugTools';

const WORLD_W = 1920;
const WORLD_H = 1080;
const TARGET_SCORE = 8;

/**
 * The playable loop: drive a craft around a bounded arena, collect glowing
 * relays, win at the target count. Systems are separated (input, camera, audio,
 * HUD, debug) so the scene stays readable as the game grows.
 */
export class PlayScene extends Phaser.Scene {
  private player!: Player;
  private controller!: InputController;
  private audio!: AudioSystem;
  private hud!: Hud;
  private relays!: Phaser.Physics.Arcade.Group;
  private blocks!: Phaser.Physics.Arcade.StaticGroup;
  private background!: Phaser.GameObjects.TileSprite;

  private score = 0;
  private elapsed = 0;
  private frame = 0;
  private complete = false;

  constructor() {
    super('Play');
  }

  create(): void {
    this.score = 0;
    this.elapsed = 0;
    this.frame = 0;
    this.complete = false;

    this.physics.world.setBounds(0, 0, WORLD_W, WORLD_H);
    this.background = this.add
      .tileSprite(0, 0, WORLD_W, WORLD_H, 'tile')
      .setOrigin(0, 0)
      .setDepth(-10);

    const rng = new Phaser.Math.RandomDataGenerator(['phaser-vite-game']);

    this.blocks = this.physics.add.staticGroup();
    for (let i = 0; i < 14; i += 1) {
      const x = rng.between(160, WORLD_W - 160);
      const y = rng.between(160, WORLD_H - 160);
      (this.blocks.create(x, y, 'block') as Phaser.Physics.Arcade.Sprite).setDepth(1);
    }

    this.player = new Player(this, WORLD_W / 2, WORLD_H / 2);
    this.physics.add.collider(this.player.sprite, this.blocks);

    this.relays = this.physics.add.group();
    spawnRelays(this, this.relays, TARGET_SCORE, WORLD_W, WORLD_H, rng);
    this.physics.add.overlap(this.player.sprite, this.relays, (_player, relay) => {
      this.collectRelay(relay as Phaser.Physics.Arcade.Image);
    });

    this.controller = new InputController(this);
    new CameraRig(this, this.player.sprite, WORLD_W, WORLD_H);
    this.audio = new AudioSystem(this);
    this.hud = new Hud(TARGET_SCORE);
    new DebugTools(this);

    this.hud.setScore(0);
    this.hud.setStatus('Collect relays');
    this.writeDiagnostics();
  }

  private collectRelay(relay: Phaser.Physics.Arcade.Image): void {
    if (!relay.active) {
      return;
    }
    relay.disableBody(true, true);
    this.score += 1;
    this.audio.blip();
    this.cameras.main.shake(90, 0.003);

    const burst = this.add.particles(relay.x, relay.y, 'spark', {
      speed: { min: 60, max: 200 },
      lifespan: 420,
      quantity: 14,
      scale: { start: 1, end: 0 },
      blendMode: 'ADD',
    });
    burst.explode(16, relay.x, relay.y);
    this.time.delayedCall(450, () => burst.destroy());

    this.hud.setScore(this.score);
    if (this.score >= TARGET_SCORE && !this.complete) {
      this.complete = true;
      this.hud.setStatus('All relays online!');
      this.cameras.main.flash(220, 120, 220, 255);
    }
  }

  update(_time: number, delta: number): void {
    this.frame += 1;
    if (!this.complete) {
      this.elapsed += delta;
    }

    const { move, dash } = this.controller.sample();
    this.player.drive(move, dash, delta);

    this.background.setTilePosition(
      this.cameras.main.scrollX * 0.5,
      this.cameras.main.scrollY * 0.5,
    );

    this.hud.setTime(this.elapsed);
    this.writeDiagnostics();
  }

  private writeDiagnostics(): void {
    const canvas = this.game.canvas;
    const type =
      this.renderer.type === Phaser.WEBGL
        ? 'WEBGL'
        : this.renderer.type === Phaser.CANVAS
          ? 'CANVAS'
          : 'HEADLESS';

    window.__PHASER_GAME_DIAGNOSTICS__ = {
      frame: this.frame,
      elapsed: this.elapsed,
      score: this.score,
      targetScore: TARGET_SCORE,
      complete: this.complete,
      player: {
        position: { x: this.player.sprite.x, y: this.player.sprite.y },
        speed: this.player.speedNow(),
      },
      renderer: {
        type,
        fps: Math.round(this.game.loop.actualFps),
        activeObjects: this.children.length,
      },
      canvas: {
        clientWidth: canvas.clientWidth,
        clientHeight: canvas.clientHeight,
        width: canvas.width,
        height: canvas.height,
        dpr: window.devicePixelRatio || 1,
      },
    };
  }
}
