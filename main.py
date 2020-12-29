from easygui import *
import logging
import os
from gui import Gui


production = True


def main():
    gui = Gui()
    gui.start()


dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.DEBUG, filename=f'{dir_path}/loklingsbane.log')

if production:
    try:
        main()
    except Exception as ex:
        msgbox(ex)
        logging.exception("Exception:")
else:
    main()
