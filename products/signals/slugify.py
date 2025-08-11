from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Central registry of models and the field to slugify from
# SLUGIFY_MODELS = {}

# def register_slugify_model(model_class, source_field_name):
#     SLUGIFY_MODELS[model_class] = source_field_name

# @receiver(pre_save)
# def auto_generate_slug(sender, instance, **kwargs):
#     source_field = SLUGIFY_MODELS.get(sender)
#     if not source_field:
#         return  # Skip if not registered
#     if not hasattr(instance, 'slug') or getattr(instance, 'slug'):
#         return  # Skip if already has slug or no slug field
#     value = getattr(instance, source_field, None)
#     if value:
#         instance.slug = slugify(value, allow_unicode=True)
