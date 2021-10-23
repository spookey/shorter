from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
)

from shorter.forms.short import ShortFindForm
from shorter.models.short import Short
from shorter.support import BLOCKLIST

BLUEPRINT_PLUS = Blueprint("plus", __name__, url_prefix="/plus")


@BLUEPRINT_PLUS.route("/")
def index():
    form = ShortFindForm(
        term=request.args.get("q"),
    )

    return render_template(
        "plus/index.html",
        title="Plus",
        form=form,
    )


@BLUEPRINT_PLUS.route(
    "/show/<string:field>/<any(asc,desc):sort>/<int:page>",
    methods=["POST", "GET"],
)
@BLUEPRINT_PLUS.route(
    "/show/<string:field>/<int:page>", methods=["POST", "GET"]
)
@BLUEPRINT_PLUS.route("/show/<int:page>", methods=["POST", "GET"])
@BLUEPRINT_PLUS.route("/show", methods=["POST", "GET"])
def show(page=None, field=None, sort=None):
    term = request.args.get("q", None)
    form = ShortFindForm(term=term)
    if form.validate_on_submit():
        target = form.action()
        if target:
            return redirect(target)

    query = (
        Short.searched(term, field=field, rev=sort == "desc")
        if term is not None
        else Short.ordered(field=field, rev=sort == "desc")
    )
    if not query:
        abort(404)

    return render_template(
        "plus/show.html",
        title="Show",
        form=form,
        elements=query.paginate(
            page=page, per_page=current_app.config["PAGINATION"]
        ),
    )


@BLUEPRINT_PLUS.route("/block/<string:field>/<any(asc,desc):sort>/<int:page>")
@BLUEPRINT_PLUS.route("/block/<string:field>/<int:page>")
@BLUEPRINT_PLUS.route("/block/<int:page>")
@BLUEPRINT_PLUS.route("/block")
def block(page=None, field=None, sort=None):
    query = Short.blocked(BLOCKLIST, field=field, rev=sort == "desc")
    if not query:
        abort(404)

    return render_template(
        "plus/show.html",
        title="Blocked",
        elements=query.paginate(
            page=page, per_page=current_app.config["PAGINATION"]
        ),
    )
