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
from openerp.exceptions import Warning

class res_organisation_type(models.Model):
	_name = 'res.organisation.type'
	
	name = fields.Char('Organisatietype', size=128, required=True)
	function_type_ids = fields.Many2many('res.function.type', 'res_organisation_type_function_rel', 'organisation_type_id', 'function_type_id', 'Functietypes')
	analytic_account_required = fields.Boolean('Analytische code verplicht')
	unique_type = fields.Boolean('Uniek')
	organisation = fields.Boolean('Organisatie')
	remittance = fields.Boolean('Afdracht')
	organisation_relation_ids = fields.Many2many('res.organisation.relation', 'res_organisation_type_relation_rel', 'organisation_type_id', 'relation_type_id', 'Organisatierelaties')
	display_functions_company = fields.Boolean('Toon functies vzw')
	display_functions_person = fields.Boolean('Toon functies persoon')
	display_remittance = fields.Boolean('Toon afdracht')
	display_relations = fields.Boolean('Toon relaties-tab')
	display_relations_vertical = fields.Boolean('Toon verticale relaties')
	display_relations_horizontal = fields.Boolean('Toon horizontale relaties')
	display_reference = fields.Boolean('Toon referentie')
	display_partner_up = fields.Boolean('Toon bovenliggende relatie')
	display_analytic = fields.Boolean('Toon analytische code')
	display_address = fields.Boolean('Toon adres')
	display_regional_level = fields.Boolean('Toon regionaal niveau')

res_organisation_type()

class res_function_categ(models.Model):
	_name = 'res.function.categ'
	
	name = fields.Char('Functiecategorie', size=128, required=True)

res_function_categ()

class res_function_type(models.Model):
	_name = 'res.function.type'
	
	name = fields.Char('Functietype', size=128, required=True)
	organisation_type_ids = fields.Many2many('res.organisation.type', 'res_organisation_type_function_rel', 'function_type_id', 'organisation_type_id', 'Organisatietypes')
	unique_type = fields.Boolean('Uniek')
	categ_id = fields.Many2one('res.function.categ', 'Functiecategorie', select=True, ondelete='cascade')
	membership_required = fields.Boolean('Lidmaatschap verplicht')

res_function_type()

class res_organisation_relation(models.Model):
	_name = 'res.organisation.relation'

	name = fields.Char('Relatie', size=128, required=True)
	organisation_type_ids = fields.Many2many('res.organisation.type', 'res_organisation_type_relation_rel', 'relation_type_id', 'organisation_type_id', 'Organisatietypes')
	partner_ids = fields.Many2many('res.partner', 'res_partner_relation_rel', 'relation_id', 'partner_id', 'Partners')
	function_ids = fields.One2many('res.organisation.function', 'organisation_relation_id', 'Functies')
	valid_from_date = fields.Date('Geldig van')
	valid_to_date = fields.Date('Geldig tot')
	remittance_pct = fields.Float('Afdracht')
	remittance_new_members = fields.Float('Afdracht nieuwe leden')
	partner_id = fields.Many2one('res.partner', 'Partner', select=True, ondelete='cascade')

res_organisation_relation()

class res_organisation_function(models.Model):
	_name = 'res.organisation.function'

	name = fields.Char('Functietype', size=128, required=True)
	organisation_relation_id = fields.Many2one('res.organisation.relation', 'Organisatierelatie', select=True)
	partner_id = fields.Many2one('res.partner', 'Partner', select=True)
	person_id = fields.Many2one('res.partner', 'Persoon', select=True, required=True)
	function_type_id = fields.Many2one('res.function.type', 'Functietype', select=True)
	valid_from_date = fields.Date('Geldig van')
	valid_to_date = fields.Date('Geldig tot')
	function_categ_id = fields.Many2one(string='Functiecategorie', related='function_type_id.categ_id')

	@api.one	
	@api.constrains('function_type_id','person_id')
	def _check_function_person_membership(self):
		if self.function_type_id.membership_required:
			if self.person_id.membership_state in (None, 'old', 'none', 'canceled'):
				raise Warning(_('Persoon heeft geen geldige lidmaatschapsstatus.'))

	@api.onchange('person_id','function_type_id')
	def _onchange_function_person_membership(self):
		if self.function_type_id.membership_required:
			if self.person_id.membership_state in (None, 'old', 'none', 'canceled'):
				raise Warning(_('Persoon heeft geen geldige lidmaatschapsstatus.'))
	
