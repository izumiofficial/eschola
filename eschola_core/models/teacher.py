from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Teacher(models.Model):
    _name = 'teacher'
    _description = 'Eschola Teachers'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete="cascade")
    name = fields.Char('Name', required=True)
    email = fields.Char(string='Email')
    mobile = fields.Char(unaccent=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], 'Gender')
    nationality = fields.Many2one('res.country', 'Nationality')
    emp_id = fields.Many2one('hr.employee', 'HR Employee')
    active = fields.Boolean(default=True)

    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'gender': record.gender,
                'private_state_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'partner_share': True, 'employee': True})
