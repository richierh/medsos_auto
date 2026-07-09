from django.db import models

# Create your models here.


class VideoTemplate(models.Model):
    name = models.CharField(max_length=100)
    template_data = models.JSONField()

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'VideoTemplate'
        verbose_name = 'Video Template'
        verbose_name_plural = 'Video Templates'

class Content(models.Model):

    title = models.CharField(max_length=255)

    text_1 = models.TextField()
    text_2 = models.TextField(blank=True)
    text_3 = models.TextField(blank=True)
    text_4 = models.TextField(blank=True)
    text_5 = models.TextField(blank=True)

    template = models.ForeignKey(
        VideoTemplate,
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=20,
        default="pending"
    )

class RenderJob(models.Model):

    STATUS = [
        ("pending", "Pending"),
        ("rendering", "Rendering"),
        ("done", "Done"),
        ("failed", "Failed")
    ]

    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE
    )

    output_video = models.FileField(
        upload_to="renders/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
