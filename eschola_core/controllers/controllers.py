# -*- coding: utf-8 -*-
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
        data = json.loads(kw['student_line_ids'])
        for i in data:
            print(i)


        if request.httprequest.method == 'POST':
            # 1. Data Collection
            guardian_name = kw.get('guardian_name')
            email = kw.get('email')
            mobile = kw.get('mobile')
            country = kw.get('country')

            # 2. Basic Data Validation (Add more checks as needed)
            if not all([guardian_name, email, mobile, country]):
                return request.render("eschola_core.register_form_template",
                                      {'error_message': 'All fields are required.'})

            # 3. Create the admission record
            request.env['admission.register'].sudo().create({
                'name': guardian_name,
                'email': email,
                'mobile': mobile,
                'country': country,
            })

            # 4. Provide User Feedback
            return request.render("eschola_core.register_form_template",
                                  {'success_message': 'Registration successful!'})

        # If not a POST request, redirect back to the form
        return request.redirect('/register_form')


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
