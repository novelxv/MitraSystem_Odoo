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

    @api.model
    def search(self, domain=None, offset=0, limit=None, order=None, count=False):
        domain = domain or []
        user = self.env.user

        if user.has_group('mitrasystem.group_pic_proyek'):
            domain = ['|', ('pic_id', '=', user.id), ('pic_id', '=', False)] + domain

        return super().search(domain, offset=offset, limit=limit, order=order, count=count)