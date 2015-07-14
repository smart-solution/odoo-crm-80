# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
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

class non_profit_partner_config_settings(osv.osv_memory):
	_name = 'non.profit.partner.config.settings'
	_inherit = 'res.config.settings'

	_columns = {
		'module_partner_membership_origin': fields.boolean('Maintain Member Origin Categories',
			help ="""
This installs the module partner_membership_origin.
 - Adds membership origin categories to the configuration in menu Association
 - Adds membership origin selection to the partner forms
 - If defined in the membership origin category, 
      the recruiting member is also added to the partner forms 
				"""),
		'module_partner_areas_of_interest': fields.boolean('Maintain Member Areas of Interest',
			help ="""
This installs the module partner_areas_of_interest.
 - Adds areas of interest categories to the configuration in menu Association
 - Adds areas of interest selection to the partner forms
				"""),
		'module_partner_address_origin': fields.boolean('Maintain Address Origin Categories',
			help ="""
This installs the module partner_address_origin.
 - Adds address origin categories to the configuration in menu Association
 - Adds address origin selection to the partner forms
				"""),
		'module_partner_address_check': fields.boolean('Check for Double Address',
			help ="""
This installs the module partner_address_check.
 - Warns for multiple use of same address at partner creation
				"""),
		'module_partner_personal_data': fields.boolean('Use Personal Data',
			help ="""
This installs the module partner_personal_data.
 - Adds several fields to the partner and allows to maintain them
 	- relationship to another parten (husband-wife relation)
 	- social security number
 	- birthdate
 	- gender
 	- deceased / date-deceased
				"""),
		'module_partner_tax_certif': fields.boolean('Use Tax Certification',
			help ="""
This installs the module partner_tax_certif.
 - Adds a flag to the partner to determine if the partner needs a tax certificate
				"""),
		'module_partner_welcome_package': fields.boolean('Use Welcome Package',
			help ="""
This installs the module partner_welcome_package.
 - Adds a flag to the partner to determine if the partner received a welcome package
				"""),
		'module_partner_no_magazine': fields.boolean('Use No Magazine',
			help ="""
This installs the module partner_no_magazine.
 - Adds a flag to the partner to determine if the the partner 
   does not want to receive magazines
				"""),
		'module_orgstruct': fields.boolean('Use Organisation Structures',
			help ="""
This installs the module orgstruct.
 - Adds Organisation to the base menu
 - Allows the management of an organisation making use of
 	- organisation types (also defines what you want to maintain on this type,
 		such as functions, relations, analytic code, ...)
 	- function categories
 	- function types
 - Allows to define as well a horizontal as a hierarchical structure
   that defines your organisation.
   On each organisation level, you can define partners that have a function
   in that organisation.
				"""),
		'module_orgstruct_radius_action': fields.boolean('Use Fields of Operation',
			help ="""
This installs the module orgstruct_radius_action.
 - Enhances the organisation structure to maintain the field of operation
   of an organisation item.
				"""),
		'module_orgstruct_niche': fields.boolean('Use Organisation Niche',
			help ="""
This installs the module orgstruct_niche.
 - Enhances the organisation structure to maintain niches
   of an organisation item.
				"""),
		'module_non_profit_projects': fields.boolean('Use Non Profit Projects',
			help ="""
This installs the module non_profit_projects.
 - This module enhances projects:
 	- Define a project Theme
 	- Adds states ('design','entered','partialy approved','approved',...)
 	  that allow the follow-up of the project
    - Adds several tabs on the project form to maintain information as
       - requested and approved budgets
       - partners involved in the project
       - contracts, certificates, documents,...
				"""),
		'module_membership_unlimited': fields.boolean('Use Memberships Unlimited in Time',
			help ="""
This installs the module membership_unlimited.
- This module replaces the standard membership module,
  adding functionality that 
	- allows to have a membership product
	  without an end-date
	- allows to define an invoice schedule on a membership
  	  such as monthly, per trimester, yearly,... and 
  	  an automatic daily job to create the needed invoices.
				"""),
		'module_donation': fields.boolean('Use Donations',
			help ="""
This installs the module donation.
- Enhances partner, membership product and journal in order
  to manage (reoccuring) donations by partners and assign them
  to an analytic account.
  The module will also create the needed invoices (using mandates
  for Direct Debet functionality) based on the defined schedule.
				"""),
		'module_partner_no_free_member': fields.boolean('Set Free Member to False for New Partners',
			help ="""
This installs the module partner_no_free_member.
- This module changes the default for free membership to False
- WARNING: uninstalling this module requires a manual update of 
           the membership module to reset the default to True
				"""),
		'module_partner_address_state': fields.boolean('Maintain Address States',
			help ="""
This installs the module partner_address_state.
- Allows to define different address states (with valid address flag)
  and adds the address state to the partner forms.
				"""),
		'module_partner_use_crab': fields.boolean('Use CRAB Addresses',
			help ="""
This installs the module partner_use_crab.
- This module adds tables with CRAB address information that
  can be maintained in Sales-Address Book-Localization.
  On the partner forms, the CRAB tables are used to enter 
  the partner address if the CRAB-tables for the selected country 
  are loaded.
- This module also adds a flag that allows to create a partner
  without any address information.
For information on how to populate the CRAB tables with the 
needed data for the Netherlands or Belgium, please contact
the author or supplier of the module.
				"""),
		'module_partner_address_history': fields.boolean('Maintain Address History',
			help ="""
This installs the module partner_address_history.
- This module adds a tab Address History on the partner screens and
  keeps track of all changes to the address information of a partner.
				"""),
		'module_first_name_last_name': fields.boolean('Maintain First and Last Name',
			help ="""
This installs the module first_name_last_name.
- This module adds fields to maintain
	- First Name
	- Middle Name
	- Last Name
	- Initials
  on the partner screens
				"""),
				}

	def onchange_orgstruct_radius_action(self, cr, uid, ids, module_orgstruct_radius_action, context=None):
		if module_orgstruct_radius_action:
			return {'value': {'module_orgstruct': True}}
		return {}

	def onchange_orgstruct_niche(self, cr, uid, ids, module_orgstruct_niche, context=None):
		if module_orgstruct_niche:
			return {'value': {'module_orgstruct': True}}
		return {}
	def onchange_orgstruct(self, cr, uid, ids, module_orgstruct, context=None):
		if not module_orgstruct:
			return {'value': {'module_orgstruct_radius_action': False,
							  'module_orgstruct_niche': False}}
		return {}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
