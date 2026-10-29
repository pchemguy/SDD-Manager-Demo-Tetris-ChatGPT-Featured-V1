/** Shared DOM presentation. The view consumes snapshots and emits commands only. */
import type { Action, GameState } from '../core/model.js';
import { cells } from '../core/geometry.js';

export function mountView(root: HTMLElement, command: (action: Action) => void) {
  const doc = root.ownerDocument;
  const make = <K extends keyof HTMLElementTagNameMap>(tag: K, className = '', text = '') => {
    const node = doc.createElement(tag); node.className = className; node.textContent = text; return node;
  };
  const shell = make('section', 'game-shell');
  shell.append(make('h1', '', 'Classic Tetris'));
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
  start.type = restart.type = 'button';
  const begin = () => command({ type: 'start' }), reset = () => command({ type: 'restart' });
  start.addEventListener('click', begin); restart.addEventListener('click', reset);
  side.append(status, start, restart, make('p', 'instructions', 'Arrows: move / soft drop. Up or X: clockwise. Z: counterclockwise. R: restart.'));
  layout.append(stage, side); shell.append(layout); root.replaceChildren(shell);
  const labels = { ready: 'Ready', running: 'Playing', paused: 'Paused', 'game-over': 'Game over' };
  return {
    surface,
    /** Render authoritative cells without inferring legal moves or game rules. */
    render(state: GameState) {
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
    /** Remove owned callbacks and nodes while preserving the caller's root. */
    dispose() { start.removeEventListener('click', begin); restart.removeEventListener('click', reset); shell.remove(); },
  };
}
