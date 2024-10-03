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
    # other_guardian = fields.Many2one()

    @api.onchange('name')
    def _update_name(self):
        # if name in guardian is change, name in res.partner also change/updated
        for record in self:
            if record.partner_id:
                record.partner_id.name = record.name

    @api.onchange('country')
    def _update_country(self):
        # if country in guardian is change, country in res.partner also change/updated
        for record in self:
            if record.partner_id:
                record.partner_id.country_id = record.country

    @api.onchange('email')
    def _update_email(self):
        # if email in guardian is change, email in res.partner also change/updated
        for record in self:
            if record.partner_id:
                record.partner_id.email = record.email

    @api.onchange('mobile')
    def _update_mobile(self):
        # if mobile in guardian is change, mobile in res.partner also change/updated
        for record in self:
            if record.partner_id:
                record.partner_id.mobile = record.mobile