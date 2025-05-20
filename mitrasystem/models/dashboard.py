from odoo import models, fields, api

class MitraSystemDashboard(models.Model):
    _name = 'mitrasystem.dashboard'
    _description = 'Dashboard MitraSystem'

    name = fields.Char(string='Judul', default='Dashboard', readonly=True)

    total_project = fields.Integer(string='Total Proyek', compute='_compute_dashboard')
    active_project = fields.Integer(string='Proyek Aktif', compute='_compute_dashboard')
    finished_project = fields.Integer(string='Proyek Selesai', compute='_compute_dashboard')
    attention_project = fields.Integer(string='Perlu Perhatian', compute='_compute_dashboard')

    def _compute_dashboard(self):
        Project = self.env['mitrasystem.project']
        self.total_project = Project.search_count([])
        self.active_project = Project.search_count([('status', '=', 'aktif')])
        self.finished_project = Project.search_count([('status', '=', 'selesai')])
        self.attention_project = Project.search_count([('progress', '<', 50)])
    
    def name_get(self):
        return [(record.id, "Dashboard") for record in self]

    @api.model
    def default_get(self, fields):
        res = super(MitraSystemDashboard, self).default_get(fields)
        existing_dashboard = self.search([], limit=1)
        if existing_dashboard:
            return existing_dashboard.read(fields)[0]
        return res
