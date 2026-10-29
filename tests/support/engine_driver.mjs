/** Execute compiled production operations; pytest owns all expected results. */
import fs from 'node:fs';
import * as geometry from '../../dist/core/geometry.js';
const request = JSON.parse(fs.readFileSync(0, 'utf8'));
const original = JSON.stringify(request);
try {
  let piece = request.piece ?? geometry.spawn(request.kind);
  for (let i = 0; i < (request.turns ?? 0); i++) piece = geometry.rotate(piece, request.direction ?? 1);
  const result = request.board ? { fits: geometry.fits(request.board, piece) } : { piece, cells: geometry.cells(piece) };
  process.stdout.write(JSON.stringify({ ...result, inputUnchanged: JSON.stringify(request) === original }));
} catch (error) { process.stdout.write(JSON.stringify({ error: error.message })); }
