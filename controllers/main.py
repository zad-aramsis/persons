import logging
from odoo import http, fields, http, api, _
from odoo.http import request, Response
from odoo.addons.persons.controllers.validate_token import validate_token
from odoo.exceptions import AccessError, UserError, AccessDenied

_logger = logging.getLogger(__name__)


class PersonDetailsController(http.Controller):
    @http.route('/print_hello_world', wedsite=True, type='http', auth='public')
    def hello_world(self, **kw):
        return "Hello, world"

    @http.route('/all_persons_as_objects', type='http', auth='public')
    def all_persons_as_objects(self, **kw):
        return request.render('persons.list_objects', {
            'root': '/',
            'objects': http.request.env['person.details'].sudo().search([]),
        })

    @http.route('/person_as_object/<model("person.details"):obj>', type='http', auth='public')
    def person_as_object(self, obj, **kw):
        return request.render('persons.get_object', {'object': obj})

    @http.route('/web_view_persons', type="http", auth="public", website=True)
    def web_view_persons(self):
        persons = request.env['person.details'].sudo().search([])
        values = {'records': persons}
        return request.render("persons.tmp_person_data", values)

    @validate_token
    @http.route("/read_all_persons", type="json", methods=['GET'], auth="none")
    def read_all_persons(self):
        persons = request.env['person.details'].sudo().search([])
        if persons:
            vals = [
                {
                    'id': str(rec.id),
                    'name': str(rec.name),
                    'email': str(rec.email),
                    'phone': str(rec.phone),
                    'date': str(rec.date),
                }
                for rec in persons
            ]
            return {'status': 200, 'response': vals}
        else:
            return {'status': 404, 'response': 'Not Found'}

    @validate_token
    @http.route("/read_person/<id>", type="json", methods=['GET'], auth="none")
    def read_person(self, id=None):
        persons = request.env['person.details'].sudo().search([('id', '=', id)])
        if persons:
            vals = {
                'id': persons.id,
                'name': persons.name,
                'email': persons.email,
                'phone': persons.phone,
                'date': persons.date,
            }
            return {'status': 200, 'response': vals}
        else:
            return {'status': 404, 'response': 'Not Found'}

    @validate_token
    @http.route('/create_new_person', type='json', methods=['POST'], auth='none')
    def create_new_person(self, **post):
        person = request.env['person.details']
        if request.httprequest.method == 'POST' and post:
            new_person = person.sudo().create(self.prepare_api_vals(post))
            if new_person:
                data = {'status': 200, 'person_id': new_person.id}
            else:
                data = {'status': 404, 'response': 'Not Found'}
        else:
            data = {'status': 101, 'response': 'NO Details to Create'}
        return data

    def prepare_api_vals(self, post):
        return {
            'name': post['name'] or '',
            'email': post['email'] or '',
            'phone': post['phone'] or 0.0,
            'date': post['date'] or '',
        }

    @validate_token
    @http.route('/write_person/<id>', type='json', methods=['POST'], auth='none')
    def write_person(self, **post):
        if request.httprequest.method == 'POST' and post:
            person = request.env['person.details'].sudo().search([('id', '=', post['id'])])
            if person:
                values = {
                    'name': str(post['name']),
                    'email': str(post['email']),
                    'phone': str(post['phone']),
                    'date': str(post['date'])
                }
                person.write(values)
                data = {'status': 200, 'person_id': person.id}
            else:
                data = {'status': 404, 'response': 'Not Found'}
        else:
            data = {'status': 101, 'response': 'NO Details to Write'}
        return data

    @validate_token
    @http.route("/delete_person/<id>", type="json", methods=['GET'], auth="none")
    def delete_person(self, id=None):
        person = request.env['person.details'].sudo().search([('id', '=', id)])
        if person:
            person.unlink()
            return {'status': 200, 'response': 'Done'}
        else:
            return {'status': 404, 'response': 'Not Found'}

    @http.route("/all", type="json", auth="none")
    def read_all(self, db, login, password):
        if not http.db_filter([db]):
            raise AccessError("Database not found.")
        else:
            db = db
        # data = request.httprequest.get_data()
        # vals = json.loads(data)
        login_params_missing = login is None or password is None or db is None
        if login_params_missing:
            return {'error': "Login Parameters Missing"}  # missing parameters
        else:
            try:
                uid = request.session.authenticate(db, login, password)
            except Exception as e:
                return {'error': "Authenticate Error", 'message': e}  # Bad credentials
            if not uid:
                return {'error': "User not found"}  # Bad credentials
        persons_rec = request.env['person.details'].sudo().search([])
        persons = [
            {
                'id': str(rec.id),
                'name': str(rec.name),
                'email': str(rec.email),
                'phone': str(rec.phone),
                'date': str(rec.date),
            }
            for rec in persons_rec
        ]
        return {'status': 200, 'response': persons}
