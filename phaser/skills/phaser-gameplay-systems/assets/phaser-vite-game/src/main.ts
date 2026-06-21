import './styles.css';
import Phaser from 'phaser';
import { createGameConfig } from './game/GameConfig';
import { bindTouchControls } from './systems/touchControls';

bindTouchControls();

const game = new Phaser.Game(createGameConfig());

// Handy for manual debugging in the console.
(window as unknown as { __PHASER_GAME__?: Phaser.Game }).__PHASER_GAME__ = game;
