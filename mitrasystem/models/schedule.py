from odoo import models, fields, api
from datetime import datetime, timedelta

class ProjectSchedule(models.Model):
    _name = 'mitrasystem.schedule'
    _description = 'Penjadwalan Proyek'
    _rec_name = 'task_name'
    _inherit = ['mail.thread']

    task_name = fields.Char(string='Nama Tugas', required=True)
    project_id = fields.Many2one('mitrasystem.project', string='Proyek', required=True)
    assigned_to = fields.Many2one('res.users', string='Dikerjakan Oleh (User)')
    assigned_staff_id = fields.Many2one('mitrasystem.staff', string='Dikerjakan Oleh (Staf)')
    start_date = fields.Date(string='Tanggal Mulai', required=True)
    end_date = fields.Date(string='Tanggal Selesai', required=True)
    
    # Field untuk tampilan timeline
    duration = fields.Integer(string='Durasi (hari)', compute='_compute_duration', store=True)
    
    # Progress fields
    auto_progress = fields.Boolean(string='Progress Otomatis', default=False, 
                                  help="Jika diaktifkan, progress akan dihitung otomatis berdasarkan tanggal")
    progress = fields.Integer(string='Progress (%)', default=0, tracking=True)
    
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
                
                # Update progress jika auto_progress aktif
                if record.auto_progress:
                    record.progress = progress
    
    @api.depends('start_date', 'end_date', 'state')
    def _compute_is_current(self):
        today = fields.Date.today()
        for record in self:
            record.is_current = record.start_date and record.end_date and record.start_date <= today <= record.end_date
            record.is_overdue = record.end_date and record.end_date < today and record.state != 'done'
    
    @api.onchange('state')
    def _onchange_state(self):
        for record in self:
            if record.state == 'done':
                record.progress = 100
            elif record.state == 'pending' and record.progress == 0:
                continue
            elif record.state == 'pending':
                record.progress = 0

    def write(self, vals):
        # Keep track of staff/user assignment changes
        old_assigned_to = None
        old_assigned_staff_id = None
        new_assigned_to = None 
        new_assigned_staff_id = None
        
        if 'assigned_to' in vals and any(self.mapped('assigned_to')):
            old_assigned_to = self.mapped('assigned_to')
            new_assigned_to = self.env['res.users'].browse(vals['assigned_to']) if vals['assigned_to'] else False
        
        if 'assigned_staff_id' in vals and any(self.mapped('assigned_staff_id')):
            old_assigned_staff_id = self.mapped('assigned_staff_id')
            new_assigned_staff_id = self.env['mitrasystem.staff'].browse(vals['assigned_staff_id']) if vals['assigned_staff_id'] else False
        
        result = super(ProjectSchedule, self).write(vals)
          # Create handover record if assignment changed
        if (old_assigned_to and new_assigned_to and old_assigned_to != new_assigned_to) or \
           (old_assigned_staff_id and new_assigned_staff_id and old_assigned_staff_id != new_assigned_staff_id):
            for record in self:
                # Create handover record
                handover_vals = {
                    'project_id': record.project_id.id,
                    'task_id': record.id,
                    'date': fields.Date.today(),
                }
                
                # Set the from fields
                if old_assigned_to:
                    handover_vals['from_user_id'] = old_assigned_to[0].id
                elif old_assigned_staff_id:
                    handover_vals['from_staff_id'] = old_assigned_staff_id[0].id
                
                # Set the to fields
                if new_assigned_to:
                    handover_vals['to_user_id'] = new_assigned_to.id
                elif new_assigned_staff_id:
                    handover_vals['to_staff_id'] = new_assigned_staff_id.id
                
                # Create the handover record
                self.env['mitrasystem.handover'].create(handover_vals)
        
        # Update project progress when task progress changes
        if 'progress' in vals or 'state' in vals:
            projects_to_update = self.mapped('project_id')
            for project in projects_to_update:
                project._compute_progress_from_tasks()
        return result
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super(ProjectSchedule, self).create(vals_list)
        # Update project progress when new task is created
        projects = records.mapped('project_id')
        for project in projects:
            project._compute_progress_from_tasks()
        return records    
    
    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        user = self.env.user
        if user.has_group('mitrasystem.group_pic_proyek'):
            # Find staff linked to current user
            staff = self.env['mitrasystem.staff'].search([('user_id', '=', user.id)], limit=1)
            
            domain_extension = ['|', ('assigned_to', '=', user.id), ('assigned_to', '=', False)]
            
            # Add staff condition if staff record exists for current user
            if staff:
                domain_extension = ['|'] + domain_extension + [('assigned_staff_id', '=', staff.id)]
                
            domain = domain_extension + domain
        return super(ProjectSchedule, self).search(domain, offset=offset, limit=limit, order=order)