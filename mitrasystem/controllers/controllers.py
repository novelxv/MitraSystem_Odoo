from odoo import http
from odoo.http import request
import json

class MitraSystem(http.Controller):
    @http.route('/mitrasystem/dashboard', type='http', auth='user', website=True)
    def dashboard(self, **kw):
        # Get project statistics
        projects = request.env['mitra.project'].search([])
        active_projects = request.env['mitra.project'].search([('state', '=', 'in_progress')])
        completed_projects = request.env['mitra.project'].search([('state', '=', 'completed')])
        overdue_projects = request.env['mitra.project'].search([
            ('is_overdue', '=', True),
            ('state', 'in', ['in_progress', 'on_hold'])
        ])
        
        # Get recent activities
        activities = request.env['mitra.project.progress'].search([], limit=10, order='date desc, id desc')
        
        # Get upcoming deadlines
        upcoming_deadlines = request.env['mitra.project'].search([
            ('state', 'in', ['in_progress', 'on_hold']),
            ('is_overdue', '=', False)
        ], limit=5, order='end_date asc')
        
        # Get complaints statistics
        new_complaints = request.env['mitra.complaint'].search_count([('state', '=', 'new')])
        in_progress_complaints = request.env['mitra.complaint'].search_count([('state', '=', 'in_progress')])
        
        # Prepare data for charts
        project_states = {}
        for project in projects:
            if project.state in project_states:
                project_states[project.state] += 1
            else:
                project_states[project.state] = 1
        
        # Convert to format suitable for charts
        project_states_data = {
            'labels': list(project_states.keys()),
            'datasets': [{
                'data': list(project_states.values()),
                'backgroundColor': [
                    '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'
                ]
            }]
        }
        
        values = {
            'projects': projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'overdue_projects': overdue_projects,
            'activities': activities,
            'upcoming_deadlines': upcoming_deadlines,
            'new_complaints': new_complaints,
            'in_progress_complaints': in_progress_complaints,
            'project_states_data': json.dumps(project_states_data)
        }
        
        return request.render('mitrasystem.dashboard_template', values)
    
    @http.route('/mitrasystem/project/<int:project_id>', type='http', auth='user', website=True)
    def project_detail(self, project_id, **kw):
        project = request.env['mitra.project'].browse(project_id)
        return request.render('mitrasystem.project_detail_template', {
            'project': project
        })
    
    @http.route('/mitrasystem/api/projects', type='json', auth='user')
    def get_projects(self, **kw):
        projects = request.env['mitra.project'].search([])
        result = []
        for project in projects:
            result.append({
                'id': project.id,
                'name': project.name,
                'client': project.client_id.name,
                'pic': project.pic_id.name,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'state': project.state,
                'progress': project.progress
            })
        return result
    
    @http.route('/mitrasystem/api/project/<int:project_id>/progress', type='json', auth='user')
    def add_progress(self, project_id, description, state, **kw):
        project = request.env['mitra.project'].browse(project_id)
        if not project:
            return {'error': 'Project not found'}
        
        progress = request.env['mitra.project.progress'].create({
            'project_id': project_id,
            'description': description,
            'state': state
        })
        
        return {
            'success': True,
            'id': progress.id
        }