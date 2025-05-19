from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MitraHandover(models.Model):
    _name = 'mitra.handover'
    _description = 'Mitra Task Handover'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'
    
    name = fields.Char('ID Handover', readonly=True, copy=False, default=lambda self: _('New'))
    project_id = fields.Many2one('mitra.project', string='Proyek', required=True, tracking=True)
    task_id = fields.Many2one('mitra.project.task', string='Tugas', required=True, domain="[('project_id', '=', project_id)]", tracking=True)
    
    from_employee_id = fields.Many2one('hr.employee', string='Dari', required=True, tracking=True)
    to_employee_id = fields.Many2one('hr.employee', string='Ke', required=True, tracking=True)
    
    date = fields.Date('Tanggal', default=fields.Date.today, required=True, tracking=True)
    description = fields.Text('Deskripsi', tracking=True)
    notes = fields.Text('Catatan', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'Dalam Proses'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan')
    ], string='Status', default='draft', tracking=True)
    
    attachment_ids = fields.Many2many('ir.attachment', string='Lampiran')
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('mitra.handover') or _('New')
        return super(MitraHandover, self).create(vals)
    
    @api.constrains('from_employee_id', 'to_employee_id')
    def _check_employees(self):
        for record in self:
            if record.from_employee_id == record.to_employee_id:
                raise ValidationError(_("Karyawan asal dan tujuan tidak boleh sama!"))
    
    def action_start_handover(self):
        self.write({'state': 'in_progress'})
    
    def action_complete_handover(self):
        self.write({'state': 'completed'})
        # Update task assignee
        if self.task_id:
            self.task_id.write({'assignee_id': self.to_employee_id.id})
    
    def action_cancel_handover(self):
        self.write({'state': 'cancelled'})
    
    def action_reset_to_draft(self):
        self.write({'state': 'draft'})