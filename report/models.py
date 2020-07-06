from django.db import models
from articles.models import Discussion, Review, Comment
from threadedcomments.models import ThreadedComment
from django.contrib.auth import get_user_model

class Report(models.Model):
    short_reason = models.CharField(max_length=255)
    long_reason = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        related_name='reports',
        on_delete=models.CASCADE,
    )
    reported = models.ForeignKey(
        get_user_model(),
        related_name="reported",
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    discussion = models.ForeignKey(
        Discussion,
        default=None,
        on_delete=models.CASCADE,
        related_name='discussion_report',
        blank=True,
        null=True,
    )
    review = models.ForeignKey(
        Review,
        default=None,
        on_delete=models.CASCADE,
        related_name='review_report',
        blank=True,
        null=True,
    )
    comment = models.ForeignKey(
        ThreadedComment,
        default=None,
        on_delete=models.CASCADE,
        related_name='comment_report',
        blank=True,
        null=True,
    )
    
    def __str__(self): 
        return self.short_reason or ' '

    @classmethod
    def create(self, reported, reporter, short_reason, long_reason, discussion, review, comment):
        report = self(short_reason=short_reason, long_reason=long_reason, discussion=discussion, \
            review=review, comment=comment, author=reporter, reported=reported)
        return report

    # def get_absolute_url(self):
    #     return reverse('', args=[str(self.movie.id), str(self.id)])