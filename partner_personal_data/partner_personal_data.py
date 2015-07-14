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

class res_partner(models.Model):
	_inherit = 'res.partner'
    
	relation_partner_id = fields.Many2one('res.partner', 'Echtgeno(o)t(e)', select=True)
	relation_partner_set = fields.Boolean('Relatie', default=False)
	relation_address_set = fields.Boolean('Relatieaddress', default=False)
	birthday = fields.Date('Geboortedatum')
	deceased = fields.Boolean('Overleden', default=False)
	deceased_partner_id = fields.Many2one('res.partner', 'Overdracht Naar', select=True)
	country_person_id = fields.Char('Burgerservicenummer')
	gender = fields.Selection([('m','Man'),('f','Vrouw'),('u','Ongekend')], string='Geslacht', size=1)
    
	@api.onchange('deceased')
	def _onchange_deceased(self):
		if self.deceased:
			self.active = False
			self.deceased_partner_id = self.relation_partner_id.id
		else:
			self.active = True
			self.deceased_partner_id = None

	@api.model
	def onchange_relation_partner_id(self, partner, vals):
		old_relation = self.env['res.partner'].search([('relation_partner_id', '=', partner.id)])
		old_relation.write({'relation_partner_id': None, 'relation_partner_set': False })
		if vals['relation_partner_id']:
			new_relation = self.env['res.partner'].search([('id', '=', vals['relation_partner_id']),('relation_partner_set', '=', False)])
			if partner.crab_used == True:
				new_relation.write({
							'relation_partner_id': partner.id,
							'relation_partner_set': True,
							'relation_address_set': True,
							'use_parent_address': False,
							'no_address': partner.no_address,
							'country_id': partner.country_id.id,
							'state_id': partner.state_id.id,
							'zip_id': partner.zip_id.id,
							'street_id': partner.street_id.id,
							'zip': partner.zip,
							'city': partner.city,
							'street': partner.street,
							'street2': partner.street2,
							'street_nbr': partner.street_nbr,
							'street_bus': partner.street_bus,
							'postbus_nbr': partner.postbus_nbr,
							})
			else:
				new_relation.write({
							'relation_partner_id': partner.id,
							'relation_partner_set': True,
							'relation_address_set': True,
							'use_parent_address': False,
							'crab_used': False,
							'country_id': partner.country_id.id,
							'city': partner.city,
							'state_id': partner.state_id.id,
							'zip': partner.zip,
							'street': partner.street,
							'street2': partner.street2,
							})
			self.relation_partner_set = True
			self.relation_address_set = True
		return

	@api.model
	def onchange_address_with_partner(self, partner, vals):
		new_relation = self.env['res.partner'].search([('id', '=', partner.relation_partner_id.id)])
		if partner.crab_used == True:
			new_relation.write({
						'relation_partner_id': partner.id,
						'relation_partner_set': True,
						'relation_address_set': True,
						'use_parent_address': False,
						'no_address': partner.no_address,
						'country_id': partner.country_id.id,
						'state_id': partner.state_id.id,
						'zip_id': partner.zip_id.id,
						'street_id': partner.street_id.id,
						'zip': partner.zip,
						'city': partner.city,
						'street': partner.street,
						'street2': partner.street2,
						'street_nbr': partner.street_nbr,
						'street_bus': partner.street_bus,
						'postbus_nbr': partner.postbus_nbr,
						})
		else:
			new_relation.write({
						'relation_partner_id': partner.id,
						'relation_partner_set': True,
						'relation_address_set': True,
						'use_parent_address': False,
						'crab_used': False,
						'country_id': partner.country_id.id,
						'city': partner.city,
						'state_id': partner.state_id.id,
						'zip': partner.zip,
						'street': partner.street,
						'street2': partner.street2,
						})
		self.relation_partner_set = True
		self.relation_address_set = True		
		return

	@api.multi
	def write(self, vals):
		print "personal_data write self", self
		print "personal_data write vals", vals
		res = super(res_partner, self).write(vals)
		if 'relation_partner_set' in vals:
			return res
		if 'relation_partner_id' in vals:
			for partner in self:
				self.onchange_relation_partner_id(partner, vals)
		if 'relation_address_set' in vals:
			return res
		if 'street' in vals or 'street2' in vals or 'zip' in vals or 'city' in vals or 'state_id' in vals or 'country_id' in vals:
			for partner in self:
				if partner.relation_address_set == True:
					self.onchange_address_with_partner(partner, vals)
		return res

res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
