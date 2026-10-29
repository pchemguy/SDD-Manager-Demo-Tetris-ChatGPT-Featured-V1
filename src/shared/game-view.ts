/** Shared DOM presentation. The view consumes snapshots and emits commands only. */
import type { Action, GameState } from '../core/model.js';
import { cells, spawn } from '../core/geometry.js';

/** Mount an owned view. Render immutable snapshots; emitted commands belong to the host. */
export function mountView(root: HTMLElement, command: (action: Action) => void) {
  const doc = root.ownerDocument;
  const make = <K extends keyof HTMLElementTagNameMap>(tag: K, className = '', text = '') => {
    const node = doc.createElement(tag); node.className = className; node.textContent = text; return node;
  };
  const shell = make('section', 'game-shell');
  const header = make('header'); header.append(make('p', 'eyebrow', 'THE ORIGINAL CHALLENGE'), make('h1', '', 'Classic Tetris'));
  shell.append(header);
  const layout = make('div', 'layout'), stage = make('div', 'stage');
  const surface = make('div', 'board'); surface.tabIndex = 0;
  surface.setAttribute('role', 'img'); surface.setAttribute('aria-label', 'Tetris board, 10 columns and 20 rows');
  const tiles = Array.from({ length: 200 }, (_, index) => {
    const tile = make('div', 'cell'); tile.dataset.index = String(index); surface.append(tile); return tile;
  });
  const overlay = make('div', 'overlay'); stage.append(surface, overlay);
  const side = make('aside', 'side');
  const status = make('p', 'status'); status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
  const start = make('button', 'primary', 'Start'), restart = make('button', '', 'Restart');
  const toggle = make('button', 'toggle', 'Pause');
  let phase: GameState['phase'] = 'ready';
  const pause = () => command({ type: phase === 'paused' ? 'resume' : 'pause' });
  toggle.type = start.type = restart.type = 'button';
  toggle.addEventListener('click', pause);
  const begin = () => command({ type: 'start' }), reset = () => command({ type: 'restart' });
  start.addEventListener('click', begin); restart.addEventListener('click', reset);
  const preview = make('div', 'preview'); preview.setAttribute('role', 'img');
  const previewTiles = Array.from({ length: 16 }, () => { const tile = make('div', 'preview-cell'); preview.append(tile); return tile; });
  const stats = make('dl', 'stats');
  const values = new Map<string, HTMLElement>();
  for (const name of ['score', 'lines', 'level']) {
    const item = make('div', `stat ${name}`), value = make('dd'); value.dataset.stat = name;
    item.append(make('dt', '', name), value); stats.append(item); values.set(name, value);
  }
  const next = make('section', 'next'); next.append(make('h2', '', 'Next piece'), preview);
  const buttons = make('div', 'controls'); buttons.append(start, toggle, restart);
  const instructions = make('section', 'instructions'); instructions.append(make('h2', '', 'How to play'));
  for (const [keys, meaning] of [['Left / Right', 'Move'], ['Down', 'Soft drop'], ['Up / X', 'Rotate clockwise'], ['Z', 'Rotate counterclockwise'], ['P / Esc', 'Pause / resume'], ['R', 'Restart']]) {
    const row = make('p'); row.append(make('kbd', '', keys), make('span', '', meaning)); instructions.append(row);
  }
  side.append(status, stats, next, buttons, instructions);
  layout.append(stage, side); shell.append(layout); root.replaceChildren(shell);
  const labels = { ready: 'Ready', running: 'Playing', paused: 'Paused', 'game-over': 'Game over' };
  return {
    surface,
    /** Render authoritative cells without inferring legal moves or game rules. */
    render(state: GameState) {
      phase = state.phase;
      toggle.hidden = phase !== 'running' && phase !== 'paused';
      toggle.textContent = phase === 'paused' ? 'Resume' : 'Pause';
      values.get('score')!.textContent = String(state.score).padStart(6, '0');
      values.get('lines')!.textContent = String(state.lines).padStart(2, '0');
      values.get('level')!.textContent = String(state.level);
      preview.setAttribute('aria-label', state.next ? `Next piece: ${state.next}` : 'No next piece');
      const nextCells = new Set(state.next ? cells({ ...spawn(state.next), x: 0, y: 0 }).map(c => c.y * 4 + c.x) : []);
      previewTiles.forEach((tile, i) => { tile.className = 'preview-cell' + (nextCells.has(i) ? ` filled piece-${state.next}` : ''); });
      const active = new Set(state.active ? cells(state.active).map(cell => cell.y * 10 + cell.x) : []);
      tiles.forEach((tile, index) => {
        const falling = active.has(index);
        const kind = falling ? state.active!.kind : state.board[Math.floor(index / 10)][index % 10];
        tile.className = 'cell' + (kind ? ` filled piece-${kind}${falling ? ' active' : ' settled'}` : '');
      });
      const label = labels[state.phase];
      if (status.textContent !== label) status.textContent = label;
      overlay.textContent = label; overlay.hidden = state.phase === 'running';
      start.hidden = state.phase !== 'ready';
    },
    /** Replace a partially rendered session with a safe recovery message. */
    error() { const alert = make('p', 'fatal', 'Game unavailable. Reload to retry.'); alert.setAttribute('role', 'alert'); shell.replaceChildren(alert); },
    /** Remove owned callbacks and nodes while preserving the caller's root. */
    dispose() { toggle.removeEventListener('click', pause); start.removeEventListener('click', begin); restart.removeEventListener('click', reset); shell.remove(); },
  };
}
