from odoo import models, fields, api

class ProjectComplaint(models.Model):
    _name = 'mitrasystem.project.complaint'
    _description = 'Komplain Proyek'

    name = fields.Char(string='ID Komplain', required=True, copy=False, readonly=True, default='New')
    project_id = fields.Many2one('mitrasystem.project', string='Proyek', required=True)
    client = fields.Char(string='Klien', required=True)
    description = fields.Text(string='Deskripsi Komplain', required=True)
    date = fields.Date(string='Tanggal Komplain', default=fields.Date.context_today)
    pic_id = fields.Many2one('res.users', string='PIC Proyek', related='project_id.pic_id', store=True, readonly=True)
    status = fields.Selection([
        ('pending', 'Menunggu Respon'),
        ('in_progress', 'Dalam Penanganan'),
        ('done', 'Selesai'),
    ], string='Status', default='pending')

    @api.model
    def _search_domain_user(self):
        if self.env.user.has_group('mitrasystem.group_admin_sistem'):
            return []
        else:
            return [('pic_id', '=', self.env.uid)]

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args += self._search_domain_user()
        return super().search(args, offset=offset, limit=limit, order=order, count=count)