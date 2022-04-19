import html

from htbuilder import H, HtmlElement, styles
from htbuilder.units import unit
import streamlit as st
# Only works in 3.7+: from htbuilder import div, span
div = H.div
span = H.span

# Only works in 3.7+: from htbuilder.units import px, rem, em
px = unit.px
rem = unit.rem
em = unit.em

# Colors from the Streamlit palette.
# These are red-70, orange-70, ..., violet-70, gray-70.
PALETTE = [
    "#ff4b4b",
    "#ffa421",
    "#ffe312",
    "#21c354",
    "#00d4b1",
    "#00c0f2",
    "#1c83e1",
    "#803df5",
    "#808495",
]

OPACITIES = [
    "33", "66",
]

def highlight(body, background=None, color=None, **style):
    """Build an HtmlElement span object with the given body.
    The end result will look something like this:
        [body]
    Parameters
    ----------
    body : string
        The string to put in the "body" part .
    background : string or None (should be string)
        The color to use for the background "chip" containing this highlight.
        If None, will use a random color based on the label.
    color : string or None
        The color to use for the body.
        If None, will use the document's default text color.
    style : dict
        Any CSS you want to apply to the containing "chip". This is useful for things like
    Examples
    --------
    Produce a simple annotation with default colors:
    >>> highlight("apple")
    >>> highlight("apple", background="#FF0", color="black")
    >>> highlight("apple", background="#FF0", border="1px dashed red")
    """

    color_style = {}

    if color:
        color_style['color'] = color

    if not background:
        '''
        Updated Soon 
        Don't recommend 
        '''
        label_sum = sum(ord(c) for c in label)
        background_color = PALETTE[label_sum % len(PALETTE)]
        background_opacity = OPACITIES[label_sum % len(OPACITIES)]
        background = background_color + background_opacity

    return (
        span(
            style=styles(
                background=background,
                border_radius=rem(0.33),
                padding=(rem(0.125), rem(0.5)),
                overflow="hidden",
                **color_style,
                **style,
            ))
            (

            html.escape(body),

        )
    )


def get_highlighted_html(*args):
    """Writes text with highlights into an HTML string.
    Parameters
    ----------
    *args : see highlighted_text()
    Returns
    -------
    str
        An HTML string.
    """

    out = div()

    for arg in args:
        if isinstance(arg, str):
            out(html.escape(arg))

        elif isinstance(arg, HtmlElement):
            out(arg)

        elif isinstance(arg, tuple):
            out(highlight(*arg))

        else:
            raise Exception("Oh noes!")

    return out


def highlighted_text(*args):
    """Writes text with annotations into your Streamlit app.
    Parameters
    ----------
    *args : str, tuple or htbuilder.HtmlElement
        Arguments can be:
        - strings, to draw the string as-is on the screen.
        - tuples of the form (main_text, background, color) where
          background and foreground colors are optional and should be an CSS-valid string such as
          "#aabbcc" or "rgb(10, 20, 30)"
        - HtmlElement objects in case you want to customize the annotations further. In particular,
          you can import the `highlight()` function from this module to easily produce annotations
          whose CSS you can customize via keyword arguments.
    Examples
    --------
    >>> highlight_text(
    ...     "This ",
    ...     ("is", "#8ef"),
    ...     " some ",
    ...     ("annotated", "#faa"),
    ...     ("text", "#afa"),
    ...     " for those of ",
    ... )
    >>> highlighted_text(
    ...     "Hello ",
    ...     highlight("world!", color="#8ef", border="1px dashed red"),
    ... )
    """
    st.markdown(
        get_highlighted_html(*args),
        unsafe_allow_html=True,
    )


if __name__=="__main__": 
    a = ("hihi","#8ef")
    x = get_highlighted_html(a)
    print("\n")
    y = highlight("hihi","#8ef")
    print(y)