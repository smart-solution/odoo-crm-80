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

from openerp import models, fields, api, exceptions
from openerp.tools.translate import _
from datetime import datetime

class res_partner(models.Model):
	_inherit = "res.partner"
	
	address_origin_id = fields.Many2one('res.partner.address.origin', String='Herkomst Address', select=True, ondelete='set null')
	address_origin_date = fields.Date('Datum Herkomst Adres')

	@api.constrains('address_origin_date')
	def _check_address_origin_date(self):
		if self.address_origin_date:
			if self.address_origin_date > datetime.today().strftime('%Y-%m-%d'):
				raise exceptions.ValidationError("Datum herkomst address mag niet in de toekomst liggen")

	@api.onchange('address_origin_date')
	def _check_future_date(self):
		if self.address_origin_date > datetime.today().strftime('%Y-%m-%d'):
			return {'warning': {'title': 'Fout',
								'message': 'Datum herkomst address mag niet in de toekomst liggen',}}

res_partner()

class res_partner_address_origin(models.Model):
    _name = 'res.partner.address.origin'

    name = fields.Char('Name', len=64)
    ref = fields.Char('Code', len=32)
    address_origin_category_id = fields.Many2one('res.partner.address.origin.category', String='Categorie Herkomst', select=True, ondelete='set null')
    
    _sql_constraints = [('ref_uniq', 'unique (ref)', 'Code moet uniek zijn !'),]

res_partner_address_origin()

class res_partner_address_origin_category(models.Model):
	_name = 'res.partner.address.origin.category'

	name = fields.Char('Name', len=64)
	ref = fields.Char('Code', len=32)

	_sql_constraints = [('ref_uniq', 'unique (ref)', 'Code moet uniek zijn !'),]

res_partner_address_origin_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
