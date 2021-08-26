import urllib.request
import zipfile
import io
import argparse
import sys

setup_domain = "setup.roblox.com"

client_types = {
    "player": [
        ("RobloxApp.zip", ""),
        ("content-avatar.zip", "content\\avatar\\"),
        ("content-configs.zip", "content\\configs\\"),
        ("content-fonts.zip", "content\\fonts\\"),
        ("content-sky.zip", "content\\sky\\"),
        ("content-sounds.zip", "content\\sounds\\"),
        ("content-textures2.zip", "content\\textures\\"),
        ("content-models.zip", "content\\models\\"),
        ("content-textures3.zip", "PlatformContent\\pc\\textures\\"),
        ("content-terrain.zip", "PlatformContent\\pc\\terrain\\"),
        ("content-platform-fonts.zip", "PlatformContent\\pc\\fonts\\"),
        ("extracontent-luapackages.zip", "ExtraContent\\LuaPackages\\"),
        ("extracontent-translations.zip", "ExtraContent\\translations\\"),
        ("extracontent-models.zip", "ExtraContent\\models\\"),
        ("extracontent-textures.zip", "ExtraContent\\textures\\"),
        ("extracontent-places.zip", "ExtraContent\\places\\"),
        ("shaders.zip", "shaders\\"),
        ("ssl.zip", "ssl\\"),
        ("content-luapackages.zip", "content\\LuaPackages\\"),
        ("content-translations.zip", "content\\translations\\")
    ],
    "studio": [
        ("redist.zip", ""),
        ("RobloxStudio.zip", ""),
        ("Libraries.zip", ""),
        ("content-avatar.zip", "content\\avatar\\"),
        ("content-configs.zip", "content\\configs\\"),
        ("content-fonts.zip", "content\\fonts\\"),
        ("content-sky.zip", "content\\sky\\"),
        ("content-sounds.zip", "content\\sounds\\"),
        ("content-textures2.zip", "content\\textures\\"),
        ("content-models.zip", "content\\models\\"),
        ("content-textures3.zip", "PlatformContent\\pc\\textures\\"),
        ("content-terrain.zip", "PlatformContent\\pc\\terrain\\"),
        ("content-platform-fonts.zip", "PlatformContent\\pc\\fonts\\"),
        ("content-qt_translations.zip", "content\\qt_translations\\"),
        ("extracontent-scripts.zip", "ExtraContent\\scripts\\"),
        ("extracontent-luapackages.zip", "ExtraContent\\LuaPackages\\"),
        ("extracontent-translations.zip", "ExtraContent\\translations\\"),
        ("extracontent-models.zip", "ExtraContent\\models\\"),
        ("extracontent-textures.zip", "ExtraContent\\textures\\"),
        ("shaders.zip", "shaders\\"),
        ("BuiltInPlugins.zip", "BuiltInPlugins\\"),
        ("BuiltInStandalonePlugins.zip", "BuiltInStandalonePlugins\\"),
        ("LibrariesQt5.zip", ""),
        ("Plugins.zip", "Plugins\\"),
        ("Qml.zip", "Qml\\"),
        ("StudioFonts.zip", "StudioFonts\\"),
        ("ssl.zip", "ssl\\"),
        ("content-translations.zip", "content\\translations\\")
    ]
}

def printraw(str):
    sys.stdout.write("\r%s" % str)
    sys.stdout.flush()

def download(version_hash, name, path):
    printraw("Downloading %s-%s" % (version_hash, name))
    try:
        with urllib.request.urlopen("http://%s/%s-%s" % (setup_domain, version_hash, name)) as res:
            with zipfile.ZipFile(io.BytesIO(res.read()), "r") as zf:
                zf.extractall("%s/%s" % (version_hash, path))
    except Exception:
        printraw("Failed to download %s-%s \n" % (version_hash, name))
    else:
        printraw("Downloaded %s-%s  \n" % (version_hash, name))

def main():
    global setup_domain
    parser = argparse.ArgumentParser()
    parser.add_argument("-ct", help="client type (%s)" % ", ".join(client_types.keys()))
    parser.add_argument("-vh", help="version hash")
    parser.add_argument("-sd", help="setup domain (default %s)" % setup_domain)
    parser.add_argument("-dl", help="download a roblox launcher for easy launching through browser", action="store_true")
    args = parser.parse_args()

    if not args.ct in client_types:
        print("Invalid client type")
        exit(1)
    elif not args.vh:
        print("No specified version hash")
        exit(1)
    elif args.sd:
        setup_domain = args.sd
        print("Setup domain set to", setup_domain)

    for file in client_types[args.ct]:
        download(args.vh, *file)
    with open("%s/AppSettings.xml" % args.vh, "x", encoding="utf8") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Settings>\n   <ContentFolder>content</ContentFolder>\n	<BaseUrl>http://www.roblox.com</BaseUrl>\n</Settings>\n")
        print("Created %s/AppSettings.xml" % args.vh)

    if args.dl:
        printraw("Downloading roblox launcher")
        try:
            with urllib.request.urlopen("https://github.com/yafyz/roblox_player_launcher/releases/download/h/main.exe") as res:
                with open("%s/RobloxPlayerLauncher.exe" % args.vh, "xb") as f:
                    f.write(res.read())
        except Exception:
            printraw("Failed to download roblox launcher\n")
        else:
            printraw("Downloaded roblox launcher  \n")


if __name__ == "__main__":
    main()