/** Physical-key mapping; native button activation remains the DOM's concern. */
import type { Action } from '../../core/model.js';
const commands: Record<string, Action> = {
  ArrowLeft: { type: 'move', dx: -1 }, ArrowRight: { type: 'move', dx: 1 },
  ArrowDown: { type: 'softDrop' }, ArrowUp: { type: 'rotate', direction: 1 },
  KeyX: { type: 'rotate', direction: 1 }, KeyZ: { type: 'rotate', direction: -1 }, KeyR: { type: 'restart' },
};
/** Report recognized-but-ignored repeats so the host can still prevent scrolling. */
export function mapKey(event: Pick<KeyboardEvent, 'code' | 'repeat' | 'ctrlKey' | 'altKey' | 'metaKey'>): { handled: boolean; action: Action | null } {
  const action = Object.hasOwn(commands, event.code) ? commands[event.code] : undefined;
  if (!action || event.ctrlKey || event.altKey || event.metaKey) return { handled: false, action: null };
  const discrete = action.type === 'rotate' || action.type === 'restart';
  return { handled: true, action: event.repeat && discrete ? null : { ...action } };
}
