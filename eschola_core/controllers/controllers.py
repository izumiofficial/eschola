# -*- coding: utf-8 -*-
# from odoo import http


# class EscholaCore(http.Controller):
#     @http.route('/eschola_core/eschola_core', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eschola_core/eschola_core/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eschola_core.listing', {
#             'root': '/eschola_core/eschola_core',
#             'objects': http.request.env['eschola_core.eschola_core'].search([]),
#         })

#     @http.route('/eschola_core/eschola_core/objects/<model("eschola_core.eschola_core"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eschola_core.object', {
#             'object': obj
#         })

