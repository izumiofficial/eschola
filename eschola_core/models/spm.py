from odoo import models, fields, api, _

class Spm(models.Model):
    _name = 'spm'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute="_create_name", string='Name')
    partner_id = fields.Many2one('res.partner', 'Partner')
    fullname = fields.Char(string='Fullname', translate=True, required=True)
    birth_date = fields.Date(string='Birth Date', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    nationality = fields.Many2one('res.country', 'Nationality')
    active = fields.Boolean(default=True)

    @api.depends('fullname')
    def _create_name(self):
        # name will be created according to the fullname
        for record in self:
            record.name = record.fullname
