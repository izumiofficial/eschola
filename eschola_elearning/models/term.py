from odoo import api, fields, models


class Term(models.Model):
    _name = "term"
    _description = "Term"

    name = fields.Char(string='Name')
    school_year_id = fields.Many2one('school.year', string='School Year')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    sequence = fields.Integer()
