from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    admission_register_id = fields.Many2one('admission.register', string="Admission Register")

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')

    std_created = fields.Boolean(string='Student Created', default=False)
    gdn_created = fields.Boolean(string='Guardian Created', default=False)
    flak = fields.Char(string='FLAK')

    def _create_portal_user(self, partner_id, email):
        """Helper function to create a portal user."""
        return self.env['res.users'].sudo().create({
            'login': email,
            'partner_id': partner_id,
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
        })

    def action_create_student(self):
        for record in self:
            student = record.env['student'].create({
                'name': record.name,
                'email': record.email,
                'mobile': record.mobile,
                'gender': record.gender,
                'country': record.country.id,
            })

            self._create_portal_user(student.partner_id.id, record.email)
            record.std_created = True

    def action_create_guardian(self):
        for record in self:
            guardian = record.env['guardian'].create({
                'name': record.name,
                'email': record.email,
                'mobile': record.mobile,
                'country': record.country.id,
            })

            self._create_portal_user(guardian.partner_id.id, record.email)
            record.gdn_created = True
