# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from relengapi.util import make_support_class
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from flask.ext.login import current_user
from .user import User


bp = Blueprint('userauth', __name__, template_folder='templates')


@bp.route('/login_request')
def login_request():
    """Redirect here to ask the user to authenticate"""
    if current_user.is_authenticated():
        next_url = request.args.get('next') or url_for('root')
        return redirect(next_url)
    return current_app.auth.login_request()


@bp.record
def init_blueprint(state):
    from relengapi import login_manager
    app = state.app

    @login_manager.user_loader
    def login_manager_user_loader(authenticated_email):
        return User(authenticated_email)

    # configure the login manager to redirect to a bare "please login" page when
    # a login is required
    login_manager.login_view = 'userauth.login_request'
    login_manager.login_message = 'Please authenticate to the Releng API before proceeding'
    login_manager.init_app(app)

    auth_mechanisms = {
        'browserid': ('.browserid', 'BrowserIDAuth'),
        'external': ('.external', 'ExternalAuth'),
    }
    app.auth = make_support_class(app, __name__, auth_mechanisms,
                                  'RELENGAPI_AUTHENTICATION',
                                  'browserid')
