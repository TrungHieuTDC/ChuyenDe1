from django import forms
from .models import Profile,BlogPost,Comment
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget

class BasicCKEditorWidget(CKEditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config['toolbar'] = [
        ['Bold', 'Italic', 'Underline'],
        ['FontSize'],
        ['Strike'],
        ['NumberedList', 'BulletedList', 'Blockquote', 'CreateDiv', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
        ['Styles', 'Format', 'Font', 'FontSize'],
]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','avatar','gender']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of the Blog'}),
            'content': BasicCKEditorWidget(),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Nhập nội dung bình luận của bạn...'})
        }


