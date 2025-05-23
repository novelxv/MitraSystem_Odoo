{
    'name': 'MitraSystem',
    'version': '1.0',
    'summary': 'Sistem Manajemen Proyek dan Alur Kerja Terintegrasi',
    'description': 'Modul untuk mengelola proyek, jadwal, staf, laporan, evaluasi, handover, dan komplain',
    'author': 'MitraSystem Team',
    'depends': ['base', 'mail'],
    'data': [
        'views/dashboard_views.xml',
        'views/project_views.xml',
        'views/schedule_views.xml',
        'views/handover_views.xml',
        'views/staff_views.xml',
        'views/project_report_views.xml',
        'views/project_evaluation_views.xml',
        'views/project_complaint_views.xml',
        'data/sequence.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
