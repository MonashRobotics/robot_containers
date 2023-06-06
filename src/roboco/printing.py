
from InquirerPy import get_style

green = "#00ffa1"
red = "#ff5858"
yellow = "#e5e512"
blue = "#61afef"
style = get_style(
    {"input": blue, "questionmark": yellow, "answermark": f"{green} bold"},
    style_override=False,
)
orange = "#ff4c05"
tick = "\u2714"
