from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import datetime, date, timedelta
from odoo.addons.website_slides.controllers.main import WebsiteSlides

class Portal(CustomerPortal):

    @http.route(['/view_class_list_izlan'], type='http', auth="user", website=True)
    def portal_class_list(self, **kw):
        class_list = request.env['elearning.class_timetable'].search([])

        vals = {
            'class_list': class_list,
            'page_name': 'class_portal_list'
        }
        return request.render("custom_elearning.class_portal_list", vals)

    @http.route(['/classes/<model("elearning.class_timetable"):id>'], type='http', auth='user', website=True)
    def class_list_view_portal(self, id, **kw):
        vals = {
            'class_id': id,
            'page_name': 'attendance_check_in_button'
        }
        return request.render('custom_elearning.attendance_check_in_button', vals)

    @http.route(['/classes/joined/<model("elearning.class_timetable"):id>'], type='http', auth='user', website=True)
    def attendance_check_in(self, id):
        partner_id = request.env.user.partner_id.id
        attendance_model = request.env['class.attendance'].search([('class_id','=',id.id),('partner_id','=',partner_id)], limit=1)

        if attendance_model:
            if attendance_model.attendance_status != 'attend':
                attendance_model.write({
                    'date':datetime.today(),
                    'attendance_status':'attend'
                })
                # print(,attendance_model,partner_id,attendance_model.attendance_status)

                return request.render('custom_elearning.attendance_attend')
            else:
                return request.render('custom_elearning.attendance_not_attend_2')
        else:
            return request.render('custom_elearning.attendance_not_attend_1')

class WebsiteSlidesInherit(WebsiteSlides):
    @http.route('/slides', type='http', auth="user", website=True, sitemap=True)
    def slides_channel_home(self, **post):
        res = super(WebsiteSlidesInherit, self).slides_channel_home(**post)
        return res
