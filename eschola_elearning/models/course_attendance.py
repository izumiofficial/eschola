from odoo import api, fields, models


class CourseAttendance(models.Model):
    _name = 'course.attendance'
    _inherit = ["mail.thread"]

    name = fields.Char('Name', readonly=True, size=32)
    spm = fields.Many2one('res.users', string='SPM')
    course_id = fields.Many2one('slide.channel', string='Course')
    session_id = fields.Many2one('session', 'Session')
    student_id = fields.Many2one('res.partner', 'Student')
    present = fields.Boolean('Present', default=True, tracking=True)
    absent = fields.Boolean('Absent', tracking=True)
    absent_type = fields.Many2one('absent.type', string='Attendance')
    camera_on = fields.Boolean(string='Camera On', default=False)
    participation = fields.Boolean(string='Participation', default=False)
    remark = fields.Char('Remark', size=256, tracking=True)
    remarks = fields.Text("Remark")
    attendance_date = fields.Date(
        'Date', default=lambda self: fields.Date.today(),
        tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('start', 'Attendance Start'),
        ('done', 'Checked'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    attendance_line = fields.One2many('attendance.line', 'attendance_id', 'Attendance Line')

    def attendance_draft(self):
        self.state = 'draft'

    def attendance_start(self):
        self.state = 'start'

    def attendance_done(self):
        self.state = 'done'

    def attendance_cancel(self):
        self.state = 'cancel'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sheet = self.env['ir.sequence'].next_by_code('course.attendance')
            register = self.env['slide.channel'].browse(vals['spm']).id
            print(sheet)
            print(register)
            vals['name'] = str(register) + sheet
        return super(CourseAttendance, self).create(vals_list)
