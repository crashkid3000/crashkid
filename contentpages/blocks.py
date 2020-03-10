from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndParagraphBlock(blocks.StructBlock):
    """A title and a rich text block"""

    title = blocks.CharBlock(max_length=150, required=False, help_text="A title for the below text")
    text = blocks.RichTextBlock(required=True, help_text="The text for this paragraph")

    class Meta:
        template = "blocks/title_and_paragraph.html"
        icon = "edit"
        label = "Titled Paragraph"


class TitleAndParagraphWithImage(blocks.StructBlock):
    """A title and a text block, with a nice image scrolling by below that"""

    title = blocks.CharBlock(max_length=150, required=False, help_text="A title for the below text")
    text = blocks.RichTextBlock(required=True, help_text="The text for this paragraph")
    image = ImageChooserBlock(required=True, help_text="The image below the text that scrolls by")
    caption = blocks.CharBlock(max_length=500, required=False, help_text="A caption to describe the image")

    class Meta:
        template = "blocks/title_and_paragraph_with_image.html"
        icon = "edit"
        label = "Titled Paragraph, with Image"



