from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AdmissionRegister(models.Model):
    _name = 'admission.register'
    _description = 'Admission of family'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Guardian Name', translate=True)
    # secondary_guardian_name = fields.Char(string="Secondary Guardian Name")

    email = fields.Char(string='Email')
    mobile = fields.Char(unaccent=False)
    country = fields.Many2one('res.country', string='Country of Residence')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')
    ])

    # child_ids = fields.One2many('registered.child', 'admission_id', string="Student")

    # def action_confirm_registration(self):
    #     for child in self.child_ids:
    #         self.env['admission'].create({
    #             'child_name': child.name,
    #             'child_age': child.age,
    #         })
