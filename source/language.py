"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import pkg_resources
import configparser

class Language:

    _regions:dict = {
        "af": "Afrikaans",
        "ar-ae": "Arabic (U.A.E.)",
        "ar-bh": "Arabic (Bahrain)",
        "ar-dz": "Arabic (Algeria)",
        "ar-eg": "Arabic (Egypt)",
        "ar-iq": "Arabic (Iraq)",
        "ar-jo": "Arabic (Jordan)",
        "ar-kw": "Arabic (Kuwait)",
        "ar-lb": "Arabic (Lebanon)",
        "ar-ly": "Arabic (Libya)",
        "ar-ma": "Arabic (Morocco)",
        "ar-om": "Arabic (Oman)",
        "ar-qa": "Arabic (Qatar)",
        "ar-sa": "Arabic (Saudi Arabia)",
        "ar-sy": "Arabic (Syria)",
        "ar-tn": "Arabic (Tunisia)",
        "ar-ye": "Arabic (Yemen)",
        "be": "Belarusian",
        "bg": "Bulgarian",
        "ca": "Catalan",
        "cs": "Czech",
        "cy": "Welsh",
        "da": "Danish",
        "de": "German (Standard)",
        "de-at": "German (Austria)",
        "de-ch": "German (Switzerland)",
        "de-li": "German (Liechtenstein)",
        "de-lu": "German (Luxembourg)",
        "el": "Greek",
        "en": "English",
        "en-au": "English (Australia)",
        "en-bz": "English (Belize)",
        "en-ca": "English (Canada)",
        "en-gb": "English (United Kingdom)",
        "en-ie": "English (Ireland)",
        "en-jm": "English (Jamaica)",
        "en-nz": "English (New Zealand)",
        "en-tt": "English (Trinidad)",
        "en-us": "English (United States)",
        "en-za": "English (South Africa)",
        "es": "Spanish (Spain)",
        "es-ar": "Spanish (Argentina)",
        "es-bo": "Spanish (Bolivia)",
        "es-cl": "Spanish (Chile)",
        "es-co": "Spanish (Colombia)",
        "es-cr": "Spanish (Costa Rica)",
        "es-do": "Spanish (Dominican Republic)",
        "es-ec": "Spanish (Ecuador)",
        "es-gt": "Spanish (Guatemala)",
        "es-hn": "Spanish (Honduras)",
        "es-mx": "Spanish (Mexico)",
        "es-ni": "Spanish (Nicaragua)",
        "es-pa": "Spanish (Panama)",
        "es-pe": "Spanish (Peru)",
        "es-pr": "Spanish (Puerto Rico)",
        "es-py": "Spanish (Paraguay)",
        "es-sv": "Spanish (El Salvador)",
        "es-uy": "Spanish (Uruguay)",
        "es-ve": "Spanish (Venezuela)",
        "et": "Estonian",
        "eu": "Basque",
        "fa": "Farsi",
        "fi": "Finnish",
        "fo": "Faeroese",
        "fr": "French (Standard)",
        "fr-be": "French (Belgium)",
        "fr-ca": "French (Canada)",
        "fr-ch": "French (Switzerland)",
        "fr-lu": "French (Luxembourg)",
        "ga": "Irish",
        "gd": "Gaelic (Scotland)",
        "he": "Hebrew",
        "hi": "Hindi",
        "hr": "Croatian",
        "hu": "Hungarian",
        "id": "Indonesian",
        "is": "Icelandic",
        "it": "Italian (Standard)",
        "it-ch": "Italian (Switzerland)",
        "ja": "Japanese",
        "ji": "Yiddish",
        "ko": "Korean (Johab)",
        "ku": "Kurdish",
        "lt": "Lithuanian",
        "lv": "Latvian",
        "mk": "Macedonian (FYROM)",
        "ml": "Malayalam",
        "ms": "Malaysian",
        "mt": "Maltese",
        "nb": "Norwegian (Bokmål)",
        "nl": "Dutch (Standard)",
        "nl-be": "Dutch (Belgium)",
        "nn": "Norwegian (Nynorsk)",
        "no": "Norwegian",
        "pa": "Punjabi",
        "pl": "Polish",
        "pt": "Portuguese (Portugal)",
        "pt-br": "Portuguese (Brazil)",
        "rm": "Rhaeto-Romanic",
        "ro": "Romanian",
        "ro-md": "Romanian (Republic of Moldova)",
        "ru": "Russian",
        "ru-md": "Russian (Republic of Moldova)",
        "sb": "Sorbian",
        "sk": "Slovak",
        "sl": "Slovenian",
        "sq": "Albanian",
        "sr": "Serbian",
        "sv": "Swedish",
        "sv-fi": "Swedish (Finland)",
        "th": "Thai",
        "tn": "Tswana",
        "tr": "Turkish",
        "ts": "Tsonga",
        "ua": "Ukrainian",
        "ur": "Urdu",
        "ve": "Venda",
        "vi": "Vietnamese",
        "xh": "Xhosa",
        "zh-cn": "Chinese (PRC)",
        "zh-hk": "Chinese (Hong Kong)",
        "zh-sg": "Chinese (Singapore)",
        "zh-tw": "Chinese (Taiwan)",
        "zu": "Zulu"
    }
    _config:configparser.ConfigParser
    _currentRegionCode:str = "en"

    @staticmethod
    def init():
        output = pkg_resources.resource_string(__name__, "/language.ini")
        Language._config = configparser.ConfigParser()
        Language._config.read_string(output.decode('utf-8'))
        Language._currentRegionCode = Language._config.get("config", "region")

    @staticmethod
    def getRegionName() -> str:
        return Language._regions[Language._currentRegionCode]

    @staticmethod
    def get(name: str) -> str:
        return Language._config.get(Language._currentRegionCode, name)
