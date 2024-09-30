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

    is_parent = fields.Boolean("Is a Parent")
    is_student = fields.Boolean("Is a Student")
    contact_type = fields.Selection([
        ('primary_guardian', 'Primary Guardian'),
        ('secondary_guardian', 'Secondary Guardian'),
        ('teacher', 'Teacher'),
        ('spm', 'SPM'),
    ], string='Contact Type')

    user_type = fields.Selection([
        ('parent', 'Parent'),
        ('student', 'Student'),
    ], string='User Type')  # Make it computed and stored

    @api.onchange('user_type')
    def _onchange_user_type(self):
        if self.user_type == 'parent':
            self.is_parent = True
            self.is_student = False
        elif self.user_type == 'student':
            self.is_parent = False
            self.is_student = True
        else:
            self.is_parent = False
            self.is_student = False

    @api.onchange('is_parent')
    def _onchange_is_parent(self):
        if self.is_parent:
            self.is_student = False
            self.user_type = 'parent'

    @api.onchange('is_student')
    def _onchange_is_student(self):
        if self.is_student:
            self.is_parent = False
            self.user_type = 'student'


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
            })

            self._create_portal_user(student.partner_id.id, record.email)
            record.std_created = True

    def action_create_guardian(self):
        for record in self:
            guardian = record.env['guardian'].create({
                'name': record.name,
                'email': record.email,
                'mobile': record.mobile,
            })

            self._create_portal_user(guardian.partner_id.id, record.email)
            record.gdn_created = True
