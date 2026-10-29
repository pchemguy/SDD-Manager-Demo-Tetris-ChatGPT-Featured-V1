/** Immutable game data and explicit commands shared by rules and presentation. */
export type Kind = 'I' | 'J' | 'L' | 'O' | 'S' | 'T' | 'Z';
export type Rotation = 0 | 1 | 2 | 3;
export type Board = ReadonlyArray<ReadonlyArray<Kind | null>>;
export interface Piece { readonly kind: Kind; readonly rotation: Rotation; readonly x: number; readonly y: number }
export interface GameState {
  readonly phase: 'ready' | 'running' | 'paused' | 'game-over';
  readonly board: Board;
  readonly active: Piece | null;
  readonly next: Kind | null;
  readonly score: number;
  readonly lines: number;
  readonly level: number;
  readonly remainingMs: number;
}
export type Action = { type: 'start' | 'restart' | 'softDrop' | 'pause' | 'resume' }
  | { type: 'move'; dx: -1 | 1 }
  | { type: 'rotate'; direction: -1 | 1 }
  | { type: 'advance'; elapsedMs: number };
export type RandomSource = () => number;
