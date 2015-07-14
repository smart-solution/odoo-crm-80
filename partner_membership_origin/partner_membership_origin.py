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
	_inherit = "res.partner"
	
	membership_origin_id = fields.Many2one('res.partner.membership.origin', String='Herkomst Lidmaatschap', select=True, ondelete='set null')
	member_recruit_member = fields.Boolean('Leden Werven Leden')
	recruiting_member_id = fields.Many2one('res.partner', String='Wervend Lid', select=True, ondelete='set null')

	def onchange_membership_origin(self, cr, uid, ids, membership_origin_id, context=None):
		res = {}
		membership_origin_obj = self.pool.get('res.partner.membership.origin')
		if membership_origin_id:
			membership_origin = membership_origin_obj.browse(cr, uid, membership_origin_id, context=context)
			res['member_recruit_member'] = membership_origin.member_recruit_member
			res['recruiting_member_id'] = None
		else:
			res['member_recruit_member'] = False
			res['recruiting_member_id'] = None
		return {'value':res}

res_partner()

class res_partner_membership_origin(models.Model):
	_name = 'res.partner.membership.origin'

	name = fields.Char('Name', len=64)
	ref = fields.Char('Code', len=32)
	member_recruit_member = fields.Boolean('Leden Werven Leden')
	date_end = fields.Date('Einddatum')
	membership_origin_category_id = fields.Many2one('res.partner.membership.origin.category', string='Categorie Herkomst', select=True, ondelete='set null')

	_sql_constraints = [('ref_uniq', 'unique (ref)', 'Code moet uniek zijn !'),]

res_partner_membership_origin()

class res_partner_membership_origin_category(models.Model):
	_name = 'res.partner.membership.origin.category'

	name = fields.Char('Name', len=64)
	ref = fields.Char('Code', len=32)

	_sql_constraints = [('ref_uniq', 'unique (ref)', 'Code moet uniek zijn !'),]

res_partner_membership_origin_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
