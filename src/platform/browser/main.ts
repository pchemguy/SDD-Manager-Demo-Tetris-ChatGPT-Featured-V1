/** Static browser entry. Shared rules and presentation are composed by the host. */
import { mountGame } from './host.js';
const root = document.querySelector<HTMLElement>('#app');
if (!root) throw new Error('Application root missing');
mountGame(root);
