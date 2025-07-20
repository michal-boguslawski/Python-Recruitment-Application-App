from django.forms.models import model_to_dict
from django.db.models import Model, ForeignKey, OneToOneField

def recursive_model_to_dict(instance, seen=None):
    if seen is None:
        seen = set()
    
    opts = instance._meta
    data = {}

    for field in opts.get_fields():
        if field.auto_created and not field.concrete:
            continue  # skip reverse relations

        value = getattr(instance, field.name, None)

        if isinstance(field, (ForeignKey, OneToOneField)) and isinstance(value, Model):
            # prevent infinite loops
            if value in seen:
                continue
            seen.add(value)
            data[field.name] = recursive_model_to_dict(value, seen)
        else:
            data[field.name] = value

    return data

def explode_dict(d, parent_key='', sep='.'):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(explode_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items
