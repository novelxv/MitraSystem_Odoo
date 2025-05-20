from odoo import models, fields, api
from datetime import datetime, timedelta

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
        for record in self:
            record.total_project = Project.search_count([])
            record.active_project = Project.search_count([('status', '=', 'aktif')])
            record.finished_project = Project.search_count([('status', '=', 'selesai')])
            record.attention_project = Project.search_count(['|', ('progress', '<', 50), ('deadline', '<', (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d'))])
    
    def name_get(self):
        return [(record.id, "Dashboard") for record in self]

    def view_nearest_deadline_projects(self):
        return {
            'name': 'Proyek Aktif dengan Deadline Terdekat',
            'type': 'ir.actions.act_window',
            'res_model': 'mitrasystem.project',
            'view_mode': 'list,form',
            'domain': [('status', '=', 'aktif')],
            'context': {'search_default_deadline': 1},
            'limit': 5,
            'target': 'current',
        }
    
    def view_attention_projects(self):
        today = datetime.today()
        deadline_date = (today + timedelta(days=30)).strftime('%Y-%m-%d')
        return {
            'name': 'Proyek Perlu Perhatian',
            'type': 'ir.actions.act_window',
            'res_model': 'mitrasystem.project',
            'view_mode': 'list,form',
            'domain': ['|', ('progress', '<', 50), ('deadline', '<', deadline_date)],
            'target': 'current',
        }

    @api.model
    def default_get(self, fields):
        res = super(MitraSystemDashboard, self).default_get(fields)
        existing_dashboard = self.search([], limit=1)
        if existing_dashboard:
            return existing_dashboard.read(fields)[0]
        return res
