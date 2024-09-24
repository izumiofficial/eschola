from odoo import http
from odoo.http import request

class MyChildController(http.Controller):
    @http.route('/my/child', auth='user', website=True)
    def my_child(self):
        # Fetch the current user's guardian record
        guardian = request.env['guardian'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)

        if guardian:
            # Fetch children data based on the guardian record
            children = guardian.child_ids

            return request.render('eschola_core.website_my_child_template', {'children': children})
        else:
            # Handle the case where the user doesn't have a guardian record
            return request.render('http_routing.403')
