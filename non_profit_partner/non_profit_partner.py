# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _

class res_partner(models.Model):
	_inherit = "res.partner"
	
	crab_used = fields.Boolean("CRAB-code", default=False)

res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: