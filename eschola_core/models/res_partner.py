from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    admission_register_id = fields.Many2one('admission.register', string="Admission Register")

    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
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

    student_ids = fields.One2many('student', 'partner_id', string="Students")

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
        try:
            return self.env['res.users'].sudo().create({
                'login': email,
                'partner_id': partner_id,
                'groups_id': [(6, 0, [self.env['ir.model.data'].xmlid_to_res_id('base.group_portal')])],
                # 'password': 'your_default_password'  # If you want to set a default password
            })
        except Exception as e:
            # Handle the exception, e.g., log the error or show a warning message
            print(f"Error creating portal user: {e}")

    def action_create_student(self):
        for record in self:
            student = record.env['student'].create({
                'name': record.name,
                'email': record.email,
                'mobile': record.mobile,
                'gender': record.gender,
                'student_img': record.image_1920,
                'partner_id': record.id # create linked partner id to student model
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

    @api.onchange('name')
    def _update_name(self):
        # if name in student is change, name in student_ids also change/updated
        for record in self:
            if record.student_ids:
                record.student_ids.write({'name': record.name})

    @api.onchange('country')
    def _update_country(self):
        # if name in country is change, country in student_ids also change/updated
        for record in self:
            for student in record.student_ids:
                student.country = record.country_id

    @api.onchange('email')
    def _update_email(self):
        # if name in email is change, email in student_ids also change/updated
        for record in self:
            for student in record.student_ids:
                student.email = record.email

    @api.onchange('mobile')
    def _update_mobile(self):
        # if name in mobile is change, mobile in student_ids also change/updated
        for record in self:
            if record.student_ids:
                record.student_ids.write({'mobile': record.mobile})

    @api.onchange('gender')
    def _update_gender(self):
        # if name in gender is change, gender in student_ids also change/updated
        for record in self:
            for student in record.student_ids:
                student.gender = record.gender

    @api.onchange('image_1920')
    def _update_image(self):
        # if picture is change, picture in res.partner also change
        for record in self:
            for student in record.student_ids:
                student.student_img = record.image_1920
