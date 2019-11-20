from django.db import models

class AnalyzedRequirement(models.Model):
    PRIORITY_CHOICES = (
        (0, 'low'),
        (1, 'medium'),
        (2, 'high'),
    )

    IS_FUNCTIONAL_CHOICES = (
        (False, 'non-functional'),
        (True, 'functional'),
    )

    text = models.TextField(null=False, blank=False)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1, null=False, blank=False)
    is_functional = models.IntegerField(choices=IS_FUNCTIONAL_CHOICES, default=False, null=False, blank=False)

    def __str__(self):
        return '{} ({} | {})'.format(self.text, self.priority, self.is_functional)
