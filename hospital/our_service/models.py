"""General project's models."""
from typing import Collection, Union
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

PRICE_VALIDATORS: list = [
    MinValueValidator(0, 'Нарх ай нол майда намешава.'),
    MaxValueValidator(100000, 'Ай 100000 зиёд? Навса бкап охи.')
]
MIN_MAX_PRICE_HELP_TEXT: str = 'If price is constant put 0.'


class HospitalServiceBaseModel(models.Model):
    """Hospital's and Service's base model.

    Attributes:
        name (CharField): The name of the hospital.
        description (TextField): The description of the hospital.
        average_rank (FloatField): The hospitals's average rank
    (note: calculates automaticly).
    """

    name = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    average_rank = models.FloatField(editable=False)

    def save(self, *args, **kwargs) -> None:
        """Save object to database."""
        super().save(*args, **kwargs)
        all_ranks = self.ranks.all()
        if not all_ranks.count():
            total_rank = sum(rank.value for rank in all_ranks)
            self.average_rank = total_rank / len(all_ranks)
        else:
            self.average_rank = 0
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return string to show when call str() method on current object."""
        return self.name[:20]

    class Meta:
        """Meta data of the class."""

        abstract = True


class Hospital(HospitalServiceBaseModel):
    """The hospitals.

    Attributes:
        name (CharField): The name of the hospital.
        description (TextField): The description of the hospital.
        work_time (TextField): The work time of the hospital in format
    "Mon-Fri 8:00-22:00(a break 12:00-13:00), Sat 8:00-20:00(...), Sun Closed".
        small_imgae (ImageField): The image with resolution 450x600.
        big_imgage (ImageField): The image with resoulution 1920x1080.
        comments (ManyToManyField(Comment)): Hospital's comments.
        ranks (ManyToManyField(Rank)): Hospital's ranks.
        average_rank (FloatField): The hospitals's average rank
    (note: calculates automaticly).
    """

    work_time = models.TextField(max_length=256)
    small_image = models.ImageField(upload_to='hospital_images')
    big_image = models.ImageField(upload_to='hospital_images')
    comments = models.ManyToManyField(
        'Comment', related_name='comments_from_hospital')
    ranks = models.ManyToManyField(
        'Rank', related_name='ranks_from_hospital')


class Service(HospitalServiceBaseModel):
    """The hospital's service.

    Attributes:
        name (CharField): The name of the service.
        description (TextField): The description of the service.
        price (FloatField): The price of the service
    (note: if price is not constant put 0).
        min_price (FloatField): The min_price of the service
    (note: if price is constant put 0).
        max_price (FloatField): The max_price of the service
    (note: if price is constant put 0).
        hospital (ForeignKey(Hospital)): Service's hospital.
        comments (ManyToManyField(Comment)): Service's comments.
        ranks (ManyToManyField(Rank)): Service's ranks.
        average_rank (FloatField): The service's average rank
    (note: calculates automaticly).
    """

    price = models.FloatField(validators=PRICE_VALIDATORS,
                              help_text='If price is not constant put 0.',
                              default=0)
    min_price = models.FloatField(validators=PRICE_VALIDATORS,
                                  help_text=MIN_MAX_PRICE_HELP_TEXT,
                                  default=0)
    max_price = models.FloatField(validators=PRICE_VALIDATORS,
                                  help_text=MIN_MAX_PRICE_HELP_TEXT,
                                  default=0)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE,
                                 related_name='hospital')
    comments = models.ManyToManyField(
        'Comment', related_name='comments_from_service')
    ranks = models.ManyToManyField(
        'Rank', related_name='ranks_from_service')

    def clean_fields(
        self,
        exclude: Union[Collection[str], None] = None
    ) -> None:
        """Validate fields."""
        super().clean_fields(exclude)
        if self.price == 0 and self.min_price == 0 and self.max_price == 0:
            raise ValidationError(
                'The price of the service did not determined. '
                'Choose one couple of fields: (price) or'
                '(min_price and max_price).')
        if self.price == 0:
            if self.max_price < self.min_price:
                raise ValidationError(
                    'The "max_price" can not be less than "min_price."')
        else:
            if self.max_price != 0 or self.min_price > 0:
                raise ValidationError(
                    'You can only choose between determining these couple '
                    'of fields: (price) or (min_price and max_price).'
                )


class CommentRankBaseModel(models.Model):
    """Comment's and Rank's base model.

    Attributes:
        author (ForeignKey(User)): The author of the comment.
        created_at (DateTimeField): The time of comment's creation.
        updated_at (DateTimeField): The time of comment's updation.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta data of the CommentRankBaseModel class."""

        abstract = True
        ordering = ('updated_at',)


class Comment(CommentRankBaseModel):
    """Comments.

    Attributes:
        text (TextField): The text of the comment.
        author (ForeignKey(User)): The author of the comment.
        created_at (DateTimeField): The time of comment's creation.
        updated_at (DateTimeField): The time of comment's updation.
    """

    text = models.TextField(help_text='Comment text')


class Rank(CommentRankBaseModel):
    """Ranks.

    Attributes:
        value (IntegerField): The rank value from 0 to 10.
        author (ForeignKey(User)): The author of the rank.
        created_at (DateTimeField): The time of rank's creation.
        updated_at (DateTimeField): The time of rank's updation.
    """

    value = models.IntegerField(
        validators=[
            MinValueValidator(0, 'Rate can not be less than 0.'),
            MaxValueValidator(10, 'Rate can not be more than 10')]
    )
