# tests/mommy.py

from ckeditor_uploader.fields import RichTextUploadingField
from model_mommy import mommy, random_gen


class CustomMommy(mommy.Mommy):
    """
    Extends the base Mommy class with custom field mappings
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Implement generator for CKEditor uploading field
        self.type_mapping[RichTextUploadingField] = random_gen.gen_text
