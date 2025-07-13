from django.db import models
from core.models.base import TimeStampedModel
from django.core.exceptions import ValidationError

class ProjectInfo(TimeStampedModel):
    """
    Stores global configuration and project-wide information.
    This model should only have one row.
    """
    site_name = models.CharField(max_length=100, verbose_name="اسم الموقع")
    contact_email = models.EmailField(verbose_name="البريد الإلكتروني للتواصل")
    support_phone = models.CharField(max_length=20, verbose_name="رقم الدعم")
    whatsapp_number = models.CharField(max_length=20, verbose_name="رقم الواتساب")
    tiktok_url = models.URLField(blank=True, null=True, verbose_name="رابط لينكد إن")
    facebook_url = models.URLField(verbose_name="رابط فيسبوك")
    twitter_url = models.URLField(blank=True, null=True, verbose_name="رابط تويتر")
    instagram_url = models.URLField(blank=True, null=True, verbose_name="رابط إنستجرام")
    youtube_url = models.URLField(blank=True, null=True, verbose_name="رابط يوتيوب")
    logo = models.ImageField(upload_to='project_info/logos/', blank=True, null=True, verbose_name="شعار الموقع")
    favicon = models.ImageField(upload_to='project_info/favicons/', blank=True, null=True, verbose_name="أيقونة الموقع")

    description = models.TextField(verbose_name="وصف الموقع")
    places = models.TextField(verbose_name="أماكن فروعنا",help_text="قائمة بأسماء أماكن فروعنا")
    vision = models.TextField( verbose_name="رؤية الموقع")
    mission = models.TextField( verbose_name="رسالة الموقع")
    
    address = models.TextField(blank=True, null=True, verbose_name="العنوان")

    class Meta:
        verbose_name = "Information Project"

    def __str__(self):
        return "information project"

    def clean(self):
        if ProjectInfo.objects.exclude(pk=self.pk).exists():
            raise ValidationError("No more than one ProjectInfo instance is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()  # trigger clean() before saving
        super().save(*args, **kwargs)
