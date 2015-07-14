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

from openerp import fields, models, api
from openerp.tools.translate import _

class res_partner(models.Model):
	_inherit = 'res.partner'
    
	address_history_ids =  fields.One2many('res.partner.address.history', 'partner_id', 'Verhuishistoriek')
    
	@api.model
	def create(self, vals):
		res = super(res_partner, self).create(vals)
		if self.street:
			province = None
			if self.state_id:
				province = self.state_id.name
			country = None
			if self.country_id:
				country = self.country_id.id
			rec = self.env['res.partner.address.history']
			rec_id = rec.create({
				'user_id': self.env.user.id,
				'partner_id': self.id,
				'name': self.name,
				'ref': self.ref,
				'street': self.street,
				'street2': self.street2,
				'zip': self.zip,
				'city': self.city,
				'state': province,
				'country_id': country,
			})
		return res

	@api.multi
	def write(self, vals):
		print "address_history write self", self
		print "address_history write vals", vals
		res = super(res_partner, self).write(vals)
		if 'street' in vals or 'street2' in vals or 'zip' in vals or 'city' in vals or 'state_id' in vals or 'country_id' in vals:
			state_name = None
			if self.state_id:
				state_name = self.state_id.name
			rec = self.env['res.partner.address.history']
			rec_id = rec.create({
				'user_id': self.env.user.id,
				'partner_id': self.id,
				'name': self.name,
				'ref': self.ref,
				'street': self.street,
				'street2': self.street2,
				'zip': self.zip,
				'city': self.city,
				'state': state_name,
				'country_id': self.country_id.id,
			})
		return res

res_partner()

class res_partner_address_history(models.Model):
	_name = 'res.partner.address.history'

	_order = 'date_move desc, id desc'

	date_move = fields.Date('Verhuisdatum', default=fields.Date.today)
	user_id = fields.Many2one('res.users', 'Gebruiker', select=True)
	partner_id = fields.Many2one('res.partner', 'Relatie', select=True)
	name = fields.Char('Naam', len=128)
	ref = fields.Char('Code', len=32)
	street = fields.Char('Straat', len=64)
	street2 = fields.Char('Straat(2)', len=64)
	zip = fields.Char('Postcode', len=64)
	city = fields.Char('Gemeente', len=64)
	state = fields.Char('State', len=64)
	country_id = fields.Many2one('res.country', 'Country', select=True)

res_partner_address_history()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
