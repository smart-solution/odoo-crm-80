# -*- encoding: utf-8 -*-

import datetime
from mx import DateTime
import time

from openerp.osv import fields, osv
from openerp import netsvc
from openerp.tools.translate import _

class account_bank_statement_line(osv.osv):
	_inherit = "account.bank.statement.line"

	def create_partner(self, cr, uid, ids, context=None):
		view_id = self.pool.get('ir.ui.view').search(cr, uid, [('model','=','bank.statement.create.partner'),('name','=','view.bank.statement.create.partner.form')])
		stmt = self.browse(cr, uid, ids)[0]
		context['stmt_id'] = stmt.id
		context['default_stmt_id'] = stmt.id
		context['default_transaction_amount'] = stmt.amount
		context['default_free_comm'] = stmt.name
		context['bank_account_id'] = stmt.bank_account_id.id
		if stmt.partner_id:
			context['default_partner_id'] = stmt.partner_id.id
			address = ''
			street = ''
			zip = ''
			city = ''
			if stmt.partner_id.street:
				street = stmt.partner_id.street
			if stmt.partner_id.zip:
				zip = stmt.partner_id.zip
			if stmt.partner_id.city:
				city = stmt.partner_id.city
			address = street + ' ' + zip + ' ' + city
			context['default_partner_address'] = address
			if stmt.partner_id.membership_state == 'none':
				membership_state = 'Geen lid'
			else:
				if stmt.partner_id.membership_state == 'canceled':
					membership_state = 'Opgezegd lid'
				else:
					if stmt.partner_id.membership_state == 'old':
						membership_state = 'Oud lid'
					else:
						if stmt.partner_id.membership_state == 'waiting':
							membership_state = 'Wachtend lid'
						else:
							if stmt.partner_id.membership_state == 'invoiced':
								membership_state = 'Gefactureerd lid'
							else:
								if stmt.partner_id.membership_state == 'paid':
									membership_state = 'Betaald lid'
								else:
									if stmt.partner_id.membership_state == 'wait_member':
										membership_state = 'Wachtend lidmaatschap'
									else:
										if stmt.partner_id.membership_state == 'free':
											membership_state = 'Gratis lid'
										else:
											membership_state = 'Geen lid'
			context['default_membership_state'] = membership_state
			context['default_name'] = stmt.partner_id.name
			context['default_last_name'] = stmt.partner_id.last_name
			context['default_first_name'] = stmt.partner_id.first_name
			context['default_zip'] = stmt.partner_id.zip
			context['default_city'] = stmt.partner_id.city
			context['default_street'] = stmt.partner_id.street
		else:
			context['default_name'] = ''
			context['default_last_name'] = ''
			context['default_first_name'] = ''
			context['default_zip'] = ''
			context['default_city'] = ''
			context['default_street'] = ''

		return {
			'type': 'ir.actions.act_window',
			'name': 'Aanmaken Partner',
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': view_id[0],
			'res_model': 'bank.statement.create.partner',
			'target': 'new',
			'context': context,
		}

	def write(self, cr, uid, ids, vals, context=None):
		if 'partner_id' in vals and (not(vals['partner_id']) or vals['partner_id'] == ''):
			for absl in ids:
				sql_stat = 'update account_bank_statement_line set partner_id = NULL where id = %d' % (absl, )
				cr.execute(sql_stat)
				cr.commit()
				del vals['partner_id']
		return super(account_bank_statement_line, self).write(cr, uid, ids, vals, context)

	_columns = {
		'analytic_account_id': fields.many2one('account.analytic.account', 'Analytische code', select=True),
		'membership_invoice_id': fields.many2one('account.invoice', 'Lidmaatschap factuur', select=True),
	}

account_bank_statement_line()

class bank_statement_create_partner(osv.osv_memory):
	_name = "bank.statement.create.partner"

	def onchange_name(self, cr, uid, ids, first_name, middle_name, last_name, name, context=None):
		res = {}
		name = ''
		if first_name:
			name = first_name
		if first_name and middle_name:
			name = name + ' '
		if middle_name:
			name = name + middle_name
		if (first_name or middle_name) and last_name:
			name = name + ' '
		if last_name:
			name = name + last_name
		res['name'] = name
		return {'value':res}

	def onchange_bankacct(self, cr, uid, ids, bank_account, context=None):
		res = {}
		warning = ''

		if bank_account:
			sql_stat = "select res_partner.id, res_partner.name, res_partner.ref from res_partner_bank, res_partner where replace(acc_number, ' ', '') = replace('%s', ' ', '') and res_partner.id = res_partner_bank.partner_id" % (bank_account, )
			cr.execute(sql_stat)
			for sql_res in cr.dictfetchall():
				if warning == '':
					warning = sql_res['name'] + ' (' + str(sql_res['id']) + ')'
				else:
					warning = warning + ', ' + sql_res['name'] + ' (' + str(sql_res['id']) + ')'
				warning = warning + ''' 
'''

		if not (warning == ''):
			warning_msg = { 
				'title': _('Warning!'),
				'message': _('''De volgende contacten zijn reeds geregistreerd met dit rekeningnummer: 
%s''' % (warning))
			}   
			return {'warning': warning_msg}
		return res

	def onchange_address(self, cr, uid, ids, street, zip, city, context=None):
		res = {}

		error_msg = ''
		if street and city:
			address_obj = self.pool.get('res.partner')
			if zip:
				address_search = address_obj.search(cr, uid, [('street','=',street),('zip','=',zip),('city','=',city)])
			else:
				address_search = address_obj.search(cr, uid, [('street','=',street),('city','=',city)])
			if address_search:
				for address_get in address_obj.browse(cr, uid, address_search):
					error_msg = error_msg + address_get.name + ' (' + str(address_get.id) + ')'
					error_msg = error_msg + '''
'''
				res['double_address'] = error_msg

		return {'value':res}

	_columns = {
		'name': fields.char('Naam'),
		'last_name': fields.char('Achternaam'),
		'first_name': fields.char('Voornaam'),
		'middle_name': fields.char('Tussenvoegsel'),
		'initials': fields.char('Initialen'),
		'street': fields.char('Straat'),
		'zip': fields.char('Postcode', size=16),
		'city': fields.char('Gemeente'),
		'bic': fields.char('BIC Code', size=16),
		'bank_account': fields.char('Bankrekening', size=20),
		'transaction_amount': fields.float('Bedrag transactie'),
		'free_comm': fields.char('Vrije Communicatie'),
		'partner_id': fields.many2one('res.partner', 'Partner', select=True),
		'add_bank_account': fields.boolean('Bankrekening Toevoegen'),
		'membership_state': fields.char('Status Lidmaatschap', translate=True),
		'partner_address': fields.char('Adres'),
		'accept_address': fields.boolean('Adres Aanvaarden'),
		'double_address': fields.text('Adrescontrole'),
		'stmt_id': fields.many2one('account.bank.statement.line', 'Lijn Rekeninguitreksel', select=True),
		'bank_account_id': fields.many2one('res.partner.bank', 'Bankrekening', select=True),
		'membership_partner': fields.boolean('Lidmaatschap'),
		'donation_partner': fields.boolean('Donatie'),
		'analytic_account_id': fields.many2one('account.analytic.account', 'Analytische code', select=True),
		'membership_invoice_id': fields.many2one('account.invoice', 'Lidmaatschap factuur', select=True),
	}

