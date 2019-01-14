from django import template
import json

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def decode_json(json_str):
    if json_str:
        return json.loads(json_str)
    return None


@register.filter
def get_tag_name(array, tag_id):
    for tag in array:
        if tag.id == tag_id:
            return tag.name
    return None