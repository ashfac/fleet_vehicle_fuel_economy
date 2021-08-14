# -*- coding: utf-8 -*-
{
    'name': "Fleet Fuel Economy",

    'summary': """
        Adds fuel economy calculations to fleet module
    """,

    'author': "Odoo",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Fleet',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet'],

    # always loaded
    'data': [
        'views/fleet_vehicle.xml',
        'views/fleet_vehicle_log_services.xml',
    ],
}
