from django import template
import re

register = template.Library()

@register.filter(name='camel_case_to_words_first_letter_uppercase')
def camel_case_to_words_first_letter_uppercase(camel_case_string):
    words = re.sub(r"([A-Z])", r" \1", camel_case_string).split()
    if words:
        words = [word.capitalize() for word in words] #capitalize the first letter of each word
    return " ".join(words).strip()