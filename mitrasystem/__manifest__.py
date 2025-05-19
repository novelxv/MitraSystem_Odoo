{
    'name': 'MitraSystem',
    'version': '1.0',
    'summary': 'Sistem Manajemen Proyek dan Alur Kerja Terintegrasi',
    'description': """
        Sistem Manajemen Proyek dan Alur Kerja Terintegrasi untuk CV. Mitra Mandiri
        
        Fitur:
        - Dashboard Proyek
        - Manajemen Data Proyek
        - Update Progress Harian
        - Penjadwalan Proyek
        - Handover Tugas
        - Manajemen Akun Staf
        - Evaluasi Proyek
        - Monitoring & Laporan
        - Komplain dan Layanan Purna Jual
    """,
    'author': 'MitraSystem Team',
    'category': 'Project Management',
    'depends': ['base', 'mail', 'project', 'hr'],
    'data': [
        'security/mitrasystem_security.xml',
        'security/ir.model.access.csv',
        'data/mitrasystem_data.xml',
        'views/project_views.xml',
        'views/staff_views.xml',
        'views/handover_views.xml',
        'views/evaluation_views.xml',
        'views/complaint_views.xml',
        'views/report_views.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
        'views/templates.xml',
        'report/project_report_templates.xml',
        'report/project_reports.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'mitrasystem/static/src/css/style.css',
            'mitrasystem/static/src/js/dashboard.js',
            'mitrasystem/static/lib/dhtmlxgantt/dhtmlxgantt.css',
            'mitrasystem/static/lib/dhtmlxgantt/dhtmlxgantt.js',
            'mitrasystem/static/src/js/gantt_view.js',
        ],
    },
    'license': 'LGPL-3',
}