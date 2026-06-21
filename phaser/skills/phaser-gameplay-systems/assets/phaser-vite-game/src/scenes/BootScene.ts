import Phaser from 'phaser';

/**
 * Boot is the first scene. In a production game this is where you load the tiny
 * assets needed to render a loading screen, then hand off to Preload.
 */
export class BootScene extends Phaser.Scene {
  constructor() {
    super('Boot');
  }

  create(): void {
    this.scene.start('Preload');
  }
}
