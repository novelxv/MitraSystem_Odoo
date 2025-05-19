# -*- coding: utf-8 -*-
# from odoo import http


# class Mitrasystem(http.Controller):
#     @http.route('/mitrasystem/mitrasystem', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mitrasystem/mitrasystem/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mitrasystem.listing', {
#             'root': '/mitrasystem/mitrasystem',
#             'objects': http.request.env['mitrasystem.mitrasystem'].search([]),
#         })

#     @http.route('/mitrasystem/mitrasystem/objects/<model("mitrasystem.mitrasystem"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mitrasystem.object', {
#             'object': obj
#         })

