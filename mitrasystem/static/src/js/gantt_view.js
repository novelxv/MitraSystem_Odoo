odoo.define('mitrasystem.gantt_view', function (require) {
    "use strict";
    
    var core = require('web.core');
    var Widget = require('web.Widget');
    var ajax = require('web.ajax');
    var view_registry = require('web.view_registry');
    
    var GanttView = Widget.extend({
        template: 'project_gantt_view',
        
        init: function (parent, dataset, view_id, options) {
            this._super.apply(this, arguments);
            this.dataset = dataset;
            this.model = dataset.model;
            this.options = options || {};
        },
        
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._renderGantt();
            });
        },
        
        _renderGantt: function () {
            var self = this;
            
            // Inisialisasi Gantt
            gantt.init(this.$el.find("#gantt_here")[0]);
            
            // Ambil data proyek dari server
            return ajax.jsonRpc('/mitrasystem/gantt_data', 'call', {
                model: this.model
            }).then(function (data) {
                // Format data untuk Gantt
                var tasks = [];
                var links = [];
                
                _.each(data, function (record) {
                    tasks.push({
                        id: record.id,
                        text: record.name,
                        start_date: moment(record.start_date).format('DD-MM-YYYY'),
                        end_date: moment(record.end_date).format('DD-MM-YYYY'),
                        progress: record.progress / 100,
                        open: true
                    });
                    
                    if (record.task_ids && record.task_ids.length) {
                        _.each(record.task_ids, function (task) {
                            tasks.push({
                                id: 't_' + task.id,
                                text: task.name,
                                start_date: moment(task.start_date).format('DD-MM-YYYY'),
                                end_date: moment(task.end_date).format('DD-MM-YYYY'),
                                progress: task.progress / 100,
                                parent: record.id
                            });
                            
                            if (task.dependency_ids && task.dependency_ids.length) {
                                _.each(task.dependency_ids, function (dep) {
                                    links.push({
                                        id: 'l_' + dep.id,
                                        source: 't_' + dep.task_from_id,
                                        target: 't_' + dep.task_to_id,
                                        type: '0'
                                    });
                                });
                            }
                        });
                    }
                });
                
                // Load data ke Gantt
                gantt.parse({
                    data: tasks,
                    links: links
                });
            });
        }
    });
    
    view_registry.add('gantt_custom', GanttView);
    
    return GanttView;
});