import Phaser from 'phaser';

/**
 * Generates all placeholder textures procedurally so the scaffold runs with zero
 * external asset files. Replace these with loaded spritesheets/atlases from
 * phaser-sprite-generator / phaser-image-generator for production art.
 */
export function createPlaceholderTextures(scene: Phaser.Scene): void {
  // Player
  let g = scene.add.graphics();
  g.fillStyle(0x66ccff, 1);
  g.fillCircle(18, 18, 16);
  g.fillStyle(0xffffff, 0.9);
  g.fillCircle(18, 11, 5);
  g.lineStyle(2, 0xffffff, 0.5);
  g.strokeCircle(18, 18, 16);
  g.generateTexture('player', 36, 36);
  g.destroy();

  // Relay pickup
  g = scene.add.graphics();
  g.fillStyle(0xffd166, 1);
  g.fillCircle(12, 12, 9);
  g.fillStyle(0xffffff, 0.85);
  g.fillCircle(12, 12, 4);
  g.generateTexture('relay', 24, 24);
  g.destroy();

  // Spark particle
  g = scene.add.graphics();
  g.fillStyle(0xffffff, 1);
  g.fillCircle(4, 4, 4);
  g.generateTexture('spark', 8, 8);
  g.destroy();

  // Floor tile with subtle grid
  g = scene.add.graphics();
  g.fillStyle(0x121826, 1);
  g.fillRect(0, 0, 64, 64);
  g.lineStyle(1, 0x1d2740, 1);
  g.strokeRect(0, 0, 64, 64);
  g.lineStyle(1, 0x223052, 0.6);
  g.beginPath();
  g.moveTo(32, 0);
  g.lineTo(32, 64);
  g.moveTo(0, 32);
  g.lineTo(64, 32);
  g.strokePath();
  g.generateTexture('tile', 64, 64);
  g.destroy();

  // Obstacle block
  g = scene.add.graphics();
  g.fillStyle(0x2a3550, 1);
  g.fillRoundedRect(0, 0, 48, 48, 8);
  g.lineStyle(2, 0x415178, 1);
  g.strokeRoundedRect(1, 1, 46, 46, 8);
  g.generateTexture('block', 48, 48);
  g.destroy();
}
