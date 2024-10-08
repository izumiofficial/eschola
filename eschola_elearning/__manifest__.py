# -*- coding: utf-8 -*-
{
    'name': "eSchola Custom eLearning",

    'summary': "The customization of eLearning app for eschola",

    'description': """
    """,

    'author': "Computs Sdn Bhd",
    'website': "https://www.computs.com.my",
    'sequence': -999,
    'application': True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_slides', 'calendar', 'mail', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menuitem.xml',
        'data/attendance_sheet_sequence.xml',
        'data/grading_sequence.xml',
        'views/school_year_views.xml',
        'views/term_views.xml',
        'views/slide_channel_views.xml',
        'views/session_views.xml',
        'views/timing_view.xml',
        'views/absent_type.xml',
        'views/assignments.xml',
        'views/grading_structure.xml',
        'views/grading_line.xml',
        'views/attendance_line_view.xml',
        'views/attendance_sheet_view.xml',
        'views/student_grading.xml',
        'views/grading.xml',
        'views/website_slides_templates_course.xml',
        'wizard/generate_timetable_view.xml',
        'wizard/session_confirmation.xml',
        'wizard/slide_channel_invite_views.xml',
    ],

    'assets': {
            'web.assets_frontend': [
                'eschola_elearning/static/src/css/templates_course.css'
            ],
            'web.assets_backend': [
                'eschola_elearning/static/src/views/calendar/*',
                'eschola_elearning/static/src/views/view_dialog/*'
            ],
        }
}

