from odoo import api,fields,models

class ResPartner(models.Model):
    _inherit = "res.partner"

    unique_id = fields.Char(string='Unique ID')

    _sql_constraints = [('uniq_id', 'unique(unique_id)', 'User ID must be unique!')]

