# -*- coding: utf-8 -*-
{
    'name': "eSchola Core",

    'summary': "The core app for eschola",

    'description': """
This core app contains all custom modules for eschola. it will install several app which (admission, guardian and student) is the main app to be install
    """,

    'author': "Computs Sdn Bhd",
    'website': "http://www.computs.com.my",
    'sequence': -999,
    'application': True,
    'category': 'Website',
    'version': '1.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menuitem.xml',
        # 'views/admission.xml',
        'views/admission_register.xml',
        'views/guardian.xml',
        'views/student.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

