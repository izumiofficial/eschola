from odoo import api, fields, models


class SchoolYear(models.Model):
    _name = "school.year"
    _description = "School Year"

    name = fields.Char(string='School Year')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer()
