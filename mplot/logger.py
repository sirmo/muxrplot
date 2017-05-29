"""
Copyright (c) 2017 Muxr, http://www.eevblog.com/forum/profile/?u=105823

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
"""

import time
import serial
import sys
import argparse
import os
import signal
import itertools

original_sigint = None


class Unbuffered(object):
    """
        overwrites the sys.stdout so that the output isn't buffered
        generally if you're writting a lot of data you'd want it to be buffered
        but in this script we usually only write once a second and the immediate
        feedback is prefered
    """
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)
sys.stdout = Unbuffered(sys.stdout)


class Progress(object):

    def __init__(self):
        self.frames = '/-\|'
        self.pos = 0

    def show(self):
        if self.pos >= len(self.frames):
            self.pos = 0
        sys.stdout.write('\r' + self.frames[self.pos:][0])
        sys.stdout.flush()
        self.pos += 1


def exit_gracefully(signum, frame):
    global original_sigint
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)


def format_time(ts):
    return time.strftime("%D %H:%M:%S", time.localtime(int(ts)))


def log(options):
    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port=options.device,
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )

    prog = Progress()

    with open(options.outfile, 'w') as the_file:
        the_file.write('timestamp;value\n')
        while True:
            # \r\n is for device terminators set to CR LF
            ser.write((':FETCh?\r\n'))

            # wait one second before reading output.
            time.sleep(options.interval)
            out = ''
            while ser.inWaiting() > 0:
                out += ser.read(1)
            if out != '':
                out = out.rstrip()
                res = "%s;%s\n" % (time.time(), float(out))
                the_file.write(res)
                the_file.flush()
                prog.show()


def main():
    global original_sigint
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile', nargs='?')
    parser.add_argument('-d',
                        '--device',
                        dest='device',
                        action='store',
                        default='/dev/cu.usbserial',
                        help='Path to the serial device')
    parser.add_argument('-i',
                        '--interval',
                        dest='interval',
                        action='store',
                        default=1,
                        type=float,
                        help='Polling interval')
    options = parser.parse_args()

    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    index = 1
    if os.path.exists(options.outfile):
        while os.path.exists(options.outfile + '_' + str(index)):
            index += 1
            if index > 100:
                print "filenames exhausted"
                sys.exit(1)
        options.outfile = options.outfile + '_' + str(index)
    print 'logging to: {}'.format(options.outfile)
    log(options)

if __name__ == '__main__':
    main()
