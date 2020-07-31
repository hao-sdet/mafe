from cement import App
from cement.core.exc import CaughtSignal
from .controllers import BaseController


class Mafe(App):
    class Meta:
        label = 'mafe'
        exit_on_close = True
        extensions = ['tabulate']
        output_handler = 'tabulate'
        handlers = [
            BaseController
        ]


def main():
    with Mafe() as app:
        try:
            app.run()
        except CaughtSignal as e:
            app.log.error(f'\n {e}')
        finally:
            app.close()


if __name__ == '__main__':
    main()