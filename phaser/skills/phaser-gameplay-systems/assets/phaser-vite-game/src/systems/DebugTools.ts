import Phaser from 'phaser';

/**
 * Press the backtick key (`) to toggle Arcade physics body overlays plus a small
 * fps / object-count readout. Debug UI is screen-fixed (scrollFactor 0) and on a
 * high depth so it sits above gameplay.
 */
export class DebugTools {
  private readonly scene: Phaser.Scene;
  private readonly text: Phaser.GameObjects.Text;
  private visible = false;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.text = scene.add
      .text(8, scene.scale.height - 22, '', {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#7fffd4',
      })
      .setScrollFactor(0)
      .setDepth(2000)
      .setVisible(false);

    scene.input.keyboard?.on('keydown-BACKTICK', () => this.toggle());
    scene.events.on(Phaser.Scenes.Events.UPDATE, this.refresh, this);
    scene.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
      scene.events.off(Phaser.Scenes.Events.UPDATE, this.refresh, this);
    });
  }

  private toggle(): void {
    this.visible = !this.visible;
    this.text.setVisible(this.visible);
    const world = this.scene.physics.world;
    world.drawDebug = this.visible;
    if (!this.visible) {
      world.debugGraphic?.clear();
    }
  }

  private refresh(): void {
    if (!this.visible) {
      return;
    }
    const fps = Math.round(this.scene.game.loop.actualFps);
    this.text.setText(`fps ${fps}  objects ${this.scene.children.length}`);
  }
}
