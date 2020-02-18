from django import template

register = template.Library()

@register.filter
def get_at_index(list, index):
    return list[index]

@register.filter
def get_influx_responsetime(list,index):
    return list[index][0]['rt']

@register.filter
def get_influx_statuscode(list,index):
    return list[index][0]['sc']