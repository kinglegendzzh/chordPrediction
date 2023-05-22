from flexx import app, ui
class KeyRecorder(ui.Widget):
    def init(self):
        # self.keylog = react.String('')
        self.keydown.connect(self._on_key_down)
        self.keyup.connect(self._on_key_up)

    def _on_key_down(self, e):
        key = e.key
        self.keylog += 'Key Down: ' + key + '\n'

    def _on_key_up(self, e):
        key = e.key
        self.keylog += 'Key Up: ' + key + '\n'

    def render(self):
        return ui.VBox(
            ui.Label(text='Press keys and see events in log:'),
            ui.TextArea(text=self.keylog)
        )

if __name__ == '__main__':
    m = app.launch(KeyRecorder)
    app.run()