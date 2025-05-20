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
    progress = fields.Integer(string='Progress (%)')
    
    # Relasi dengan jadwal
    schedule_count = fields.Integer(string='Jumlah Tugas', compute='_compute_schedule_count')
    
    def _compute_schedule_count(self):
        for record in self:
            record.schedule_count = self.env['mitrasystem.schedule'].search_count([('project_id', '=', record.id)])
    
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
