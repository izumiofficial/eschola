import calendar
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import pytz

week_days = [(calendar.day_name[0], _(calendar.day_name[0])),
             (calendar.day_name[1], _(calendar.day_name[1])),
             (calendar.day_name[2], _(calendar.day_name[2])),
             (calendar.day_name[3], _(calendar.day_name[3])),
             (calendar.day_name[4], _(calendar.day_name[4])),
             (calendar.day_name[5], _(calendar.day_name[5])),
             (calendar.day_name[6], _(calendar.day_name[6]))]


class Session(models.Model):
    _name = "session"
    _inherit = ["mail.thread"]
    _description = "Session"

    course_id = fields.Many2one('slide.channel', string='Course')
    user_id = fields.Many2one('res.users', string='SPM', related='course_id.user_id')
    teacher_id = fields.Many2one('teacher', string='Teacher', related='course_id.teacher_id')
    term_id = fields.Many2one('term', string='Term', related='course_id.term_id')
    school_year_id = fields.Many2one('school.year', string='School Year', related='course_id.school_year_id')

    name = fields.Char(compute='_compute_name', string='Name', store=True)
    timing_id = fields.Many2one('op.timing', 'Timing', tracking=True)
    start_datetime = fields.Datetime('Start Time', required=True, default=lambda self: fields.Datetime.now())
    end_datetime = fields.Datetime('End Time', required=True)

    color = fields.Integer('Color Index')
    type = fields.Char(compute='_compute_day', string='Day', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('done', 'Done'), ('cancel', 'Canceled')],
        string='Status', default='draft')
    active = fields.Boolean(default=True)
    days = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')],
        'Days',
        group_expand='_expand_groups', store=True
    )
    timing = fields.Char(compute='_compute_timing')

    @api.depends('start_datetime', 'end_datetime')
    def _compute_timing(self):
        tz = pytz.timezone(self.env.user.tz)
        for session in self:
            session.timing = str(session.start_datetime.astimezone(tz).strftime('%I:%M%p')) + ' - ' + str(
                session.end_datetime.astimezone(tz).strftime('%I:%M%p'))

    @api.model
    def _expand_groups(self, days, domain, order):
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        return [day for day in weekdays if day in days]

    @api.depends('start_datetime')
    def _compute_day(self):
        days = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday', 6: 'sunday'}
        for record in self:
            record.type = days.get(record.start_datetime.weekday()).capitalize()
            record.days = days.get(record.start_datetime.weekday())

    @api.depends('course_id', 'start_datetime', 'end_datetime')
    def _compute_name(self):
        tz = pytz.timezone(self.env.user.tz)
        for session in self:
            if session.course_id \
                    and session.start_datetime and session.end_datetime:
                session.name = \
                    session.course_id.name + ' ' + str(
                        session.start_datetime.astimezone(tz).strftime('%I:%M%p')) + '-' + str(
                        session.end_datetime.astimezone(tz).strftime('%I:%M%p'))

    def lecture_draft(self):
        self.state = 'draft'

    def lecture_confirm(self):
        self.state = 'confirm'

    def lecture_done(self):
        self.state = 'done'

    def lecture_cancel(self):
        self.state = 'cancel'

    @api.constrains('start_datetime', 'end_datetime')
    def _check_date_time(self):
        if self.start_datetime > self.end_datetime:
            raise ValidationError(_(
                'End Time cannot be set before Start Time.'))

    @api.constrains('course_id', 'start_datetime', 'end_datetime')
    def check_timetable_fields(self):
        res_param = self.env['ir.config_parameter'].sudo()
        course_constraint = res_param.search([
            ('key', '=', 'timetable.is_course_constraint')])
        is_course_constraint = course_constraint.value
        sessions = self.env['session'].search([])
        for session in sessions:
            if self.id != session.id:
                if is_course_constraint:
                    if self.course_id.id == session.course_id.id and \
                            self.start_datetime.date() == session.start_datetime.date() and (
                            session.start_datetime.time() < self.start_datetime.time() < session.end_datetime.time() or
                            session.start_datetime.time() < self.end_datetime.time() < session.end_datetime.time() or
                            self.start_datetime.time() <= session.start_datetime.time() < self.end_datetime.time() or
                            self.start_datetime.time() < session.end_datetime.time() <= self.end_datetime.time()):
                        raise ValidationError(_(
                            'You cannot create a session'
                            ' with same course on same date '
                            'and time'))

    # @api.model_create_multi
    # def create(self, values):
    #     res = super(Session, self).create(values)
    #     mfids = res.message_follower_ids
    #     partner_val = []
    #     partner_ids = []
    #     for val in mfids:
    #         partner_val.append(val.partner_id.id)
    #     if res.teacher_id and res.teacher_id.user_id:
    #         partner_ids.append(res.teacher_id.user_id.partner_id.id)
    #     subtype_id = self.env['mail.message.subtype'].sudo().search([
    #         ('name', '=', 'Discussions')])
    #     if partner_ids and subtype_id:
    #         mail_followers = self.env['mail.followers'].sudo()
    #         for partner in list(set(partner_ids)):
    #             if partner in partner_val:
    #                 continue
    #             mail_followers.create({
    #                 'res_model': res._name,
    #                 'res_id': res.id,
    #                 'partner_id': partner,
    #                 'subtype_ids': [[6, 0, [subtype_id[0].id]]]
    #             })
    #     return res

    # @api.onchange('course_id')
    # def onchange_course(self):
    #     if self.course_id:
    #         subject_ids = self.env['op.course'].search([
    #             ('id', '=', self.course_id.id)]).subject_ids
    #         return {'domain': {'subject_id': [('id', 'in', subject_ids.ids)]}}

    # def write(self, vals):
    #     data = super(Session, self.with_context(check_move_validity=False)).write(vals)
    #     for session in self:
    #         if session.state not in ('draft', 'done'):
    #             session.notify_user()
    #     return data

    def action_attendance(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance',
            'res_model': 'course.attendance',
            'domain': [('channel_id', '=', self.course_id.id)],
            'view_mode': 'form',
            'target': 'current',
        }
