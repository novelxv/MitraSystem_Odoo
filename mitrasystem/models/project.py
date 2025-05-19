from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class MitraProject(models.Model):
    task_count = fields.Integer(string='Jumlah Tugas', compute='_compute_task_count', store=True)
    document_count = fields.Integer(string='Jumlah Dokumen', compute='_compute_document_count', store=True)

    @api.depends('task_ids')
    def _compute_task_count(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)

    @api.depends('document_ids')
    def _compute_document_count(self):
        for rec in self:
            rec.document_count = len(rec.document_ids)
    _name = 'mitra.project'
    _description = 'Mitra Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char('Nama Proyek', required=True, tracking=True)
    code = fields.Char('Kode Proyek', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    client_id = fields.Many2one('res.partner', string='Klien', required=True, tracking=True)
    pic_id = fields.Many2one('hr.employee', string='PIC Proyek', required=True, tracking=True)
    start_date = fields.Date('Tanggal Mulai', required=True, tracking=True)
    end_date = fields.Date('Deadline', required=True, tracking=True)
    description = fields.Text('Deskripsi', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'Aktif'),
        ('on_hold', 'Tertunda'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan')
    ], string='Status', default='draft', tracking=True)
    
    progress = fields.Float('Progress (%)', default=0.0, tracking=True)
    budget_planned = fields.Float('Anggaran Direncanakan', tracking=True)
    budget_actual = fields.Float('Anggaran Aktual', tracking=True)
    
    task_ids = fields.One2many('mitra.project.task', 'project_id', string='Tugas')
    progress_update_ids = fields.One2many('mitra.project.progress', 'project_id', string='Update Progress')
    team_member_ids = fields.Many2many('hr.employee', string='Anggota Tim')
    document_ids = fields.One2many('mitra.project.document', 'project_id', string='Dokumen')
    
    days_left = fields.Integer(string='Hari Tersisa', compute='_compute_days_left', store=True)
    is_overdue = fields.Boolean(string='Terlambat', compute='_compute_days_left', store=True)
    
    @api.depends('end_date')
    def _compute_days_left(self):
        today = fields.Date.today()
        for project in self:
            if project.end_date:
                delta = project.end_date - today
                project.days_left = delta.days
                project.is_overdue = delta.days < 0
            else:
                project.days_left = 0
                project.is_overdue = False
    
    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('mitra.project') or _('New')
        return super(MitraProject, self).create(vals)
    
    def action_start_project(self):
        self.write({'state': 'in_progress'})
    
    def action_hold_project(self):
        self.write({'state': 'on_hold'})
    
    def action_complete_project(self):
        self.write({'state': 'completed', 'progress': 100.0})
    
    def action_cancel_project(self):
        self.write({'state': 'cancelled'})
    
    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("Tanggal mulai tidak boleh setelah tanggal deadline!"))

class MitraProjectTask(models.Model):
    _name = 'mitra.project.task'
    _description = 'Mitra Project Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Nama Tugas', required=True, tracking=True)
    project_id = fields.Many2one('mitra.project', string='Proyek', required=True, ondelete='cascade')
    assignee_id = fields.Many2one('hr.employee', string='Penanggung Jawab', tracking=True)
    deadline = fields.Date('Deadline', tracking=True)
    description = fields.Text('Deskripsi')
    
    state = fields.Selection([
        ('not_started', 'Belum Dimulai'),
        ('in_progress', 'Dalam Pengerjaan'),
        ('completed', 'Selesai'),
        ('blocked', 'Terhambat')
    ], string='Status', default='not_started', tracking=True)
    
    priority = fields.Selection([
        ('0', 'Rendah'),
        ('1', 'Normal'),
        ('2', 'Tinggi'),
        ('3', 'Mendesak')
    ], string='Prioritas', default='1', tracking=True)
    
    progress = fields.Float('Progress (%)', default=0.0, tracking=True)
    
    def action_start_task(self):
        self.write({'state': 'in_progress'})
    
    def action_complete_task(self):
        self.write({'state': 'completed', 'progress': 100.0})
    
    def action_block_task(self):
        self.write({'state': 'blocked'})
    
    def action_reset_task(self):
        self.write({'state': 'not_started'})

class MitraProjectProgress(models.Model):
    _name = 'mitra.project.progress'
    _description = 'Mitra Project Progress Update'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'
    
    project_id = fields.Many2one('mitra.project', string='Proyek', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='Pengguna', default=lambda self: self.env.user, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Karyawan', compute='_compute_employee', store=True)
    date = fields.Date('Tanggal', default=fields.Date.today, required=True)
    description = fields.Text('Deskripsi Aktivitas', required=True)
    
    state = fields.Selection([
        ('in_progress', 'Dalam Pengerjaan'),
        ('completed', 'Selesai'),
        ('blocked', 'Terhambat')
    ], string='Status', default='in_progress', required=True, tracking=True)
    
    @api.depends('user_id')
    def _compute_employee(self):
        for record in self:
            employee = self.env['hr.employee'].search([('user_id', '=', record.user_id.id)], limit=1)
            record.employee_id = employee.id if employee else False

class MitraProjectDocument(models.Model):
    _name = 'mitra.project.document'
    _description = 'Mitra Project Document'
    
    name = fields.Char('Nama Dokumen', required=True)
    project_id = fields.Many2one('mitra.project', string='Proyek', required=True, ondelete='cascade')
    file = fields.Binary('File', attachment=True, required=True)
    file_name = fields.Char('Nama File')
    file_type = fields.Char('Tipe File', compute='_compute_file_type', store=True)
    file_size = fields.Char('Ukuran File', compute='_compute_file_size', store=True)
    uploaded_by = fields.Many2one('res.users', string='Diunggah Oleh', default=lambda self: self.env.user, readonly=True)
    upload_date = fields.Date('Tanggal Unggah', default=fields.Date.today, readonly=True)
    
    @api.depends('file_name')
    def _compute_file_type(self):
        for record in self:
            if record.file_name:
                file_extension = record.file_name.split('.')[-1].lower() if '.' in record.file_name else ''
                record.file_type = file_extension
            else:
                record.file_type = ''
    
    @api.depends('file')
    def _compute_file_size(self):
        for record in self:
            if record.file:
                # This is a simplified calculation, actual implementation may vary
                size_bytes = len(record.file) * 3/4  # Approximate size for base64 encoded data
                if size_bytes < 1024:
                    record.file_size = f"{size_bytes:.2f} B"
                elif size_bytes < 1024 * 1024:
                    record.file_size = f"{size_bytes/1024:.2f} KB"
                else:
                    record.file_size = f"{size_bytes/(1024*1024):.2f} MB"
            else:
                record.file_size = "0 B"