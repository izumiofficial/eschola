# -*- coding: utf-8 -*-
{
    'name': 'External and Local Videos - eLearning Platform',
    'version': '1.0',
    'summary': 'Manage and publish local and external videos in elearning platform website_slides',
    'category': 'Website/Website',
    'description': """
Insert external videos
======================

Featuring

 * MP4 external videos
 * Livestreaming origin
 * Support local uploaded Videos (mp4)
""",
    'author': 'Josue Rodriguez - GAMA Recursos Tecnologicos (PERU)',
    'website': 'https://www.recursostecnologicos.pe',
    'depends': ['website_slides'],
    'data': [
        'views/slide_slide.xml',
        'views/res_config_settings.xml',
        'views/qweb.xml',
        ],
    'assets': {
        'web.assets_backend': [
        ],
        'web.assets_frontend': [
            '/elearning_external_videos/static/src/css/styles.scss',
            '/elearning_external_videos/static/src/js/clappr.min.js',
            '/elearning_external_videos/static/src/js/fullscreen_.js',
        ],
        'web.assets_tests': [
        ],
        'website.assets_editor': [
        ],
        'website_slides.slide_embed_assets': [
        ],
        'web.qunit_suite_tests': [
        ],
        'web.assets_qweb': [
        ],
        'web.assets_common': [
        ],
    },
    'demo': [
     ],
    'test': [],
    'images': ['images/main_screenshot.png','images/main_1.png', 'images/main_2.png'],
    'installable': True,
    'auto_install': True,
    'application': True,
    'price': 20.00,
    'currency': 'EUR',
    'license': 'OPL-1',
    'support': 'info@recursostecnologicos.pe',
}
