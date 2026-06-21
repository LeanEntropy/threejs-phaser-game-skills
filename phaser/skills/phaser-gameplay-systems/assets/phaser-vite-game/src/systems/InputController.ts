import Phaser from 'phaser';
import { touchState } from './touchControls';

/**
 * Merges keyboard (arrows + WASD + space) and the DOM virtual stick into one
 * normalized movement vector plus a dash flag, so gameplay code stays
 * input-agnostic.
 */
export class InputController {
  private readonly cursors: Phaser.Types.Input.Keyboard.CursorKeys;
  private readonly wasd: {
    up: Phaser.Input.Keyboard.Key;
    down: Phaser.Input.Keyboard.Key;
    left: Phaser.Input.Keyboard.Key;
    right: Phaser.Input.Keyboard.Key;
    dash: Phaser.Input.Keyboard.Key;
  };
  private readonly move = new Phaser.Math.Vector2();

  constructor(scene: Phaser.Scene) {
    const keyboard = scene.input.keyboard!;
    this.cursors = keyboard.createCursorKeys();
    this.wasd = {
      up: keyboard.addKey('W'),
      down: keyboard.addKey('S'),
      left: keyboard.addKey('A'),
      right: keyboard.addKey('D'),
      dash: keyboard.addKey('SPACE'),
    };
  }

  sample(): { move: Phaser.Math.Vector2; dash: boolean } {
    let x = 0;
    let y = 0;
    if (this.cursors.left.isDown || this.wasd.left.isDown) x -= 1;
    if (this.cursors.right.isDown || this.wasd.right.isDown) x += 1;
    if (this.cursors.up.isDown || this.wasd.up.isDown) y -= 1;
    if (this.cursors.down.isDown || this.wasd.down.isDown) y += 1;

    x += touchState.x;
    y += touchState.y;

    this.move.set(x, y);
    if (this.move.lengthSq() > 1) {
      this.move.normalize();
    }

    const dash = this.cursors.space.isDown || this.wasd.dash.isDown || touchState.dash;
    return { move: this.move, dash };
  }
}
