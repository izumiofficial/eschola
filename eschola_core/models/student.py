from odoo import models, fields, api

class Student(models.Model):
    _name = 'student'
    _description = 'To store student records'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    is_international = fields.Boolean(string='International Curriculum')
    name = fields.Char(string='Name', translate=True)
    email = fields.Char(string='Email')
    mobile = fields.Char(unaccent=False)
    birth_date = fields.Date(string='Birth Date')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female')
    ], string='Gender', default='m')
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
    ], string='Religion')

    primary_guardian_id = fields.Many2one('guardian', string="Primary Guardian")
    secondary_guardian_id = fields.Many2one('guardian', string="Secondary Guardian")
