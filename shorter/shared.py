from flask import render_template, url_for
from markupsafe import Markup


def errorhandler(error):
    return (
        render_template(
            "error.html",
            error=error,
            title=error.code,
        ),
        error.code,
    )


def redirect_meta(short):
    delay = 1 + short.delay

    return Markup(
        f"""
<meta name="referrer" content="no-referrer">
<meta http-equiv="refresh" content="{delay}; url={short.target}">
    """.strip()
    )


def redirect_link(short, text=None):
    text = Markup.escape(text if text else short.target)

    return Markup(
        f"""
<a rel="nofollow" href="{short.target}">{text}</a>
    """.strip()
    )


def redirect_script(short):
    delay = 1000 * short.delay

    return Markup(
        f"""
<script>
(function() {{ setTimeout(function() {{
  window.location.replace('{short.target}');
}}, {delay}); }})();
</script>
    """.strip()
    )


def clipboard_copy(button_id, text_id):
    return Markup(
        f"""
<script>
(function (btn, txt) {{
  if (!btn || !txt) {{ return; }}
  btn.addEventListener('click', function(event) {{
    event.preventDefault(); txt.contentEditable = true; txt.readonly = false;
    (function (rng, sel) {{
        if (!rng || !sel) {{ return; }}
        rng.selectNodeContents(txt); sel.removeAllRanges(); sel.addRange(rng);
        txt.setSelectionRange(0, 999999); document.execCommand('copy');
        txt.contentEditable = false; txt.readonly = true;
    }})(document.createRange(), window.getSelection());
  }});
}})(
  document.getElementById('{button_id}'),
  document.getElementById('{text_id}'),
);
</script>
    """.strip()
    )


def bookmarklet():
    base = url_for("main.index", _external=True)

    return Markup(
        "".join(
            src.strip()
            for src in f"""
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
        """.strip().splitlines()
        )
    )
