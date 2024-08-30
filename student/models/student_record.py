from odoo import models, fields, api

class StudentRecord(models.Model):
    _name = 'student.record'
    _description = 'To store student records'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}

    is_international = fields.Boolean(string='International Curriculum')
    first_name = fields.Char(string='First Name', translate=True, required=True)
    middle_name = fields.Char(string='Middle Name', translate=True, required=True)
    last_name = fields.Char(string='Last Name', translate=True, required=True)
    email = fields.Char(string='Email', required=True)
    mobile = fields.Char(unaccent=False)
    # birth_date = fields.Date(string='Birth Date', required=True)
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
    # city = fields.Char(string='City of Residence', required=True)
    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('christian', 'Christian')
    ], string='Gender', required=True)

