/** Pure session transitions. Callers supply elapsed time and independent randomness. */
import type { Action, GameState, Kind, RandomSource } from './model.js';
import { cells, fits, rotate, spawn } from './geometry.js';
const KINDS: readonly Kind[] = ['I', 'J', 'L', 'O', 'S', 'T', 'Z'];
const emptyRow = (): (Kind | null)[] => Array<Kind | null>(10).fill(null);
const interval = (level: number): number => Math.max(100, 1000 - 75 * (level - 1));
/** Create an idle game without consuming random values. */
export function createGame(): GameState {
  return { phase: 'ready', board: Array.from({ length: 20 }, emptyRow), active: null, next: null, score: 0, lines: 0, level: 1, remainingMs: interval(1) };
}
function draw(random: RandomSource): Kind {
  const value = random();
  if (!Number.isFinite(value) || value < 0 || value >= 1) throw new Error('Random source must return a finite value in [0,1)');
  return KINDS[Math.floor(value * 7)];
}
function downward(state: GameState, random: RandomSource): GameState {
  if (!state.active) throw new Error('Running game requires an active piece');
  const candidate = { ...state.active, y: state.active.y + 1 };
  if (fits(state.board, candidate)) return { ...state, active: candidate };
  const board = state.board.map(row => [...row]);
  for (const { x, y } of cells(state.active)) board[y][x] = state.active.kind;
  const survivors = board.filter(row => row.some(cell => cell === null));
  const cleared = 20 - survivors.length;
  const resolved = [...Array.from({ length: cleared }, emptyRow), ...survivors];
  const basePoints = [0, 40, 100, 300, 1200][cleared];
  if (basePoints === undefined) throw new Error('Invalid board clear count');
  const lines = state.lines + cleared, level = Math.floor(lines / 10) + 1;
  // Award using the pre-clear level; spawn uses the resulting level's cadence.
  const complete = { ...state, board: resolved, score: state.score + basePoints * state.level, lines, level, remainingMs: interval(level) };
  if (!state.next) throw new Error('Running game requires a queued piece');
  const active = spawn(state.next);
  if (!fits(resolved, active)) return { ...complete, active: null, phase: 'game-over' };
  return { ...complete, active, next: draw(random) };
}
/** Apply one validated action atomically; illegal player placements are no-ops. */
export function transition(state: GameState, action: Action, random: RandomSource): GameState {
  if (!action || !['start', 'restart', 'move', 'rotate', 'softDrop', 'advance', 'pause', 'resume'].includes(action.type)) throw new Error('Unknown action');
  if (action.type === 'move' && action.dx !== -1 && action.dx !== 1) throw new Error('Invalid move direction');
  if (action.type === 'rotate' && action.direction !== -1 && action.direction !== 1) throw new Error('Invalid rotation direction');
  if (action.type === 'advance' && (!Number.isFinite(action.elapsedMs) || action.elapsedMs < 0)) throw new Error('Elapsed time must be finite and nonnegative');
  if (action.type === 'restart' || action.type === 'start') {
    if (action.type === 'start' && state.phase !== 'ready') return state;
    return { ...createGame(), phase: 'running', active: spawn(draw(random)), next: draw(random) };
  }
  if (action.type === 'pause') return state.phase === 'running' ? { ...state, phase: 'paused' } : state;
  if (action.type === 'resume') return state.phase === 'paused' ? { ...state, phase: 'running' } : state;
  if (state.phase !== 'running') return state;
  if (!state.active) throw new Error('Running game requires an active piece');
  if (action.type === 'move' || action.type === 'rotate') {
    const active = action.type === 'move' ? { ...state.active, x: state.active.x + action.dx } : rotate(state.active, action.direction);
    return fits(state.board, active) ? { ...state, active } : state;
  }
  if (action.type === 'softDrop') return downward(state, random);
  if (action.type === 'advance') {
    if (action.elapsedMs < state.remainingMs) return { ...state, remainingMs: state.remainingMs - action.elapsedMs };
    return downward({ ...state, remainingMs: interval(state.level) }, random);
  }
  return state;
}
