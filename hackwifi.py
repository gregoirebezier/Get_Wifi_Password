import platform
import subprocess
from typing import Any, Dict
import ctypes
import locale
from translate import Translator

All_Lang = {
	'ab': 'Abkhaz',
	'aa': 'Afar',
	'af': 'Afrikaans',
	'ak': 'Akan',
	'sq': 'Albanian',
	'am': 'Amharic',
	'ar': 'Arabic',
	'an': 'Aragonese',
	'hy': 'Armenian',
	'as': 'Assamese',
	'av': 'Avaric',
	'ae': 'Avestan',
	'ay': 'Aymara',
	'az': 'Azerbaijani',
	'bm': 'Bambara',
	'ba': 'Bashkir',
	'eu': 'Basque',
	'be': 'Belarusian',
	'bn': 'Bengali',
	'bh': 'Bihari',
	'bi': 'Bislama',
	'bs': 'Bosnian',
	'br': 'Breton',
	'bg': 'Bulgarian',
	'my': 'Burmese',
	'ca': 'Catalan; Valencian',
	'ch': 'Chamorro',
	'ce': 'Chechen',
	'ny': 'Chichewa; Chewa; Nyanja',
	'zh': 'Chinese',
	'cv': 'Chuvash',
	'kw': 'Cornish',
	'co': 'Corsican',
	'cr': 'Cree',
	'hr': 'Croatian',
	'cs': 'Czech',
	'da': 'Danish',
	'dv': 'Divehi; Maldivian;',
	'nl': 'Dutch',
	'dz': 'Dzongkha',
	'en': 'English',
	'eo': 'Esperanto',
	'et': 'Estonian',
	'ee': 'Ewe',
	'fo': 'Faroese',
	'fj': 'Fijian',
	'fi': 'Finnish',
	'fr': 'French',
	'ff': 'Fula',
	'gl': 'Galician',
	'ka': 'Georgian',
	'de': 'German',
	'el': 'Greek, Modern',
	'gn': 'Guaraní',
	'gu': 'Gujarati',
	'ht': 'Haitian',
	'ha': 'Hausa',
	'he': 'Hebrew (modern)',
	'hz': 'Herero',
	'hi': 'Hindi',
	'ho': 'Hiri Motu',
	'hu': 'Hungarian',
	'ia': 'Interlingua',
	'id': 'Indonesian',
	'ie': 'Interlingue',
	'ga': 'Irish',
	'ig': 'Igbo',
	'ik': 'Inupiaq',
	'io': 'Ido',
	'is': 'Icelandic',
	'it': 'Italian',
	'iu': 'Inuktitut',
	'ja': 'Japanese',
	'jv': 'Javanese',
	'kl': 'Kalaallisut',
	'kn': 'Kannada',
	'kr': 'Kanuri',
	'ks': 'Kashmiri',
	'kk': 'Kazakh',
	'km': 'Khmer',
	'ki': 'Kikuyu, Gikuyu',
	'rw': 'Kinyarwanda',
	'ky': 'Kirghiz, Kyrgyz',
	'kv': 'Komi',
	'kg': 'Kongo',
	'ko': 'Korean',
	'ku': 'Kurdish',
	'kj': 'Kwanyama, Kuanyama',
	'la': 'Latin',
	'lb': 'Luxembourgish',
	'lg': 'Luganda',
	'li': 'Limburgish',
	'ln': 'Lingala',
	'lo': 'Lao',
	'lt': 'Lithuanian',
	'lu': 'Luba-Katanga',
	'lv': 'Latvian',
	'gv': 'Manx',
	'mk': 'Macedonian',
	'mg': 'Malagasy',
	'ms': 'Malay',
	'ml': 'Malayalam',
	'mt': 'Maltese',
	'mi': 'Māori',
	'mr': 'Marathi (Marāṭhī)',
	'mh': 'Marshallese',
	'mn': 'Mongolian',
	'na': 'Nauru',
	'nv': 'Navajo, Navaho',
	'nb': 'Norwegian Bokmål',
	'nd': 'North Ndebele',
	'ne': 'Nepali',
	'ng': 'Ndonga',
	'nn': 'Norwegian Nynorsk',
	'no': 'Norwegian',
	'ii': 'Nuosu',
	'nr': 'South Ndebele',
	'oc': 'Occitan',
	'oj': 'Ojibwe, Ojibwa',
	'cu': 'Old Church Slavonic',
	'om': 'Oromo',
	'or': 'Oriya',
	'os': 'Ossetian, Ossetic',
	'pa': 'Panjabi, Punjabi',
	'pi': 'Pāli',
	'fa': 'Persian',
	'pl': 'Polish',
	'ps': 'Pashto, Pushto',
	'pt': 'Portuguese',
	'qu': 'Quechua',
	'rm': 'Romansh',
	'rn': 'Kirundi',
	'ro': 'Romanian, Moldavan',
	'ru': 'Russian',
	'sa': 'Sanskrit (Saṁskṛta)',
	'sc': 'Sardinian',
	'sd': 'Sindhi',
	'se': 'Northern Sami',
	'sm': 'Samoan',
	'sg': 'Sango',
	'sr': 'Serbian',
	'gd': 'Scottish Gaelic',
	'sn': 'Shona',
	'si': 'Sinhala, Sinhalese',
	'sk': 'Slovak',
	'sl': 'Slovene',
	'so': 'Somali',
	'st': 'Southern Sotho',
	'es': 'Spanish; Castilian',
	'su': 'Sundanese',
	'sw': 'Swahili',
	'ss': 'Swati',
	'sv': 'Swedish',
	'ta': 'Tamil',
	'te': 'Telugu',
	'tg': 'Tajik',
	'th': 'Thai',
	'ti': 'Tigrinya',
	'bo': 'Tibetan',
	'tk': 'Turkmen',
	'tl': 'Tagalog',
	'tn': 'Tswana',
	'to': 'Tonga',
	'tr': 'Turkish',
	'ts': 'Tsonga',
	'tt': 'Tatar',
	'tw': 'Twi',
	'ty': 'Tahitian',
	'ug': 'Uighur, Uyghur',
	'uk': 'Ukrainian',
	'ur': 'Urdu',
	'uz': 'Uzbek',
	've': 'Venda',
	'vi': 'Vietnamese',
	'vo': 'Volapük',
	'wa': 'Walloon',
	'cy': 'Welsh',
	'wo': 'Wolof',
	'fy': 'Western Frisian',
	'xh': 'Xhosa',
	'yi': 'Yiddish',
	'yo': 'Yoruba',
	'za': 'Zhuang, Chuang',
	'zu': 'Zulu',
}


