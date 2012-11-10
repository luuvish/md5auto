#!/usr/bin/env python

import time
from tempfile import mkstemp
from shutil import move

from hashlib import md5 as md5hash
from fnmatch import fnmatch

import sys
import os
from optparse import OptionParser


READ_BUF_SIZE = 1024 * 512

DIRS_MD5SUMS = (
    'collection/anime/best',
    'collection/anime/ghibli',
    'collection/anime/gundam',
    'collection/anime/mecanic',
    'collection/game/console',
    'collection/game/hentai',
    'collection/game/mame-roms.co.uk',
    'collection/game/windows',
    'collection/movie/foreign',
    'collection/movie/korean',
    'collection/music',
    'collection/software',
    'collection/text',
    'nominate/anime/best',
    'nominate/anime/gundam',
    'nominate/anime/mecanic',
    'nominate/game/hentai',
    'nominate/game/windows',
    'nominate/movie/foreign',
    'nominate/movie/korean',
    'nominate/movie/porno',
    'private',
)


class FileLog:

    def __init__(self, name=''):
        self.name = name

    def open(self):
        if self.name:
            fd, self.temp = mkstemp()
            self.file = os.fdopen(fd, 'wt')
        else:
            self.file = ''
        self.stime = time.time()

    def write(self, *args, **kargs):
        if self.name:
            self.file.write(*args, **kargs)
        sys.stdout.write(*args, **kargs)

    def close(self):
        self.etime = time.time()
        lofmt = lambda f, t: time.strftime(f, time.localtime(t))
        gmfmt = lambda f, t: time.strftime(f, time.gmtime(t))
        stime = lofmt('%Y/%m/%d,%H:%M:%S', self.stime)
        etime = lofmt('%Y/%m/%d,%H:%M:%S', self.etime)
        times = gmfmt('%H:%M:%S', self.etime - self.stime)
        self.write('  # created in %s ~ %s (%s)\n' % (stime, etime, times))
        if self.name:
            self.file.close()
            etime = lofmt('%Y%m%d-%H%M%S', self.etime)
            move(self.temp, self.name + '.' + etime)


def md5_digest_file(filename):

    md5 = md5hash()

    f = open(filename, 'rb')
    while True:
        data = f.read(READ_BUF_SIZE)
        if not data:
            break
        md5.update(data)
    f.close()

    return filename, md5.hexdigest()

def md5_digest_path(pathname):

    def files_in_subdirs(pathname):
        for (base, dirs, files) in os.walk(pathname):
            for f in files:
                if fnmatch(f, '@ea*'):
                    continue
                yield os.path.normpath(base + '/' + f)

    fs = list(files_in_subdirs(pathname))
    fs.sort()
    for f in fs:
        yield md5_digest_file(f)

def md5sums(pathname, md5name, logname='', check=False):

    try:
        mode = 'rt' if check else 'wt'
        md5file = open(md5name, mode)
    except IOError:
        sys.stderr.write("Can't open %s file\n" % md5name)
        return

    if check:
        md5lines = md5file.readlines()
        match = 0
    total = 0

    logfile = FileLog(logname)
    logfile.open()

    for fn, hd in md5_digest_path(pathname):
        if not check:
            md5file.write('%s *%s\n' % (hd, fn))
            logfile.write('md5(%s) = %s\n' % (fn, hd))
        elif ('%s *%s\n' % (hd, fn)) in md5lines:
            logfile.write('match(%s) = %s\n' % (fn, hd))
            match += 1
        else:
            logfile.write('error(%s) = %s\n' % (fn, hd))
        total += 1

    if check:
        logfile.write('  # %i/%i checksums matched\n' % (match, total))
    else:
        logfile.write('  # %i/%i checksums created\n' % (total, total))

    logfile.close()
    md5file.close()


if __name__ == '__main__':

    p = OptionParser()

    p.add_option('-p', '--path', action='store', type='string', dest='path', default='.', help='working directory')
    p.add_option('-c', '--check', action='store_true', dest='check', default=False, help='check md5')
    p.add_option('-l', '--log', action='store_true', dest='log', default=False, help='dump log file')

    opts, args = p.parse_args(sys.argv[1:])

    md5dir = os.getcwd()
    if not md5dir:
        md5dir = '.'

    logdir = os.path.normpath(md5dir + '/log') if opts.log else ''
    if logdir and not os.path.exists(logdir):
        os.mkdir(logdir)

    if not args:
        args = DIRS_MD5SUMS

    for a in args:
        cwd = os.getcwd()
        os.chdir(os.path.normpath(opts.path + '/' + a))

        md5name = os.path.normpath(md5dir + '/' + a.replace('/', '-') + '.md5')
        logname = os.path.normpath(logdir + '/' + a.replace('/', '-') + '.log') if logdir else ''

        md5sums('.', md5name, logname, opts.check)

        os.chdir(cwd)
