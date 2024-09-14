import base64

from markupsafe import Markup

from odoo import api,fields,models
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta
import qrcode
from io import BytesIO
from odoo.tools.translate import _

class ClassTimetable(models.Model):
    _name = 'elearning.class_timetable'
    _description = 'E-learning Class Timetable'

    name = fields.Char(string='Name', required=True)
    day_of_weeks = fields.Char(string='Day of Week', compute='_compute_day_of_week', store=True)
    date_field = fields.Datetime(string='Date')
    date_end = fields.Datetime(string='Date end')
    time_start = fields.Float(string='Start Time')
    time_end = fields.Float(string='End Time')
    duration = fields.Float(string='Duration (hours)', compute='_compute_duration')
    course_id = fields.Many2one('slide.channel', string='Course')

    #QR Code
    qr_code = fields.Binary(string='Qr Code')

    #for debugging purpose
    # the_link = fields.Char(string="The link")

    class_mode = fields.Selection([
        ('live', 'In Person'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid')
    ], string='Class Mode', related='course_id.class_mode')

    # instructor_related = fields.One2many('slide.channel', related='instructor', string='Instructor', readonly=True)

    class_link = fields.Char(string='Class Link')

    record_count = fields.Integer('Record Count', compute='_compute_record_count')

    @api.depends('date_field', 'date_end')
    def _compute_duration(self):
        for record in self:
            if record.date_field and record.date_end:
                # Calculate duration
                duration = (record.date_end - record.date_field).total_seconds() / 3600
                record.duration = duration
            else:
                record.duration = 0.0

    @api.depends('date_field')
    def _compute_day_of_week(self):
        for record in self:
            if record.date_field:
                # Ensure that date_field is a string before using strptime
                date_string = fields.Date.to_string(record.date_field)

                # Convert the date string to a datetime object
                date_object = datetime.strptime(date_string, "%Y-%m-%d")

                # Get the day of the week as a string (e.g., 'Monday')
                day_of_weeks = date_object.strftime('%A')

                # Update the computed field
                record.day_of_weeks = day_of_weeks
            else:
                record.day_of_weeks = False


    # @api.depends('time_start', 'time_end')
    # def _compute_duration(self):
    #     for record in self:
    #         if record.time_start and record.time_end:
    #             # Calculate the duration in hours
    #             record['duration'] = record.time_end - record.time_start
    #         else:
    #             record['duration'] = 0.0

    @api.onchange('date_field', 'date_end')
    def update_time(self):
        for record in self:
            if record.date_field and record.date_end:
                record['time_start'] = float(record.date_field.time().strftime('%H%M%S'))
                record['time_end'] = float(record.date_end.time().strftime('%H%M%S'))
            else:
                record['time_start'] = 0
                record['time_end'] = 0

    def _compute_record_count(self):
        for record in self:
            record_count = record.env['class.attendance'].search_count([('class_id', '=', record.id)])
            record.record_count = record_count
    def action_attendance(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance',
            'res_model': 'class.attendance',
            'domain': [('class_id', '=', self.id)],
            'view_mode': 'tree',
            'target': 'current',
            'context': {'default_class_id': self.id}
        }

    def generate_qr_code(self):
        for record in self:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            system_web_url = self.env['ir.config_parameter'].get_param('web.base.url', '')
            class_name = record.name
            decap_name = str(class_name).lower().replace(" ", "-")
            qr.add_data(f'{system_web_url}/classes/{decap_name}-{record.id}')
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer)
            qr_code_image = buffer.getvalue()

            record.qr_code = base64.b64encode(qr_code_image)
            # print(f'{system_web_url}/classes/{decap_name}-{record.id}')

class AttendeeRelation(models.Model):
    _name = 'class.attendance'
    _rec_name = 'class_id'

    class_id = fields.Many2one('elearning.class_timetable', string='Class', index=True, required=True, ondelete='cascade')
    attendance_status = fields.Selection([
        ('attend', 'Attend'),
        ('absent', 'Absent'),
        ('joined', 'Joined')
    ], string='Attendance', default='joined')
    partner_id = fields.Many2one('res.partner', index=True, required=True, ondelete='cascade')
    partner_email = fields.Char(related='partner_id.email', readonly=True)
    date = fields.Datetime(string='Date')

    def action_open_composer(self):
        if not self.partner_id:
            raise UserError(_("There are no Instructor on these Course"))
        template_id = self.env['ir.model.data']._xmlid_to_res_id('custom_elearning.mail_template_slide_channel_invite_attendee_class', raise_if_not_found=False)
        # The mail is sent with datetime corresponding to the sending user TZ
        default_composition_mode = self.env.context.get('default_composition_mode', self.env.context.get('composition_mode', 'comment'))
        compose_ctx = dict(
            default_composition_mode=default_composition_mode,
            default_model='class.attendance',
            default_res_ids=self.ids,
            default_template_id=template_id,
            default_partner_ids=self.partner_id.ids,
            mail_tz=self.env.user.tz,
        )
        return {
            'type': 'ir.actions.act_window',
            'name': _('Class Invitation'),
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': compose_ctx,
        }