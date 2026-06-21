import Phaser from 'phaser';

type AudioContextCtor = typeof AudioContext;

/**
 * Minimal procedural audio so the scaffold ships zero asset files yet still has
 * an audio hook. Browsers block audio until a user gesture, so the context is
 * created lazily on first input. For production, load real assets with
 * this.load.audio and play via this.sound.add — see phaser-audio-generator.
 */
export class AudioSystem {
  private ctx?: AudioContext;

  constructor(scene: Phaser.Scene) {
    const create = (): void => {
      if (this.ctx) {
        return;
      }
      const Ctor =
        window.AudioContext ??
        (window as unknown as { webkitAudioContext?: AudioContextCtor }).webkitAudioContext;
      if (Ctor) {
        try {
          this.ctx = new Ctor();
        } catch {
          this.ctx = undefined;
        }
      }
    };
    scene.input.once('pointerdown', create);
    scene.input.keyboard?.once('keydown', create);
  }

  blip(): void {
    const ctx = this.ctx;
    if (!ctx) {
      return;
    }
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.value = 520;
    gain.gain.value = 0.06;
    osc.connect(gain).connect(ctx.destination);
    const t = ctx.currentTime;
    osc.frequency.exponentialRampToValueAtTime(880, t + 0.08);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.18);
    osc.start(t);
    osc.stop(t + 0.2);
  }
}
