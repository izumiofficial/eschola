from odoo import api, fields, models

class Grading(models.Model):
    _name = 'grading'
    _description = 'Grading'

    name = fields.Char('Name', readonly=True, size=32)
    student_id = fields.Many2one('res.partner', 'Student')
    course_id = fields.Many2one('slide.channel', string='Course', domain=[('is_published', '=', True)])
    school_year_id = fields.Many2one('school.year', string='School Year', related='course_id.school_year_id')
    academic_stage = fields.Many2one('student.grades', string='Academic Stage')
    assignments_id = fields.Many2one('assignments', string='Assignment Type')
    assignment_date = fields.Date(string='Assignment Date')
    scored_marks = fields.Integer(string='Scored')
    total_marks = fields.Integer(string='Total Marks')
    state = fields.Selection([
        ('draft', 'Waiting Submission'),
        ('no_submission', 'Not Submit'),
        ('late', 'Late Submission'),
        ('submit', 'Submitted')
    ], string='Status', default='draft')
    grading_id = fields.Many2one('student.grading', 'Student Grading')
    mark_percent = fields.Float(string='Percentage', compute='_get_percentage')  # calculate percentage scored_marks/total_marks

    @api.depends('scored_marks', 'total_marks')
    def _get_percentage(self):
        for record in self:
            if record.total_marks > 0:
                record.mark_percent = (record.scored_marks / record.total_marks) * 100
            else:
                record.mark_percent = 0
