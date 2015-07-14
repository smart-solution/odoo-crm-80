# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _

class res_partner(models.Model):
	_inherit = "res.partner"
	
	crab_used = fields.Boolean("CRAB-code", default=True)
	no_address = fields.Boolean("Geen addres", default=False)
	street_id = fields.Many2one('res.country.city.street', ondelete='set null', string="Straat ID")
	street_nbr = fields.Char("Huisnummer", size=16)
	street_bus = fields.Char("Bus", size=16)
	zip_id = fields.Many2one('res.country.city', ondelete='set null', string="Gemeente ID")
	postbus_nbr = fields.Char('Postbus', len=16)
	
	def onchange_zip_id(self, cr, uid, ids, zip_id, context=None):
		res = {}
		if not zip_id:
			res['street'] = ""
			res['street2'] = ""
			res['city'] = ""
			res['country_id'] = ""
			res['zip'] = ""
		else:
			city_obj = self.pool.get('res.country.city')
			city = city_obj.browse(cr, uid, zip_id, context=context)
			res['city'] = city.name
			res['country_id'] = city.country_id.id
			res['zip'] = city.zip
			res['state_id'] = city.state_id.id
			res['street'] = ""
			res['street2'] = ""
			res['street_nbr'] = ""
			res['street_bus'] = ""
			res['street_id'] = False
			res['postbus_nbr'] = ""
		return {'value':res}

	def onchange_street_id(self, cr, uid, ids, zip_id, street_id, street_nbr, street_bus, context=None):
		res = {}
		partner_obj = self.pool.get('res.partner')
		if not street_id:
			res['street'] = ""
		else:
			street_obj = self.pool.get('res.country.city.street')
			street = street_obj.browse(cr, uid, street_id, context=context)
			if street_nbr and street_bus:
				res['street'] = street.name + ' ' + street_nbr + '/' + street_bus
			else:
				if street_nbr:
					res['street'] = street.name + ' ' + street_nbr
				else:
					res['street'] = street.name

		id_member = 0
		warning = ''
		if context and 'web' in context:
			web = True
		else:
			web = False
		if street_nbr == False:
			street_nbr = ''
		if street_bus == False:
			street_bus = ''
		if not ids:
			if street_nbr and street_bus:
				partners = partner_obj.search(cr, uid, [('zip_id','=',zip_id),('street_id','=',street_id),('street_nbr','=',street_nbr),('street_bus','=',street_bus),('no_address','=','False')])
			else:
				if street_nbr:
					partners = partner_obj.search(cr, uid, [('zip_id','=',zip_id),('street_id','=',street_id),('street_nbr','=',street_nbr),('no_address','=','False')])
				else:
					partners = partner_obj.search(cr, uid, [('zip_id','=',zip_id),('street_id','=',street_id),('no_address','=','False')])
			print "Partners:", partners
			if partners:
				for partner in partner_obj.browse(cr, uid, partners, context=none):
					if warning == '':
						warning = partner.name
					else:
						warning = warning + partner.name
					if partner.id:
						warning = warning + ' (' + str(partner.id) + ')'
					warning = warning + ''' 
'''
# 			sql_stat = "select id, name, ref from res_partner where zip_id = %d and street_id = %d and (street_nbr = '%s' or street_nbr IS NULL) and (street_bus = '%s' or street_bus IS NULL)" % (zip_id, street_id, street_nbr, street_bus, )
# 			cr.execute(sql_stat)
# 			for sql_res in cr.dictfetchall():
# 				if warning == '':
# 					warning = sql_res['name']
# 				else:
# 					warning = warning + sql_res['name']
# 				if sql_res['id']:
# 					warning = warning + ' (' + str(sql_res['id']) + ')'
# 				warning = warning + ''' 
# '''
		print "IDS", ids
		for id_member in ids:
			if street_nbr and street_bus:
				partners = partner_obj.search(cr, uid, [('zip_id','=',zip_id),('street_id','=',street_id),('street_nbr','=',street_nbr),('street_bus','=',street_bus),('no_address','=','False')])
			else:
				if street_nbr:
					partners = partner_obj.search(cr, uid, [('zip_id','=',zip_id),('street_id','=',street_id),('street_nbr','=',street_nbr),('no_address','=','False')])
				else:
					partners = partner_obj.search(cr, uid, [('zip_id','=',zip_id),('street_id','=',street_id),('no_address','=','False')])
			print "Partners2:", partners
			if partners:
				for partner in partner_obj.browse(cr, uid, partners, context=context):
					if warning == '':
						warning = partner.name
					else:
						warning = warning + partner.name
					if partner.id:
						warning = warning + ' (' + str(partner.id) + ')'
					warning = warning + ''' 
'''
# 			sql_stat = "select id, name, ref from res_partner where zip_id = %d and street_id = %d and (street_nbr = '%s' or street_nbr IS NULL) and (street_bus = '%s' or street_bus IS NULL)" % (zip_id, street_id, street_nbr, street_bus, )
# 			print sql_stat
# 			cr.execute(sql_stat)
# 			for sql_res in cr.dictfetchall():
# 				if not(id_member == sql_res['id']):
# 					if warning == '':
# 						warning = sql_res['name'] + ' (' + str(sql_res['id']) + ')'
# 					else:
# 						warning = warning + ', ' + sql_res['name'] + ' (' + str(sql_res['id']) + ')'
# 					warning = warning + ''' 
# '''

		if not (warning == '') and not web:
			warning_msg = { 
					'title': _('Warning!'),
					'message': _('De volgende contacten zijn reeds geregistreerd op dit adres: %s'%(warning))
				}   
			return {'value': res, 'warning': warning_msg}

		return {'value':res}

	def onchange_postbus_nbr(self, cr, uid, ids, postbus_nbr, context=None):
		res = {}
		if postbus_nbr != '':
			if postbus_nbr != False:
				res['street_id'] = False
				res['street_nbr'] = False
				res['street_bus'] = False
				res['street'] = 'Postbus ' + postbus_nbr
				res['street2'] = False
		return {'value':res}

	def onchange_crab_used(self, cr, uid, ids, crab_used, context=None):
		res = {}
		res['street'] = ''
		res['street2'] = ''
		res['zip'] = ''
		res['city'] = ''
		res['street_nbr'] = ''
		res['street_bus'] = ''
		res['postbus_nbr'] = ''
		res['street_id'] = False
		res['zip_id'] = False
		res['state_id'] = False
		if not crab_used:
			res['country_id'] = False
		return {'value':res}

	def onchange_no_address(self, cr, uid, ids, no_address, country_id, context=None):
		res = {}
		if not(no_address) and country_id == 21:
			res['crab_used'] = True
		return {'value': res}

	def onchange_country(self, cr, uid, ids, country_id, no_address, context=None):
		res = {}
		if country_id == 21 and no_address == False:
			res['crab_used'] = True
		else:
			res['crab_used'] = False
		return {'value':res}

res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
