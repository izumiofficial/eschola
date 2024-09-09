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

    order_id = fields.Many2one('sale.order', string='Sales Order')

    @api.onchange('primary_guardian_name')
    def _set_name(self):
        for record in self:
            record['name'] = record.primary_guardian_name or False

    def pay_admission(self):
        # move stage to 'paid'
        self.status = 'paid'

    def send_cert(self):
        placement_test = self.env['survey.survey'].sudo().search([('title', '=', 'Placement Test')], limit=1)

        if not placement_test:
            _logger.warning("Placement Test survey not found")
            return  # Exit early if the survey doesn't exist

        for child in self.child_ids:
            if child.partner_id:  # Check if partner_id exists
                self.env['survey.user_input'].create({
                    'survey_id': placement_test.id,  # Use the survey ID
                    'partner_id': child.partner_id.id,
                    'email': child.email,
                })


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
        # self.status = 'confirm'

    def action_activate_account(self):
        # Assuming you have a method to send the activation email
        self.send_activation_email()
        self.status = 'activation'

    @api.model
    def _cron_check_activated_users(self):
        """
        Cron job to check for users with active accounts and update the admission status to 'payment'.
        """
        # Find users who are active and whose admission is in 'activation' state
        activated_users = self.env['res.users'].search([
            ('state', '=', 'active'),
            ('partner_id.admission_register_id.status', '=', 'activation')
        ])

        # Change the status of corresponding admission records to 'payment'
        for user in activated_users:
            user.partner_id.admission_register_id.status = 'payment'

    # is SO state is sale, status change to paid
    # @api.depends('order_id')
    # def _onchange_order_id(self):
    #     for record in self:
    #         if record.order_id and record.order_id.state == 'sale':
    #             record.status = 'paid'

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'sale':
            admission_registers = self.env['admission.register'].search([('order_id', '=', self.id)])
            for register in admission_registers:
                register.status = 'paid'
                print(admission_registers)
                print(f"Updated admission register {register.id} status to 'paid'")
        else:
            # log error (optional, depending on your needs)
            print(f"Sale Order {self.id} - Not in 'sale' state. Current order state: {self.state}")
