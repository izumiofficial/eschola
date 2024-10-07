from odoo import api, fields, models

class GradingStructure(models.Model):
    _name = 'grading.structure'
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name")
    school_year = fields.Many2one('school.year', string='School Year')
    academic_stage = fields.Many2one('student.grades', string='Academic Stage')
    course_id = fields.Many2one('slide.channel', string='Course', domain=[('is_published', '=', True)])  # display only published slide (is_published)
    assignment_ids = fields.One2many('assignments', 'grading_structure_id', string='Assignments')
