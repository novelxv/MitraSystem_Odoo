from odoo import models, fields

class MitraTaskDependency(models.Model):
    _name = 'mitra.task.dependency'
    _description = 'Task Dependency'
    
    task_from_id = fields.Many2one('mitra.task', string='Task From', required=True, ondelete='cascade')
    task_to_id = fields.Many2one('mitra.task', string='Task To', required=True, ondelete='cascade')
    type = fields.Selection([
        ('start_to_start', 'Start to Start'),
        ('start_to_finish', 'Start to Finish'),
        ('finish_to_start', 'Finish to Start'),
        ('finish_to_finish', 'Finish to Finish')
    ], string='Type', default='finish_to_start', required=True)

class MitraTask(models.Model):
    _name = 'mitra.task'
    _inherit = 'mitra.task'
    
    dependency_ids = fields.One2many('mitra.task.dependency', 'task_from_id', string='Dependencies')
    dependent_ids = fields.One2many('mitra.task.dependency', 'task_to_id', string='Dependents')