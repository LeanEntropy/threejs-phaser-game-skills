/// <reference types="vite/client" />

interface PhaserGameDiagnostics {
  frame: number;
  elapsed: number;
  score: number;
  targetScore: number;
  complete: boolean;
  player: {
    position: { x: number; y: number };
    speed: number;
  };
  renderer: {
    type: 'WEBGL' | 'CANVAS' | 'HEADLESS';
    fps: number;
    activeObjects: number;
  };
  canvas: {
    clientWidth: number;
    clientHeight: number;
    width: number;
    height: number;
    dpr: number;
  };
}

interface Window {
  __PHASER_GAME_DIAGNOSTICS__?: PhaserGameDiagnostics;
}
