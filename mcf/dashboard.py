from admin_tools_stats.modules import DashboardChart, get_active_graph

# append an app list module
self.children.append(modules.AppList(
    _('Dashboard Stats Settings'),
    models=('admin_tools_stats.*', ),
))

if context['request'].user.has_perm('admin_tools_stats.view_dashboardstats'):
        graph_list = get_active_graph()
else:
        graph_list = []

for i in graph_list:
    kwargs = {}
    kwargs['require_chart_jscss'] = True
    kwargs['graph_key'] = i.graph_key

    for key in context['request'].POST:
        if key.startswith('select_box_'):
            kwargs[key] = context['request'].POST[key]

    self.children.append(DashboardChart(**kwargs))