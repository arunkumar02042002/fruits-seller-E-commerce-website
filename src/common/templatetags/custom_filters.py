from django import template

register = template.Library()


def addplaceholder(value, token):
    value.field.widget.attrs["placeholder"] = token
    return value


def lower_case(value):
    return value.lower()


def addclass(value, token):
    value.field.widget.attrs["class"] = token
    return value

def findRange(value):
    return range(value)

def roundValue(value):
    return round(value, 2)


register.filter(addplaceholder)
register.filter(lower_case)
register.filter(addclass)
register.filter(findRange)
register.filter(roundValue)