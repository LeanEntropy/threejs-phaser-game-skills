import Phaser from 'phaser';
import { BootScene } from '../scenes/BootScene';
import { PreloadScene } from '../scenes/PreloadScene';
import { PlayScene } from '../scenes/PlayScene';

export const DESIGN_WIDTH = 960;
export const DESIGN_HEIGHT = 540;

/**
 * Single source of truth for the game configuration. The renderer is AUTO
 * (WebGL with a Canvas fallback). The Scale Manager keeps a fixed design
 * resolution and letterboxes to fit any viewport, desktop or mobile.
 */
export function createGameConfig(): Phaser.Types.Core.GameConfig {
  return {
    type: Phaser.AUTO,
    backgroundColor: '#0b0e14',
    scale: {
      // RESIZE makes the canvas track the parent element size (full-window play,
      // stable bounding box for QA tooling). Switch to Phaser.Scale.FIT +
      // autoCenter if you prefer a fixed design resolution with letterboxing.
      mode: Phaser.Scale.RESIZE,
      parent: 'app',
      width: DESIGN_WIDTH,
      height: DESIGN_HEIGHT,
    },
    physics: {
      default: 'arcade',
      arcade: {
        gravity: { x: 0, y: 0 },
        debug: false,
      },
    },
    render: {
      antialias: true,
      powerPreference: 'high-performance',
    },
    callbacks: {
      // Phaser creates the canvas during boot (after the constructor returns), so
      // tag it here where game.canvas is guaranteed to exist. QA tooling and CSS
      // target #game-canvas.
      postBoot: (game) => {
        game.canvas.id = 'game-canvas';
        game.canvas.setAttribute('aria-label', 'Playable Phaser game canvas');
      },
    },
    scene: [BootScene, PreloadScene, PlayScene],
  };
}
