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

from openerp.osv import fields, osv

class res_organisation_type(osv.osv):
	_name = 'res.organisation.type'
	
	_columns = {
		'name': fields.char('Organisatietype', size=128, required=True),
		'function_type_ids': fields.many2many('res.function.type', 'res_organisation_type_function_rel', 'organisation_type_id', 'function_type_id', 'Functietypes'),
		'analytic_account_required': fields.boolean('Analytische code verplicht'),
		'unique_type': fields.boolean('Uniek'),
		'organisation': fields.boolean('Organisatie'),
		'remittance': fields.boolean('Afdracht'),
		'radius_of_action': fields.boolean('Werkingsveld'),
		'organisation_relation_ids': fields.many2many('res.organisation.relation', 'res_organisation_type_relation_rel', 'organisation_type_id', 'relation_type_id', 'Organisatierelaties'),
		'nature_area': fields.boolean('Natuurgebied'),
		'display_functions_company': fields.boolean('Toon functies vzw'),
		'display_functions_person': fields.boolean('Toon functies persoon'),
		'display_remittance': fields.boolean('Toon afdracht'),
		'display_relations': fields.boolean('Toon relaties-tab'),
		'display_relations_vertical': fields.boolean('Toon verticale relaties'),
		'display_relations_horizontal': fields.boolean('Toon horizontale relaties'),
		'display_radius_action': fields.boolean('Toon werkingsveld'),
		'display_niche': fields.boolean('Toon niche'),
		'display_reference': fields.boolean('Toon referentie'),
		'display_npca': fields.boolean('Toon NPCA'),
		'display_regional_level': fields.boolean('Toon regionaal niveau'),
		'display_nature_up': fields.boolean('Toon bovenliggend natuurgebied'),
		'display_partner_up': fields.boolean('Toon bovenliggende relatie'),
		'display_regional_definition': fields.boolean('Toon regionale definitie'),
		'display_regional_definition_m2m': fields.boolean('Toon regionale definitie (m2m)'),
		'display_analytic': fields.boolean('Toon analytische code'),
		'display_address': fields.boolean('Toon adres'),
		'display_regional_partnership': fields.boolean('Toon regionaal samenwerkingsverband'),
	}

res_organisation_type()

class res_function_categ(osv.osv):
	_name = 'res.function.categ'
	
	_columns = {
		'name': fields.char('Functiecategorie', size=128, required=True),
	}

res_function_categ()

class res_function_type(osv.osv):
	_name = 'res.function.type'
	
	_columns = {
		'name': fields.char('Functietype', size=128, required=True),
		'organisation_type_ids': fields.many2many('res.organisation.type', 'res_organisation_type_function_rel', 'function_type_id', 'organisation_type_id', 'Organisatietypes'),
		'unique_type': fields.boolean('Uniek'),
        	'categ_id': fields.many2one('res.function.categ', 'Functiecategorie', select=True, ondelete='cascade'),
	}

res_function_type()

class res_radius_action(osv.osv):
	_name = 'res.radius.action'
	
	_columns = {
		'name': fields.char('Werkingsveld', size=128, required=True),
        'partner_ids': fields.many2many('res.partner', 'res_partner_radius_action_rel', 'radius_action_id', 'partner_id', 'Partners'),
	}

res_radius_action()

class res_niche_categ(osv.osv):
	_name = 'res.niche.categ'
	
	_columns = {
		'name': fields.char('Nichecategorie', size=128, required=True),
	}

res_function_categ()

class res_niche(osv.osv):
	_name = 'res.niche'
	
	_columns = {
		'name': fields.char('Niche', size=128, required=True),
        'partner_ids': fields.many2many('res.partner', 'res_partner_niche_rel', 'niche_id', 'partner_id', 'Partners'),
        'categ_id': fields.many2one('res.niche.categ', 'Nichecategorie', select=True, ondelete='cascade'),
	}

res_niche()

class res_organisation_relation(osv.osv):
	_name = 'res.organisation.relation'

	_columns = {
		'name': fields.char('Relatie', size=128, required=True),
		'organisation_type_ids': fields.many2many('res.organisation.type', 'res_organisation_type_relation_rel', 'relation_type_id', 'organisation_type_id', 'Organisatietypes'),
		'partner_ids': fields.many2many('res.partner', 'res_partner_relation_rel', 'relation_id', 'partner_id', 'Partners'),
        'function_ids': fields.one2many('res.organisation.function', 'organisation_relation_id', 'Functies'),
		'valid_from_date': fields.date('Geldig van'),
		'valid_to_date': fields.date('Geldig tot'),
		'remittance_pct': fields.float('Afdracht'),
		'remittance_new_members': fields.float('Afdracht nieuwe leden'),
        	'partner_id': fields.many2one('res.partner', 'Partner', select=True, ondelete='cascade'),
	}

res_organisation_relation()

class res_organisation_function(osv.osv):
	_name = 'res.organisation.function'

	_columns = {
		'name': fields.char('Functietype', size=128, required=True),
		'organisation_relation_id': fields.many2one('res.organisation.relation', 'Organisatierelatie', select=True),
#		'partner_ids': fields.many2many('res.partner', 'res_partner_function_rel', 'function_id', 'partner_id', 'Partners'),
		'partner_id': fields.many2one('res.partner', 'Partner', select=True),
		'person_id': fields.many2one('res.partner', 'Persoon', select=True, required=True),
		'function_type_id': fields.many2one('res.function.type', 'Functietype', select=True),
		'valid_from_date': fields.date('Geldig van'),
		'valid_to_date': fields.date('Geldig tot'),
		'function_categ_id': fields.related('function_type_id','categ_id',type='many2one',relation='res.function.categ',string='Functiecategorie'),
	}

