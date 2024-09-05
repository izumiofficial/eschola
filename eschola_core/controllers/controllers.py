# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request

class NewRegister(http.Controller):

    @http.route(['/register_form'], type='http', auth='public', website=True)
    def portal_register_form(self, **kw):
        countries = request.env['res.country'].sudo().search([])

        # render the form template when this route is accessed
        return request.render("eschola_core.register_form_template", {'countries': countries})

    @http.route('/submit_form', type='http', auth='public', website=True, csrf=False)
    def submit_register_form(self, **kw):
        # Data from JSON which contains applicant children basic information
        data = json.loads(kw['student_line_ids'])

        if request.httprequest.method == 'POST':
            # 1. Data Collection
            guardian_name = kw.get('guardian_name')
            email = kw.get('email')
            mobile = kw.get('mobile')
            country = kw.get('country')

            # 2. Basic Data Validation (Add more checks as needed)
            if not all([guardian_name, email, mobile, country]):
                return request.render("eschola_core.register_form_template", {'error_message': 'All fields are required.'})

            # 3. Process Children Data
            child_data = []
            for child in data:
                # Assuming 'child_name' and 'child_age' are fields in the 'childs_ids' one2many
                child_data.append((0, 0, {
                    'name': child.get('name'),
                    'email': child.get('email'),
                    'gender': child.get('gender'),
                    'grade': child.get('grade'),

                }))

            # 4. Create the admission record
            new_admission = request.env['admission.register'].sudo().create({
                'name': guardian_name,
                'primary_guardian_name': guardian_name,
                'email': email,
                'mobile': mobile,
                'country': country,
                'status': 'draft',
                'child_ids': child_data  # Link the child data to the admission record
            })

            # 5. Provide User Feedback
            return request.render("eschola_core.register_form_template",
                                  {'success_message': 'Registration successful!'})

        # If not a POST request, redirect back to the form
        return request.redirect('/register_form')
