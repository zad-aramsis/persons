from odoo import models, fields, api


class PersonDetails(models.Model):
    _name = 'person.details'
    _description = 'Person'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    img = fields.Image("Person Image")
    phone = fields.Integer()
    email = fields.Char()
    date = fields.Date()
