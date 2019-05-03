from flask import render_template
from jinja2 import Markup


def errorhandler(error):
    return render_template(
        'error.html',
        error=error,
        title=error.code,
    ), error.code


def redirect_meta(short):
    return Markup('''
<meta name="referrer" content="no-referrer" />
<meta http-equiv="refresh" content="{delay}; url={href}" />
    '''.format(
        delay=short.delay,
        href=short.target,
    ).strip())


def redirect_link(short, text=None):
    return Markup('''
<a rel="nofollow" href="{href}">{text}</a>
    '''.format(
        href=short.target,
        text=text if text else short.target,
    ).strip())


def redirect_script(short):
    return Markup('''
<script>
setTimeout(function() {{
  window.location.replace("{href}");
}}, {delay});
</script>
    '''.format(
        delay=1000 * short.delay,
        href=short.target,
    ).strip())
