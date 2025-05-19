from odoo import models, fields

class ProjectSchedule(models.Model):
    _name = 'mitrasystem.schedule'
    _description = 'Penjadwalan Proyek'
    _rec_name = 'task_name'

    task_name = fields.Char(string='Nama Tugas', required=True)
    project_id = fields.Many2one('mitrasystem.project', string='Proyek', required=True)
    assigned_to = fields.Many2one('res.users', string='Dikerjakan Oleh')
    start_date = fields.Date(string='Tanggal Mulai')
    end_date = fields.Date(string='Tanggal Selesai')