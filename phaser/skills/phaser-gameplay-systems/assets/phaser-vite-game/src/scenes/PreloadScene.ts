import Phaser from 'phaser';
import { createPlaceholderTextures } from '../utils/textures';

/**
 * Preload loads (or, here, generates) all gameplay assets, then starts Play.
 * For production: replace createPlaceholderTextures with this.load.atlas /
 * this.load.spritesheet / this.load.audio calls and drive a loading bar from
 * this.load.on('progress', ...).
 */
export class PreloadScene extends Phaser.Scene {
  constructor() {
    super('Preload');
  }

  preload(): void {
    // Example for real assets:
    // this.load.atlas('sheet', 'sprites/sheet.png', 'sprites/sheet.json');
    // this.load.audio('blip', ['audio/blip.ogg', 'audio/blip.mp3']);
  }

  create(): void {
    createPlaceholderTextures(this);
    this.scene.start('Play');
  }
}
