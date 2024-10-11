from odoo import api, fields, models

class AttendanceReport(models.Model):
    _name = 'attendance.report'
    _description = 'Attendance Report'

    name = fields.Char(string='Name')
