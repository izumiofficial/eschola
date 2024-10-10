from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError, UserError

class GradingStructure(models.Model):
    _name = 'grading.structure'
    _description = 'Grading Structure'
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name")
    school_year = fields.Many2one('school.year', string='School Year')
    academic_stage = fields.Many2one('student.grades', string='Academic Stage')
    course_id = fields.Many2one('slide.channel', string='Course', domain=[('is_published', '=', True)])  # display only published slide (is_published)
    grading_line_ids = fields.One2many('grading.line', 'grading_structure_id', string='Assignments')

    total_weightage = fields.Integer(string='Total %', compute='_compute_total_weightage')  # calculate the weightage from grading_line_ids and show error if exceeding 100

    @api.depends('grading_line_ids.weightage')
    def _compute_total_weightage(self):
        for record in self:
            if record.grading_line_ids:  # Only calculate if there are grading lines
                total = sum(record.grading_line_ids.mapped('weightage'))
                if total != 100:
                    raise ValidationError("Total weightage must be exactly 100%")
                record.total_weightage = total
            else:
                record.total_weightage = 0  # Or leave it undefined
