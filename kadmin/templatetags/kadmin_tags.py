from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag
def build_table_row(obj,admin_class):
    """应用反射生产一条记录的element"""
    element = ''
    for column in admin_class.list_display:
        # print('column:',column)
        column_obj = admin_class.model._meta.get_field(column)
        # print('column_obj:',column_obj)
        # print('column_obj.choices:',column_obj.choices)
        if column_obj.choices:
            column_data = getattr(obj,'get_{}_display'.format(column))()
            # print('column_data:',column_data)
        else:
            column_data = getattr(obj,column)
            # print('column_data:', column_data)
        td_ele = '<td>{}</td>'.format(column_data)
        # print('td_ele:',td_ele)
        element += td_ele
        # print('element:',element)
    # print("*"*60)
    return mark_safe(element)

@register.simple_tag
def build_filter_element(filter_column,admin_class):
    filter_element = '<select name = "{}">'.format(filter_column)
    column_obj = admin_class.model._meta.get_field(filter_column)
    for choice in column_obj.choices:
        option = '<option value="%s">%s</option>' %choice
        filter_element += option
    filter_element +='</select>'
    print("*"*60)
    print(filter_element)
    return mark_safe(filter_element)