/**
 * DOM virtual-stick + dash button shared with the Phaser InputController.
 * Lives outside Phaser so the same normalized vector feeds keyboard and touch.
 */
export interface TouchState {
  x: number;
  y: number;
  dash: boolean;
}

export const touchState: TouchState = { x: 0, y: 0, dash: false };

export function bindTouchControls(): void {
  const stick = document.getElementById('touch-stick');
  const knob = document.getElementById('touch-knob');
  const dash = document.getElementById('dash-button');
  if (!stick || !knob) {
    return;
  }

  let activeId = -1;

  const reset = (): void => {
    touchState.x = 0;
    touchState.y = 0;
    knob.style.transform = 'translate(-50%, -50%)';
  };

  const move = (clientX: number, clientY: number): void => {
    const rect = stick.getBoundingClientRect();
    const radius = rect.width * 0.5;
    let dx = (clientX - (rect.left + rect.width / 2)) / radius;
    let dy = (clientY - (rect.top + rect.height / 2)) / radius;
    const len = Math.hypot(dx, dy);
    if (len > 1) {
      dx /= len;
      dy /= len;
    }
    touchState.x = dx;
    touchState.y = dy;
    knob.style.transform = `translate(calc(-50% + ${dx * 40}%), calc(-50% + ${dy * 40}%))`;
  };

  stick.addEventListener('pointerdown', (event) => {
    activeId = event.pointerId;
    stick.setPointerCapture(activeId);
    move(event.clientX, event.clientY);
  });
  stick.addEventListener('pointermove', (event) => {
    if (event.pointerId === activeId) {
      move(event.clientX, event.clientY);
    }
  });
  const end = (event: PointerEvent): void => {
    if (event.pointerId === activeId) {
      activeId = -1;
      reset();
    }
  };
  stick.addEventListener('pointerup', end);
  stick.addEventListener('pointercancel', end);

  if (dash) {
    dash.addEventListener('pointerdown', (event) => {
      event.preventDefault();
      touchState.dash = true;
    });
    const clear = (): void => {
      touchState.dash = false;
    };
    dash.addEventListener('pointerup', clear);
    dash.addEventListener('pointercancel', clear);
  }
}
