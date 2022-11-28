import platform
import subprocess
from typing import Any, Dict
import ctypes
import locale
from translate import Translator

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
        windll = ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()
        lang = locale.windows_locale[windll.GetUserDefaultUILanguage()].split("_")[0]
        if (lang != "fr"):
            TranslateSentence = self.Translate("Profil Tous les utilisateurs", lang)
        profiles = []
        for line in data:
            line = line.replace(TranslateSentence, "")
            line = line.replace("        ", "")
            line = line.replace(": ", "")
            line = line.replace('"', '')
            if (len(line) >= 30):
                continue
            profiles.append(line)
        if (lang != "fr"):
            TranslateSentence2 = self.Translate("Contenu de la clée", lang)
            TranslateSentence2 += "            : "
            TranslateSentence3 = self.Translate("Paramètres", lang)
            TranslateSentence3 = "\\r\\n\\r\\n" + TranslateSentence3
        else:
            TranslateSentence2 = "Contenu de la cl\\x82            : "
            TranslateSentence3 = "\\r\\n\\r\\nParam"
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