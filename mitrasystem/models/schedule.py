from odoo import models, fields, api

class ProjectSchedule(models.Model):
    _name = 'mitrasystem.schedule'
    _description = 'Penjadwalan Proyek'
    _rec_name = 'task_name'

    task_name = fields.Char(string='Nama Tugas', required=True)
    project_id = fields.Many2one('mitrasystem.project', string='Proyek', required=True)
    assigned_to = fields.Many2one('res.users', string='Dikerjakan Oleh')
    start_date = fields.Date(string='Tanggal Mulai')
    end_date = fields.Date(string='Tanggal Selesai')

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        user = self.env.user
        if user.has_group('mitrasystem.group_pic_proyek'):
            domain = ['|', ('assigned_to', '=', user.id), ('assigned_to', '=', False)] + domain
        return super(ProjectSchedule, self).search(domain, offset=offset, limit=limit, order=order)