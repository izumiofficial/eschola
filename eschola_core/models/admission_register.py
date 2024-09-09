from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

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
        ('activation', 'Activation'),
        ('payment', 'Payment'),
        ('paid', 'Paid'),
        ('placement', 'Placement'),
        ('cancel', 'Cancelled')
    ], default='draft', string='Status')

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

    def action_activate_account(self):
        # Assuming you have a method to send the activation email
        self.send_activation_email()
        self.status = 'activation'

    @api.model
    def _cron_check_activated_users(self):
        # Find users who have activated their accounts
        activated_users = self.env['res.users'].search([
            ('active', '=', True),
            ('partner_id.admission_register_id.status', '=', 'activation')
        ])

        # Change the status of corresponding admission records to 'payment'
        for user in activated_users:
            user.partner_id.admission_register_id.status = 'payment'

    @api.model
    def _cron_check_paid_admissions(self):
        """
        Cron job to check for admissions with 'paid' status and send "Placement Test"
        certification invitations to children.
        """
        paid_admissions = self.env['admission.register'].search([('status', '=', 'paid')])

        for admission in paid_admissions:
            for child in admission.child_ids:
                # Check if the child has a linked user
                if child.user_id:
                    # Find the "Placement Test" survey
                    placement_test = self.env['survey.survey'].sudo().search([('title', '=', 'Placement Test')], limit=1)
                    if placement_test:
                        # Trigger the invitation process
                        placement_test.invite_user(child.user_id.partner_id)
                    else:
                        _logger.warning(f"Placement Test survey not found for child {child.name}")
