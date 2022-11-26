import platform
import subprocess
from typing import Any, Dict


class BCScan:
    def __init__(self) -> None:
        self.json_output: Dict[Any, Any] = {}

    def collect(self) -> Dict[Any, Any]:
        ...


class CollectSSID(BCScan):
    def __init__(self) -> None:
        super().__init__()

    def collect(self) -> Dict[Any, Any]:
        if not platform.uname().system.lower() == "windows":
            raise OSError("Requires the Windows operating system")
        ssid_pw_map: Dict[Any, Any] = {}
        data = str(subprocess.check_output(
            ["netsh", "wlan", "show", "profiles"]))
        data = data.replace("\\r", "")
        data = data.replace("\\n", "")
        data = data.split("\\xff")
        # print(data)
        profiles = []
        for line in data:
            line = line.replace("Profil Tous les utilisateurs", "")
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
                "Contenu de la cl\\x82            : "):]
            results = results.replace(
                "Contenu de la cl\\x82            : ", "")
            results = results[:results.find("\\r\\n\\r\\nParam")]
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