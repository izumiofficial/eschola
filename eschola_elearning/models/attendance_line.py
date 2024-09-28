from odoo import models, fields, api


class AttendanceLine(models.Model):
    _name = "attendance.line"
    _inherit = ["mail.thread"]
    # _rec_name = "attendance_id"
    _description = "Attendance Lines"
    _order = "attendance_date desc"

    attendance_id = fields.Many2one(
        'course.attendance', 'Attendance Sheet', required=True,
        tracking=True, ondelete="cascade")
    student_id = fields.Many2one(
        'slide.channel.partner',  # Change the model
        'Student',
        tracking=True
    )
    # participant_id = fields.Many2one(
    #     'slide.channel.partner',  # Relate to slide.channel.partner
    #     'Student',
    #     tracking=True,
    #     domain="[('channel_id', '=', course_id)]"  # Filter based on course_id
    # )
    present = fields.Boolean('Present', default=True, tracking=True)
    absent = fields.Boolean('Absent', tracking=True)
    absent_type = fields.Many2one('absent.type', string='Absent Type')
    course_id = fields.Many2one('slide.channel', 'Course')
    camera_on = fields.Boolean(string='On Camera', default=False)
    participation = fields.Boolean(string='Participation', default=False)
    remark = fields.Char('Remark', size=256, tracking=True)
    attendance_date = fields.Date(
        'Date', related='attendance_id.attendance_date', store=True,
        readonly=True, tracking=True)
    active = fields.Boolean(default=True)
