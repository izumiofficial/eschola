from odoo import api, fields, models

class Assignments(models.Model):
    _name = 'assignments'

    name = fields.Char(string='Assignment Type')
    active = fields.Boolean(string='Active')

    grading_structure_id = fields.Many2one('grading.structure', string='Grading Structure')
