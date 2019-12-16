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
                td_ele = '<td><input row-select="true" type="checkbox" value="{}"></td><td><a href="{}/change/">{}</a></td>'.format(obj.id,obj.id, column_data)
            else:
                td_ele = '</td><td>{}</td>'.format(column_data)
            element += td_ele
            counter += 1
    else:
        td_ele = '<td><input type="checkbox" value=""></td><td><a href="{}/change/">{}</a></td>'.format(obj.id,obj.id, obj)
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

    th_element = '<th><input type="checkbox" onclick="SelectAllObjs(this)"></th>'
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


@register.simple_tag
def get_field_value(form_obj, field):
    """返回不可修改字段，在前段的显示值"""
    return getattr(form_obj.instance, field)


@register.simple_tag
def get_avilable_m2m_data(admin_class, column_name, form_obj):
    """返回的是many to many 关联表的所有数据"""
    filed_obj = admin_class.model._meta.get_field(column_name)
    set1 = set(filed_obj.related_model.objects.all())
    if form_obj.instance.id:
        set2 = set(getattr(form_obj.instance, column_name).all())
        obj_list = set1 - set2  # set 交集，差集的知识
        return obj_list
    else:
        return set1


@register.simple_tag
def get_selected_m2m_data(admin_class, column_name, form_obj):
    """返回已选的many to many 的数据"""
    if form_obj.instance.id:
        seleted_data = getattr(form_obj.instance, column_name).all()
        return seleted_data
    else:
        return []


@register.simple_tag
def display_all_related_objs(obj):
    """
    显示要被删除对象的所有关联对象
    :param obj:
    :return:
    """
    ele = "<ul>"
    print(obj._meta.related_objects)
    for reversed_fk_obj in obj._meta.related_objects:
        related_table_name = reversed_fk_obj.name
        related_lookup_key = "%s_set" % related_table_name
        related_objs = getattr(obj, related_lookup_key).all()  # 反向查所有关联的数据
        ele += "<li>%s<ul> " % related_table_name
        if reversed_fk_obj.get_internal_type() == "ManyToManyField":  # 不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/kadmin/%s/%s/%s/change/'>%s</a> 记录里与[%s]相关的的数据将被删除</li>" \
                       % (i._meta.app_label, i._meta.model_name, i.id, i, obj)
        else:
            for i in related_objs:
                ele += "<li><a href='/kadmin/%s/%s/%s/change/'>%s</a></li>" % (i._meta.app_label,
                                                                                  i._meta.model_name,
                                                                                  i.id, i)
                ele += display_all_related_objs(i)
        ele += "</ul></li>"
    ele += "</ul>"
    return ele
