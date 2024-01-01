from operator import itemgetter
from odoo.http import request, Response
from odoo import http, fields, http, api, _
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers.portal import CustomerPortal, pager


class PortalController(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        persons_count = request.env['person.details'].search_count([])
        if persons_count:
            values['persons_count'] = persons_count
        return values

    @http.route(['/my/persons', '/my/persons/page/<int:page>'], auth="user", type='http', wedsite=True)
    def persons_list_view(self, page=1, sortby='id', search="", search_in="All", groupby="none", **kw):
        if not groupby:
            groupby = 'none'
        sorted_list = {
            'id': {'label': 'Newest', 'order': 'id desc'},
            'name': {'label': 'Name', 'order': 'name'},
            'email': {'label': 'Email', 'order': 'email'},
        }
        search_list = {
            'All': {'label': 'All', 'input': 'All', 'domain': []},
            'Name': {'label': 'Person Name', 'input': 'Name', 'domain': [('name', 'ilike', search)]},
            'Email': {'label': 'Person Email', 'input': 'Email', 'domain': [('email', 'ilike', search)]},
        }
        groupby_list = {
            'none': {'input': 'none', 'label': _("None"), "order": 1},
            'date': {'input': 'date', 'label': _("Date"), "order": 1},
            'phone': {'input': 'phone', 'label': _("Phone"), "order": 1},
        }

        person_group_by = groupby_list.get(groupby, {})
        search_domain = search_list[search_in]['domain']
        default_order_by = sorted_list[sortby]['order']
        if groupby in ("date", "phone"):
            person_group_by = person_group_by.get("input")
            default_order_by = person_group_by + "," + default_order_by
        else:
            person_group_by = ''
        person_obj = request.env['person.details']
        total_persons = person_obj.sudo().search_count(search_domain)
        stud_url = '/my/persons'
        page_detail = pager(url=stud_url, total=total_persons, page=page, step=10,
                            url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby})
        persons = person_obj.sudo().search(search_domain, limit=10, order=default_order_by, offset=page_detail['offset'])
        if person_group_by:
            persons_group_list = [{person_group_by: k, 'persons': person_obj.concat(*g)} for k, g in groupbyelem(persons, itemgetter(person_group_by))]
        else:
            persons_group_list = [{'persons': persons}]
        vals = {
            # 'persons':persons,
            'group_persons': persons_group_list,
            'page_name': 'persons_list_view',
            'pager': page_detail,
            'default_url': stud_url,
            'groupby': groupby,
            'sortby': sortby,
            'searchbar_sortings': sorted_list,
            'searchbar_groupby': groupby_list,
            'search_in': search_in,
            'searchbar_inputs': search_list,
            'search': search,
        }
        return request.render("persons.portal_my_persons_list_view", vals)

    @http.route(['/my/person/<model("person.details"):person_id>'], auth="user", type='http', website=True)
    def person_form_view(self, person_id, **kw):
        vals = {"person": person_id, 'page_name': 'persons_form_view'}
        person_records = request.env['person.details'].search([])
        person_ids = person_records.ids
        person_index = person_ids.index(person_id.id)
        if person_index != 0 and person_ids[person_index - 1]:
            vals['prev_record'] = '/my/person/{}'.format(person_ids[person_index - 1])
        if person_index < len(person_ids) - 1 and person_ids[person_index + 1]:
            vals['next_record'] = '/my/person/{}'.format(person_ids[person_index + 1])
        return request.render("persons.portal_my_persons_form_view", vals)

    @http.route("/my/person/print/<model('person.details'):person_id>", auth="user", type="http", website=True)
    def person_report_print(self, person_id, **kw):
        return self._show_report(model=person_id, report_type='pdf', download=False,
                                 report_ref='persons.person_profile_report_temp')

    @http.route(["/new/person"], type="http", methods=["POST", "GET"], auth="user", website=True)
    def register_new_person_profile(self, **kw):
        create_uid_list = request.env['res.users'].search([])
        vals = {'users': create_uid_list, 'page_name': "register_person"}
        if request.httprequest.method == "POST":
            error_list = []
            if not kw.get("name"):
                error_list.append("Name field is mandatory.")
            if not kw.get("user"):
                error_list.append("User field is mandatory.")
            if not kw.get("user").isdigit():
                error_list.append("Invalid user field.")
            elif not request.env['res.users'].search([('id', '=', int(kw.get("user")))]):
                error_list.append("Invalid user field selected value.")
            elif not error_list:
                request.env['person.details'].create({"name": kw.get("name"), "create_uid": int(kw.get("user"))})
                success = "Successfully person registered!"
                vals['success_msg'] = success
            else:
                vals['error_list'] = error_list
        else:
            print("GET Method..........")

        return request.render("persons.new_person_form_view_portal", vals)
