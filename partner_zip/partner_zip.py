# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _

class res_country_city(models.Model):
	_name = 'res.country.city'
	
	name = fields.Char('Name', size=128, required=True)
	code = fields.Integer('Code')
	zip = fields.Char('Zipcode', size=24, select=True, required=True)
	ref = fields.Char('Zipcode', size=24, select=True)
	country_id = fields.Many2one('res.country', 'Country', required=True)
	state_id = fields.Many2one('res.country.state', 'State')
	street_ids = fields.One2many('res.country.city.street', 'city_id', 'Streets')
	lang_id = fields.Many2one('res.lang','Lang')
			
	@api.multi
	def name_get(self):
		res = []
		for r in self:
			res.append((r.id, r.name + ' (' + r.zip + ')'))
		return res
	
	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		recs = self.browse()
		recs = self.search([('zip', operator, name)]+ args, limit=limit)
		recs += self.search([('name', operator, name)]+ args, limit=limit)
 		return recs.name_get()

	_order = 'name'
		
res_country_city()

class res_country_city_street(models.Model):
	_name = 'res.country.city.street'
	
	name = fields.Char('Name', size=128, required=True)
	code = fields.Integer('Code')
	city_id = fields.Many2one('res.country.city', 'City', required=True)
	country_id = fields.Many2one(related='city_id.country_id', store=True, string='Country', readonly=True)
	zip = fields.Char(related='city_id.zip', store=True, string='Zip', readonly=True)

	_order = 'name'

res_country_city_street()



