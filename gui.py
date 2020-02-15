from gooey import Gooey

import main


@Gooey
def gooey_app():
    main.main()


if __name__ == "__main__":
    gooey_app()