res_organisation_function()

class res_partner(osv.osv):
	_name = 'res.partner'
	_inherit = 'res.partner'

	_columns = {
        'organisation_type_id': fields.many2one('res.organisation.type', 'Organisatietype', select=True),
        'organisation_relation_ids': fields.many2many('res.partner', 'res_partner_organisation_rel', 'partner_id', 'relation_id', 'Relaties'),
		'relation_ids': fields.many2many('res.organisation.relation', 'res_organisation_relation_rel', 'partner_id', 'relation_id', 'Partners'),
        'partner_up_id': fields.many2one('res.partner', 'Bovenliggende relatie', select=True, ondelete='cascade'),
        'partner_down_ids': fields.one2many('res.partner', 'partner_up_id', 'Onderliggende relaties'),
		'organisation_function_parent_ids': fields.one2many('res.organisation.function', 'partner_id', 'Functies voor vzw'),
		'organisation_function_child_ids': fields.one2many('res.organisation.function', 'person_id', 'Functies voor persoon'),
        'radius_action_ids': fields.many2many('res.radius.action', 'res_organisation_radius_action_rel', 'partner_id', 'radius_action_id', 'Werkingsveld'),
        'niche_ids': fields.many2many('res.niche', 'res_organisation_niche_rel', 'partner_id', 'niche_id', 'Niches'),
        'zip_ids': fields.many2many('res.country.city', 'res_organisation_city_rel', 'partner_id', 'zip_id', 'Gemeentes'),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytische code', select=True, ondelete='cascade'),
        'regional_level': fields.selection([('L','Lokaal'),('G','Gewestelijk'),('R','Regionaal'),('P','Provinciaal')], string='Regionaal niveau', size=1),
        'nature_up_id': fields.many2one('res.partner', 'Bovenliggend natuurgebied', select=True, ondelete='cascade'),
		'remittance_new_member': fields.float('Afdracht nieuw lid'),
		'remittance_exist_member': fields.float('Afdracht bestaand lid'),
		'display_functions_company': fields.related('organisation_type_id','display_functions_company',type='boolean',string='Toon functies vzw'),
		'display_functions_person': fields.related('organisation_type_id','display_functions_person',type='boolean',string='Toon functies persoon'),
		'display_remittance': fields.related('organisation_type_id','display_remittance',type='boolean',string='Toon afdracht'),
		'display_relations': fields.related('organisation_type_id','display_relations',type='boolean',string='Toon relaties'),
		'display_relations_vertical': fields.related('organisation_type_id','display_relations_vertical',type='boolean',string='Toon verticale relaties'),
		'display_relations_horizontal': fields.related('organisation_type_id','display_relations_horizontal',type='boolean',string='Toon horizontale relaties'),
		'display_radius_action': fields.related('organisation_type_id','display_radius_action',type='boolean',string='Toon werkingsveld'),
		'display_niche': fields.related('organisation_type_id','display_niche',type='boolean',string='Toon niche'),
		'display_reference': fields.related('organisation_type_id','display_reference',type='boolean',string='Toon referentie'),
		'display_npca': fields.related('organisation_type_id','display_npca',type='boolean',string='Toon NPCA'),
		'display_regional_level': fields.related('organisation_type_id','display_regional_level',type='boolean',string='Toon regionaal niveau'),
		'display_nature_up': fields.related('organisation_type_id','display_nature_up',type='boolean',string='Toon bovenliggend natuurgebied'),
		'display_partner_up': fields.related('organisation_type_id','display_partner_up',type='boolean',string='Toon bovenliggende relatie'),
		'display_regional_definition': fields.related('organisation_type_id','display_regional_definition',type='boolean',string='Toon regionale definitie'),
		'display_regional_definition_m2m': fields.related('organisation_type_id','display_regional_definition_m2m',type='boolean',string='Toon regionale definitie (m2m)'),
		'display_analytic': fields.related('organisation_type_id','display_analytic',type='boolean',string='Toon analytische code'),
		'display_address': fields.related('organisation_type_id','display_address',type='boolean',string='Toon adres'),
		'regional_partnership': fields.boolean('Regionaal samenwerkingsverband'),
		'display_regional_partnership': fields.related('organisation_type_id','display_regional_partnership',type='boolean',string='Toon regionaal samenwerkingsverband'),
	}

res_partner()

class res_country_city(osv.osv):
	_inherit = 'res.country.city'

	_columns = {
        'org_partner_ids': fields.many2many('res.partner', 'res_organisation_city_rel', 'zip_id', 'partner_id', 'Afdelingen'),
	}

res_country_city()

class account_analytic_account(osv.osv):
    _inherit = 'account.analytic.account'

    _columns = {
    }

    def write(self, cr, uid, ids, vals, context=None):
        res = super(account_analytic_account, self).write(cr, uid, ids, vals, context=context)

	for analytic_account_id in ids:
            if 'name' in vals:
                sql_stat = "update res_partner set name = '%s' where analytic_account_id = %d" % (vals['name'], analytic_account_id, )
                cr.execute(sql_stat)

        return res

account_analytic_account()

