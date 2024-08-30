from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GuardianRecord(models.Model):
    _name = "guardian.record"
    _description = "Parent"

    salutation = fields.Selection([
        ('mr', 'Mr.'),
        ('ms', 'Ms.'),
        ('mrs', 'Mrs.')
    ], string='Title')
    first_name = fields.Char(string='First Name', translate=True, required=True)
    middle_name = fields.Char(string='Middle Name', translate=True, required=True)
    last_name = fields.Char(string='Last Name', translate=True, required=True)
    email = fields.Char(string='Email', required=True)
    mobile = fields.Char(unaccent=False)
    country = fields.Many2one('res.country', string='Country of Residence')
