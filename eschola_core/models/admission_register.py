from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AdmissionRegister(models.Model):
    _name = 'admission.register'
    _description = 'Admission of family'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', translate=True)
    # secondary_guardian_name = fields.Char(string="Secondary Guardian Name")

    primary_guardian_name = fields.Char(string='Primary Guardian Name')
    email = fields.Char(string='Email')
    mobile = fields.Char(unaccent=False)
    country = fields.Many2one('res.country', string='Country of Residence')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')
    ])

    child_ids = fields.One2many('registered.child', 'admission_id', string="Student")
    primary_guardian_id = fields.Many2one('guardian', string="Primary Guardian")

    @api.onchange('primary_guardian_name')
    def _set_name(self):
        for record in self:
            record['name'] = record.primary_guardian_name or False

    def pay_admission(self):
        # move stage to 'paid'
        self.status = 'paid'


    def admission_confirm(self):

        # create guardian
        self['primary_guardian_id'] = self.env['guardian'].create({
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'country': self.country.id,
        })

        partner = self.env['res.partner'].create({
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'country_id': self.country.id
        })

        # Create a portal user for the new contact
        user = self.env['res.users'].create({
            'login': self.email,  # Or any other suitable login
            'partner_id': partner.id,
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]  # Add to the Portal user group
        })

        # child_ids will be separated and put in another model called admission.py
        for child in self.child_ids:
            # Extract the required child information
            name = child.name
            email = child.email
            gender = child.gender
            grade = child.grade

            # Create a new record in the 'admission.py' model
            self.env['admission'].create({  # Assuming 'admission.application' is the model in admission.py
                'name': name,
                'email': email,
                'gender': gender,
                'grade': grade,
                'status': 'draft',
                'country': self.country.id,  # Get country field from the guardian
                'primary_guardian_id': self.primary_guardian_id.id,
                # ... Add other child-related fields as needed
            })

        # Update the 'admission_id' field for each child
        self.child_ids.write({'admission_id': self.id})

        # Update the status of the admission register to 'confirm'
        self.status = 'confirm'
