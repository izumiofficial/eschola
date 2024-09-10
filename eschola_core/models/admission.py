from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.exceptions import UserError


class Admission(models.Model):
    _name = 'admission'
    _description = 'Admission Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Student Name', translate=True)
    email = fields.Char(string='Email')
    mobile = fields.Char(unaccent=False)
    country = fields.Many2one('res.country', string='Country of Residence')
    grade = fields.Selection([
        ('grade_7', 'Grade 7'),
        ('grade_8', 'Grade 8'),
        ('grade_9', 'Grade 9'),
        ('grade_10', 'Grade 10'),
        ('al_as', 'AL/AS')
    ], string='Grade')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female')
    ], string='Gender', default='m')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Placement'),
        ('cancel', 'Failed')
    ], default='draft', string='Status')
    primary_guardian_id = fields.Many2one('guardian', string="Primary Guardian")

    # placement_test_id = fields.Many2one('survey.user_inputput', string="Student's Certificate")

    # def action_view_certificate(self):
    #     self.ensure_one()
    #     placement_test = self.env['survey.survey'].sudo().search([('title', '=', 'Placement Test')], limit=1)
    #
    #     if not self.placement_test_id:
    #         raise UserError("No Certificate is linked to this admission record.")
    #
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'survey.survey',
    #         'views': [[False, 'form']],
    #         'res_id': self.placement_test_id.id,
    #     }
