from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    admission_register_id = fields.Many2one('admission.register', string="Admission Register")
    # is_activated = fields.Boolean(string='Is Activated', default=False)
