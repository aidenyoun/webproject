from django import template

register = template.Library()

@register.filter
def category_to_korean(value):
    category_dict = {
        'notice': '공지사항',
        'free': '자유게시판',
        'question': '질문게시판',
        'review': '후기게시판',
        'suggestion': '건의사항'
    }
    return category_dict.get(value, value)