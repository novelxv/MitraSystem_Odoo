from odoo import models, fields

class MitraSystemStaff(models.Model):
    _name = 'mitrasystem.staff'
    _description = 'Data Staf'
    
    name = fields.Char(string='Nama', required=True)
    email = fields.Char(string='Email')
    position = fields.Char(string='Jabatan')
    department = fields.Char(string='Departemen')
    user_id = fields.Many2one('res.users', string='Akun Pengguna', help='Opsional: tautkan staf dengan akun pengguna')
    user_id = fields.Many2one('res.users', string='Akun Pengguna', help='Opsional: tautkan staf dengan akun pengguna')
    role = fields.Selection([
        ('admin', 'Admin Sistem'),
        ('manager', 'Manajemen'),
        ('senior', 'Manajemen Senior'),
        ('pic', 'PIC Proyek'),
        ('staf', 'Staf'),
    ], string='Peran', required=True)
    status = fields.Selection([
        ('aktif', 'Aktif'),
        ('nonaktif', 'Nonaktif'),
    ], string='Status', default='aktif')