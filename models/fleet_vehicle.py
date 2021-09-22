# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class FleetVehicle(models.Model):
    _name = 'fleet.vehicle'
    _inherit = ["fleet.vehicle"]

    fuel_tank_capacity = fields.Float(string="Fuel Tank Capacity", help="Fuel Tank Capacity in Leters", store=True)
    
    @api.depends('odometer')
    def _compute_mileage(self):
        mileage = 0
        FleetVehicalOdometer = self.env['fleet.vehicle.odometer']
        for record in self:
            first_odometer = FleetVehicalOdometer.search([('vehicle_id', '=', record.id)], limit=1, order='value asc')
            if first_odometer:
                mileage = self.odometer - first_odometer.value

        return mileage

    mileage = fields.Float(string="Mileage", default=_compute_mileage, store=False, readonly=True)

    fuel_economy = fields.Text(compute='_compute_fuel_economy', store=False, readonly=True,
        string="Fuel Economy",
        help="Average fuel economoy in Liter/100 km / MPG")

    def _compute_fuel_economy(self):
        for record in self:
            FleetVehicalServices = self.env['fleet.vehicle.log.services']
            service_ids = FleetVehicalServices.search([('vehicle_id', '=', record.id), ('fuel_economy', '!=', 0)])

            if service_ids:
                sum = 0.0
                count = 0
                for service_id in service_ids:
                    sum += service_id.fuel_economy
                    count += 1

                fuel_economy_average = sum / count
                _logger.info('_compute_fuel_economy::service_ids(average) : %r = %r', service_ids, fuel_economy_average)
                self.fuel_economy=str(round(fuel_economy_average, 1)) + " / " + str(round(235.214583 / fuel_economy_average)) + "  (l/100 km / MPG)"
            else:
                _logger.info('_compute_fuel_economy:: no record found' )
                self.fuel_economy="0.0"
