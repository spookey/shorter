from flask import render_template, url_for
from jinja2 import Markup


def errorhandler(error):
    return render_template(
        'error.html',
        error=error,
        title=error.code,
    ), error.code


def redirect_meta(short):
    return Markup('''
<meta name="referrer" content="no-referrer">
<meta http-equiv="refresh" content="{delay}; url={href}">
    '''.format(
        delay=short.delay,
        href=short.target,
    ).strip())


def redirect_link(short, text=None):
    return Markup('''
<a rel="nofollow" href="{href}">{text}</a>
    '''.format(
        href=short.target,
        text=Markup.escape(text if text else short.target),
    ).strip())


def redirect_script(short):
    return Markup('''
<script>
(function() {{ setTimeout(function() {{
  window.location.replace('{href}');
}}, {delay}); }})();
</script>
    '''.format(
        delay=1000 * short.delay,
        href=short.target,
    ).strip())


def clipboard_copy(button_id, text_id):
    return Markup('''
<script>
(function (btn, txt) {{
  if (!btn || !txt) {{ return; }}
  btn.addEventListener('click', function(event) {{
    event.preventDefault(); txt.select(); document.execCommand('copy');
  }});
}})(document.getElementById('{btn_id}'), document.getElementById('{txt_id}'));
</script>
    '''.format(
        btn_id=button_id,
        txt_id=text_id,
    ).strip())


def bookmarklet():
    return Markup(
        ''.join(src.strip() for src in '''
javascript:(
  function(){{
    window.location.assign(
        '{base}'.concat(
            '?target=',
            encodeURIComponent(window.location)
        )
    );
  }}
)();
        '''.format(
            base=url_for('main.index', _external=True)
        ).strip().splitlines())
    )
