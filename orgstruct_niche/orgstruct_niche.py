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

class res_niche(models.Model):
	_name = 'res.niche'
	
	name = fields.Char('Niche', size=128, required=True)
	partner_ids = fields.Many2many('res.partner', 'res_partner_niche_rel', 'niche_id', 'partner_id', 'Partners')

res_niche()

class res_organisation_type(models.Model):
	_inherit = 'res.organisation.type'

	display_niche = fields.Boolean('Toon Niche')

res_organisation_type()

class res_partner(models.Model):
	_inherit = 'res.partner'

	niche_ids = fields.Many2many('res.niche', 'res_partner_niche_rel', 'partner_id', 'niche_id', 'Niche')
	display_niche = fields.Boolean('Toon Niche', related='organisation_type_id.display_niche')

res_partner()

