from odoo import models, fields

class MitraSystemProjectIssue(models.Model):
    _name = 'mitrasystem.project.issue'
    _description = 'Masalah Proyek'

    evaluation_id = fields.Many2one('mitrasystem.project.evaluation', string='Evaluasi')
    name = fields.Text(string='Deskripsi Masalah', required=True)