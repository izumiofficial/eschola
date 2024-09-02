# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class NewRegister(http.Controller):
    @http.route('/submit_register_form_for_love', type='http', auth='public', website=True, csrf=False)
    def submit_register_form(self, **post):
        print(**post)
        guardian_name = post.get('guardian_name')
        # secondary_guardian_name = post.get('secondary_guardian_name')
        email = post.get('email')
        mobile = post.get('mobile')
        country = post.get('country')
        print(f'{guardian_name}, {email}, {mobile}, {country}')
        # Create the admission record
        register = request.env['admission.register'].sudo().create({
            'name': guardian_name,
            'email': email,
            'mobile': mobile,
            'country': country,

        })


        # Create child records and link them to the admission.register
        # for child_data in post.get('children_data'):
        #     request.env['registered.child'].sudo().create({
        #         'name': child_data.get('name'),
        #         'admission_id': register.id,
        #     })

        # Redirect to a success page or display a message
        # return request.redirect('/admission_success')
        #
        # return request.render("admission_register.form_submission_success")  # Render a success template
