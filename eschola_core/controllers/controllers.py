# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


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
                return request.render("eschola_core.register_form_template",
                                      {'error_message': 'All fields are required.'})

            # 3. Process Children Data
            child_data = []
            for child in data:
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
                'status': 'activation',
                'child_ids': child_data  # Link the child data to the admission record
            })

            # 5. Create guardian contact upon submit registration
            partner = request.env['res.partner'].create({
                'name': guardian_name,
                'email': email,
                'mobile': mobile,
                'country_id': int(country),
                'admission_register_id': new_admission.id,
            })

            # 6. Give user portal access to guardian
            user = request.env['res.users'].create({
                'login': email,
                'partner_id': partner.id,
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])]
            })

            print(user.partner_id)
            print(user.partner_id.admission_register_id)

            # Send the activation email to the guardian
            template_id = request.env.ref('eschola_core.activation_email_template').id
            request.env['mail.template'].browse(template_id).send_mail(user.partner_id.id, force_send=True)

            # generate child account
            for child in new_admission.child_ids:
                child_partner = request.env['res.partner'].create({  # Use request.env
                    'name': child.name,
                    'email': child.email if child.email else None,
                    'parent_id': partner.id,
                    'admission_register_id': new_admission.id,  # Link child to the admission record
                })

                if child.email:
                    child_user = request.env['res.users'].create({  # Use request.env
                        'login': child.email,
                        'partner_id': child_partner.id,
                        'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])]
                    })

                    # Send activation email to the child
                    if child_user:
                        request.env['mail.template'].browse(template_id).send_mail(child_user.partner_id.id, force_send=True)

            # 7. Fetch the number of children
            num_children = len(new_admission.child_ids)

            # 8. Get the product ID based on the product name
            product = request.env['product.product'].sudo().search([('name', '=', 'Placement Test')], limit=1)
            if not product:
                return request.render("eschola_core.register_form_template",
                                      {'error_message': 'Product "Placement Test" not found.'})

            # 9. Create the sales order
            sale_order = request.env['sale.order'].sudo().create({
                'partner_id': partner.id,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': num_children,
                    'price_unit': product.list_price,
                })]
            })

            # Provide User Feedback
            return request.render("eschola_core.activation_email_sent",
                                  {'success_message': 'Registration successful!'})

        # If not a POST request, redirect back to the form
        return request.redirect('/register_form')