#	_defaults = {
#		'add_bank_account':True,
#	}

	def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
		res = {}
		if partner_id:
			partner_obj = self.pool.get('res.partner')
			partner = partner_obj.browse(cr, uid, partner_id, context=context)
			if partner.membership_state == 'none':
				membership_state = 'Geen lid'
			else:
				if partner.membership_state == 'canceled':
					membership_state = 'Opgezegd lid'
				else:
					if partner.membership_state == 'old':
						membership_state = 'Oud lid'
					else:
						if partner.membership_state == 'waiting':
							membership_state = 'Wachtend lid'
						else:
							if partner.membership_state == 'invoiced':
								membership_state = 'Gefactureerd lid'
							else:
								if partner.membership_state == 'paid':
									membership_state = 'Betaald lid'
								else:
									if partner.membership_state == 'wait_member':
										membership_state = 'Wachtend lidmaatschap'
									else:
										if partner.membership_state == 'free':
											membership_state = 'Gratis lid'
										else:
											membership_state = 'Geen lid'
			res['membership_state'] = membership_state
			street = ''
			zip = ''
			city = ''
			if partner.street:
				street = partner.street
			if partner.zip:
				zip = partner.zip
			if partner.city:
				city = partner.city
			res['partner_address'] = street + ' ' + zip + ' ' + city
			res['name'] = partner.name
 
		return {'value':res}

	def create_partner(self, cr, uid, ids, context=None):
		print 'CONTEXT:',context
		res = {}
		partner_obj = self.pool.get('res.partner')
		for partner in self.browse(cr, uid, ids, context):
			partner_name = ''
			if partner.last_name:
				partner_name = partner.last_name
			if partner.first_name:
				partner_name = partner.first_name + ' ' + partner_name
			if partner.partner_id:
				partner_id = partner.partner_id.id
			else:
				partner_id = partner_obj.create(cr, uid, {
					'name': partner_name,
					'last_name': partner.last_name,
					'first_name': partner.first_name,
					'middle_name': partner.middle_name,
					'initials': partner.initials,
					'street': partner.street,
					'zip': partner.zip,
					'city': partner.city,
					'lang': 'nl_NL',
					'membership_state': 'none',
					'bank_ids': False,
					'customer': False,
					'supplier': False,
				}, context)
			res['partner_id'] = partner_id

			if partner.add_bank_account:
				bank_obj = self.pool.get('res.bank')
				bank = bank_obj.search(cr, uid, [('bic','=',partner.bic)])
				if bank:
					bank_rec = bank_obj.browse(cr, uid, bank[0])
					bank_id = bank_rec.id
				else:
					bank_id = bank_obj.create(cr, uid, {
						'name': partner.bic,
						'bic': partner.bic,
						'active': True,
					}, context=context)

				partner_bank_obj = self.pool.get('res.partner.bank')
				partner_bank_id = partner_bank_obj.create(cr, uid, {
					'bank_name': partner.bic,
					'owner_name': partner.name,
					'sequence': 50,
					'street': partner.street,
					'partner_id': partner_id,
					'bank': bank_id,
					'bank_bic': partner.bic,
					'city': partner.city,
					'name': partner_name,
					'zip': partner.zip,
					'state': 'iban',
					'acc_number': partner.bank_account,
				}, context=context) 

		analytic_account_id = None
		if partner.analytic_account_id:
			analytic_account_id = partner.analytic_account_id.id
		invoice_id = None
		if partner.membership_invoice_id:
			invoice_id = partner.membership_invoice_id.id

		if 'stmt_id' in context and context['stmt_id']:
			stmt_obj = self.pool.get('account.bank.statement.line')
			stmt = stmt_obj.search(cr, uid, [('id','=',context['stmt_id'])])
			stmt_obj.write(cr, uid, stmt, {
				'partner_id': partner_id,
				'analytic_account_id': analytic_account_id,
				'membership_invoice_id': invoice_id,
			}, context=context)
			
		return {'type':'ir.actions.act_window_close'}

bank_statement_create_partner()

