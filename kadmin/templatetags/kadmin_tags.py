from django.template import Library
from django.utils.safestring import mark_safe
import datetime, time

register = Library()

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()


@register.simple_tag
def build_table_row(obj, admin_class):
    """应用反射生产一条记录的element"""
    element = ''
    if admin_class.list_display:
        for column in admin_class.list_display:
            column_obj = admin_class.model._meta.get_field(column)
            if column_obj.choices:
                column_data = getattr(obj, 'get_{}_display'.format(column))()
            else:
                column_data = getattr(obj, column)
            td_ele = '<td>{}</td>'.format(column_data)
            element += td_ele
    else:
        td_ele = '<td>{}</td>'.format(obj)
        element += td_ele
    return mark_safe(element)


@register.simple_tag
def build_filter_element(filter_column, admin_class):
    column_obj = admin_class.model._meta.get_field(filter_column)
    try:
        filter_element = '<select name = "{}">'.format(filter_column)
        for choice in column_obj.get_choices():
            selected = ''
            if filter_column in admin_class.filter_condition:
                if str(choice[0]) == admin_class.filter_condition.get(filter_column):
                    selected = 'selected'
            if choice[0] == '':
                option = '<option value="" %s>All %s</option>' % (selected, filter_column)
            else:
                option = '<option value="%s" %s>%s</option>' % (choice[0], selected, choice[1])
            filter_element += option
    except AttributeError as e:
        if column_obj.get_internal_type() in ('Datafield', 'DateTimeField'):
            filter_element = '<select name = "{}__gte">'.format(filter_column)
            time_obj = datetime.datetime.now()
            time_list = [
                ('', ''),
                (time_obj, 'Today'),
                (time_obj - datetime.timedelta(7), 'Past 7 Days'),
                (time_obj.replace(day=1), 'This Month'),
                (time_obj - datetime.timedelta(90), 'Past 90 days'),
                (time_obj - datetime.timedelta(180), 'Past 6 Month'),
                (time_obj.replace(month=1, day=1), 'This yeas'),
            ]
            for i in time_list:
                selected = ''
                if i[0] is not '': # 复杂写法 '' if not i[0] %s-%s-%s' % (i[0].year, i[0].month, i[0].day)
                    filter_date = '%s-%s-%s' % (i[0].year, i[0].month, i[0].day)
                    if '%s__gte' % filter_column in admin_class.filter_condition:
                        if filter_date == admin_class.filter_condition.get('%s__gte' % filter_column):
                            selected = 'selected'
                if i[0] == '':
                    option = '<option value="" %s>All %s</option>' % (selected, filter_column)
                else:
                    option = '<option value="%s-%s-%s" %s>%s</option>' % (i[0].year, i[0].month, i[0].day, selected, i[1])
                filter_element += option
    filter_element += '</select>'
    return mark_safe(filter_element)
