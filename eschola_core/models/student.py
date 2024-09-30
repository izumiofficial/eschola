from odoo import models, fields, api

class Student(models.Model):
    _name = 'student'
    _description = 'To store student records'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    is_international = fields.Boolean(string='International Curriculum')
    partner_id = fields.Many2one('res.partner', string="Partner")
    name = fields.Char(string='Name', translate=True)
    email = fields.Char(string='Email')
    mobile = fields.Char(unaccent=False)
    birth_date = fields.Date(string='Birth Date')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female')
    ], string='Gender', default='m')
    grade = fields.Selection([
        ('grade_7', 'Grade 7'),
        ('grade_8', 'Grade 8'),
        ('grade_9', 'Grade 9'),
        ('grade_10', 'Grade 10'),
        ('al_as', 'AL/AS')
    ], string='Grade')
    nationality = fields.Many2one('res.country', string='Nationality')
    country = fields.Many2one('res.country', string='Country of Residence')
    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('christian', 'Christian')
    ], string='Religion')

    primary_guardian_id = fields.Many2one('guardian', string="Primary Guardian")
    secondary_guardian_id = fields.Many2one('guardian', string="Secondary Guardian")

    course_id = fields.Many2one('slide.channel', string='Course')

    def create_contact(self):
        # Create a new contact (res.partner)
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

        # update the admission status to 'confirm'
        self.status = 'confirm'

    def action_view_course(self):
        # smart button function to view course taken from slide.channel.partner
        self.ensure_one()  # Ensure only one record is being processed

        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'slide.channel',  # Model to open
            'res_id': self.course_id.id,  # ID of the specific record
            'view_mode': 'form',  # Open in form view
            'target': 'current',  # Open in the same window
        }

        return action
