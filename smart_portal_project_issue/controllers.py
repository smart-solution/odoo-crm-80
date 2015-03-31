# -*- coding: utf-8 -*-
from openerp import http

# class SmartPortalProjectIssue(http.Controller):
#     @http.route('/smart_portal_project_issue/smart_portal_project_issue/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smart_portal_project_issue/smart_portal_project_issue/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smart_portal_project_issue.listing', {
#             'root': '/smart_portal_project_issue/smart_portal_project_issue',
#             'objects': http.request.env['smart_portal_project_issue.smart_portal_project_issue'].search([]),
#         })

#     @http.route('/smart_portal_project_issue/smart_portal_project_issue/objects/<model("smart_portal_project_issue.smart_portal_project_issue"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smart_portal_project_issue.object', {
#             'object': obj
#         })