import vim

class ConqueScreen(object):
    buffer = None
    screen_top = 1
    screen_width = 80
    screen_height = 80
    screen_encoding = 'utf-8'

    def __init__(self):
        self.buffer = vim.current.buffer
        self.screen_top = 1
        self.screen_width = vim.current.window.width
        self.screen_height = vim.current.window.height
        self.screen_encoding = vim.eval('&fileencoding')

    def __len__(self):
        return len(self.buffer)

    def __getitem__(self, key):
        buffer_line = self.get_real_idx(key)
        if buffer_line >= len(self.buffer):
            for i in range(len(self.buffer), buffer_line + 1):
                self.append(' ')
        return u(self.buffer[buffer_line], 'utf-8')

    def __setitem__(self, key, value):
        buffer_line = self.get_real_idx(key)
        if CONQUE_PYTHON_VERSION == 2:
            val = value.encode(self.screen_encoding)
        else:
            val = str(value)
        if buffer_line == len(self.buffer):
            self.buffer.append(val)
        else:
            self.buffer[buffer_line] = val

    def __delitem__(self, key):
        del self.buffer[self.screen_top + key - 2]

    def append(self, value):
        if len(self.buffer) > self.screen_top + self.screen_height - 1:
            self.buffer[len(self.buffer) - 1] = value
        else:
            self.buffer.append(value)
        if len(self.buffer) > self.screen_top + self.screen_height - 1:
            self.screen_top += 1
        if vim.current.buffer.number == self.buffer.number:
            vim.command('normal! G')

    def insert(self, line, value):
        logging.debug('insert at line ' + str(self.screen_top + line - 2))
        l = self.screen_top + line - 2
        try:
            self.buffer.append(value, l)
        except:
            self.buffer[l:l] = [value]

    def get_top(self):
        return self.screen_top

    def get_real_idx(self, line):
        return (self.screen_top + line - 2)

    def get_buffer_line(self, line):
        return (self.screen_top + line - 1)

    def set_screen_width(self, width):
        self.screen_width = width

    def clear(self):
        self.screen_width = width
        self.buffer.append(' ')
        vim.command('normal! Gzt')
        self.screen_top = len(self.buffer)

    def set_cursor(self, line, column):
        buffer_line = self.screen_top + line - 1
        if buffer_line > len(self.buffer):
            for l in range(len(self.buffer) - 1, buffer_line):
                self.buffer.append('')
        real_column = column
        if len(self.buffer[buffer_line - 1]) < real_column:
            self.buffer[buffer_line - 1] = self.buffer[buffer_line - 1] + ' ' * (real_column - len(self.buffer[buffer_line - 1]))
        if not CONQUE_FAST_MODE:
            vim.command('call cursor(' + str(buffer_line) + ', byteidx(getline(' + str(buffer_line) + '), ' + str(real_column) + '))')
        else:
            try:
                vim.current.window.cursor = (buffer_line, real_column - 1)
            except:
                vim.command('call cursor(' + str(buffer_line) + ', ' + str(real_column) + ')')

    def reset_size(self, line):
        logging.debug('buffer len is ' + str(len(self.buffer)))
        logging.debug('buffer height ' + str(vim.current.window.height))
        logging.debug('old screen top was ' + str(self.screen_top))
        buffer_line = self.screen_top + line
        self.screen_width = vim.current.window.width
        self.screen_height = vim.current.window.height
        self.screen_top = len(self.buffer) - vim.current.window.height + 1
        if self.screen_top < 1:
            self.screen_top = 1
        logging.debug('new screen top is  ' + str(self.screen_top))
        vim.command('normal! ' + str(self.screen_height) + 'kG')
        return (buffer_line - self.screen_top)

    def align(self):
        vim.command('normal! ' + str(self.screen_height) + 'kG')
