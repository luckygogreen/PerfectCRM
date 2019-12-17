import json

from django.shortcuts import render



class BaseKadmin(object):
    def __init__(self):
        self.actions.extend(self.default_actions)

    list_display = []
    list_filter = []
    search_fields = []
    list_editable = []
    readonly_fields = []
    filter_horizontal = []
    list_per_page = 5
    default_actions = ['delete_selected_objs',]
    actions = []

    def delete_selected_objs(self, request, querysets):
        querysets_ids = json.dumps([i.id for i in querysets])
        return render(request, 'table_object_delete.html', {'admin_class': self,
                                                                   'objs': querysets,
                                                                   'querysets_ids': querysets_ids
                                                                   })