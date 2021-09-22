# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class FleetVehicleLogServices(models.Model):
    _name = 'fleet.vehicle.log.services'
    _inherit = ["fleet.vehicle.log.services"]

    fuel = fields.Float("Fuel", store=True,  readonly=False)

    previous_odometer = fields.Float(compute="_get_previous_odometer", inverse='_set_previous_odometer', store=False, readonly=False,
        string="Previous Odometer",
        help='Odometer measure of the vehicle at previous service interval of this type')

    mileage = fields.Float(compute="_compute_mileage", store=False, readonly=True,
        string="Mileage",
        help="Mileage since previous service interval of this type")

    full_tank_mileage = fields.Float(compute="_compute_full_tank_mileage", store=False, readonly=True,
        string="Full Tank Mileage",
        help="Extrapolated mileage if the vehicle were to use all the fuel in the tank")

    fuel_economy = fields.Float(compute="_compute_fuel_economy", store=True, readonly=True,
        string="l/100km",
        help="Fuel economoy in Liter/100 km")

    fuel_economy_mpg = fields.Float(compute="_compute_fuel_economy_mpg", store=False, readonly=True,
        string="MPG",
        help="Fuel economoy in MPG")

    price_per_liter = fields.Float(compute="_compute_price_per_liter", store=False, readonly=True,
        string="Price/Liter",
        help="Calculated price of fuel per liter")

    @api.onchange('vehicle_id', 'service_type_id')
    def _get_previous_odometer_id(self):
        for record in self:
            FleetVehicalServices = self.env['fleet.vehicle.log.services']
            previous_service = FleetVehicalServices.search([('vehicle_id', '=', record.vehicle_id.id), ('service_type_id', '=', record.service_type_id.id)],
            limit=1, order='id desc')

            if previous_service:
                self.previous_odometer_id = previous_service.odometer_id
                _logger.info('_get_previous_odometer_id::previous_odometer_id(service) : %r = %r', previous_service.odometer_id.id, previous_service.odometer_id.value )

            else:
                FleetVehicalOdometer = self.env['fleet.vehicle.odometer']
                previous_odometer = FleetVehicalOdometer.search([('vehicle_id', '=', record.vehicle_id.id)], limit=1, order='value desc')

                if previous_odometer:
                    self.previous_odometer_id = previous_odometer
                    _logger.info('_get_previous_odometer_id::previous_odometer_id(odometer) : %r = %r', previous_odometer.id, previous_odometer.value )

    previous_odometer_id = fields.Many2one('fleet.vehicle.odometer', 'Odometer', default=_get_previous_odometer_id, store=True,
        help='Odometer measure of the vehicle at previous service interval of this type')

    @api.onchange('previous_odometer_id')
    def _get_previous_odometer(self):
        for record in self:
            if record.previous_odometer_id:
                record.previous_odometer = record.previous_odometer_id.value

    def _set_previous_odometer(self):
        for record in self:
            odometer = 0
            if record.previous_odometer:
                FleetVehicalOdometer = self.env['fleet.vehicle.odometer']
                odometer = FleetVehicalOdometer.search([('value', '=', record.previous_odometer)], limit=1, order='value desc')

            if odometer:
                _logger.info('_set_previous_odometer::previous_odometer exists: %r = %r', odometer.id, odometer.value )
                self.previous_odometer_id = odometer

            else:
                new_odometer = self.env['fleet.vehicle.odometer'].create({
                    'value': record.previous_odometer,
                    'date': record.date or fields.Date.context_today(record),
                    'vehicle_id': record.vehicle_id.id
                })
                self.previous_odometer_id = new_odometer
                _logger.info('_set_previous_odometer:new_odometer: %r = %r', new_odometer.id, new_odometer.value )

    @api.onchange('odometer', 'previous_odometer')
    def _compute_mileage(self):
        for record in self:
            if record.odometer and record.previous_odometer and record.odometer > record.previous_odometer:
                record.mileage = record.odometer - record.previous_odometer
            else:
                record.mileage = 0.0

    @api.depends('fuel', 'mileage')
    def _compute_fuel_economy(self):
        for record in self:
            if record.mileage == 0 or record.fuel == 0:
                record['fuel_economy'] = 0.0
            else:
                record['fuel_economy'] = 100 * record.fuel / record.mileage

    @api.depends('fuel_economy')
    def _compute_fuel_economy_mpg(self):
        for record in self:
            if record.fuel_economy == 0:
                record['fuel_economy_mpg'] = 0.0
            else:
                record['fuel_economy_mpg'] = 235.214583 / record.fuel_economy


    @api.depends('fuel', 'mileage')
    def _compute_full_tank_mileage(self):
        for record in self:
            if record.fuel == 0:
                record['full_tank_mileage'] = 0.0
            else:
                record['full_tank_mileage'] = record.vehicle_id.fuel_tank_capacity * record.mileage / record.fuel

    @api.depends('fuel', 'amount')
    def _compute_price_per_liter(self):
        for record in self:
            if record.fuel == 0:
                record['price_per_liter'] = 0.0
            else:
                record['price_per_liter'] = record.amount / record.fuel
