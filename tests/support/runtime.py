"""Launch options for trusted local tests, with an explicitly gated remedy."""
import os

def launch_browser(runner, engine):
    """Keep the default sandbox unless this host's diagnosed flag is supplied."""
    options = {'headless': True, 'timeout': 15000}
    if engine == 'firefox' and os.environ.get('TETRIS_FIREFOX_CONTENT_SANDBOX') == '1':
        options['env'] = dict(os.environ, MOZ_DISABLE_CONTENT_SANDBOX='1')
    return getattr(runner, engine).launch(**options)
