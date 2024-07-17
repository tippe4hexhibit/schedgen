import drawsvg as dw


class SchedulePane:
    def __init__(self, file_name="pane", width=554, height=768, fill=None,
                 max_rows=12,
                 heading_font_family='Gill Sans',
                 heading_1_text=None, heading_1_size=48, heading_1_weight='bold',
                 heading_1_color='#ffffff',
                 heading_2_text=None, heading_2_size=32, heading_2_weight='bold',
                 heading_2_color='#ffffff'
                 ):

        self._width = width
        self._height = height
        self._name = file_name

        self._HEADING_1_Y = 45
        self._HEADING_2_Y = 100
        self._FIRST_LINE_Y = 140

        self._background = dw.Group(id='background', fill='none')
        self._textarea = dw.Group(id='textarea', fill='none')

        self._current_row = 0
        self._current_subheading = None
        self._max_rows = max_rows

        self._file_name = file_name
        self._current_file = 0

        if fill:
            self._background.append(dw.Rectangle(0, 0,
                                                 "100%", "100%",
                                                 fill=fill))

        if heading_1_text:
            self._background.append(
                dw.Text(heading_1_text,
                        font_family=heading_font_family,
                        font_weight=heading_1_weight,
                        font_size=heading_1_size,
                        x=width / 2, y=self._HEADING_1_Y,
                        fill=heading_1_color,
                        dominant_baseline='hanging',
                        text_anchor='middle'))

        if heading_2_text:
            self._background.append(dw.Text(heading_2_text,
                                            font_family=heading_font_family,
                                            font_weight=heading_2_weight,
                                            font_size=heading_2_size,
                                            x=width / 2, y=self._HEADING_2_Y,
                                            fill=heading_2_color,
                                            dominant_baseline='hanging',
                                            text_anchor='middle'
                                            )
                                    )

    def add_subheading(self, subheading_text,
                       subheading_font_family='Gill Sans MT', subheading_size=28,
                       subheading_weight='bold', subheading_color='#ffffff',
                       ):

        if self._current_row >= self._max_rows - 2:
            self._cut_page()

        self._current_subheading = subheading_text

        self._textarea.append(dw.Text(subheading_text,
                                      font_family=subheading_font_family,
                                      font_weight=subheading_weight,
                                      font_size=subheading_size,
                                      x=15, y=self._FIRST_LINE_Y + ((subheading_size + 5) * self._current_row),
                                      fill=subheading_color,
                                      dominant_baseline='hanging',
                                      ))
        self._current_row += 1

    def add_text(self, text,
                 text_font_family='Gill Sans MT', text_font_size=24,
                 text_font_weight='', text_color='#ffffff',
                 ):

        if self._current_row >= self._max_rows - 2:
            self._cut_page()
            self.add_subheading(self._current_subheading)

        self._textarea.append(dw.Text(text,
                                      font_family=text_font_family,
                                      font_weight=text_font_weight,
                                      font_size=text_font_size,
                                      x=15, y=self._FIRST_LINE_Y + ((text_font_size + 5) * self._current_row),
                                      fill=text_color,
                                      dominant_baseline='hanging',
                                      ))
        self._current_row += 1

    def _cut_page(self):
        self.save_png()
        self.save_svg()

        self._textarea = dw.Group(id='textarea', fill='none')
        self._current_row = 0
        self._current_file += 1

    def _get_filename(self, file_name):
        return f'{file_name}_{str(self._current_file).zfill(3)}'

    def save_png(self,):
        d = dw.Drawing(self._width, self._height)
        d.append(self._background)
        d.append(self._textarea)
        d.save_png(f'{self._get_filename(self._file_name)}.png')

    def save_svg(self):
        d = dw.Drawing(self._width, self._height)
        d.append(self._background)
        d.append(self._textarea)
        d.save_svg(f'{self._get_filename(self._file_name)}.svg')
