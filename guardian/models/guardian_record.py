from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GuardianRecord(models.Model):
    _name = "guardian.record"
    _description = "Parent"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', translate=True)
    email = fields.Char(string='Email', required=True)
    mobile = fields.Char(unaccent=False)
    country = fields.Many2one('res.country', string='Country of Residence')

    student_ids = fields.One2many('student.record', string='Child')

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(GuardianRecord, self).create(vals_list)
    #     for vals in vals_list:
    #         if vals.get('student_ids', False) and res.name.user_id:
    #             student_ids = self.student_ids.browse(res.student_ids.ids)
    #             user_ids = [student_id.user_id.id for student_id in student_ids if student_id.user_id]
    #             res.user_id.child_ids = [(6, 0, user_ids)]
    #     return res
    #
    # def write(self, vals):
    #     for rec in self:
    #         res = super(GuardianRecord, self).write(vals)
    #         if vals.get('student_ids', False) and rec.name.user_id:
    #             student_ids = rec.student_ids.browse(rec.student_ids.ids)
    #             usr_ids = [student_id.user_id.id for student_id in student_ids if student_id.user_id]
    #             rec.user_id.child_ids = [(6, 0, usr_ids)]
    #         rec.env.registry.clear_cache()
    #         return res
    #
    # def unlink(self):
    #     for record in self:
    #         if record.name.user_id:
    #             record.user_id.child_ids = [(6, 0, [])]
    #         return super(GuardianRecord, self).unlink()
