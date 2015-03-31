# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_users(models.Model):
     _inherit = 'res.users'

     portal_project_id = fields.Many2one('project.project','Default Project for Portal Issues')
     portal_customer_id = fields.Many2one('res.partner','Customer for Portal Issues',domain=[('is_company','=',True),('customer','=',True)])


class res_partner(models.Model):
    _inherit = 'res.partner'

    project_ids = fields.One2many('project.project', 'partner_id', 'Projects')


class project_issue(models.Model):
    _inherit = 'project.issue'

    in_warranty = fields.Boolean('Under Warranty')
    estimated_time = fields.Float('Estimated Duration')
    project_ids = fields.One2many('project.project', 'partner_id', string='Projects')

    def create(self, cr, uid, vals, context=None):
        """Fills the issue project with the user default project for portal issues"""
        if ('project_id' not in vals or 'project_id' in vals and not vals['project_id']) and 'partner_id' in vals and vals['partner_id']:
            user_id = self.pool.get('res.users').search(cr, uid, [('partner_id','=',vals['partner_id'])])
            if user_id:
                user = self.pool.get('res.users').browse(cr, uid, user_id[0])
                vals['project_id'] = user.portal_project_id and user.portal_project_id.id or False
        return super(project_issue, self).create(cr, uid, vals, context=context)

