from odoo import api, fields, models

class CourseAttendance(models.Model):
    _name = 'course.attendance'

    name = fields.Char('Name', readonly=True, size=32)
    spm = fields.Many2one('res.users', string='SPM')
    course_id = fields.Many2one('course_id')
    session_id = fields.Many2one('session', 'Session')
    attendance_date = fields.Date(
        'Date', default=lambda self: fields.Date.today(),
        tracking=True)
