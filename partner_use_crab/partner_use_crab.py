# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _

class res_partner(models.Model):
	_inherit = "res.partner"
	
	no_address = fields.Boolean("Geen addres", default=False)
	street_id = fields.Many2one('res.country.city.street', ondelete='set null', string="Straat ID")
	street_nbr = fields.Char("Huisnummer", size=16)
	street_bus = fields.Char("Bus", size=16)
	zip_id = fields.Many2one('res.country.city', ondelete='set null', string="Gemeente ID")
	postbus_nbr = fields.Char('Postbus', len=16)
	
	@api.onchange('zip_id')
	def _onchange_zip_id(self):
		if self.name:
			if not self.zip_id:
				self.street = ''
				self.street2 = ''
				self.street_nbr = ''
				self.street_bus = ''
				self.postbus_nbr = ''
				self.city = ''
				self.zip = ''
			else:
				street_id = False
				if len(self.zip_id.street_ids) == 1:
					street_id = self.zip_id.street_ids[0].id
				self.city = self.zip_id.name
				self.state_id = self.zip_id.state_id.id
				self.zip = self.zip_id.zip
				self.street = ''
				self.street2 = ''
				self.street_nbr = ''
				self.street_bus = ''
				self.postbus_nbr = ''
				self.street_id = street_id
	
	@api.onchange('street_id','street_nbr','street_bus')
	def _onchange_street_id(self):
		if not self.street_id:
			self.street = ''
		else:
			if self.street_nbr and self.street_bus:
				self.street = self.street_id.name + ' ' + self.street_nbr + '/' + self.street_bus
			else:
				if self.street_nbr:
					self.street = self.street_id.name + ' ' + self.street_nbr
				else:
					self.street = self.street_id.name


	@api.onchange('postbus_nbr')
	def _onchange_postbus_nbr(self):
		if self.postbus_nbr != '':
			if self.postbus_nbr != False:
				self.street_id = False
				self.street_nbr = False
				self.street_bus = False
				self.street = 'Postbus' + self.postbus_nbr
				self.street2 = False

	@api.onchange('use_parent_address')
	def _onchange_use_parent_address(self):
		if not self.use_parent_address:
			self.street = ''
			self.street2 = ''
			self.zip = ''
			self.city = ''
			self.street_nbr = ''
			self.street_bus = ''
			self.postbus_nbr = ''
			self.crab_used = False
			self.street_id = False
			self.zip_id = False
			self.state_id = False
			
	@api.onchange('no_address')
	def _onchange_no_address(self):
		if self.no_address:
			self.crab_used = False
			self.street = ''
			self.street2 = ''
			self.zip = ''
			self.city = ''
			self.street_nbr = ''
			self.street_bus = ''
			self.postbus_nbr = ''
			self.crab_used = False
			self.street_id = False
			self.zip_id = False
			self.state_id = False
		else:
			countryrec = self.env['res.country.city'].search([('country_id', '=', self.country_id.id)], limit=1)
			if countryrec:
				self.crab_used = True
			else:
				self.crab_used = False
			
	@api.onchange('country_id')
	def _onchange_country_id(self):
		if not self.use_parent_address:
			self.crab_used = False
			self.street = ''
			self.street2 = ''
			self.zip = ''
			self.city = ''
			self.street_nbr = ''
			self.street_bus = ''
			self.postbus_nbr = ''
			self.street_id = False
			self.zip_id = False
			self.state_id = False
			countryrec = self.env['res.country.city'].search([('country_id', '=', self.country_id.id)], limit=1)
			if countryrec and self.no_address == False:
				self.crab_used = True

	def onchange_address(self, cr, uid, ids, use_parent_address, parent_id, context=None):
		result = super(res_partner, self).onchange_address(cr, uid, ids, use_parent_address, parent_id, context=context)
		print "use_crab - use_parent_address", use_parent_address
		print "use_crab - ids", ids
		if ids:
			partner = self.browse(cr, uid, ids[0], context=context)
			countryrec = self.pool.get('res.country.city').search(cr, uid, [('country_id', '=', partner[0].country_id.id)], context=context, limit=1)
			crab_used = False
			if countryrec and partner.no_address == False:
				crab_used = True
			if not use_parent_address:
				result['value'] = {'crab_used': crab_used}
			else:
				result['value'] = {'crab_used': False,
									'street_id': False,
									'zip_id': False,
									'street_nbr': '',
									'street_bus': '',
									'postbus_nbr': '',}
			
		return result
		
res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
