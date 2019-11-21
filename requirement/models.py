from django.db import models

from pythainlp.corpus.common import thai_words
from pythainlp.tag import pos_tag
from pythainlp import Tokenizer

THAI_WORDS = set(thai_words())
for i in open('requirement/data/custom_tokenizer.txt', encoding="utf-8"):
    THAI_WORDS.add(i.replace('\n', '').strip())

TOKENIZER = Tokenizer(THAI_WORDS)

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
    priority = models.IntegerField(choices=PRIORITY_CHOICES, null=True, blank=True)
    is_functional = models.BooleanField(choices=IS_FUNCTIONAL_CHOICES, null=True, blank=True)

    def __str__(self):
        return '{} ({} | {})'.format(self.text, self.priority, self.is_functional)

    def get_words(self):
        return TOKENIZER.word_tokenize(self.text)

    def get_pos_tag(self):
        return pos_tag(self.get_words())

    def get_pos_tag_refined(self, remove_list=('NCMN', 'RPRE', 'VACT', 'VATT', 'VSTA')):
        return [i for i in self.get_pos_tag() if i[1] not in remove_list and i[0] != ' ']
