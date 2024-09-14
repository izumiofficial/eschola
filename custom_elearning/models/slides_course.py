import webbrowser

from odoo import api,fields,models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class SlidesCourse(models.Model):
    _inherit = "slide.channel"

    external_link = fields.Char("External Link")

    instructor = fields.Many2many(comodel_name='res.partner', string='Instructor')
    course_date = fields.Date(string='Course Date')

    instructor_count = fields.Integer(compute='_compute_instructor_count')

    class_mode = fields.Selection([
        ('online', 'Online'),
        ('inperson', 'Face-to-face'),
        ('hybrid', 'Hybrid')
    ], string='Class Mode')

    course_ids = fields.One2many('elearning.class_timetable','course_id')

    def action_open_composer(self):
        if not self.instructor:
            raise UserError(_("There are no Instructor on these Course"))
        template_id = self.env['ir.model.data']._xmlid_to_res_id('custom_elearning.mail_template_slide_channel_invite_instructor', raise_if_not_found=False)
        # The mail is sent with datetime corresponding to the sending user TZ
        default_composition_mode = self.env.context.get('default_composition_mode', self.env.context.get('composition_mode', 'comment'))
        compose_ctx = dict(
            default_composition_mode=default_composition_mode,
            default_model='slide.channel',
            default_res_ids=self.ids,
            default_template_id=template_id,
            default_partner_ids=self.instructor.ids,
            mail_tz=self.env.user.tz,
        )
        return {
            'type': 'ir.actions.act_window',
            'name': _('Contact Instructor'),
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': compose_ctx,
        }

    @api.depends('instructor')
    def _compute_instructor_count(self):
        if self.instructor:
            self['instructor_count'] = len(self.instructor.ids)
        else:
            self['instructor_count'] = 0


class SlideSlide(models.Model):
    _inherit = 'slide.slide'

    survey_id = fields.Many2one('survey.survey', 'Certification')
