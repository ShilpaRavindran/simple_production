{
    'name': 'Simple Production',
    'version': '14.0.1.0.0',
    'sequence': -201,
    'summary': '',
    'description': "Simple Production",
    'depends': ['mail','stock','account','sale','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/production_location.xml',
        'data/email_template.xml',
        'views/production.xml',
        'views/component.xml',
        'views/account_move.xml',
        'views/sale.xml',
        'views/purchase.xml'
        ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}