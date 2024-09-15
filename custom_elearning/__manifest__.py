# -*- coding: utf-8 -*-
{
    'name': "custom_elearning",

    'summary': "Tailored Odoo e-learning model for personalized educational experiences.",

    'description': """
Our custom Odoo e-learning model is meticulously crafted to meet the unique needs of your organization, offering a comprehensive and personalized educational experience. From customizable course content and user-friendly interfaces to advanced tracking and reporting features, our solution seamlessly integrates with Odoo, providing a tailored platform that fosters efficient learning management. Empower your team or community with a flexible and scalable e-learning environment designed to optimize engagement, knowledge retention, and overall training effectiveness. With our customized Odoo e-learning model, unlock the full potential of education tailored to your specific requirements, ensuring a dynamic and impactful learning journey for every participant.
    """,

    'author': "Computs Sdn Bhd",
    'website': "https://www.computs.com.my",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'E-learning',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_slides', 'calendar', 'website', 'portal', 'contacts','website_forum'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menuitem.xml',
        'views/slides_course.xml',
        'views/res_partner.xml',
        'views/class_timetable_views.xml',
        'views/portal_extend.xml',
        'views/attendance_relation_views.xml',
        'views/templates.xml',
        'views/attendance_check_in.xml',
        'data/mail_template_data.xml',
        'reports/certification_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
