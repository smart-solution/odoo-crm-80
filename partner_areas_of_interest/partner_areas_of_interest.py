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
	
	area_of_interest_ids = fields.Many2many('res.partner.area.of.interest', String='Areas of Interest')

res_partner()

class res_partner_area_of_interest(models.Model):
    _name = 'res.partner.area.of.interest'

    name = fields.Char('Name', len=64)
    ref = fields.Char('Code', len=32)
    area_of_interest_category_id = fields.Many2one('res.partner.area.of.interest.category', String='Interest Category', select=True, ondelete='set null')
    
    _sql_constraints = [('ref_uniq', 'unique (ref)', 'Code moet uniek zijn !'),]

res_partner_area_of_interest()

class res_partner_area_of_interest_category(models.Model):
	_name = 'res.partner.area.of.interest.category'

	name = fields.Char('Name', len=64)
	ref = fields.Char('Code', len=32)

	_sql_constraints = [('ref_uniq', 'unique (ref)', 'Code moet uniek zijn !'),]

res_partner_area_of_interest_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
