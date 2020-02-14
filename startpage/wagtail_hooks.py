from wagtail.admin.rich_text.converters.html_to_contentstate import (InlineStyleElementHandler)
from wagtail.core import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features

@hooks.register("register_rich_text_features")
def register_code_styling(features):
    """Add <code></code> to rich text editor"""

    # Step one - define variables
    feature_name = "code"  # the name of this feature
    type_ = "CODE"  # what it's called like in the DB
    tag = "code"  # the HTML Tag coming out of this

    # Step 2 - create control reference for Draftail
    control = {
        "type": type_,
        "label": "</>",
        "description": "Code style"
    }

    # Step 3 - add control reference to Draftail
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Step 4 - tell DB how our style should be mapped
    db_conversion = {
        "from_database_format": { tag: InlineStyleElementHandler(type_), },
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    # Step 5: Add mapping to DB
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6 (Optional): Register Feature with all rich text editors by default
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_center_text_styling(features):
    """Add <div style="text-align:center;"></div> to code"""
    # Step one - define variables
    feature_name = "center"  # the name of this feature
    type_ = "CENTER_TEXT"  # what it's called like in the DB
    tag = "div"  # the HTML Tag coming out of this

    # Step 2 - create control reference for Draftail
    control = {
        "type": type_,
        "label": "Center",
        "description": "Centered text",
        "style": {  # some CSS -- Draftail only!
            "display": "block",
            "text-align": "center",
        },
    }

    # Step 3 - add control reference to Draftail
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Step 4 - tell DB how our style should be mapped
    db_conversion = {
        "from_database_format": { tag: InlineStyleElementHandler(type_), },
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {"class": "d-block text-center",
                              "style": "", }
                }
            }
        }
    }

    # Step 5: Add mapping to DB
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6 (Optional): Register Feature with all rich text editors by default
    features.default_features.append(feature_name)

@hooks.register("register_rich_text_features")
def register_keyboard_key_styling(features):
    """Add <div style="text-align:center;"></div> to code"""
    # Step one - define variables
    feature_name = "keybrdkey"  # the name of this feature
    type_ = "KEYBOARD_KEY"  # what it's called like in the DB
    tag = "span"  # the HTML Tag coming out of this

    # Step 2 - create control reference for Draftail
    control = {
        "type": type_,
        "label": "⌨",
        "description": "Keyboard key",
        "style": {  # some CSS -- Draftail only!
            "background-color": "black",
            "color": "white",
        },
        "class": ("badge", "badge-primary", ),
    }

    # Step 3 - add control reference to Draftail
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Step 4 - tell DB how our style should be mapped
    db_conversion = {
        "from_database_format": { tag: InlineStyleElementHandler(type_), },
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {"class": "badge badge-primary",
                              "style": "", }
                }
            }
        }
    }

    # Step 5: Add mapping to DB
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6 (Optional): Register Feature with all rich text editors by default
    features.default_features.append(feature_name)
