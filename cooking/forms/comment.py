from django import forms

from cooking.models import Comment


class CommentForm(forms.ModelForm):
    """Форма для написания комментария"""

    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "текст вашего комментария",
                },
            )
        }
