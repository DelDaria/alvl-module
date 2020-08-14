from django.db import models
from django.conf import settings


USER_MODEL = settings.AUTH_USER_MODEL

PRIORITY_CHOICES = (
    ('Low', ("Low")),
    ('Medium', ("Medium")),
    ('High', ("High"))
    )

STATUS_CHOICES = (
    ('Draft', ("Draft")),
    ('Pending', ("Pending")),
    ('Declined', ("Declined")),
    ('In progress', ("In progress")),
    ('Done', ("Done"))
)


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Issue(TimeStampModel):
    author = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL,
                               blank=True, null=True)
    topic = models.CharField(max_length=80)
    text = models.CharField(max_length=500)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=11)
    status = models.CharField(choices=STATUS_CHOICES, default='Draft', max_length=11)
    i = models.PositiveSmallIntegerField(default=0)   # times of restoring
    reason = models.CharField(max_length=200, blank=True, null=True)   # reason of declining

    def __str__(self):
        return f"{self.topic}"


class Comment(TimeStampModel):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL,
                               blank=True, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}, {self.text}"

