python -m PyQt5.uic.pyuic ui_main.ui -o ui_main.py --from-imports
python -m PyQt5.uic.pyuic ui_nsfw_scann.ui -o ui_nsfw_scann.py --from-imports
::python3 -m PyQt5.uic.pyuic ui_main.ui -o ui_main.py --from-imports &&  python3 -m PyQt5.uic.pyuic ui_nsfw_scann.ui -o ui_nsfw_scann.py --from-imports