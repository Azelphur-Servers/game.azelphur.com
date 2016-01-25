from django.db import models
from markdown import markdown


class FAQ(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    body_html = models.TextField(
        editable=False,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.body_html = markdown(self.body)
        super(FAQ, self).save(*args, **kwargs)
