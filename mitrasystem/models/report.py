from odoo import models, fields, api, _
from datetime import datetime, timedelta

class MitraReport(models.Model):
    _name = 'mitra.report'
    _description = 'Mitra Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char('Nama Laporan', required=True, tracking=True)
    
    report_type = fields.Selection([
        ('weekly', 'Mingguan'),
        ('monthly', 'Bulanan'),
        ('quarterly', 'Kuartal'),
        ('project', 'Proyek'),
        ('custom', 'Kustom')
    ], string='Jenis Laporan', required=True, tracking=True)
    
    date_from = fields.Date('Dari Tanggal', required=True, tracking=True)
    date_to = fields.Date('Sampai Tanggal', required=True, tracking=True)
    
    project_id = fields.Many2one('mitra.project', string='Proyek', tracking=True)
    creator_id = fields.Many2one('res.users', string='Dibuat Oleh', default=lambda self: self.env.user, readonly=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('generated', 'Dihasilkan'),
        ('sent', 'Terkirim')
    ], string='Status', default='draft', tracking=True)
    
    report_file = fields.Binary('File Laporan', attachment=True)
    report_filename = fields.Char('Nama File')
    
    format = fields.Selection([
        ('pdf', 'PDF'),
        ('xlsx', 'Excel'),
        ('pptx', 'PowerPoint'),
        ('docx', 'Word')
    ], string='Format', default='pdf', required=True)
    
    notes = fields.Text('Catatan')
    
    @api.onchange('report_type')
    def _onchange_report_type(self):
        today = fields.Date.today()
        if self.report_type == 'weekly':
            self.date_from = today - timedelta(days=today.weekday())
            self.date_to = self.date_from + timedelta(days=6)
        elif self.report_type == 'monthly':
            self.date_from = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            self.date_to = next_month.replace(day=1) - timedelta(days=1)
        elif self.report_type == 'quarterly':
            quarter = (today.month - 1) // 3
            self.date_from = today.replace(month=quarter*3+1, day=1)
            if quarter == 3:
                self.date_to = today.replace(year=today.year+1, month=1, day=1) - timedelta(days=1)
            else:
                self.date_to = today.replace(month=quarter*3+4, day=1) - timedelta(days=1)
    
    def action_generate_report(self):
        # todo: implement report generation logic
        self.write({'state': 'generated'})
    
    def action_send_report(self):
        # todo: implement report sending logic
        self.write({'state': 'sent'})