from odoo import models, fields

class MitraSystemProjectReport(models.Model):
    _name = 'mitrasystem.project.report'
    _description = 'Laporan Proyek'

    name = fields.Char(string='Nama Laporan', required=True)
    type = fields.Selection([
        ('mingguan', 'Mingguan'),
        ('bulanan', 'Bulanan'),
        ('proyek', 'Proyek'),
        ('kuartal', 'Kuartal'),
        ('kustom', 'Kustom')
    ], string='Jenis', required=True)
    project_id = fields.Many2one('mitrasystem.project', string='Proyek Terkait')
    period = fields.Char(string='Periode')
    created_by = fields.Char(string='Dibuat Oleh')
    created_date = fields.Date(string='Tanggal Dibuat', default=fields.Date.today)
    format = fields.Selection([
        ('pdf', 'PDF'),
        ('xlsx', 'XLSX'),
        ('pptx', 'PPTX')
    ], string='Format', required=True)
    attachment = fields.Binary(string='Lampiran File')
    filename = fields.Char(string='Nama File')