from odoo import models, fields, api, _

class MitraStaff(models.Model):
    _name = 'mitra.staff'
    _description = 'Mitra Staff'
    _inherits = {'hr.employee': 'employee_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    employee_id = fields.Many2one('hr.employee', string='Related Employee', required=True, ondelete='cascade')
    
    role = fields.Selection([
        ('admin', 'Admin Sistem'),
        ('pic', 'PIC Proyek'),
        ('staff', 'Staf'),
        ('management', 'Manajemen Senior')
    ], string='Peran', required=True, tracking=True)
    
    department = fields.Selection([
        ('it', 'IT'),
        ('design', 'Design'),
        ('qa', 'QA'),
        ('management', 'Manajemen'),
        ('admin', 'Admin'),
        ('production', 'Produksi'),
        ('marketing', 'Marketing')
    ], string='Departemen', tracking=True)
    
    is_active = fields.Boolean('Aktif', default=True, tracking=True)
    
    project_ids = fields.One2many('mitra.project', 'pic_id', string='Proyek yang Ditangani')
    project_count = fields.Integer(string='Jumlah Proyek', compute='_compute_project_count')
    
    @api.depends('project_ids')
    def _compute_project_count(self):
        for record in self:
            record.project_count = len(record.project_ids)
    
    def toggle_active(self):
        for record in self:
            record.is_active = not record.is_active