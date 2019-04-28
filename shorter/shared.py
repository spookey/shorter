from flask import render_template


def errorhandler(error):
    return render_template(
        'error.html',
        error=error,
    ), error.code
