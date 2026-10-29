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
  const doc = root.ownerDocument, win = doc.defaultView!;
  const random = options.random ?? (() => Math.random());
  const now = options.now ?? (() => win.performance.now());
  const schedule = options.requestFrame ?? (callback => win.requestAnimationFrame(callback));
  const cancel = options.cancelFrame ?? (handle => win.cancelAnimationFrame(handle));
  let state = createGame(), previous = now(), frame: number | null = null, disposed = false, failed = false;
  const view = mountView(root, dispatch);
  function removeHandlers() {
    view.surface.removeEventListener('keydown', keydown);
    doc.removeEventListener('visibilitychange', visibility);
    win.removeEventListener('blur', blur);
  }
  function stopFrame() { if (frame !== null) { const old = frame; frame = null; cancel(old); } }
  function safely(work: () => void) {
    if (disposed || failed) return;
    try { work(); } catch {
      failed = true;
      try { stopFrame(); } catch { /* A faulty scheduler cannot prevent recovery. */ }
      removeHandlers();
      try { view.error(); } catch { root.textContent = 'Game unavailable. Reload to retry.'; }
    }
  }
  function synchronize() {
    const current = now();
    state = transition(state, { type: 'advance', elapsedMs: Math.max(0, current - previous) }, random);
    previous = current;
  }
  function refresh() {
    view.render(state);
    if (state.phase === 'running' && frame === null) frame = schedule(tick);
    if (state.phase !== 'running') stopFrame();
  }
  function tick() { if (disposed || failed || state.phase !== 'running') return; frame = null; safely(() => { synchronize(); refresh(); }); }
  function dispatch(action: Action) {
    safely(() => {
      synchronize();
      if (action.type === 'resume' && doc.hidden) return;
      state = transition(state, action, random); refresh();
      if (action.type === 'start' || action.type === 'restart' || action.type === 'resume') view.surface.focus();
    });
  }
  const keydown = (event: KeyboardEvent) => {
    if (doc.activeElement !== view.surface) return;
    const mapped = mapKey(event, state.phase);
    if (mapped.handled) event.preventDefault();
    if (mapped.action) dispatch(mapped.action);
  };
  const blur = () => { if (state.phase === 'running') dispatch({ type: 'pause' }); };
  const visibility = () => { if (doc.hidden) blur(); };
  view.surface.addEventListener('keydown', keydown);
  doc.addEventListener('visibilitychange', visibility); win.addEventListener('blur', blur);
  safely(refresh);
  return {
    /** Idempotent disposal prevents stale callbacks from changing/rendering state. */
    dispose() {
      if (disposed) return;
      disposed = true; stopFrame(); removeHandlers(); view.dispose();
    },
  };
}
