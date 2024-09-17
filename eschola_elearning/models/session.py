from odoo import api, fields, models


class Session(models.Model):
    _name = "session"
    _description = "Session"

    name = fields.Char(string='Name')
    start_datetime = fields.Datetime(string='Start Date')
    end_datetime = fields.Datetime(string='End Date')
    course_id = fields.Many2one('slide.channel', string='Course')
