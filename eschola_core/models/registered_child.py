from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RegisteredChild(models.Model):
    _name = 'registered.child'
    _description = 'Dynamically admin the kids'

    is_international = fields.Boolean(string='International Curriculum')
    name = fields.Char(string='Name', translate=True)
    email = fields.Char(string='Email', required=True)
    mobile = fields.Char(unaccent=False)
    birth_date = fields.Date(string='Birth Date', required=True)
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female')
    ], string='Gender', required=True, default='m')
    grade = fields.Selection([
        ('grade_7', 'Grade 7'),
        ('grade_8', 'Grade 8'),
        ('grade_9', 'Grade 9'),
        ('grade_10', 'Grade 10'),
        ('al_as', 'AL/AS')
    ], string='Grade', requred=True)
    nationality = fields.Many2one('res.country', string='Nationality')
    country = fields.Many2one('res.country', string='Country of Residence')
    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('christian', 'Christian')
    ], string='Gender', required=True)
    admission_id = fields.Many2one('admission.register', string="Register")
