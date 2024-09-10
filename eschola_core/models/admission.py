from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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
        ('cancel', 'Cancelled')
    ], default='draft', string='Status')
    primary_guardian_id = fields.Many2one('guardian', string="Primary Guardian")

    def confirm_admission(self):
        # Find the corresponding registered.child record
        child = self.env['admission.register'].search([('child_ids', 'in', self.id)])

        if child:  # Ensure a child record was found
            # Create a new record in the 'student.py' model
            self.env['student'].create({
                'name': self.name,
                'email': self.email,
                'mobile': self.mobile,
                'country': self.country.id,
                'grade': self.grade,
                'gender': self.gender,
                'primary_guardian_id': child.primary_guardian_id.id,  # Link to the guardian through the child record
                # ... Add other necessary fields from the admission model
            })

            # Update the admission status to 'confirm'
            self.status = 'confirm'
