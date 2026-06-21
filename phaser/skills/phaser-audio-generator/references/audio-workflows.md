# Phaser Audio Workflows

Use this reference before generating or integrating audio for a Phaser 3 game.

## Audio Planning

Create an audio matrix before generating files:

| Category | Required events | Asset count | Loop? | Sound bus |
| --- | --- | ---: | --- | --- |
| UI | hover, confirm, cancel, pause, fail | 3-8 | no | ui |
| Movement | jump, double-jump, dash, land, slide | 3-10 | sometimes | sfx |
| Interaction | coin, pickup, hit, shield, score, checkpoint | 4-12 | no | sfx |
| Threat | enemy attack, laser, warning, impact, boss cue | 4-12 | no | sfx |
| Ambience | room tone, wind, engines, crowd, weather | 1-4 | yes | ambience |
| Voice | announcer, boss, tutorial, combat barks | optional | no | voice |

For a first premium pass, generate at least:

- 1 ambience loop.
- 3 UI sounds.
- 5 gameplay SFX tied to real events.
- Optional voice only if the design benefits from dialogue or callouts.

## Prompting

Good prompts specify source, transient, tail, mix density, genre, and gameplay use:

```text
short [event] sound for [2D game genre], [material/source], clear transient, [tail length], no music, no voice, readable under gameplay mix
```

Examples:

- `short shield absorb impact for 2D shoot-em-up boss fight, glassy plasma hit, bright transient, low sub thump, 0.8s tail, no music, no voice`
- `looping abandoned cathedral ambience for dark fantasy top-down dungeon, distant wind through stone arches, subtle torch crackle, no melody, seamless loop`
- `tiny premium menu confirm click, soft mechanical latch, warm sparkle tail, no harsh beep`

Avoid prompts that are only mood words (`epic`, `AAA`, `cool`). Name the gameplay event.

## Generation Strategy

- Generate short SFX individually instead of one long mixed file.
- Make loops deliberately with `--loop`; test them looping in the game.
- Avoid music inside SFX prompts unless the user asked for music.
- Keep UI sounds quieter and shorter than gameplay SFX.
- Generate variants for high-frequency events (footsteps, coins, lasers) to avoid repetition.
- Output web-friendly formats: provide both `.ogg` and `.mp3` so Phaser can pick a codec the browser supports.
- Bundle many tiny SFX into an audio sprite (one file + a JSON marker map) to cut HTTP requests; see Audio Sprites below.
- Normalize in the game through sound bus volumes, not by editing every file manually during early iteration.

## Voice Strategy

Use TTS when the line can be generated from text and exact acting is less important.

Use voice-change when:

- The user or agent can record a scratch performance.
- Timing, breaths, laughter, anger, fear, or delivery need to be preserved.
- A boss, announcer, narrator, or character line needs stronger acting than text prompt alone.

Clean noisy scratch recordings with `isolate` before conversion unless `voice-change --remove-background-noise` is sufficient.

Do not generate or convert voices that imply impersonation of a real private person. For characters, describe a fictional voice style or use a licensed/available voice ID.

## Runtime Integration

Phaser's `SoundManager` (`this.sound`) is the audio manager — prefer it over ad hoc `new Audio()` calls. With Web Audio (the default backend) you get gain control, looping, pan, and a built-in unlock flow.

- Load audio in a Preload scene; pass an array so Phaser selects a supported codec:
  ```ts
  this.load.audio('coin', ['assets/audio/sfx/coin.ogg', 'assets/audio/sfx/coin.mp3']);
  this.load.audio('overworld', ['assets/audio/ambience/overworld-loop.ogg', 'assets/audio/ambience/overworld-loop.mp3']);
  ```
- Create reusable Sound objects and play with per-call config:
  ```ts
  const coin = this.sound.add('coin');
  coin.play({ volume: 0.6 });
  const music = this.sound.add('overworld', { loop: true, volume: 0.4 });
  music.play();
  ```
- Maintain buses by tracking groups of Sound instances (music, sfx, ui, ambience, voice). Expose mute and per-bus volume: set `this.sound.mute = true` for master mute, and adjust each Sound's `setVolume()` for per-bus levels. `this.sound.volume` controls master volume.
- Loop ambience/music with `{ loop: true }`; Phaser restarts the buffer seamlessly. Stop the old instance before launching a new one on scene restart.
- Stop/clean up sounds when restarting scenes: `this.sound.stopAll()` or stop the specific instances you started, and let scene `shutdown` release them.
- Do not trigger the same high-volume SFX every frame; add cooldowns (timestamp guards or `this.time` events) or variant pools.
- Pause/resume with the game pause state and page visibility: `this.sound.pauseAll()` / `resumeAll()`. Phaser also auto-pauses on focus loss when `pauseOnBlur` is enabled.
- Spatial / pan: pass `{ pan: -1..1 }` in the play config, or compute pan from an entity's screen-x relative to the camera for a simple 2D stereo cue.

Web Audio unlock (autoplay policy): browsers block audio until a user gesture. Phaser auto-attaches an unlock handler, but make it explicit so nothing plays before unlock:

```ts
// In a scene, after load:
if (this.sound.locked) {
  this.sound.once(Phaser.Sound.Events.UNLOCKED, () => {
    this.sound.add('overworld', { loop: true, volume: 0.4 }).play();
  });
} else {
  this.sound.add('overworld', { loop: true, volume: 0.4 }).play();
}
// Or force a resume on first input:
this.input.once('pointerdown', () => this.sound.unlock());
```

## Audio Sprites

For many short SFX, pack them into a single audio sprite (one audio file per codec plus a JSON of named markers) to reduce requests:

```ts
// Preload
this.load.audioSprite('sfx', 'assets/audio/sfx.json',
  ['assets/audio/sfx.ogg', 'assets/audio/sfx.mp3']);

// Play a marker
const sfx = this.sound.addAudioSprite('sfx');
sfx.play('coin');
sfx.play('jump', { volume: 0.5 });
```

Keep the marker JSON in the same format Phaser expects (`spritemap` with `start`/`end`/`loop` per marker).

## Verification Checklist

Report pass/fail:

- Files exist under `public/assets/audio/...` (or the project's static dir).
- Each sound loads with an ogg + mp3 fallback and decodes without console errors.
- Main gameplay events trigger the expected sounds.
- Ambience/music loop starts, loops, and stops cleanly.
- Scene restart does not stack duplicate loops (old instances stopped).
- Web Audio unlock on first input is handled; nothing plays while `this.sound.locked`.
- Master mute and per-bus (music vs SFX) volume controls work.
- Mobile Safari/Chrome unlock is considered (pointerdown unlock path).
- Audio sprite markers (if used) play the correct segments.

## Final Evidence

Include:

- Audio matrix with generated file paths.
- Prompt/text/input/source for every generated or processed file.
- Duration, loop flag, output format (ogg + mp3), voice ID when applicable.
- Runtime trigger mapping (event -> load key / sprite marker -> bus).
- Verification notes and remaining gaps.
