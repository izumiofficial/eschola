from odoo import api, fields, models


class Channel(models.Model):
    _inherit = "slide.channel"

    teacher_id = fields.Many2one('teacher', string='Teacher')
    term_id = fields.Many2one('term', string='Term')
    school_year_id = fields.Many2one('school.year', string='School Year', related='term_id.school_year_id')
    start_date = fields.Date(string='Start Date', related='term_id.start_date')
    end_date = fields.Date(string='End Date', related='term_id.end_date')

    session_ids = fields.One2many('session', 'course_id', string='Sessions')
