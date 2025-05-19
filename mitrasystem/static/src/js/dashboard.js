odoo.define('mitrasystem.dashboard', function (require) {
    'use strict';

    var core = require('web.core');
    var session = require('web.session');
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var QWeb = core.qweb;
    var _t = core._t;

    // Dashboard Widget
    var MitraDashboard = Widget.extend(ControlPanelMixin, {
        template: 'mitrasystem.dashboard',
        events: {
            'click .o_dashboard_action': '_onDashboardActionClick',
            'click .o_dashboard_project': '_onProjectClick',
        },

        init: function (parent, context) {
            this._super(parent, context);
            this.dashboardData = {};
            this.charts = {};
        },

        willStart: function () {
            var self = this;
            return $.when(
                this._super.apply(this, arguments),
                this._fetchDashboardData()
            );
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._renderCharts();
                self._setupProjectProgressChart();
                self._setupProjectStatusChart();
            });
        },

        _fetchDashboardData: function () {
            var self = this;
            return ajax.jsonRpc('/mitrasystem/api/projects', 'call', {})
                .then(function (result) {
                    self.dashboardData.projects = result;
                });
        },

        _renderCharts: function () {
            if (window.Chart && document.getElementById('projectProgressChart') && document.getElementById('projectStatusChart')) {
                this._setupProjectProgressChart();
                this._setupProjectStatusChart();
            }
        },

        _setupProjectProgressChart: function () {
            var ctx = document.getElementById('projectProgressChart');
            if (!ctx) return;

            // Extract data from projects
            var labels = [];
            var data = [];
            var backgroundColors = [];
            var borderColors = [];

            if (this.dashboardData.projects) {
                this.dashboardData.projects.forEach(function (project) {
                    labels.push(project.name);
                    data.push(project.progress);
                    
                    // Assign colors based on progress
                    if (project.progress < 25) {
                        backgroundColors.push('rgba(231, 74, 59, 0.2)');
                        borderColors.push('rgba(231, 74, 59, 1)');
                    } else if (project.progress < 50) {
                        backgroundColors.push('rgba(246, 194, 62, 0.2)');
                        borderColors.push('rgba(246, 194, 62, 1)');
                    } else if (project.progress < 75) {
                        backgroundColors.push('rgba(54, 185, 204, 0.2)');
                        borderColors.push('rgba(54, 185, 204, 1)');
                    } else {
                        backgroundColors.push('rgba(28, 200, 138, 0.2)');
                        borderColors.push('rgba(28, 200, 138, 1)');
                    }
                });
            }

            this.charts.progressChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Progress (%)',
                        data: data,
                        backgroundColor: backgroundColors,
                        borderColor: borderColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        },

        _setupProjectStatusChart: function () {
            var ctx = document.getElementById('projectStatusChart');
            if (!ctx) return;

            // Count projects by state
            var stateCounts = {
                'draft': 0,
                'in_progress': 0,
                'on_hold': 0,
                'completed': 0,
                'cancelled': 0
            };

            if (this.dashboardData.projects) {
                this.dashboardData.projects.forEach(function (project) {
                    if (stateCounts.hasOwnProperty(project.state)) {
                        stateCounts[project.state]++;
                    }
                });
            }

            // Prepare data for chart
            var labels = [
                _t('Draft'),
                _t('In Progress'),
                _t('On Hold'),
                _t('Completed'),
                _t('Cancelled')
            ];
            
            var data = [
                stateCounts.draft,
                stateCounts.in_progress,
                stateCounts.on_hold,
                stateCounts.completed,
                stateCounts.cancelled
            ];
            
            var backgroundColors = [
                '#4e73df',
                '#1cc88a',
                '#f6c23e',
                '#36b9cc',
                '#e74a3b'
            ];

            this.charts.statusChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: backgroundColors,
                        hoverBackgroundColor: backgroundColors,
                        hoverBorderColor: "rgba(234, 236, 244, 1)",
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    cutout: '70%',
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        },

        _onDashboardActionClick: function (ev) {
            ev.preventDefault();
            var $action = $(ev.currentTarget);
            var actionName = $action.attr('name');
            var actionContext = $action.attr('context');
            
            this.do_action(actionName, {
                additional_context: actionContext ? JSON.parse(actionContext) : {},
            });
        },

        _onProjectClick: function (ev) {
            ev.preventDefault();
            var projectId = $(ev.currentTarget).data('id');
            if (projectId) {
                this.do_action({
                    type: 'ir.actions.act_window',
                    res_model: 'mitra.project',
                    res_id: projectId,
                    views: [[false, 'form']],
                    target: 'current',
                });
            }
        }
    });

    core.action_registry.add('mitrasystem.dashboard', MitraDashboard);

    // Initialize charts on dashboard page
    $(document).ready(function() {
        if (window.Chart) {
            // Project Status Chart
            var projectStatusChartEl = document.getElementById('projectStatusChart');
            if (projectStatusChartEl) {
                var projectStatusData = JSON.parse(projectStatusChartEl.getAttribute('data-chart'));
                var projectStatusChart = new Chart(projectStatusChartEl, {
                    type: 'doughnut',
                    data: {
                        labels: projectStatusData.labels,
                        datasets: projectStatusData.datasets
                    },
                    options: {
                        maintainAspectRatio: false,
                        cutout: '70%',
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
            }

            // Project Progress Chart
            var projectProgressChartEl = document.getElementById('projectProgressChart');
            if (projectProgressChartEl) {
                var projectProgressData = JSON.parse(projectProgressChartEl.getAttribute('data-chart'));
                var projectProgressChart = new Chart(projectProgressChartEl, {
                    type: 'bar',
                    data: {
                        labels: projectProgressData.labels,
                        datasets: projectProgressData.datasets
                    },
                    options: {
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            }
        }
    });

    return MitraDashboard;
});