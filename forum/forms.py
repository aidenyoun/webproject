from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('notice', '공지사항'),
        ('free', '자유게시판'),
        ('question', '질문게시판'),
        ('review', '후기게시판'),
        ('suggestion', '건의사항'),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']