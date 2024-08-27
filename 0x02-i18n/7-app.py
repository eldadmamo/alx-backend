#!/usr/bin/env python3
"""Flask app"""
from typing import Dict

from flask import Flask, g, render_template, request
from flask_babel import Babel
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError

app = Flask(__name__)
babel = Babel(app)


class Config:
    """Config app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = LANGUAGES[0]
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

users = {
    1: {
        "name": "Balou",
        "locale": "fr",
        "timezone": "Europe/Paris"
    },
    2: {
        "name": "Beyonce",
        "locale": "en",
        "timezone": "US/Central"
    },
    3: {
        "name": "Spock",
        "locale": "kg",
        "timezone": "Vulcan"
    },
    4: {
        "name": "Teletubby",
        "locale": None,
        "timezone": "Europe/London"
    },
}


def get_user() -> Dict:
    """Get user from request"""
    try:
        return users.get(int(request.args.get('login_as')))
    except Exception:
        return None


@app.route('/')
def welcome() -> str:
    """message"""
    username = None
    user = g.get('user', None)
    if user:
        username = user.get('name', None)

    return render_template('7-index.html', username=username)


@app.before_request
def before_request():
    """Find a user if any, and set it as a global on flask.g.user"""
    user = get_user()
    if user:
        g.user = user


@babel.localeselector
def get_locale():
    """locale request"""
    lang = request.args.get('locale')
    if lang in Config.LANGUAGES:
        return lang
    user = get_user()
    if user:
        lang = user.get('locale')
        if lang in Config.LANGUAGES:
            return lang
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone(tz) -> str:
    """timezone request"""
    try:
        if tz:
            return timezone(tz).zone
        tz_arg = request.args.get('timezone')
        if tz_arg:
            return timezone(request.args.get('timezone')).zone
        else:
            user = get_user()
            if user and user.get('timezone'):
                return timezone(user.get('timezone')).zone
    except UnknownTimeZoneError:
        pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == '__main__':
    app.run()
