/** Static browser entry with readable containment of bootstrap failures. */
import { mountGame } from './host.js';
try {
  const root = document.querySelector<HTMLElement>('#app');
  if (!root) throw new Error('Application root missing');
  mountGame(root);
} catch {
  const alert = document.createElement('p'); alert.setAttribute('role', 'alert');
  alert.textContent = 'Game unavailable. Reload to retry.';
  (document.querySelector('#app') ?? document.body).replaceChildren(alert);
}
