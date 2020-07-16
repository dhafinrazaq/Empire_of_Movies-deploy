from django.forms import ModelForm
from .models import Review
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class ReviewCreateForm(ModelForm):
    class Meta:
        model = Review
        # Define fields you want here, it is best practice not to use '__all__'
        fields = ["title", "body", "rating"]

    def clean(self):
        cleaned_data = super(ReviewCreateForm, self).clean()

        title = cleaned_data.get('title')
        body = cleaned_data.get('body')
        rating = cleaned_data.get('rating')

        # Values may be None if the fields did not pass previous validations.
        if title is not None and body is not None and rating is not None:
            # If fields have values, perform validation:
            if rating >= 1 and rating <= 10:
                # Use None as the first parameter to make it a non-field error.
                # If you feel is related to a field, use this field's name.
                self.add_error(None, ValidationError('Rating must be between 1 and 10'))

        # Required only if Django version < 1.7 :
        return cleaned_data


# class ReviewCreateForm(forms.Form):
#     title = forms.CharField(label='Title', max_length=255)
#     body = forms.CharField(widget=forms.Textarea)
#     rating = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])




