# -*- coding: utf-8 -*-
# from odoo import http


# class Guardian(http.Controller):
#     @http.route('/guardian/guardian', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/guardian/guardian/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('guardian.listing', {
#             'root': '/guardian/guardian',
#             'objects': http.request.env['guardian.guardian'].search([]),
#         })

#     @http.route('/guardian/guardian/objects/<model("guardian.guardian"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('guardian.object', {
#             'object': obj
#         })

