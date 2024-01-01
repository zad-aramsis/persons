{
    'name': "persons",
    'summary': """
        Custom Model Of Person For APIs and Portal
        """,
    'version': '16.0',
    'category': 'Portal',
    'author': 'Abanob Ashraf',
    'website': "http://zadsolutions.com",
    'depends': ['base', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'views/portal_views.xml',
        'views/person_details_views.xml',
        'views/templates.xml',
        'report/person_report_template.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets':
        {'web.assets_frontend': ['persons/static/src/js/new_parson_validation.js']}
}
