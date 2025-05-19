from odoo import models, fields

class MitraSystemProjectEvaluation(models.Model):
    _name = 'mitrasystem.project.evaluation'
    _description = 'Evaluasi Proyek'

    project_id = fields.Many2one('mitrasystem.project', string='Proyek', required=True)
    status = fields.Selection([
        ('selesai', 'Selesai'),
        ('dalam_pengerjaan', 'Dalam Pengerjaan'),
    ], string='Status', required=True)
    completion = fields.Integer(string='Persentase Penyelesaian (%)', required=True)
    
    budget_planned = fields.Monetary(string='Anggaran Rencana')
    budget_actual = fields.Monetary(string='Anggaran Aktual')
    currency_id = fields.Many2one('res.currency', string='Mata Uang', default=lambda self: self.env.company.currency_id)
    
    time_planned = fields.Integer(string='Waktu Rencana (hari)')
    time_actual = fields.Integer(string='Waktu Aktual (hari)')

    quality = fields.Selection([
        ('1', 'Sangat Buruk'),
        ('2', 'Buruk'),
        ('3', 'Cukup'),
        ('4', 'Baik'),
        ('5', 'Sangat Baik'),
    ], string='Kualitas Proyek', required=True)

    issue_ids = fields.One2many('mitrasystem.project.issue', 'evaluation_id', string='Masalah yang Ditemui')