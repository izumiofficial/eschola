from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AdmissionRegister(models.Model):
    _name = 'admission.register'
    _description = 'Admission of family'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Student Name', translate=True)
    email = fields.Char(string='Email', required=True)
    mobile = fields.Char(unaccent=False)
    country = fields.Many2one('res.country', string='Country of Residence')
    grade = fields.Selection([
        ('grade_7', 'Grade 7'),
        ('grade_8', 'Grade 8'),
        ('grade_9', 'Grade 9'),
        ('grade_10', 'Grade 10'),
        ('al_as', 'AL/AS')
    ], string='Grade', requred=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')
    ])

    child_ids = fields.One2many('registered.child', 'admission_id', string="Student")
