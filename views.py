# coding: utf-8

from barcamp import app
from flask import render_template, abort
from login_misc import check_auth, get_account
from talks import get_talks, get_talks_dict
from utils import menu, markdown_static_page, markdown_markup
from entrant import get_count, get_entrants
from vote import get_user_votes
from program import times


@app.route("/")
def index():
    user = check_auth()
    user_hash = None
    talks, extra_talks = get_talks()
    if user:
        user_hash = user['user_hash']
    return render_template(
        "index.html",
        user=user,
        menu=menu(),
        times=times,
        entrant_count=get_count(),
        entrants=get_entrants()[50:0:-1],
        #user_votes=get_user_votes(user_hash),
        sponsors_main=markdown_markup('sponsors_main'),
        sponsors=markdown_markup('sponsors'),
        talks=get_talks_dict())


@app.route('/ucastnici/')
def entrants():
    return render_template(
        "entrants.html",
        user=check_auth(),
        menu=menu(),
        entrant_count=get_count(),
        entrants=reversed(get_entrants())
    )


@app.route('/partneri/')
def sponsors():
    return render_template(
        "partneri.html",
        user=check_auth(),
        menu=menu(),
        sponsors_main=markdown_markup('sponsors_main'),
        sponsors=markdown_markup('sponsors'),
        sponsors_other=markdown_markup('sponsors_other'),
    )


@app.route('/profil/<user_hash>/')
def profile(user_hash):
    data = get_account(user_hash)
    if not data:
        abort(404)

    return render_template(
        'profil.html',
        user=check_auth(),
        menu=menu(),
        profile=data
    )


@app.route("/stranka/<page>/")
def static_page(page):
    return markdown_static_page(page)
