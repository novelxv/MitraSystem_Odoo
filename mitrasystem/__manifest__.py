{
    'name': 'MitraSystem',
    'version': '1.0',
    'summary': 'Sistem Manajemen Proyek dan Alur Kerja Terintegrasi',
    'description': 'Modul untuk mengelola proyek, jadwal, staf, laporan, evaluasi, handover, dan komplain',
    'author': 'MitraSystem Team',
    'depends': ['base'],
    'data': [
        'views/project_views.xml',
        'views/schedule_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
