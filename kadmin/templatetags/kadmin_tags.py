from django.template import Library
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator
import datetime, time

register = Library()


@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()


@register.simple_tag
def build_table_row(obj, admin_class, appname, modelname):
    """应用反射生产一条记录的element"""
    element = ''
    if admin_class.list_display:
        counter = 1
        for index, column in enumerate(admin_class.list_display):
            column_obj = admin_class.model._meta.get_field(column)
            if column_obj.choices:
                column_data = getattr(obj, 'get_{}_display'.format(column))()
            else:
                column_data = getattr(obj, column)
            if index == 0:
                td_ele = '<td><a href="{}/change/">{}</a></td>'.format(obj.id, column_data)
            else:
                td_ele = '<td>{}</td>'.format(column_data)
            element += td_ele
            counter += 1
    else:
        td_ele = '<td><a href="{}/change/">{}</a></td>'.format(obj.id, obj)
        element += td_ele
    return mark_safe(element)


@register.simple_tag  # 筛选
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
                if i[0] is not '':  # 复杂写法 '' if not i[0] %s-%s-%s' % (i[0].year, i[0].month, i[0].day)
                    filter_date = '%s-%s-%s' % (i[0].year, i[0].month, i[0].day)
                    if '%s__gte' % filter_column in admin_class.filter_condition:
                        if filter_date == admin_class.filter_condition.get('%s__gte' % filter_column):
                            selected = 'selected'
                if i[0] == '':
                    option = '<option value="" %s>All %s</option>' % (selected, filter_column)
                else:
                    option = '<option value="%s-%s-%s" %s>%s</option>' % (
                        i[0].year, i[0].month, i[0].day, selected, i[1])
                filter_element += option
    filter_element += '</select>'
    return mark_safe(filter_element)


@register.simple_tag  # 分页
def render_paginator_button(queryset, admin_class, current_order_column, total_display_page):
    # print('【当前页】queryset.number:', queryset.number)
    # print('【总共显示多少页】total_display_page:', total_display_page)
    # print('【一共多少页】queryset.paginator.num_pages:', queryset.paginator.num_pages)
    # print('【是否有上一页】queryset.has_previous:', queryset.has_previous())
    # print('【是否有下一页】queryset.has_next:', queryset.has_next())
    # print('【上一页】queryset.previous_page_number:', queryset.previous_page_number)
    # print('【下一页】queryset.next_page_number:', queryset.next_page_number)
    filter_element = get_filter_element(admin_class)
    order_column = get_current_order_column(current_order_column)
    ele = """
    <nav aria-label="Page navigation">
                    <ul class="pagination pagination-sm">
    """
    if queryset.has_previous():
        ele += """
                    <li><a href="?_kpage=1%s%s" aria-label="Previous"><span aria-hidden="true">First</span></a></li>
                    <!--<li><a href="?_kpage=%s%s%s" aria-label="Previous"><span aria-hidden="true">Previous</span></a></li>-->
                    
        """ % (filter_element, order_column, queryset.previous_page_number(), filter_element, order_column)
    for i in queryset.paginator.page_range:
        if abs(queryset.number - i) < (total_display_page / 2):
            active = ''
            if queryset.number == i:
                active = 'active'
            p_ele = """<li class="%s"><a href="?_kpage=%s%s%s">%s <span class="sr-only">(current)</span></a></li>""" % (
                active, i, filter_element, order_column, i)
            ele += p_ele
    if queryset.has_next():
        ele += """
                        <!--<li><a href="?_kpage=%s%s%s" aria-label="Next"><span aria-hidden="true">Next</span></a></li>-->
                        <li><a href="?_kpage=%s%s%s" aria-label="Next"><span aria-hidden="true">Last</span></a></li>
                    </ul>
                </nav>
                """ % (
            queryset.next_page_number(), filter_element, order_column, queryset.paginator.num_pages, filter_element,
            order_column)
    else:
        ele += """</ul>"""
    return mark_safe(ele)


def get_filter_element(admin_class):
    filter_element = ''
    if admin_class.filter_condition:
        for k, v in admin_class.filter_condition.items():
            filter_element += '&%s=%s' % (k, v)
    return filter_element


def get_current_order_column(current_order_column):
    order_column = ''
    if current_order_column:
        for k, v in current_order_column.items():
            order_column += '&_o=%s' % v
    return order_column


@register.simple_tag  # 生产排序列头
def build_table_head(admin_class, current_order_column):
    # 获取筛选的筛选的表单结果
    filter_element = get_filter_element(admin_class)

    th_element = ''
    if admin_class.list_display:
        counter = 1
        for column in admin_class.list_display:
            if column in current_order_column:
                resver_current_index = -int(current_order_column[column])
                if resver_current_index >= 0:
                    order_mark = """<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>"""
                else:
                    order_mark = """<span class="glyphicon glyphicon-triangle-top" aria-hidden="true"></span>"""
            else:
                resver_current_index = counter
                order_mark = """"""
            th_element += """<th><a href="?_o=%s%s">%s %s</a></th>""" % (
                resver_current_index, filter_element, column, order_mark)
            counter += 1

    else:
        th_element = """<th>%s</th>""" % admin_class.model._meta.model_name.upper()
    return mark_safe(th_element)


@register.simple_tag  # 获取排序的键值对
def get_order_number(current_order_column):
    order_index = ''
    if current_order_column:
        for k, v in current_order_column.items():
            order_index = v
    return order_index


@register.simple_tag
def pleace_holder_search(admin_class):
    pleace_holder = ''
    if admin_class.search_fields:
        for i in admin_class.search_fields:
            pleace_holder += '%s,' % i
    else:
        pleace_holder = 'Nothing to search'
    return pleace_holder
