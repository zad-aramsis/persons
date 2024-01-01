import logging
import functools
from odoo.http import request

_logger = logging.getLogger(__name__)


def validate_token(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        access_token = request.httprequest.headers.get("Authorization")
        if not access_token:
            return {
                'status': 'fail',
                'message': 'missing access token in request header'
            }
        access_token_data = request.env["api.access_token"].sudo().search([("token", "=", access_token)],
                                                                          order="id DESC", limit=1)

        if access_token_data.find_or_create_token(user_id=access_token_data.user_id.id) != access_token:
            return {
                'status': 'fail',
                'message': 'token seems to have expired or invalid'
            }

        request.session.uid = access_token_data.user_id.id
        request.update_env = access_token_data.user_id.id
        return func(self, *args, **kwargs)

    return wrap
