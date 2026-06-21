/**
 * The HUD is plain DOM layered over the canvas (crisp text, easy responsive
 * layout, safe-area aware via CSS). For in-world UI use Phaser Text/BitmapText
 * in a dedicated UI Scene instead — see phaser-game-ui-designer.
 */
export class Hud {
  private readonly scoreEl = document.getElementById('score-value');
  private readonly targetEl = document.getElementById('target-value');
  private readonly timerEl = document.getElementById('timer-value');
  private readonly statusEl = document.getElementById('status-line');

  constructor(target: number) {
    if (this.targetEl) {
      this.targetEl.textContent = String(target);
    }
  }

  setScore(score: number): void {
    if (this.scoreEl) {
      this.scoreEl.textContent = String(score);
    }
  }

  setTime(elapsedMs: number): void {
    if (this.timerEl) {
      this.timerEl.textContent = formatTime(elapsedMs);
    }
  }

  setStatus(text: string): void {
    if (this.statusEl) {
      this.statusEl.textContent = text;
    }
  }
}

function formatTime(ms: number): string {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
