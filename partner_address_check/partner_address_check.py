# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning

class res_partner(models.Model):
	_inherit = "res.partner"
	
	
	@api.onchange('zip','city','street','street2')
	def _onchange_address(self):
		print 'partner_adress_check'
		if not self.use_parent_address:
			if not self.no_address:
				if self.street:
					if self.zip == '' or self.zip == False:
						partners = self.env['res.partner'].search_read([('city', '=', self.city),
																	('street', '=', self.street)], ['name'])
					else:
						partners = self.env['res.partner'].search_read([('zip', '=', self.zip),
																	('street', '=', self.street)], ['name'])
					if len(partners) > 0:
						warning = ''
						for partner in partners:
							warning = warning + partner['name'] + ' (ID: ' + str(partner['id']) + ')' + '''
'''
						return {
							'warning': {
								'title': "Address is already in use",
								'message': warning,}
							}
		
res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
