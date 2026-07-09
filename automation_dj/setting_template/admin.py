from django.contrib import admin
from .models import VideoTemplate,RenderJob,Content

# Register your models here.


admin.site.site_header = "Automation App"
admin.site.site_title = "Automation App Admin"
admin.site.index_title = "Dashboard"

@admin.register(VideoTemplate)
class VideoTemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(RenderJob)

class RenderJobAdmin(admin.ModelAdmin):
    pass 

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    pass