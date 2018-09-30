import vim
import re
import math
import time

class Conque:
    screen = None                  # screen object
    proc = None                    # subprocess object
    columns = 80                   # same as $COLUMNS
    lines = 24                     # same as $LINES
    working_columns = 80           # can be changed by CSI ? 3 l/h
    working_lines = 24             # can be changed by CSI r
    top = 1                        # top of scroll region relative to top of screen
    bottom = 24                    # botom of scroll region relative to top of screen
    l = 1                          # current cursor line
    c = 1                          # current cursor column
    autowrap = True                # autowrap mode
    absolute_coords = True         # absolute coordinate mode
    tabstops = []                  # tabstop positions
    enable_colors = True           # enable colors
    color_changes = {}             # color changes
    color_history = {}             # color history
    highlight_groups = {}          # color highlight cache
    color_pruning = True           # prune terminal colors
    unwrap_tables = True           # don't wrap table output
    wrap_cursor = False            # wrap CUF/CUB around line breaks
    cursor_set = False             # do we need to move the cursor?
    character_set = 'ascii'        # current character set, ascii or graphics
    read_count = 0                 # used for auto_read actions
    input_buffer = []              # input buffer, array of ordinals

    def open(self):
        command = vim.eval('command')
        options = vim.eval('options')
        self.screen = ConqueScreen()
        self.columns = vim.current.window.width
        self.lines = vim.current.window.height
        self.working_columns = vim.current.window.width
        self.working_lines = vim.current.window.height
        self.bottom = vim.current.window.height
        if int(options['offset']) > 0:
            self.l = int(options['offset'])
        self.enable_colors = options['color'] and not CONQUE_FAST_MODE
        self.init_tabstops()
        self.proc = ConqueSubprocess()
        self.proc.open(command, {
            'TERM': options['TERM'],
            'CONQUE': '1',
            'LINES': str(self.lines),
            'COLUMNS': str(self.columns)
        })
        self.update_window_size(True)

    def write(self, input, set_cursor=True, read=True):
        self.proc.write(input)
        if read:
            self.read(1, set_cursor)

    def write_ord(self, input, set_cursor=True, read=True):
        if CONQUE_PYTHON_VERSION == 2:
            self.write(unichr(input), set_cursor, read)
        else:
            self.write(chr(input), set_cursor, read)

    def write_expr(self, expr, set_cursor=True, read=True):
        if CONQUE_PYTHON_VERSION == 2:
            try:
                val = vim.eval(expr)
                self.write(unicode(val, CONQUE_VIM_ENCODING, 'ignore'), set_cursor, read)
            except:
                logging.info(traceback.format_exc())
                pass
        else:
            try:
                self.write(vim.eval(expr), set_cursor, read)
            except:
                logging.info(traceback.format_exc())
                pass

    def write_buffered_ord(self, chr):
        self.input_buffer.append(chr)

    def read(self, timeout=1, set_cursor=True, return_output=False, update_buffer=True):
        output = ''
        try:
            output = self.proc.read(timeout)
            if output == '':
                return
            if not update_buffer:
                return output
            logging.debug(output)
            output = output.replace(chr(0), '')
            chunks = CONQUE_SEQ_REGEX.split(output)
            logging.debug(str(chunks))
            if len(chunks) == 1:
                self.plain_text(chunks[0])
            else:
                for s in chunks:
                    if s == '':
                        continue
                    logging.debug('at line ' + str(self.l) + ' column ' + str(self.c))
                    if CONQUE_SEQ_REGEX_CTL.match(s[0]):
                        logging.debug('control match')
                        nr = ord(s[0])
                        if nr in CONQUE_CTL:
                            getattr(self, 'ctl_' + CONQUE_CTL[nr])()
                        else:
                            logging.info('control not found for ' + str(s))
                            pass
                    elif CONQUE_SEQ_REGEX_CSI.match(s):
                        logging.debug('csi match')
                        if s[-1] in CONQUE_ESCAPE:
                            csi = self.parse_csi(s[2:])
                            logging.debug(str(csi))
                            getattr(self, 'csi_' + CONQUE_ESCAPE[s[-1]])(csi)
                        else:
                            logging.info('csi not found for ' + str(s))
                            pass
                    elif CONQUE_SEQ_REGEX_TITLE.match(s):
                        logging.debug('title match')
                        self.change_title(s[2], s[4:-1])
                    elif CONQUE_SEQ_REGEX_HASH.match(s):
                        logging.debug('hash match')
                        if s[-1] in CONQUE_ESCAPE_HASH:
                            getattr(self, 'hash_' + CONQUE_ESCAPE_HASH[s[-1]])()
                        else:
                            logging.info('hash not found for ' + str(s))
                            pass
                    elif CONQUE_SEQ_REGEX_CHAR.match(s):
                        logging.debug('char match')
                        if s[-1] in CONQUE_ESCAPE_CHARSET:
                            getattr(self, 'charset_' + CONQUE_ESCAPE_CHARSET[s[-1]])()
                        else:
                            logging.info('charset not found for ' + str(s))
                            pass
                    elif CONQUE_SEQ_REGEX_ESC.match(s):
                        logging.debug('escape match')
                        if s[-1] in CONQUE_ESCAPE_PLAIN:
                            getattr(self, 'esc_' + CONQUE_ESCAPE_PLAIN[s[-1]])()
                        else:
                            logging.info('escape not found for ' + str(s))
                            pass
                    else:
                        self.plain_text(s)
            if set_cursor:
                self.screen.set_cursor(self.l, self.c)
            self.cursor_set = False
        except:
            logging.info('read error')
            logging.info(traceback.format_exc())
            pass
        if return_output:
            if CONQUE_PYTHON_VERSION == 3:
                return output
            else:
                return output.encode(CONQUE_VIM_ENCODING, 'replace')

    def auto_read(self):
        if len(self.input_buffer):
            for chr in self.input_buffer:
                self.write_ord(chr, set_cursor=False, read=False)
            self.input_buffer = []
            self.read(1)
        if self.read_count % 32 == 0:
            if not self.proc.is_alive():
                vim.command('call conque_term#get_instance().close()')
                return
            if self.read_count > 512:
                self.read_count = 0
                if self.enable_colors and self.color_pruning:
                    self.prune_colors()
        self.read_count += 1
        self.read(1)
        if self.c == 1:
            vim.command('call feedkeys("\<right>\<left>", "n")')
        else:
            vim.command('call feedkeys("\<left>\<right>", "n")')
        if self.cursor_set:
            return
        if not CONQUE_FAST_MODE:
            self.update_window_size()
            logging.info('window size!')
        try:
            self.set_cursor(self.l, self.c)
        except:
            logging.info('cursor set error')
            logging.info(traceback.format_exc())
            pass
        self.cursor_set = True

    def plain_text(self, input):
        if self.character_set == 'graphics':
            old_input = input
            input = u('')
            for i in range(0, len(old_input)):
                chrd = ord(old_input[i])
                logging.debug('pre-translation: ' + old_input[i])
                logging.debug('ord: ' + str(chrd))
                try:
                    if chrd > 255:
                        logging.info("over the line!!!11")
                        input = input + old_input[i]
                    else:
                        input = input + uchr(CONQUE_GRAPHICS_SET[chrd])
                except:
                    logging.info('failed')
                    pass

        logging.debug('plain -- ' + str(self.color_changes))
        current_line = self.screen[self.l]
        if len(current_line) < self.c:
            current_line = current_line + ' ' * (self.c - len(current_line))
        if self.c + len(input) - 1 > self.working_columns:
            if self.unwrap_tables and CONQUE_TABLE_OUTPUT.match(input):
                self.screen[self.l] = current_line[:self.c - 1] + input + current_line[self.c + len(input) - 1:]
                self.apply_color(self.c, self.c + len(input))
                self.c += len(input)
                return
            logging.debug('autowrap triggered')
            diff = self.c + len(input) - self.working_columns - 1
            if self.autowrap:
                self.screen[self.l] = current_line[:self.c - 1] + input[:-1 * diff]
                self.apply_color(self.c, self.working_columns)
                self.ctl_nl()
                self.ctl_cr()
                remaining = input[-1 * diff:]
                logging.debug('remaining text: "' + remaining + '"')
                self.plain_text(remaining)
            else:
                self.screen[self.l] = current_line[:self.c - 1] + input[:-1 * diff - 1] + input[-1]
                self.apply_color(self.c, self.working_columns)
                self.c = self.working_columns
        else:
            self.screen[self.l] = current_line[:self.c - 1] + input + current_line[self.c + len(input) - 1:]
            self.apply_color(self.c, self.c + len(input))
            self.c += len(input)

    def apply_color(self, start, end, line=0):
        logging.debug('applying colors ' + str(self.color_changes))
        if not self.enable_colors:
            return
        if line:
            buffer_line = line
        else:
            buffer_line = self.get_buffer_line(self.l)
        logging.debug('start ' + str(start) + ' end ' + str(end))
        to_del = []
        if buffer_line in self.color_history:
            for i in range(len(self.color_history[buffer_line])):
                syn = self.color_history[buffer_line][i]
                logging.debug('checking syn ' + str(syn))
                if syn['start'] >= start and syn['start'] < end:
                    logging.debug('first')
                    vim.command('syn clear ' + syn['name'])
                    to_del.append(i)
                    if syn['end'] > end:
                        logging.debug('first.half')
                        self.exec_highlight(buffer_line, end, syn['end'], syn['highlight'])
                elif syn['end'] > start and syn['end'] <= end:
                    logging.debug('second')
                    vim.command('syn clear ' + syn['name'])
                    to_del.append(i)
                    if syn['start'] < start:
                        logging.debug('second.half')
                        self.exec_highlight(buffer_line, syn['start'], start, syn['highlight'])
        if len(to_del) > 0:
            to_del.reverse()
            for di in to_del:
                del self.color_history[buffer_line][di]
        if len(self.color_changes) == 0:
            return
        highlight = ''
        for attr in self.color_changes.keys():
            highlight = highlight + ' ' + attr + '=' + self.color_changes[attr]
        self.exec_highlight(buffer_line, start, end, highlight)

    def exec_highlight(self, buffer_line, start, end, highlight):
        syntax_name = 'ConqueHighLightAt_%d_%d_%d_%d' % (self.proc.pid, self.l, start, len(self.color_history) + 1)
        syntax_options = 'contains=ALLBUT,ConqueString,MySQLString,MySQLKeyword oneline'
        syntax_region = 'syntax match %s /\%%%dl\%%>%dc.\{%d}\%%<%dc/ %s' % (syntax_name, buffer_line, start - 1, end - start, end + 1, syntax_options)
        hgroup = 'ConqueHL_%d' % (abs(hash(highlight)))
        if hgroup not in self.highlight_groups:
            syntax_group = 'highlight %s %s' % (hgroup, highlight)
            self.highlight_groups[hgroup] = hgroup
            vim.command(syntax_group)
        syntax_highlight = 'highlight link %s %s' % (syntax_name, self.highlight_groups[hgroup])
        logging.debug(syntax_region)
        vim.command(syntax_region)
        vim.command(syntax_highlight)
        if not buffer_line in self.color_history:
            self.color_history[buffer_line] = []
        self.color_history[buffer_line].append({'name': syntax_name, 'start': start, 'end': end, 'highlight': highlight})

    def prune_colors(self):
        logging.info('pruning colors ' + str(len(self.color_history.keys())))
        buffer_line = self.get_buffer_line(self.l)
        ks = list(self.color_history.keys())
        for line in ks:
            if line < buffer_line - CONQUE_MAX_SYNTAX_LINES:
                for syn in self.color_history[line]:
                    vim.command('syn clear ' + syn['name'])
                del self.color_history[line]

    def ctl_nl(self):
        if self.lines != self.working_lines and self.l == self.bottom:
            del self.screen[self.top]
            self.screen.insert(self.bottom, '')
        elif self.l == self.bottom:
            self.screen.append('')
        else:
            self.l += 1
        self.color_changes = {}

    def ctl_cr(self):
        self.c = 1
        self.color_changes = {}

    def ctl_bs(self):
        if self.c > 1:
            self.c += -1

    def ctl_soh(self):
        pass

    def ctl_stx(self):
        pass

    def ctl_bel(self):
        vim.command('call conque_term#bell()')

    def ctl_tab(self):
        ts = self.working_columns
        for i in range(self.c, len(self.tabstops)):
            if self.tabstops[i]:
                ts = i + 1
                break
        logging.debug('tabbing from ' + str(self.c) + ' to ' + str(ts))
        self.c = ts

    def ctl_so(self):
        self.character_set = 'graphics'

    def ctl_si(self):
        self.character_set = 'ascii'

    def esc_scroll_up(self):
        self.ctl_nl()
        self.color_changes = {}

    def esc_next_line(self):
        self.ctl_nl()
        self.c = 1

    def esc_set_tab(self):
        logging.debug('set tab at ' + str(self.c))
        if self.c <= len(self.tabstops):
            self.tabstops[self.c - 1] = True

    def esc_scroll_down(self):
        if self.l == self.top:
            del self.screen[self.bottom]
            self.screen.insert(self.top, '')
        else:
            self.l += -1
        self.color_changes = {}

    def hash_screen_alignment_test(self):
        self.csi_clear_screen(self.parse_csi('2J'))
        self.working_lines = self.lines
        for l in range(1, self.lines + 1):
            self.screen[l] = 'E' * self.working_columns

    def charset_us(self):
        self.character_set = 'ascii'

    def charset_uk(self):
        self.character_set = 'ascii'

    def charset_graphics(self):
        self.character_set = 'graphics'

    def set_cursor(self, line, col):
        self.screen.set_cursor(line, col)

    def change_title(self, key, val):
        logging.debug(key)
        logging.debug(val)
        if key == '0' or key == '2':
            logging.debug('setting title to ' + re.escape(val))
            vim.command('setlocal statusline=' + re.escape(val))
            try:
                vim.command('set titlestring=' + re.escape(val))
            except:
                pass

    def update_window_size(self, force=False):
        if force or vim.current.window.width != self.columns or vim.current.window.height != self.lines:
            self.columns = vim.current.window.width
            self.lines = vim.current.window.height
            self.working_columns = vim.current.window.width
            self.working_lines = vim.current.window.height
            self.bottom = vim.current.window.height
            self.l = self.screen.reset_size(self.l)
            self.init_tabstops()
            logging.debug('signal window resize here ---')
            self.proc.window_resize(self.lines, self.columns)

    def insert_enter(self):
        self.update_window_size()
        self.cursor_set = False

    def init_tabstops(self):
        for i in range(0, self.columns + 1):
            if i % 8 == 0:
                self.tabstops.append(True)
            else:
                self.tabstops.append(False)

    def close(self):
        self.proc.close()

    def abort(self):
        self.proc.signal(1)

    def parse_csi(self, s):
        attr = {'key': s[-1], 'flag': '', 'val': 1, 'vals': []}
        if len(s) == 1:
            return attr
        full = s[0:-1]
        if full[0] == '?':
            full = full[1:]
            attr['flag'] = '?'
        if full != '':
            vals = full.split(';')
            for val in vals:
                logging.debug(val)
                val = re.sub("\D", "", val)
                logging.debug(val)
                if val != '':
                    attr['vals'].append(int(val))
        if len(attr['vals']) == 1:
            attr['val'] = int(attr['vals'][0])
        return attr

    def bound(self, val, min, max):
        if val > max:
            return max
        if val < min:
            return min
        return val

    def get_buffer_line(self, line):
        return self.screen.get_buffer_line(line)
