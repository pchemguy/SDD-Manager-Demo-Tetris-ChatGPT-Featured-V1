/** Canonical tetromino geometry; occupied cells alone determine collisions. */
import type { Board, Kind, Piece, Rotation } from './model.js';
const SHAPES: Record<Kind, readonly string[]> = {
  I: ['....', 'IIII', '....', '....'], J: ['J..', 'JJJ', '...'],
  L: ['..L', 'LLL', '...'], O: ['OO', 'OO'], S: ['.SS', 'SS.', '...'],
  T: ['.T.', 'TTT', '...'], Z: ['ZZ.', '.ZZ', '...'],
};
function matrix(kind: Kind): readonly string[] {
  const value = SHAPES[kind];
  if (!Array.isArray(value)) throw new Error('Unknown piece kind');
  return value;
}
/** Spawn centered in the visible board with the canonical orientation. */
export function spawn(kind: Kind): Piece {
  return { kind, rotation: 0, x: Math.floor((10 - matrix(kind).length) / 2), y: 0 };
}
/** Enumerate occupied board coordinates without mutating the piece. */
export function cells(piece: Piece): { x: number; y: number }[] {
  const rows = matrix(piece.kind), size = rows.length;
  if (![piece.x, piece.y, piece.rotation].every(Number.isInteger) || piece.rotation < 0 || piece.rotation > 3) throw new Error('Invalid piece coordinates');
  const result: { x: number; y: number }[] = [];
  rows.forEach((row, y) => [...row].forEach((value, x) => {
    if (value === '.') return;
    let px = x, py = y;
    for (let turn = 0; turn < piece.rotation; turn++) [px, py] = [size - 1 - py, px];
    result.push({ x: px + piece.x, y: py + piece.y });
  }));
  return result;
}
/** Rotate about the fixed matrix origin; the caller decides placement legality. */
export function rotate(piece: Piece, direction: -1 | 1): Piece {
  if (direction !== 1 && direction !== -1) throw new Error('Invalid rotation direction');
  return { ...piece, rotation: piece.kind === 'O' ? 0 : ((piece.rotation + direction + 4) % 4) as Rotation };
}
/** Test occupied cells against visible board bounds and settled cells. */
export function fits(board: Board, piece: Piece): boolean {
  return cells(piece).every(({ x, y }) => x >= 0 && x < 10 && y >= 0 && y < 20 && board[y][x] === null);
}
