from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Admission(models.Model):
    _name = 'admission'
    _description = 'Admission of family'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Guardian Name', translate=True)
    email = fields.Char(string='Email', required=True)
    mobile = fields.Char(unaccent=False)
    country = fields.Many2one('res.country', string='Country of Residence')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')
    ])

    child_ids = fields.One2many('admission.child', 'admission_id', string="Student")

    def approve_admission(self):
        for admission in self:
            # Create student record
            student = self.env['student.record'].create({
                'name': admission.child_ids,
                # ... other student fields ...
            })

            # Handle primary guardian
            primary_guardian = self.env['guardian.guardian'].search([('name', '=', admission.primary_guardian_name)], limit=1)
            if not primary_guardian:
                primary_guardian = self.env['guardian.guardian'].create({
                    'name': admission.primary_guardian_name,
                    # ... other guardian fields ...
                })

            # Handle secondary guardian (if provided)
            secondary_guardian = None
            if admission.secondary_guardian_name:
                secondary_guardian = self.env['guardian.guardian'].search(
                    [('name', '=', admission.secondary_guardian_name)], limit=1)
                if not secondary_guardian:
                    secondary_guardian = self.env['guardian.guardian'].create({
                        'name': admission.secondary_guardian_name,
                        # ... other guardian fields ...
                    })

            # Link student to guardians
            student.write({
                'guardian_id': primary_guardian.id,
                'secondary_guardian_id': secondary_guardian.id if secondary_guardian else False
            })
