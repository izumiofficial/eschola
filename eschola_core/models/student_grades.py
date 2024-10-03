from odoo import models, fields, api, _

class StudentGrades(models.Model):
    _name = 'student.grades'

    name = fields.Char(string='Grade', required=True)
    is_active = fields.Boolean(string='Active')
    sequence = fields.Integer()

