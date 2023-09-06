"""
    Style manager
"""

# pylint: disable=C0301,C0103,C0303,C0411

from dataclasses import dataclass


@dataclass
class StyleItem:
    """Style item"""
    name : str

class StyleManager:
    """Class to save style options"""

    CUSTOM_STYLE = 'Custom'

    __STYLE_LIST : list[StyleItem] = [
        StyleItem('Salesman'),
        StyleItem('Happy Potter'),
        StyleItem('Happy New Year congratulation'),
        StyleItem('Shakespeare'),
        StyleItem('For a five year old'),
        StyleItem(CUSTOM_STYLE),
    ]

    def get_style_list(self) -> list[StyleItem]:
        """Get list of styles"""
        return  self.__STYLE_LIST
    
    def get_style_str_list(self) -> list[str]:
        """Get list of styles"""
        return  [s.name for s in self.__STYLE_LIST]