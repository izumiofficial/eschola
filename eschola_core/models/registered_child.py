from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RegisteredChild(models.Model):
    _name = 'registered.child'
    _description = 'Dynamically admin the kids'

    is_international = fields.Boolean(string='International Curriculum')
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
    admission_id = fields.Many2one('admission.register', string="Register ID")
    partner_id = fields.Many2one('res.partner', string="Contact")  # New field to link to the contact

    @api.model
    def create(self, vals):
        # Check if partner_id is provided in vals, if not, create a new partner
        if not vals.get('partner_id'):
            partner_vals = {
                'name': vals.get('name'),
                'email': vals.get('email'),
                'mobile': vals.get('mobile'),
            }
            partner = self.env['res.partner'].create(partner_vals)
            vals['partner_id'] = partner.id

        return super(RegisteredChild, self).create(vals)