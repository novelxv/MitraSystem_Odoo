from odoo import models, fields, api
from datetime import datetime, timedelta

class ProjectSchedule(models.Model):
    _name = 'mitrasystem.schedule'
    _description = 'Penjadwalan Proyek'
    _rec_name = 'task_name'
    _inherit = ['mail.thread']

    task_name = fields.Char(string='Nama Tugas', required=True)
    project_id = fields.Many2one('mitrasystem.project', string='Proyek', required=True)
    assigned_to = fields.Many2one('res.users', string='Dikerjakan Oleh')
    start_date = fields.Date(string='Tanggal Mulai', required=True)
    end_date = fields.Date(string='Tanggal Selesai', required=True)
    
    # Field untuk tampilan timeline
    duration = fields.Integer(string='Durasi (hari)', compute='_compute_duration', store=True)
    progress = fields.Integer(string='Progress (%)', default=0)
    color = fields.Integer(string='Warna')
    
    # Fields untuk tampilan kanban visual
    state = fields.Selection([
        ('pending', 'Belum Dimulai'),
        ('progress', 'Dalam Pengerjaan'),
        ('done', 'Selesai')
    ], string='Status', default='pending', tracking=True)
    
    timeline_position = fields.Char(string='Timeline Position', compute='_compute_timeline_position', store=True)
    is_current = fields.Boolean(string='Sedang Berlangsung', compute='_compute_is_current', store=True)
    is_overdue = fields.Boolean(string='Terlambat', compute='_compute_is_current', store=True)
    
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.duration = delta.days + 1
            else:
                record.duration = 0
    
    @api.depends('start_date', 'end_date')
    def _compute_timeline_position(self):
        today = fields.Date.today()
        for record in self:
            if not record.start_date or not record.end_date:
                record.timeline_position = 'pending'
                continue
                
            if record.start_date > today:
                days_to_start = (record.start_date - today).days
                if days_to_start <= 7:
                    record.timeline_position = 'soon'
                else:
                    record.timeline_position = 'future'
            elif record.end_date < today:
                record.timeline_position = 'past'
            else:
                # Sedang berlangsung
                total_days = (record.end_date - record.start_date).days
                if total_days <= 0:
                    progress = 100
                else:
                    elapsed_days = (today - record.start_date).days
                    progress = min(100, int((elapsed_days / total_days) * 100))
                record.timeline_position = f'progress-{progress}'
    
    @api.depends('start_date', 'end_date')
    def _compute_is_current(self):
        today = fields.Date.today()
        for record in self:
            record.is_current = record.start_date and record.end_date and record.start_date <= today <= record.end_date
            record.is_overdue = record.end_date and record.end_date < today and record.state != 'done'

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        user = self.env.user
        if user.has_group('mitrasystem.group_pic_proyek'):
            domain = ['|', ('assigned_to', '=', user.id), ('assigned_to', '=', False)] + domain
        return super(ProjectSchedule, self).search(domain, offset=offset, limit=limit, order=order)