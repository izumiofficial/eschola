# -*- coding: utf-8 -*-
# from odoo import http


# class PortalCustom(http.Controller):
#     @http.route('/portal_custom/portal_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/portal_custom/portal_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('portal_custom.listing', {
#             'root': '/portal_custom/portal_custom',
#             'objects': http.request.env['portal_custom.portal_custom'].search([]),
#         })

#     @http.route('/portal_custom/portal_custom/objects/<model("portal_custom.portal_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('portal_custom.object', {
#             'object': obj
#         })

