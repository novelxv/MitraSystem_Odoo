from odoo import models, fields, api

class MitraSystemHandover(models.Model):
    _name = 'mitrasystem.handover'
    _description = 'Handover Tugas'

    name = fields.Char(string='ID', required=True, copy=False, readonly=True,
                       default=lambda self: 'New')
    project_id = fields.Many2one('mitrasystem.project', string='Proyek', required=True)
    task = fields.Char(string='Tugas', required=True)
    from_staff_id = fields.Many2one('res.users', string='Dari', required=True)
    to_staff_id = fields.Many2one('res.users', string='Ke', required=True)
    date = fields.Date(string='Tanggal', required=True)
    status = fields.Selection([
        ('proses', 'Dalam Proses'),
        ('selesai', 'Selesai'),
        ('tertunda', 'Tertunda'),
    ], string='Status', default='proses')

    def name_get(self):
        return [(handover.id, f"HO-{handover.id:03}") for handover in self]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('mitrasystem.handover') or 'New'
        return super().create(vals)