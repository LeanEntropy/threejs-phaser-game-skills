import Phaser from 'phaser';

/**
 * Spawns collectible relays into an Arcade group, spaced away from the world
 * edges. Each relay pulses via a tween and glows under WebGL.
 */
export function spawnRelays(
  scene: Phaser.Scene,
  group: Phaser.Physics.Arcade.Group,
  count: number,
  worldW: number,
  worldH: number,
  rng: Phaser.Math.RandomDataGenerator,
): void {
  for (let i = 0; i < count; i += 1) {
    const x = rng.between(96, worldW - 96);
    const y = rng.between(96, worldH - 96);
    const relay = scene.physics.add.image(x, y, 'relay');
    group.add(relay);
    relay.setDepth(3);

    scene.tweens.add({
      targets: relay,
      scale: { from: 0.85, to: 1.18 },
      yoyo: true,
      repeat: -1,
      duration: 700,
      ease: 'Sine.inOut',
    });
  }
}
