from odoo import models, fields

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