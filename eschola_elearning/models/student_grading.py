from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError, UserError


class StudentGrading(models.Model):
    _name = 'student.grading'
    _description = 'Student Grading'
    _inherit = ["mail.thread"]

    name = fields.Char(string='Name')
    course_id = fields.Many2one('slide.channel', string='Course', domain=[('is_published', '=', True)])
    school_year_id = fields.Many2one('school.year', string='School Year', related='course_id.school_year_id')
    academic_stage = fields.Many2one('student.grades', string='Academic Stage')
    assignments_id = fields.Many2one('assignments', string='Assignment Type')
    assignment_date = fields.Date(string='Assignment Date')
    total_marks = fields.Integer(string='Total Marks')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Grading'),
        ('done', 'Done'),
        ('cancel', 'Canceled')
    ], string='Status', default='draft')

    def start_grading(self):
        students = self.env['slide.channel.partner'].search([('channel_id', '=', self.course_id.id)]).partner_id
        for record in students:
            print(record)
            self.env['grading'].create({
                'student_id': record.id,
                'course_id': self.course_id.id,
                'school_year_id': self.school_year_id.id,
                'academic_stage': self.academic_stage.id,
                'assignments_id': self.assignments_id.id,
                'assignment_date': self.assignment_date,
                'total_marks': self.total_marks,
                'grading_id': self.id
            })

        self.state = 'confirm'

    def action_grading(self):
        grading = self.env['grading'].search([('grading_id', '=', self.id)])
        if not grading:
            return {
                'name': 'Grading Sheet',
                'view_type': 'tree',
                'view_mode': 'tree',
                'views': [(self.env.ref('eschola_elearning.view_grading_tree').id, 'tree')],
                'res_model': 'grading',
                'view_id': False,  # Force creation of a new record
                'target': 'current',
                'context': {
                    'default_grading_id': self.id,
                    'default_course_id': self.course_id.id,
                    'default_school_year_id': self.school_year_id.id,
                    'default_academic_stage': self.academic_stage.id,
                    'default_assignments_id': self.assignments_id.id,
                    'default_assignment_date': self.assignment_date,
                    'default_total_marks': self.total_marks,
                },
            }

        # action = self.env.ref('eschola_elearning.act_open_attendance_sheet_view').read()[0]
        action = self.env['ir.actions.act_window']._for_xml_id('eschola_elearning.act_open_grading')
        action['domain'] = [('grading_id', '=', self.id)]
        action['context'] = {
            'default_grading_id': self.id,
            'default_course_id': self.course_id.id,
            'default_school_year_id': self.school_year_id.id,
            'default_academic_stage': self.academic_stage.id,
            'default_assignments_id': self.assignments_id.id,
            'default_assignment_date': self.assignment_date,
            'default_total_marks': self.total_marks,
        }
        return action
