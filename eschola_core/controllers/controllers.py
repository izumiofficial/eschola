# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.exceptions import MissingError
import logging

_logger = logging.getLogger(__name__)


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
            salutation = kw.get('salutation')
            guardian_name = kw.get('guardian_name')
            email = kw.get('email')
            mobile = kw.get('mobile')
            country = kw.get('country')
            relation_to_student = kw.get('relation_to_student')
            salutation2 = kw.get('salutation2')
            secondary_guardian_name = kw.get('secondary_guardian_name')
            email2 = kw.get('email2')
            mobile2 = kw.get('mobile2')
            country2 = kw.get('country2')
            relation_to_student2 = kw.get('relation_to_student2')

            # 2. Basic Data Validation (Add more checks as needed)
            if not all([salutation, guardian_name, email, mobile, country, relation_to_student]):
                return request.render("eschola_core.register_form_template",
                                      {'error_message': 'All primary fields are required.'})

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
                'salutation': salutation,
                'primary_guardian_name': guardian_name,
                'email': email,
                'mobile': mobile,
                'country': country,
                'relation_to_student': relation_to_student,
                'salutation2': salutation2,
                'secondary_guardian_name': secondary_guardian_name,
                'email2': email2,
                'mobile2': mobile2,
                'country2': country2,
                'relation_to_student2': relation_to_student2,
                'status': 'payment',
                'child_ids': child_data  # Link the child data to the admission record
            })

            # Commit the transaction to ensure the admission record is saved
            request.env.cr.commit()
            guardian_category = request.env['res.partner.category'].sudo().search([('name', '=', 'Guardian')], limit=1)
            if not guardian_category:
                guardian_category = request.env['res.partner.category'].sudo().create({'name': 'Guardian'})

            # 5. Create guardian contact upon submit registration
            partner = request.env['res.partner'].sudo().create({
                'name': guardian_name,
                'email': email,
                'mobile': mobile,
                'country_id': int(country),
                'category_id': [(4, guardian_category.id)], # Many2many of tag
                'admission_register_id': new_admission.id,
            })

            print(partner)

            # 6. Give user portal access to guardian
            user = request.env['res.users'].sudo().create({
                'login': email,
                'partner_id': partner.id,
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
                'state': 'active',
            })

            try:
                template_id = request.env.ref('eschola_core.activation_email_template').id
                request.env['mail.template'].browse(template_id).sudo().send_mail(user.partner_id.id, force_send=True)
            except ValueError as e:  # Catch potential ValueError if the template ID is invalid
                _logger.error(f"Error sending activation email to guardian: {e}")
            except MissingError as e:  # Catch the MissingError if the partner record is not found
                _logger.error(f"Error sending activation email to guardian: {e}")

            student_category = request.env['res.partner.category'].sudo().search([('name', '=', 'Student')], limit=1)
            if not student_category:
                student_category = request.env['res.partner.category'].sudo().create({'name': 'Student'})

            # generate child account
            for child in new_admission.child_ids:
                child_partner = request.env['res.partner'].sudo().create({  # Use request.env
                    'name': child.name,
                    'email': child.email if child.email else None,
                    'category_id': [(4, student_category.id)], # Many2many of tag
                    # 'parent_id': partner.id,
                    'admission_register_id': new_admission.id,  # Link child to the admission record
                })

                # Update the child record with the newly created partner ID
                child.partner_id = child_partner.id

                print(child.partner_id)

                print(f"Child Partner's Admission Register ID: {child_partner.admission_register_id}")

                if child.email:
                    child_user = request.env['res.users'].sudo().create({  # Use request.env
                        'login': child.email,
                        'partner_id': child_partner.id,
                        'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])]
                    })

            # 7. Fetch the number of children
            num_children = len(new_admission.child_ids)

            print(num_children)

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
                })],
                'require_signature': False,
                'require_payment': True,
                'state': 'sent',
            })

            try:
                sale_order.action_quotation_send()
                print(f"Sale order email sent successfully for order {sale_order.id}")
            except Exception as e:
                print(f"Failed to send sale order email for order {sale_order.id}: {e}")

            # Set the order_id on the admission record
            new_admission.order_id = sale_order.id

            # Provide User Feedback
            return request.render("eschola_core.activation_email_sent",
                                  {'success_message': 'Registration successful!'})

        # If not a POST request, redirect back to the form
        return request.redirect('/register_form')
