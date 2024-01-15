from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall('[a-zA-Z]', password) or not re.findall('[0-9]', password):
            raise ValidationError(
                "비밀번호는 영문자와 숫자를 모두 포함해야 합니다.",
                code='password_no_number_or_letter',
            )

    def get_help_text(self):
        return "비밀번호는 영문자와 숫자를 모두 포함해야 합니다."