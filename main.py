# -*- coding: utf-8 -*-

import sys
import argparse
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

from windows.main_window import MainWindow

from singletons.state import app_state
from singletons.translator import translator
from singletons.config import config
from singletons.languages import languages

from storages.packages import PackagesStorage
from storages.dictionaries import DictionariesStorage

from themes.stylesheet import stylesheet

import resources.resource_rc


# Ajuste de diretório para executáveis PyInstaller
if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)


def main():
    parser = argparse.ArgumentParser(description="Sims 4 Translator Application")
    parser.add_argument("--translate", type=str, help="Text to translate via CLI")
    parser.add_argument("--engine", type=str, default="Google", help="Translation engine to use (Google or Bing)")
    args = parser.parse_args()

    if args.translate:
        # Initialize singletons for CLI usage
        _ = config # Access config to ensure it's loaded
        _ = languages # Access languages to ensure it's loaded

        # Temporarily set source and destination languages for CLI translation
        config.set_value("translation", "source", "ENG_US")
        config.set_value("translation", "destination", "POR_BR")

        response = translator.translate(args.engine, args.translate)
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Erro de tradução: {response.text}")
        sys.exit(0)

    sys.argv += [
        
    ]

    app = QApplication(sys.argv)

    packages_storage = PackagesStorage()
    dictionaries_storage = DictionariesStorage()

    app_state.set_packages_storage(packages_storage)
    app_state.set_dictionaries_storage(dictionaries_storage)

    QFontDatabase.addApplicationFont(":/fonts/roboto.ttf")
    QFontDatabase.addApplicationFont(":/fonts/jetbrainsmono.ttf")
    QFontDatabase.addApplicationFont(":/fonts/jetbrainsmono-semibold.ttf")

    app.setStyleSheet(stylesheet())

    window = MainWindow()
    window.show()

    exit_status = app.exec()

    app.setStyleSheet("")

    sys.exit(exit_status)


if __name__ == "__main__":
    main()



