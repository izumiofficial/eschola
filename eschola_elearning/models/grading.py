from odoo import api, fields, models

class Grading(models.Model):
    _name = 'grading'
    _description = 'Grading'

    name = fields.Char('Name', readonly=True, size=32)
    student_id = fields.Many2one('res.partner', 'Student')
    course_id = fields.Many2one('slide.channel', string='Course', domain=[('is_published', '=', True)])
    school_year_id = fields.Many2one('school.year', string='School Year')
    academic_stage = fields.Many2one('student.grades', string='Academic Stage')
    assignments_id = fields.Many2one('assignments', string='Assignment Type')
    assignment_date = fields.Date(string='Assignment Date')
    scored_marks = fields.Integer(string='Scored')
    total_marks = fields.Integer(string='Total Marks')
    state = fields.Selection([
        ('draft', ''),
        ('no_submission', 'Missed'),
        ('late', 'Delay'),
        ('submit', 'Submitted')
    ], string='Status', default=None)
    grading_id = fields.Many2one('student.grading', 'Student Grading')
    mark_percent = fields.Char(string='Percentage', compute='_get_percentage')  # calculate percentage scored_marks/total_marks

    @api.depends('scored_marks', 'total_marks')
    def _get_percentage(self):
        for record in self:
            if record.total_marks > 0:
                percentage = (record.scored_marks / record.total_marks) * 100
                record.mark_percent = f"{percentage:.2f}%"  # Format with '%'
            else:
                record.mark_percent = "0%"  # Display 0%
