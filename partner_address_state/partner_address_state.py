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

class res_partner(models.Model):
	_inherit = "res.partner"
	
	address_state_id = fields.Many2one('res.partner.address.state', String='Address State', select=True, ondelete='set null')

res_partner()

class res_partner_address_state(models.Model):
	_name = 'res.partner.address.state'
	
	name = fields.Char('name', size=64, required=True)
	ref = fields.Char('ref', size=32, required=True)
	valid_address = fields.Boolean('Valid Address', default=False)
	
res_partner_address_state()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4