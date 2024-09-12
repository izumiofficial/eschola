from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class AdmissionRegister(models.Model):
    _name = 'admission.register'
    _description = 'Admission of family'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', translate=True)
    secondary_guardian_name = fields.Char(string="Secondary Guardian Name")
    salutation = fields.Selection([
        ('mr', 'Mr.'),
        ('ms', 'Ms.'),
        ('mrs', 'Mrs'),
    ], string='Title')
    relation_to_student = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ], string='Relation to Student')
    primary_guardian_name = fields.Char(string='Primary Guardian Name')
    email = fields.Char(string='Email')
    mobile = fields.Char(unaccent=False)
    country = fields.Many2one('res.country', string='Country of Residence')

    # 2nd guardian
    salutation2 = fields.Selection([
        ('mr', 'Mr.'),
        ('ms', 'Ms.'),
        ('mrs', 'Mrs'),
    ], string='Title')
    relation_to_student2 = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ], string='Relation to Student')
    email2 = fields.Char(string='Email')
    mobile2 = fields.Char(unaccent=False)
    country2 = fields.Many2one('res.country', string='Country of Residence')

    status = fields.Selection([
        ('draft', 'Draft'),
        # ('activation', 'Activation'),
        ('payment', 'Payment'),
        ('paid', 'Paid'),
        # ('placement', 'Placement'),
        ('cancel', 'Cancelled')
    ], default='draft', compute='_compute_status', store=True, string='Status')

    child_ids = fields.One2many('registered.child', 'admission_id', string="Student")
    primary_guardian_id = fields.Many2one('guardian', string="Primary Guardian")

    order_id = fields.Many2one('sale.order', string='Sales Order')
    # sale_order_id = fields.Many2one('sale.order', 'Sale Order')

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

    def action_view_sale_order(self):
        self.ensure_one()  # Ensure only one record is being processed

        if not self.order_id:
            # Handle the case where no sale order is linked yet
            # You might want to create a new sale order or provide a way to select an existing one
            raise UserError("No Sale Order is linked to this admission record.")

        # Check the sale order's state and update the admission register status if necessary
        # if self.order_id.state == 'sale' and self.status == 'payment':
        #     self.status = 'paid'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'views': [[False, 'form']],  # Open the sale order in form view
            'res_id': self.order_id.id,  # ID of the linked sale order
        }

    @api.depends('order_id.state')
    def _compute_status(self):
        for record in self:
            if record.order_id and record.order_id.state == 'sale':
                record.status = 'paid'
                record.send_cert()
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

                    # Create a new record in the 'student.py' model
                    self.env['student'].create({  # Assuming 'admission.application' is the model in admission.py
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


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('state')
    def _onchange_state(self):
        for record in self:
            if record.state == 'sale':
                admission_registers = record.env['admission.register'].search([('order_id', '=', record.id)])
                for register in admission_registers:
                    register.status = 'paid'
                    print(admission_registers)
                    print(f"Updated admission register {register.id} status to 'paid'")
            else:
                # log error
                print(f"Sale Order {record.id} - Not in 'sale' state. Current order state: {record.state}")
