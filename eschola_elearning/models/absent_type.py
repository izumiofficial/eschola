from odoo import api, fields, models

class AbsentType(models.Model):
    _name = 'absent.type'
    _description = 'Absent Type'

    name = fields.Char(string='Absent Type')
    is_active = fields.Boolean(string='Active')
    sequence = fields.Integer()
