import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class AccessToken(http.Controller):

    @http.route("/login", methods=["POST"], type="json", auth="none", csrf=False)
    def api_login(self, **post):
        db, username, password = (post["db"], post["login"], post["password"])

        _credentials_includes_in_body = all([db, username, password])
        if not _credentials_includes_in_body:
            # The request post body is empty the credentials maybe passed via the headers.
            headers = request.httprequest.headers
            db = headers.get("db")
            username = headers.get("login")
            password = headers.get("password")
            _credentials_includes_in_headers = all([db, username, password])
            if not _credentials_includes_in_headers:
                return {
                    "status": "fail",
                    "message": "either of the following are missing [username,password]"
                }
        # Login in odoo database:
        try:
            uid = request.session.authenticate(db, username, password)
        except Exception as e:
            return {'error': "Authenticate Error", 'message': e}  # Bad credentials
        if not uid:
            return {"status": "fail", "message": "Authentication Failed"}  # Bad credentials

        # Generate tokens
        access_token = request.env["api.access_token"].find_or_create_token(user_id=uid, create=True)
        return {
            'status': 200,
            'message': "Success",
            'access_token': access_token,
            'uid': uid,
        }
