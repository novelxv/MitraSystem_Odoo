from odoo import models, fields, api

class Project(models.Model):
    _name = 'mitrasystem.project'
    _description = 'Proyek'
    _rec_name = 'name'

    name = fields.Char(string='Nama Proyek', required=True)
    client = fields.Char(string='Klien')
    pic_id = fields.Many2one('res.users', string='PIC Proyek')
    deadline = fields.Date(string='Deadline')
    status = fields.Selection([
        ('aktif', 'Aktif'),
        ('tertunda', 'Tertunda'),
        ('selesai', 'Selesai'),
    ], string='Status', default='aktif')
    
    # Progress fields
    auto_progress = fields.Boolean(string='Progress Otomatis dari Tugas', default=True, 
                                 help="Jika diaktifkan, progress proyek akan dihitung berdasarkan progress tugas-tugas")
    progress = fields.Integer(string='Progress (%)')
    
    # Relasi dengan jadwal
    schedule_count = fields.Integer(string='Jumlah Tugas', compute='_compute_schedule_count')
    
    def _compute_schedule_count(self):
        for record in self:
            record.schedule_count = self.env['mitrasystem.schedule'].search_count([('project_id', '=', record.id)])
    
    def _compute_progress_from_tasks(self):
        for project in self:
            if not project.auto_progress:
                continue
                
            tasks = self.env['mitrasystem.schedule'].search([
                ('project_id', '=', project.id)
            ])
            
            if not tasks:
                project.progress = 0
                continue
                
            # Hitung rata-rata progress dari semua tugas
            total_progress = sum(task.progress for task in tasks)
            avg_progress = total_progress / len(tasks)
            project.progress = int(avg_progress)
            
            # Update status jika progress 100%
            if project.progress >= 100:
                project.status = 'selesai'
    
    def action_open_schedule(self):
        return {
            'name': f'Jadwal Proyek: {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'mitrasystem.schedule',
            'view_mode': 'kanban,calendar,list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
            'target': 'current',
        }
    
    def action_update_progress(self):
        self._compute_progress_from_tasks()
        return True

    @api.model
    def _search_domain_for_user(self):
        if self.env.user.has_group('mitrasystem.group_pic_proyek'):
            return ['|', ('pic_id', '=', self.env.uid), ('pic_id', '=', False)]
        return []

    @api.model
    def search(self, domain=None, offset=0, limit=None, order=None):
        domain = domain or []
        domain = self._search_domain_for_user() + domain
        return super(Project, self).search(domain, offset=offset, limit=limit, order=order)
