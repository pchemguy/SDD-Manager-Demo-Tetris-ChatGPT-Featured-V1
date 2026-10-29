/** Execute compiled production operations; pytest owns all expected results. */
import fs from 'node:fs';
import * as geometry from '../../dist/core/geometry.js';
const request = JSON.parse(fs.readFileSync(0, 'utf8'));
const original = JSON.stringify(request);
let state, draws = 0, previous, before;
try {
  if (request.op === 'session') {
    const engine = await import('../../dist/core/engine.js');
    state = request.state ?? engine.createGame();
    const snapshots = [state];
    let preserved = true;
    const random = () => { const values = request.values ?? [0.5]; return values[Math.min(draws++, values.length - 1)]; };
    for (const raw of request.actions ?? []) {
      const action = { ...raw };
      if (action.elapsedMs === 'NaN') action.elapsedMs = NaN;
      if (action.elapsedMs === 'Infinity') action.elapsedMs = Infinity;
      previous = state; before = JSON.stringify(state);
      const next = engine.transition(state, action, random);
      preserved &&= JSON.stringify(previous) === before;
      state = next; snapshots.push(state);
    }
    process.stdout.write(JSON.stringify({ state, snapshots, draws, inputUnchanged: preserved && JSON.stringify(request) === original }));
  } else {
  let piece = request.piece ?? geometry.spawn(request.kind);
  for (let i = 0; i < (request.turns ?? 0); i++) piece = geometry.rotate(piece, request.direction ?? 1);
  const result = request.board ? { fits: geometry.fits(request.board, piece) } : { piece, cells: geometry.cells(piece) };
  process.stdout.write(JSON.stringify({ ...result, inputUnchanged: JSON.stringify(request) === original }));
  }
} catch (error) { process.stdout.write(JSON.stringify({ error: error.message, state, draws, inputUnchanged: JSON.stringify(request) === original && (!previous || JSON.stringify(previous) === before) })); }
