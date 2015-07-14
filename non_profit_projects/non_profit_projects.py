# -*- coding: utf-8 -*-
##############################################################################
#
#    Smart Solution bvba
#    Copyright (C) 2010-Today Smart Solution BVBA (<http://www.smartsolution.be>).
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

import base64
import ast
import datetime, re, random

from openerp.tools.translate import _
from openerp import api, fields, models
import openerp.addons.decimal_precision as dp

class project_theme_general(models.Model):
	_name = 'project.theme.general'
	_description = 'Project Theme General'

	name = fields.Char('Naam', size=64, required=True, translate=True)

project_theme_general()

class project_theme_detail(models.Model):
	_name = 'project.theme.detail'
	_description = 'Project Theme Detail'

	name = fields.Char('Naam', size=64, required=True, translate=True)
 
project_theme_detail()
 
class project(models.Model):
	_inherit = 'project.project'
    
	full_name = fields.Text('Volledige naam', required=True, translate=True)
	ident_nbr = fields.Char('Ident. nummer', size=64)
	seq = fields.Many2one('ir.sequence', 'Volgnummer reeks', required=True, select=True )
	description = fields.Text('Omschrijving')
	theme_general_ids = fields.Many2many('project.theme.general', 'project_theme_general_rel', 'theme_general_id', 'project_id', 'Projects Themes General')
	theme_detail_ids = fields.Many2many('project.theme.detail', 'project_theme_detail_rel', 'theme_detail_id', 'project_id', 'Project Themes Detail')
	contact_id = fields.Many2one('res.partner', 'Contactpersoon', select=True)
	main_contractor_id = fields.Many2one('res.partner', 'Hoofdopdrachtgever', select=True)
	co_contractor_ids = fields.Many2many('res.partner', 'project_co_contractor_rel', 'partner_id', 'project_id', 'Co Contractors')
	sub_contractor_ids = fields.Many2many('res.partner', 'project_sub_contractor_rel', 'partner_id', 'project_id', 'Sub Contractors')
	req_amount = fields.Float('Aangevraagd bedrag', digits=(16,2))
	appr_amount_incl = fields.Float('Goedgekeurd bedrag incl', digits=(16,2))
	appr_amount_excl = fields.Float('Goedgekeurd bedrag', digits=(16,2))
	date_approved = fields.Date('Datum goedgekeurd')
	timesheet_required = fields.Boolean('Tijdsregistratie verplicht')                          
	caution = fields.Boolean('Borg', required=False)
	caution_amt = fields.Float('Borg bedrag', digits=(16,2))
	vat = fields.Boolean('BTW')
	overhead_pct = fields.Float('Overhead PCT', digits=(16,2))           
	subs_pct = fields.Float('Subsidie PCT', digits=(16,2))
	user_agreement = fields.Boolean('Gebruiksovereenkomst')
	partner_agreement = fields.Boolean('Partnerovereenkomst')
	certif = fields.Boolean('Certif. van goede uitvoering')
	subc_agreement = fields.Boolean('Overeenkomst onderaanneming')
	project_state = fields.Selection([
            ('draft', 'Ontwerp'),
            ('not_submitted', 'Niet Inged.'),
            ('submitted', 'Ingediend'),
            ('partial_approved', 'Deels Goedgek.'),
            ('approved', 'Goedgekeurd'),
            ('in_process', 'Lopend'),
            ('closed', 'Beëindigd'),
            ('refused', 'Afgekeurd'),
            ], 'Status', readonly=True, track_visibility='onchange', select=True, default='draft')

	@api.onchange('partner_id')
	def _onchange_partner_id(self):
		self.main_contractor_id = self.partner_id

	@api.onchange('vat','appr_amount_excl')
	def _onchange_vat(self):
		amount = self.appr_amount_excl
		if self.vat:
			amount = round((self.amount_excl * 1.21), 2)
		self.appr_amount_incl = amount

	@api.model
	def create(self, values):
		proj = super(project, self).create(values)
		if not 'analytic_account_id' in values:
			proj.code = self.env['ir.sequence'].next_by_id(proj.seq.id)
		else:
			proj.seq = self.env['ir.sequence'].search([('code', '=', 'project.project')], limit=1).id
			proj.full_name = 'Volledige naam'
		return proj

	@api.one
	def project_not_submitted(self):
		self.project_state = 'not_submitted'

	@api.one
	def project_submitted(self):
		self.project_state = 'submitted'

	@api.one
	def project_partial_approved(self):
		self.project_state = 'partial_approved'

	@api.one
	def project_approved(self):
		self.project_state = 'approved'

	@api.one
	def project_in_process(self):
		self.project_state = 'in_process'

	@api.one
	def project_reset_draft(self):
		self.project_state = 'draft'

	@api.one
	def project_closed(self):
		self.project_state = 'closed'

	@api.one
	def project_refused(self):
		self.project_state = 'refused'

project() 
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
