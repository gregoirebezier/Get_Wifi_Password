import platform
import subprocess
from typing import Any, Dict
import ctypes
import locale
from translate import Translator
from langcodes import *


class BCScan:
    def __init__(self) -> None:
        self.json_output: Dict[Any, Any] = {}

    def collect(self) -> Dict[Any, Any]:
        ...


class CollectSSID(BCScan):
    def __init__(self) -> None: # Init the class
        super().__init__()

    def Translate(self, text, lang):
        translator= Translator(to_lang=lang) # Translate the text to the language of the system
        translation = translator.translate(text) # Translate the text to the language of the system
        return translation # Return the translation

    def collect(self) -> Dict[Any, Any]:
        if not platform.uname().system.lower() == "windows": # Check if the system is windows
            raise OSError("Requires the Windows operating system") # Raise an error if the system is not windows
        ssid_pw_map: Dict[Any, Any] = {} # Create a dictionary
        data = str(subprocess.check_output(
            ["netsh", "wlan", "show", "profiles"])) # Get the output of the command
        data = data.replace("\\r", "")
        data = data.replace("\\n", "")
        data = data.split("\\xff")
        TranslateSentence = "Profil Tous les utilisateurs"
        TranslateSentence2 = "Contenu de la cl\\x82            : "
        TranslateSentence3 = "\\r\\n\\r\\nParam"
        windll = ctypes.windll.kernel32 # Get the language of the system
        windll.GetUserDefaultUILanguage() # Get the language of the system
        lang = locale.windows_locale[windll.GetUserDefaultUILanguage()].split("_")[0] # Get the language of the system, ex: fr, en, es, etc.
        RealLang = Language.get(lang).display_name(lang) # Get the real name of the language, ex: fr = French, en = English, es = Spanish, etc.
        if (lang != "fr"):
            TranslateSentence = self.Translate("Profil Tous les utilisateurs", RealLang) # Translate the sentence to the language of the system
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
                ["netsh", "wlan", "show", "profiles", ssid, "key=clear"])) # Get the output of the command
            results = results[results.find(
                TranslateSentence2):]
            results = results.replace(
                TranslateSentence2, "")
            results = results[:results.find(TranslateSentence3)] # Get the password
            if (results):
                ssid_pw_map.setdefault(ssid, results) # Add the ssid and the password to the dictionary
            else:
                print("No password found for SSID: {}".format(ssid)) # Print if there is no password
        for ssid, pw in ssid_pw_map.items():
            print("SSID: {} | Password: {}".format(ssid, pw)) # Print the ssid and the password
        return 0

def main():
    ssid_collector = CollectSSID() # Create an instance of the class
    ssid_collector.collect() # Call the function


if __name__ == "__main__":
    main()