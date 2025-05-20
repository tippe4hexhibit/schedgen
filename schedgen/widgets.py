import drawsvg as dw
import logging

from pathlib import Path

log = logging.getLogger(__name__)

def split_string(text, max_length):
    split_strings = []
    words = ""
    for word in text.split(' '):
        if len(words) + len(word) > max_length:
            split_strings.append(words.strip())
            words = ""

        words += f'{word} '

    if len(words) > 0:
        split_strings.append(words.strip())

    return split_strings

class SchedulePane:
    def __init__(self, output_path=Path.cwd(),
                 file_name="pane",
                 width=554, height=768, fill=None,
                 max_rows=19,
                 heading_font_family='Gill Sans',
                 heading_1_text=None, heading_1_size=48, heading_1_weight='bold',
                 heading_1_color='#ffffff',
                 heading_2_text=None, heading_2_size=32, heading_2_weight='bold',
                 heading_2_color='#ffffff'
                 ):

        self._width = width
        self._height = height
        self._name = file_name

        self._HEADING_1_Y = 25
        self._HEADING_2_Y = 80
        self._FIRST_LINE_Y = 120

        self._background = dw.Group(id='background', fill='none')
        self._textarea = dw.Group(id='textarea', fill='none')

        self._current_row = 0
        self._current_y = self._FIRST_LINE_Y
        self._current_subheading = None
        self._max_rows = max_rows

        self._output_path = output_path
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
                                            text_anchor='middle'))

    def add_subheading(self, subheading_text,
                       subheading_font_family='Gill Sans MT', subheading_size=26,
                       subheading_weight='bold', subheading_color='#ffffff'):

        self._current_subheading = subheading_text
        if self._current_row > self._max_rows - 4:
            self._cut_page()
        else:
            self._current_y += (subheading_size + 10)
            self._textarea.append(dw.Text(subheading_text,
                                          font_family=subheading_font_family,
                                          font_weight=subheading_weight,
                                          font_size=subheading_size,
                                          x=5, y=self._current_y,
                                          fill=subheading_color,
                                          dominant_baseline='hanging'))
            self._current_row += 1

    def add_text(self, text, x_offset=0, max_line_length=50,
                 text_font_family='Gill Sans MT', text_font_size=22,
                 text_font_weight='', text_color='#ffffff'):

        log.info(text)
        lines = split_string(text, max_line_length)

        if self._current_row + len(lines) > self._max_rows:
            self._cut_page()

        for line in lines:
            self._current_y += (text_font_size + 10)
            self._textarea.append(dw.Text(line,
                                          font_family=text_font_family,
                                          font_weight=text_font_weight,
                                          font_size=text_font_size,
                                          x=10 + x_offset, y=self._current_y,
                                          fill=text_color,
                                          dominant_baseline='hanging'))
            self._current_row += 1

    def add_block(self, *blocks):
        # Each block should be a dictionary with keys: text, x_offset, max_line_length, font_family, font_size, font_weight, color
        total_lines = 0
        split_blocks = []

        for block in blocks:
            lines = split_string(block['text'], block.get('max_line_length', 50))
            split_blocks.append((block, lines))
            total_lines += len(lines)

        if self._current_row + total_lines > self._max_rows:
            self._cut_page()

        for block, lines in split_blocks:
            font_family = block.get('font_family', 'Gill Sans MT')
            font_size = block.get('font_size', 22)
            font_weight = block.get('font_weight', '')
            color = block.get('color', '#ffffff')
            x_offset = block.get('x_offset', 0)

            for line in lines:
                self._current_y += (font_size + 10)
                self._textarea.append(dw.Text(line,
                                              font_family=font_family,
                                              font_weight=font_weight,
                                              font_size=font_size,
                                              x=10 + x_offset, y=self._current_y,
                                              fill=color,
                                              dominant_baseline='hanging'))
                self._current_row += 1

    def _cut_page(self):
        self.save_png()
        self.save_svg()

        self._textarea = dw.Group(id='textarea', fill='none')
        self._current_row = 0
        self._current_y = self._FIRST_LINE_Y
        self._current_file += 1

        self.add_subheading(self._current_subheading)

    def _get_filename(self, file_name):
        return f'{file_name}_{str(self._current_file).zfill(3)}'

    def save_png(self):
        d = dw.Drawing(self._width, self._height)
        d.append(self._background)
        d.append(self._textarea)
        d.save_png(str(self._output_path / f'{self._get_filename(self._file_name)}.png'))

    def save_svg(self):
        d = dw.Drawing(self._width, self._height)
        d.append(self._background)
        d.append(self._textarea)
        d.save_svg(str(self._output_path / f'{self._get_filename(self._file_name)}.svg'))