class BCScan:
    def __init__(self) -> None:
        self.json_output: Dict[Any, Any] = {}

    def collect(self) -> Dict[Any, Any]:
        ...


class CollectSSID(BCScan):
    def __init__(self) -> None:
        super().__init__()

    def Translate(self, text, lang):
        translator= Translator(to_lang=lang)
        translation = translator.translate(text)
        return translation

    def collect(self) -> Dict[Any, Any]:
        if not platform.uname().system.lower() == "windows":
            raise OSError("Requires the Windows operating system")
        ssid_pw_map: Dict[Any, Any] = {}
        data = str(subprocess.check_output(
            ["netsh", "wlan", "show", "profiles"]))
        data = data.replace("\\r", "")
        data = data.replace("\\n", "")
        data = data.split("\\xff")
        TranslateSentence = "Profil Tous les utilisateurs"
        TranslateSentence2 = "Contenu de la cl\\x82            : "
        TranslateSentence3 = "\\r\\n\\r\\nParam"
        windll = ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()
        lang = locale.windows_locale[windll.GetUserDefaultUILanguage()].split("_")[0]
        RealLang = ""
        for key, value in All_Lang.items():
            if key == lang:
                RealLang = value
        if (lang != "fr"):
            TranslateSentence = self.Translate("Profil Tous les utilisateurs", RealLang)
            TranslateSentence2 = self.Translate("Contenu de la clée", RealLang)
            TranslateSentence2 += "            : "
            TranslateSentence3 = self.Translate("Paramètres", RealLang)
            TranslateSentence3 = "\\r\\n\\r\\n" + TranslateSentence3
        profiles = []
        for line in data:
            line = line.replace(TranslateSentence, "")
            line = line.replace("        ", "")
            line = line.replace(": ", "")
            line = line.replace('"', '')
            if (len(line) >= 30):
                continue
            profiles.append(line)
        for ssid in profiles:
            results = str(subprocess.check_output(
                ["netsh", "wlan", "show", "profiles", ssid, "key=clear"]))
            results = results[results.find(
                TranslateSentence2):]
            results = results.replace(
                TranslateSentence2, "")
            results = results[:results.find(TranslateSentence3)]
            if (results):
                ssid_pw_map.setdefault(ssid, results)
            else:
                print("No password found for SSID: {}".format(ssid))
        for ssid, pw in ssid_pw_map.items():
            print("SSID: {} | Password: {}".format(ssid, pw))
        return 0

def main():
    ssid_collector = CollectSSID()
    ssid_collector.collect()


if __name__ == "__main__":
    main()