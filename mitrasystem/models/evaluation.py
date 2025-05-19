from odoo import models, fields, api, _

class MitraEvaluation(models.Model):
    _name = 'mitra.evaluation'
    _description = 'Mitra Project Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char('Nama Evaluasi', required=True, tracking=True)
    project_id = fields.Many2one('mitra.project', string='Proyek', required=True, tracking=True)
    evaluator_id = fields.Many2one('hr.employee', string='Evaluator', required=True, tracking=True)
    evaluation_date = fields.Date('Tanggal Evaluasi', default=fields.Date.today, required=True, tracking=True)
    
    # Budget metrics
    budget_planned = fields.Float('Anggaran Direncanakan', related='project_id.budget_planned', readonly=True)
    budget_actual = fields.Float('Anggaran Aktual', related='project_id.budget_actual', readonly=True)
    budget_variance = fields.Float('Selisih Anggaran', compute='_compute_budget_variance', store=True)
    budget_variance_percent = fields.Float('Selisih Anggaran (%)', compute='_compute_budget_variance', store=True)
    
    # Timeline metrics
    timeline_planned_days = fields.Integer('Durasi Direncanakan (hari)', compute='_compute_timeline_metrics', store=True)
    timeline_actual_days = fields.Integer('Durasi Aktual (hari)', compute='_compute_timeline_metrics', store=True)
    timeline_variance_days = fields.Integer('Selisih Waktu (hari)', compute='_compute_timeline_metrics', store=True)
    
    # Quality metrics
    quality_score = fields.Selection([
        ('1', '1 - Sangat Buruk'),
        ('2', '2 - Buruk'),
        ('3', '3 - Cukup'),
        ('4', '4 - Baik'),
        ('5', '5 - Sangat Baik')
    ], string='Skor Kualitas', default='3', tracking=True)
    
    # Issues and lessons learned
    issue_ids = fields.One2many('mitra.evaluation.issue', 'evaluation_id', string='Masalah')
    lesson_learned = fields.Text('Lesson Learned', tracking=True)
    
    # Overall assessment
    overall_assessment = fields.Selection([
        ('failed', 'Gagal'),
        ('below_expectations', 'Di Bawah Ekspektasi'),
        ('meets_expectations', 'Memenuhi Ekspektasi'),
        ('exceeds_expectations', 'Melebihi Ekspektasi'),
        ('outstanding', 'Luar Biasa')
    ], string='Penilaian Keseluruhan', default='meets_expectations', tracking=True)
    
    notes = fields.Text('Catatan Tambahan', tracking=True)
    
    @api.depends('budget_planned', 'budget_actual')
    def _compute_budget_variance(self):
        for record in self:
            if record.budget_planned:
                record.budget_variance = record.budget_planned - record.budget_actual
                record.budget_variance_percent = (record.budget_variance / record.budget_planned) * 100
            else:
                record.budget_variance = 0
                record.budget_variance_percent = 0
    
    @api.depends('project_id.start_date', 'project_id.end_date')
    def _compute_timeline_metrics(self):
        today = fields.Date.today()
        for record in self:
            if record.project_id.start_date and record.project_id.end_date:
                # Planned timeline
                delta_planned = record.project_id.end_date - record.project_id.start_date
                record.timeline_planned_days = delta_planned.days
                
                # Actual timeline (if project is completed, otherwise use today)
                if record.project_id.state == 'completed':
                    # Assuming there's a completion_date field or using today as fallback
                    completion_date = today  # todo: replace with actual completion date if available
                    delta_actual = completion_date - record.project_id.start_date
                    record.timeline_actual_days = delta_actual.days
                else:
                    delta_actual = today - record.project_id.start_date
                    record.timeline_actual_days = delta_actual.days
                
                # Variance
                record.timeline_variance_days = record.timeline_actual_days - record.timeline_planned_days
            else:
                record.timeline_planned_days = 0
                record.timeline_actual_days = 0
                record.timeline_variance_days = 0

class MitraEvaluationIssue(models.Model):
    _name = 'mitra.evaluation.issue'
    _description = 'Mitra Evaluation Issue'
    
    evaluation_id = fields.Many2one('mitra.evaluation', string='Evaluasi', required=True, ondelete='cascade')
    name = fields.Char('Masalah', required=True)
    description = fields.Text('Deskripsi')
    impact = fields.Selection([
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('critical', 'Kritis')
    ], string='Dampak', default='medium')
    resolution = fields.Text('Resolusi')
    is_resolved = fields.Boolean('Terselesaikan', default=False)