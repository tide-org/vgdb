import os
import signal
import pty
import tty
import select
import fcntl
import termios
import struct
import shlex

class ConqueSubprocess:
    pid = 0
    fd = None

    def open(self, command, env={}):
        command_arr = shlex.split(command)
        executable = command_arr[0]
        args = command_arr
        try:
            self.pid, self.fd = pty.fork()
            logging.info(self.pid)
        except:
            logging.info("pty.fork() failed. Did you mean pty.spork() ???")
            return False
        if self.pid == 0:
            for k in env.keys():
                os.environ[k] = env[k]
            try:
                attrs = tty.tcgetattr(1)
                attrs[0] = attrs[0] ^ tty.IGNBRK
                attrs[0] = attrs[0] | tty.BRKINT | tty.IXANY | tty.IMAXBEL
                attrs[2] = attrs[2] | tty.HUPCL
                attrs[3] = attrs[3] | tty.ICANON | tty.ECHO | tty.ISIG | tty.ECHOKE
                attrs[6][tty.VMIN] = 1
                attrs[6][tty.VTIME] = 0
                tty.tcsetattr(1, tty.TCSANOW, attrs)
            except:
                logging.info('attribute setting failed')
                pass
            os.execvp(executable, args)
        else:
            pass

    def read(self, timeout=1):
        output = ''
        read_timeout = float(timeout) / 1000
        read_ct = 0
        try:
            while 1:
                s_read, s_write, s_error = select.select([self.fd], [], [], read_timeout)
                lines = ''
                for s_fd in s_read:
                    try:
                        if read_ct < 10:
                            lines = os.read(self.fd, 32)
                        elif read_ct < 50:
                            lines = os.read(self.fd, 512)
                        else:
                            lines = os.read(self.fd, 2048)
                        read_ct += 1
                    except:
                        pass
                    output = output + lines.decode('utf-8')

                if lines == '' or read_ct > 100:
                    break
        except:
            logging.info(traceback.format_exc())
            pass
        return output

    def write(self, input):
        try:
            if CONQUE_PYTHON_VERSION == 2:
                os.write(self.fd, input.encode('utf-8', 'ignore'))
            else:
                os.write(self.fd, bytes(input, 'utf-8'))
        except:
            logging.info(traceback.format_exc())
            pass

    def signal(self, signum):
        try:
            os.kill(self.pid, signum)
        except:
            pass

    def close(self):
        self.signal(15)

    def is_alive(self):
        p_status = True
        try:
            if os.waitpid(self.pid, os.WNOHANG)[0]:
                p_status = False
        except:
            p_status = False
        return p_status

    def window_resize(self, lines, columns):
        try:
            fcntl.ioctl(self.fd, termios.TIOCSWINSZ, struct.pack("HHHH", lines, columns, 0, 0))
            os.kill(self.pid, signal.SIGWINCH)
        except:
            pass
