from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Guardian(models.Model):
    _name = "guardian"
    _description = "Parent"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', translate=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    email = fields.Char(string='Email', required=True)
    mobile = fields.Char(unaccent=False)
    country = fields.Many2one('res.country', string='Country of Residence')

    student_ids = fields.One2many('student', 'primary_guardian_id', string='Child')
    other_guardian = fields.Many2one() # in
