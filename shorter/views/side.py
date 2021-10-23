from flask import (
    Blueprint,
    abort,
    current_app,
    make_response,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from jinja2.exceptions import TemplateNotFound

from shorter.support import is_botagent

BLUEPRINT_SIDE = Blueprint("side", __name__)


@BLUEPRINT_SIDE.route("/robots.txt")
def robots():
    cont = [
        "User-Agent: *",
        f"Allow: {url_for('main.index')}$",
        f"Allow: {url_for('side.favicon')}",
        f"Allow: {url_for('side.logo')}",
        f"Allow: {url_for('side.page', name='')}",
    ]
    if is_botagent(request.user_agent):
        cont.append(f"Disallow: {url_for('main.short', symb='')}")

    resp = make_response("\n".join(cont).strip())

    resp.headers.set("Content-Type", "text/plain", charset="utf-8")
    return resp


@BLUEPRINT_SIDE.route("/logo.png", endpoint="logo")
@BLUEPRINT_SIDE.route("/favicon.ico")
@BLUEPRINT_SIDE.route("/favicon.png")
def favicon():
    return send_from_directory(
        current_app.static_folder,
        "favicon.png",
        mimetype="image/png",
    )


@BLUEPRINT_SIDE.route("/page/<string:name>")
def page(name):
    if any(name.startswith(start) for start in (".", "_")):
        abort(404)

    result = None
    try:
        result = render_template(
            f"page/{name}.html",
            title=name,
        )
    except TemplateNotFound:
        abort(404)

    return result
