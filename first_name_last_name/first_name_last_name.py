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
    
	last_name = fields.Char('Achternaam', len=64)
	first_name = fields.Char('Voornaam', len=64)
	middle_name = fields.Char('Tussenvoegsel', len=64)
	initials = fields.Char('Initialen', len=32)
	name_disp = fields.Char(compute='_function_name_disp', string='Name')
    
	@api.one
	@api.depends('first_name','middle_name','last_name')
	def _function_name_disp(self):
		work_name = ''
		if self.first_name:
			work_name = self.first_name
		if self.first_name and self.middle_name:
			work_name += ' '
		if self.middle_name:
			work_name += self.middle_name
		if self.first_name and self.last_name:
			work_name += ' '
		if self.last_name:
			work_name += self.last_name
		self.name_disp = work_name

	@api.onchange('first_name','middle_name','last_name')
	def onchange_name(self):
		work_name = ''
		if self.first_name:
			work_name = self.first_name
		if self.first_name and self.middle_name:
			work_name += ' '
		if self.middle_name:
			work_name += self.middle_name
		if self.first_name and self.last_name:
			work_name += ' '
		if self.last_name:
			work_name += self.last_name
		self.name_disp = work_name
		self.name = work_name

res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
