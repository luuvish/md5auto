#!/usr/bin/env python

import sys, os, time


class FileLog:

    def __init__(self, temp=False, echo=False):
        self.name = ''
        self.temp = temp
        self.echo = echo
        self.file = sys.stdout

    def open(self, name=''):
        self.name = name
        if self.name:
            if self.temp:
                from tempfile import mkstemp
                fd, self.temp = mkstemp()
                self.file = os.fdopen(fd, 'wt')
            else:
                dirname = os.path.dirname(self.name)
                if not os.path.exists(dirname):
                    os.mkdir(dirname)
                self.file = open(self.name, 'wt')
        self.stime = time.time()

    def write(self, *args, **kargs):
        self.file.write(*args, **kargs)
        if self.echo:
            sys.stderr.write(*args, **kargs)

    def time(self):
        self.etime = time.time()
        stime = FileLog.lofmt('%Y/%m/%d,%H:%M:%S', self.stime)
        etime = FileLog.lofmt('%Y/%m/%d,%H:%M:%S', self.etime)
        times = FileLog.gmfmt('%H:%M:%S', self.etime - self.stime)
        return (stime, etime, times)

    @staticmethod
    def lofmt(format, value):
        return time.strftime(format, time.localtime(value))

    @staticmethod
    def gmfmt(format, value):
        return time.strftime(format, time.gmtime(value))

    def close(self):
        self.etime = time.time()
        if self.name:
            self.file.close()
            if self.temp:
                dirname, basename = os.path.split(self.name)
                if not os.path.exists(dirname):
                    os.mkdir(dirname)
                etime = FileLog.lofmt('%Y%m%d-%H%M%S-', self.etime)
                from shutil import move
                move(self.temp, os.path.normpath(os.path.join(dirname, etime + basename)))


def md5hex(pathname):
    from hashlib import md5 as md5hash
    READ_BUF_SIZE = 1024 * 512

    f = open(pathname, 'rb')
    md5 = md5hash()
    while True:
        data = f.read(READ_BUF_SIZE)
        if not data:
            break
        md5.update(data)
    f.close()

    return md5.hexdigest()


def md5make(opts):
    def subdirs(pathname):
        from fnmatch import fnmatch
        dirname = os.path.dirname(pathname)
        for (dirpath, dirnames, filenames) in os.walk(pathname):
            if dirname and dirpath.find(dirname) != 0:
                continue
            path = dirpath[len(dirname):] if dirname else dirpath
            for name in filenames:
                if fnmatch(name, '@ea*'):
                    continue
                yield os.path.normpath(os.path.join(path, name))

    out = FileLog()
    out.open(opts.out)

    os.chdir(opts.path)

    for item in opts.items:
        lines = list(subdirs(item))
        lines.sort()

        nline = len(lines)
        cline = 0

        dirname = os.path.dirname(item)
        if dirname:
            out.write('#!%s\n\n' % (dirname))

        for fn in lines:
            cline += 1

            try:
                hd = md5hex(os.path.normpath(os.path.join(dirname, fn)))
            except IOError:
                sys.stderr.write('Can\'t read file: %s\n' % (fn))
                continue

            out.write('%s *%s\n' % (hd.lower(), fn))

            sys.stderr.write('md5make progress %2d%%\r' % (100 * cline / nline))

    os.chdir(opts.work)

    out.close()


def md5test(opts):
    from glob import glob

    log = FileLog(temp=True)
    log.open(opts.log)

    for item in opts.items:
        for name in glob(item):
            try:
                md5 = open(name, 'rt')
            except IOError:
                sys.stderr.write('Can\'t read file: %s\n' % (name))
                continue

            os.chdir(opts.path)

            dirname = ''

            lines = md5.readlines()
            nline = len(lines)
            cline = 0
            match = 0
            total = 0

            log.write('  # start time %s\n\n' % (log.time()[0]))

            for line in lines:
                cline += 1

                line = line.rstrip()
                if line.find('#!') == 0:
                    dirname = os.path.normpath(line[2:])

                try:
                    hd, fn = line.split(' *')
                except ValueError:
                    continue

                try:
                    crc = md5hex(os.path.normpath(os.path.join(dirname, fn)))
                except IOError:
                    crc = 'x' * 32

                if hd.lower() == crc.lower():
                    log.write('match(%s) = %s\n' % (hd.lower(), fn))
                    match += 1
                else:
                    log.write('error(%s) = %s\n' % (crc.lower(), fn))
                total += 1

                sys.stderr.write('md5test progress %2d%%\r' % (100 * cline / nline))

            log.write('\n')
            log.write('  # %i/%i checksums matched\n' % (match, total))
            log.write('  # complete in %s ~ %s (%s)\n' % log.time())
            md5.close()

            os.chdir(opts.work)

    log.close()


def options(argv):
    from optparse import OptionParser

    p = OptionParser()

    p.add_option('--md5', action='store_true', dest='md5', default=True, help='md5 checksum')
#   p.add_option('--crc', action='store_true', dest='crc', default=False, help='crc checksum')
#   p.add_option('--sha1', action='store_true', dest='sha1', default=False, help='sha1 checksum')
    p.add_option('-m', '--make', action='store_true', dest='make', default=False, help='make checksums')
    p.add_option('-t', '--test', action='store_true', dest='test', default=True, help='test checksums')
    p.add_option('-p', '--path', action='store', type='string', dest='path', default='.', help='base path')
    p.add_option('-o', '--out', action='store', type='string', dest='out', default='', help='out file name')
    p.add_option('-l', '--log', action='store', type='string', dest='log', default='', help='log file name')

    opts, args = p.parse_args(argv)

    opts.items = args
    opts.items.sort()

    if opts.make:
        opts.test, opts.log = False, ''

    opts.work = os.getcwd()

    return opts


if __name__ == '__main__':

    opts = options(sys.argv[1:])

    if opts.make:
        md5make(opts)

    if opts.test:
        md5test(opts)
