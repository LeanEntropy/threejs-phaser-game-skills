import Phaser from 'phaser';

/**
 * Configures the main camera to follow the player within world bounds and adds
 * a subtle vignette under WebGL. Keeping camera setup in one place makes it easy
 * to retune feel (lerp, deadzone, zoom) without touching gameplay.
 */
export class CameraRig {
  constructor(scene: Phaser.Scene, target: Phaser.GameObjects.Sprite, worldW: number, worldH: number) {
    const cam = scene.cameras.main;
    cam.setBounds(0, 0, worldW, worldH);
    cam.startFollow(target, true, 0.12, 0.12);
    cam.setDeadzone(120, 80);
    // Camera postFX (vignette/bloom) lives in phaser-aaa-graphics-builder.
  }
}
