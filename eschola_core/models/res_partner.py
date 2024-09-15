from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    admission_register_id = fields.Many2one('admission.register', string="Admission Register")
    # is_activated = fields.Boolean(string='Is Activated', default=False)

    # gender = fields.Selection([
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    # ], string='Gender')

    std_created = fields.Boolean(string='Student Created', default=False)
    gdn_created = fields.Boolean(string='Guardian Created', default=False)

    def action_create_student(self):
        for record in self:
            record.env['student'].create({  # Assuming 'admission.application' is the model in admission.py
                'name': record.name,
                'email': record.email,
                'mobile': record.mobile,
                # 'gender': record.gender,
                'country': record.country.id,
            })

            user = record.env['res.users'].sudo().create({
                'login': record.email,
                'partner_id': record.partner.id,
                'groups_id': [(6, 0, [record.env.ref('base.group_portal').id])],
            })

            # set std_created to True
            record.std_created = True

    def action_create_guardian(self):
        for record in self:
            record.env['guardian'].create({  # Assuming 'admission.application' is the model in admission.py
                'name': record.name,
                'email': record.email,
                'mobile': record.mobile,
                'country': record.country.id,
            })

            user = record.env['res.users'].sudo().create({
                'login': record.email,
                'partner_id': record.partner.id,
                'groups_id': [(6, 0, [record.env.ref('base.group_portal').id])],
            })

            # set gdn_created to True
            record.gdn_created = True
