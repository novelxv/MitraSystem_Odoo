from odoo import models, fields, api, _

class MitraComplaint(models.Model):
    _name = 'mitra.complaint'
    _description = 'Mitra Complaint'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char('ID Komplain', readonly=True, copy=False, default=lambda self: _('New'))
    client_id = fields.Many2one('res.partner', string='Klien', required=True, tracking=True)
    project_id = fields.Many2one('mitra.project', string='Proyek', required=True, tracking=True)
    
    description = fields.Text('Deskripsi Komplain', required=True, tracking=True)
    date = fields.Date('Tanggal', default=fields.Date.today, required=True, tracking=True)
    
    pic_id = fields.Many2one('hr.employee', string='PIC', tracking=True)
    
    state = fields.Selection([
        ('new', 'Baru'),
        ('in_progress', 'Dalam Penanganan'),
        ('waiting', 'Menunggu Respon'),
        ('resolved', 'Terselesaikan'),
        ('closed', 'Ditutup')
    ], string='Status', default='new', tracking=True)
    
    priority = fields.Selection([
        ('0', 'Rendah'),
        ('1', 'Normal'),
        ('2', 'Tinggi'),
        ('3', 'Mendesak')
    ], string='Prioritas', default='1', tracking=True)
    
    resolution = fields.Text('Resolusi', tracking=True)
    resolution_date = fields.Date('Tanggal Resolusi', tracking=True)
    
    attachment_ids = fields.Many2many('ir.attachment', string='Lampiran')
    
    # For after-sales service tracking
    is_warranty = fields.Boolean('Dalam Masa Garansi', default=True)
    warranty_end_date = fields.Date('Tanggal Akhir Garansi')
    
    # For customer satisfaction tracking
    satisfaction_rating = fields.Selection([
        ('0', 'Tidak Puas'),
        ('1', 'Kurang Puas'),
        ('2', 'Cukup Puas'),
        ('3', 'Puas'),
        ('4', 'Sangat Puas')
    ], string='Rating Kepuasan', tracking=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('mitra.complaint') or _('New')
        return super(MitraComplaint, self).create(vals)
    
    def action_in_progress(self):
        self.write({'state': 'in_progress'})
    
    def action_waiting(self):
        self.write({'state': 'waiting'})
    
    def action_resolve(self):
        self.write({
            'state': 'resolved',
            'resolution_date': fields.Date.today()
        })
    
    def action_close(self):
        self.write({'state': 'closed'})
    
    def action_reopen(self):
        self.write({'state': 'in_progress'})