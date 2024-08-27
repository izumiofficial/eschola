# -*- coding: utf-8 -*-
# from odoo import http


# class Admission(http.Controller):
#     @http.route('/admission/admission', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/admission/admission/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('admission.listing', {
#             'root': '/admission/admission',
#             'objects': http.request.env['admission.admission'].search([]),
#         })

#     @http.route('/admission/admission/objects/<model("admission.admission"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('admission.object', {
#             'object': obj
#         })

