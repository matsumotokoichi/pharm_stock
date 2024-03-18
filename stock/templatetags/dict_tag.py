from django import template
register = template.Library() 

@register.filter(name='tags')
def get_value(value, key):
    if (key in value.keys()):
        return value[key]
    else:
        return None
