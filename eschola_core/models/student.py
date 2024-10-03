from odoo import models, fields, api, _
from odoo.osv import expression

class Student(models.Model):
    _name = 'student'
    _description = 'Student'
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
    student_grades = fields.Many2one('student.grades', string='Student Grade')
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

    slide_channel_ids = fields.Many2many(
        'slide.channel', string='eLearning Courses',
        compute='_compute_slide_channel_values',
        search='_search_slide_channel_ids',
        groups="website_slides.group_website_slides_officer")
    slide_channel_count = fields.Integer(
        'Course Count', compute='_compute_slide_channel_values',
        groups="website_slides.group_website_slides_officer")

    student_img = fields.Image(string='Student Image')

    def create_contact(self):
        # Create a new contact (res.partner)
        partner = self.env['res.partner'].create({
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'country_id': self.country.id,
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
        action = self.env["ir.actions.actions"]._for_xml_id("website_slides.slide_channel_partner_action")
        action['display_name'] = _('Courses')
        action['domain'] = [('member_status', '!=', 'invited')]
        if len(self) == 1:
            action['context'] = {'search_default_partner_id': self.partner_id.id}
        else:
            action['domain'] = expression.AND([action['domain'], [('partner_id', 'in', self.partner_id.ids)]])
        return action

    @api.onchange('name')
    def _update_name(self):
        # if name in student is change, name in res.partner also change/updated
        for record in self:
            if record.partner_id:
                record.partner_id.name = record.name

    @api.onchange('country')
    def _update_country(self):
        # if name in country is change, country in res.partner also change/updated
        for record in self:
            if record.partner_id:
                record.partner_id.country_id = record.country

    @api.onchange('email')
    def _update_email(self):
        # if name in email is change, email in res.partner also change/updated
        for record in self:
            if record.partner_id:
                record.partner_id.email = record.email

    @api.onchange('mobile')
    def _update_mobile(self):
        # if name in mobile is change, mobile in res.partner also change/updated
        for record in self:
            if record.partner_id:
                record.partner_id.mobile = record.mobile

    @api.onchange('gender')
    def _update_gender(self):
        # if name in gender is change, gender in res.partner also change/updated
        for record in self:
            if record.partner_id:
                record.partner_id.gender = record.gender

    @api.onchange('student_img')
    def _update_image(self):
        # if picture is change, picture in res.partner also change
        for record in self:
            if record.partner_id:
                record.partner_id.image_1920 = record.student_img