# 	def create(self, cr, uid, vals, context=None):
# 		person_id = None
# 		function_type_id = None
# 		if 'person_id' in vals and vals['person_id']:
# 			person_id = vals['person_id']
# 		if 'function_type_id' in vals and vals['function_type_id']:
# 			function_type_id = vals['function_type_id']
# 		if function_type_id and person_id:
# 			function_type_obj = self.pool.get('res.function.type')
# 			function = function_type_obj.browse(cr, uid, function_type_id)
# 			if function.membership_required:
# 				partner_obj = self.pool.get('res.partner')
# 				partner = partner_obj.browse(cr, uid, person_id)
# 				if partner.membership_state == None or partner.membership_state == 'old' or partner.membership_state == 'none' or partner.membership_state == 'canceled':
# 					warning = 'Partner %s heeft geen geldige lidmaatschapsstatus (%s)' % (partner.name, partner.membership_state)
# 					raise osv.except_osv(_('FOUT:'), _(warning))
# 					return False
# 
# 		return super(res_organisation_function, self).create(cr, uid, vals, context=context)
# 
# 	def onchange_function(self, cr, uid, ids, person_id, function_type_id, context=None):
# 		if function_type_id and person_id:
# 			function_type_obj = self.pool.get('res.function.type')
# 			function = function_type_obj.browse(cr, uid, function_type_id)
# 			if function.membership_required:
# 				partner_obj = self.pool.get('res.partner')
# 				partner = partner_obj.browse(cr, uid, person_id)
# 				if partner.membership_state == None or partner.membership_state == 'old' or partner.membership_state == 'none' or partner.membership_state == 'canceled':
# 					warning = 'Partner %s heeft geen geldige lidmaatschapsstatus (%s)' % (partner.name, partner.membership_state)
# 					raise osv.except_osv(_('FOUT:'), _(warning))
# 					return False
# 		return True

res_organisation_function()

class res_partner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	organisation_type_id = fields.Many2one('res.organisation.type', 'Organisatietype', select=True)
	organisation_relation_ids = fields.Many2many('res.partner', 'res_partner_organisation_rel', 'partner_id', 'relation_id', 'Relaties')
	relation_ids = fields.Many2many('res.organisation.relation', 'res_organisation_relation_rel', 'partner_id', 'relation_id', 'Partners')
	partner_up_id = fields.Many2one('res.partner', 'Bovenliggende relatie', select=True, ondelete='cascade')
	partner_down_ids = fields.One2many('res.partner', 'partner_up_id', 'Onderliggende relaties')
	organisation_function_parent_ids = fields.One2many('res.organisation.function', 'partner_id', 'Functies voor vzw')
	organisation_function_child_ids = fields.One2many('res.organisation.function', 'person_id', 'Functies voor persoon')
	analytic_account_id = fields.Many2one('account.analytic.account', 'Analytische code', select=True, ondelete='cascade')
	regional_level = fields.Selection([('l','Lokaal'),('r','Regionaal'),('p','Provinciaal'),('c','Landelijk')], string='Regionaal niveau', size=1)
	remittance_new_member = fields.Float('Afdracht nieuw lid')
	remittance_exist_member = fields.Float('Afdracht bestaand lid')
	display_functions_company = fields.Boolean('Toon functies vzw', related='organisation_type_id.display_functions_company')
	display_functions_person = fields.Boolean('Toon functies persoon', related='organisation_type_id.display_functions_person')
	display_remittance = fields.Boolean('Toon afdracht', related='organisation_type_id.display_remittance')
	display_relations = fields.Boolean('Toon relaties', related='organisation_type_id.display_relations')
	display_relations_vertical = fields.Boolean('Toon verticale relaties', related='organisation_type_id.display_relations_vertical')
	display_relations_horizontal = fields.Boolean('Toon horizontale relaties', related='organisation_type_id.display_relations_horizontal')
	display_reference = fields.Boolean('Toon referentie', related='organisation_type_id.display_reference')
	display_regional_level = fields.Boolean('Toon regionaal niveau', related='organisation_type_id.display_regional_level')
	display_partner_up = fields.Boolean('Toon bovenliggende relatie', related='organisation_type_id.display_partner_up')
	display_analytic = fields.Boolean('Toon analytische code', related='organisation_type_id.display_analytic')
	display_address = fields.Boolean('Toon adres', related='organisation_type_id.display_address')

res_partner()

