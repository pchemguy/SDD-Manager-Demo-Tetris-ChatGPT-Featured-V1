/** Browser composition: serialize monotonic time and commands around shared rules. */
import { createGame, transition } from '../../core/engine.js';
import type { Action, RandomSource } from '../../core/model.js';
import { mountView } from '../../shared/game-view.js';
import { mapKey } from './input.js';
export interface HostOptions {
  random?: RandomSource;
  now?: () => number;
  requestFrame?: (callback: FrameRequestCallback) => number;
  cancelFrame?: (handle: number) => void;
}
/** Mount one owned loop/listener set; injected boundaries support reproducible hosts. */
export function mountGame(root: HTMLElement, options: HostOptions = {}) {
  const random = options.random ?? (() => Math.random());
  const now = options.now ?? (() => performance.now());
  const schedule = options.requestFrame ?? (callback => window.requestAnimationFrame(callback));
  const cancel = options.cancelFrame ?? (handle => window.cancelAnimationFrame(handle));
  let state = createGame(), previous = now(), frame: number | null = null, disposed = false;
  const view = mountView(root, dispatch);
  function synchronize() {
    const current = now();
    state = transition(state, { type: 'advance', elapsedMs: Math.max(0, current - previous) }, random);
    previous = current;
  }
  function refresh() {
    view.render(state);
    if (state.phase === 'running' && frame === null && !disposed) frame = schedule(tick);
    if (state.phase !== 'running' && frame !== null) { cancel(frame); frame = null; }
  }
  function tick() { frame = null; if (!disposed) { synchronize(); refresh(); } }
  function dispatch(action: Action) {
    if (disposed) return;
    synchronize(); state = transition(state, action, random); refresh();
    if (action.type === 'start' || action.type === 'restart') view.surface.focus();
  }
  const keydown = (event: KeyboardEvent) => {
    if (root.ownerDocument.activeElement !== view.surface) return;
    const mapped = mapKey(event);
    if (mapped.handled) event.preventDefault();
    if (mapped.action) dispatch(mapped.action);
  };
  view.surface.addEventListener('keydown', keydown); refresh();
  return {
    /** Idempotent disposal prevents stale callbacks from changing/rendering state. */
    dispose() {
      if (disposed) return;
      disposed = true;
      if (frame !== null) cancel(frame);
      frame = null; view.surface.removeEventListener('keydown', keydown); view.dispose();
    },
  };
}
