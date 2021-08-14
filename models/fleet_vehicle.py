# -*- coding: utf-8 -*-

from odoo import models, fields, api

# fuel_unit_type = [
#     ('liter', 'Liter'),
#     ('gallon', 'Gallon')
# ]

# class FleetVehicle(models.Model):
#     _name = 'fleet.vehicle'
#     _inherit = ["fleet.vehicle"]

    # fuel_tank_capacity = fields.Float("Fuel Tank Capacity", store=True, editable=True)
    # fuel_unit = fields.Selection(fuel_unit_type, store=True, copied=True, required=True, default=fuel_unit_type[0][0])

    # fuel_economy = fields.Float("Fuel Economy", store=True, editable=False)
    # fuel_economy_unit = fields.Selection(fuel_economy_unit_type, store=True, copied=True, required=True, default=fuel_economy_unit_type[0][0])

    # refueling_count = fields.Float("Tank Fill ups", store=True, readonly=True, default=0)

    # @api.depends('odometer')
    # def _compute_mileage(self):
    #     mileage = 0
    #     FleetVehicalOdometer = self.env['fleet.vehicle.odometer']
    #     for record in self:
    #         vehicle_odometer = FleetVehicalOdometer.search([('vehicle_id', '=', record.id)], limit=1, order='value asc')
    #         if vehicle_odometer:
    #             mileage = self.odometer - vehicle_odometer.value

    #     return mileage

    # mileage = fields.Float("Mileage", default=_compute_mileage, readonly=True, store=False)

    # mileage_unit = fields.Selection(related='odometer_unit', string="Unit", readonly=True)
