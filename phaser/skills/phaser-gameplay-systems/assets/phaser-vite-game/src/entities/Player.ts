import Phaser from 'phaser';

/**
 * The player avatar: an Arcade physics sprite with a dash. Movement is driven
 * each frame from a normalized input vector so keyboard and touch feel identical.
 */
export class Player {
  readonly sprite: Phaser.Physics.Arcade.Sprite;

  private readonly scene: Phaser.Scene;
  private readonly baseSpeed = 260;
  private readonly dashSpeed = 620;
  private readonly dashDuration = 140;
  private readonly dashCooldownMs = 650;
  private dashTimer = 0;
  private cooldownTimer = 0;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    this.scene = scene;
    this.sprite = scene.physics.add
      .sprite(x, y, 'player')
      .setDepth(5)
      .setCollideWorldBounds(true);
    this.sprite.setMaxVelocity(this.dashSpeed);
    (this.sprite.body as Phaser.Physics.Arcade.Body).setCircle(16);
    // For glow/bloom and other postFX, see phaser-aaa-graphics-builder (WebGL only,
    // and costly under software GL — keep the scaffold lean).
  }

  drive(move: Phaser.Math.Vector2, dash: boolean, delta: number): void {
    this.dashTimer = Math.max(0, this.dashTimer - delta);
    this.cooldownTimer = Math.max(0, this.cooldownTimer - delta);

    const moving = move.lengthSq() > 0.0001;
    if (dash && this.cooldownTimer === 0 && moving) {
      this.dashTimer = this.dashDuration;
      this.cooldownTimer = this.dashCooldownMs;
      this.scene.cameras.main.shake(70, 0.004);
    }

    const speed = this.dashTimer > 0 ? this.dashSpeed : this.baseSpeed;
    const body = this.sprite.body as Phaser.Physics.Arcade.Body;
    body.setVelocity(move.x * speed, move.y * speed);

    if (moving) {
      const target = Math.atan2(move.y, move.x) + Math.PI / 2;
      this.sprite.setRotation(Phaser.Math.Angle.RotateTo(this.sprite.rotation, target, 0.2));
    }
  }

  speedNow(): number {
    const body = this.sprite.body as Phaser.Physics.Arcade.Body;
    return Math.round(body.velocity.length());
  }
}
