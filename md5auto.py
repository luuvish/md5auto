#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, time
import codecs, unicodedata


class HashList(object):

    def __init__(self, md5=False, sha1=False):
        self.items = []
        self.stats = None
        self.error = sys.stderr.write
        self.workdir = os.getcwd()
        from hashlib import md5 as md5hash
        from hashlib import sha1 as sha1hash
        self.hash = (md5hash, sha1hash)[md5 == False]

    def init_from_paths(self, paths):
        from fnmatch import fnmatch
        items = []
        for path in paths:
            path = unicodedata.normalize('NFC', path.decode('utf-8'))
            os.chdir(path)
            item = []
            for (dirpath, dirnames, filenames) in os.walk('.'):
                for name in filenames:
                    if fnmatch(name, '@*'):
                        continue
                    fn = os.path.normpath(os.path.join(dirpath, name))
                    fn = unicodedata.normalize('NFC', fn.decode('utf-8'))
                    try:
                        fs = os.path.getsize(fn)
                    except OSError:
                        self.error('Can\'t open file: %s\n' % (fn))
                        continue
                    item.append([fn, fs, ''])
            if len(item) > 0:
                items.append([path, item])
            os.chdir(self.workdir)
        items.sort()
        self.items = items

    def init_from_files(self, files):
        items = []
        for lines in files:
            path = ''
            item = []
            for line in lines:
                line = line.rstrip()
                if line.startswith('#!path='):
                    if len(item) > 0:
                        items.append([path, item])
                    path = os.path.normpath(line[7:])
                    item = []
                    continue
                try:
                    hd, fn = line.split(' *')
                except ValueError:
                    continue
                try:
                    fs = os.path.getsize(os.path.normpath(os.path.join(path, fn)))
                except OSError:
                    self.error('Can\'t open file: %s\n' % (fn))
                    continue
                item.append([fn, fs, hd])
            if len(item) > 0:
                items.append([path, item])
        self.items = items

    def init_stats(self):
        stats = HashStats(self.items)
        self.stats = stats
        return stats

    def make_to_lines(self, lines):
        itime = time.time()
        matchs = 0
        errors = 0
        for (path, item) in self.items:
            stime = time.time()
            match = 0
            error = 0
            lines.write('\n#!path=%s\n\n' % (path))
            for (fn, fs, hd) in item:
                try:
                    hd = self.digest(os.path.normpath(os.path.join(path, fn)))
                    match += 1
                except IOError:
                    hd = 'x' * 32
                    error += 1
                lines.write('%s *%s\n' % (hd.lower(), fn))
                if self.stats:
                    self.stats.write('%3d%% (%d/%d) (%d/%d)\r' %
                                     (100 * self.stats.nbyte / self.stats.bytes,
                                      self.stats.nhash, self.stats.hashs,
                                      self.stats.nbyte, self.stats.bytes))
            etime = time.time()
            matchs += match
            errors += error
            lines.write('\n#!time=%s~%s~%s hashs=%d/%d\n' %
                        tuple(HashList.times(stime, etime) + (match, match+error)))
        if self.stats:
            self.stats.write('\n')
        if len(self.items) > 1:
            lines.write('\n#!time=%s~%s~%s hashs=%d/%d\n' %
                        tuple(HashList.times(itime, etime) + (matchs, matchs+errors)))

    def test_to_lines(self, lines):
        itime = time.time()
        matchs = 0
        errors = 0
        for (path, item) in self.items:
            stime = time.time()
            match = 0
            error = 0
            lines.write('\n')
            for (fn, fs, hd) in item:
                try:
                    hr = self.digest(os.path.normpath(os.path.join(path, fn)))
                except IOError:
                    hr = 'x' * 32
                if hd.lower() == hr.lower():
                    lines.write('match(%s) = %s\n' % (hd.lower(), fn))
                    match += 1
                else:
                    lines.write('error(%s) = %s\n' % (hr.lower(), fn))
                    error += 1
                if self.stats:
                    self.stats.write('%3d%% (%d/%d) (%d/%d)\r' %
                                     (100 * self.stats.nbyte / self.stats.bytes,
                                      self.stats.nhash, self.stats.hashs,
                                      self.stats.nbyte, self.stats.bytes))
            etime = time.time()
            matchs += match
            errors += error
            lines.write('\n#!time=%s~%s~%s error=%d/%d\n' %
                        tuple(HashList.times(stime, etime) + (error, match+error)))
        if self.stats:
            self.stats.write('\n')
        if len(self.items) > 1:
            lines.write('\n#!time=%s~%s~%s error=%d/%d\n' %
                        tuple(HashList.times(itime, etime) + (error, matchs+errors)))

    def digest(self, pathname):
        READ_BUF_SIZE = 1024 * 512
        f = open(pathname, 'rb')
        hashfn = self.hash()
        while True:
            data = f.read(READ_BUF_SIZE)
            if not data:
                break
            if self.stats:
                self.stats.nbyte += len(data)
            hashfn.update(data)
        f.close()
        if self.stats:
            self.stats.nhash += 1
        return hashfn.hexdigest()

    @staticmethod
    def times(stime, etime):
        gmfmt = lambda f, v: time.strftime(f, time.gmtime(v))
        lofmt = lambda f, v: time.strftime(f, time.localtime(v))
        times = gmfmt('%H:%M:%S', etime - stime)
        stime = lofmt('%Y/%m/%d,%H:%M:%S', stime)
        etime = lofmt('%Y/%m/%d,%H:%M:%S', etime)
        return (stime, etime, times)


class HashStats(object):

    def __init__(self, items):
        self.nhash = 0
        self.nbyte = 0
        self.hashs = 0
        self.bytes = 0
        for (path, item) in items:
            for (fn, fs, hd) in item:
                self.hashs += 1
                self.bytes += fs

    def error(self, *args, **kargs):
        sys.stderr.write(*args, **kargs)
        sys.stderr.flush()

    def write(self, *args, **kargs):
        sys.stdout.write(*args, **kargs)
        sys.stdout.flush()


class FileLog(object):

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
                fd, self.temp = mkstemp(text=False)
                self.file = codecs.EncodedFile(os.fdopen(fd, 'w'), 'utf-8')
            else:
                dirname, basename = os.path.split(self.name)
                if dirname and not os.path.exists(dirname):
                    os.mkdir(dirname)
                lofmt = lambda f, v: time.strftime(f, time.localtime(v))
                stime = lofmt('%Y%m%d-%H%M%S-', time.time())
                self.file = codecs.open(os.path.normpath(os.path.join(dirname, stime + basename)), 'w', 'utf-8')

    def close(self):
        if self.name:
            self.file.close()
            if self.temp:
                dirname, basename = os.path.split(self.name)
                if dirname and not os.path.exists(dirname):
                    os.mkdir(dirname)
                lofmt = lambda f, v: time.strftime(f, time.localtime(v))
                etime = lofmt('%Y%m%d-%H%M%S-', time.time())
                from shutil import move
                move(self.temp, os.path.normpath(os.path.join(dirname, etime + basename)))

    def write(self, *args, **kargs):
        self.file.write(*args, **kargs)
        if self.echo:
            sys.stderr.write(*args, **kargs)


def options(argv):
    from optparse import OptionParser

    p = OptionParser()

    p.add_option('--md5', action='store_true', dest='md5', default=False, help='md5 checksum')
    p.add_option('--sha1', action='store_true', dest='sha1', default=False, help='sha1 checksum')
    p.add_option('-m', '--make', action='store_true', dest='make', default=False, help='make checksums')
    p.add_option('-t', '--test', action='store_true', dest='test', default=True, help='test checksums')
    p.add_option('-o', '--out', action='store', type='string', dest='out', default='', help='out file name')
    p.add_option('-l', '--log', action='store', type='string', dest='log', default='', help='log file name')

    opts, args = p.parse_args(argv)
    opts.paths = args

    if opts.make:
        opts.test, opts.log = False, ''
        if not opts.md5 and not opts.sha1:
            pathname, ext = os.path.splitext(opts.out)
            if ext == '.md5':
                opts.md5 = True
            if ext == '.sha':
                opts.sha1 = True
    if opts.md5:
        opts.sha1 = False
    if not opts.sha1:
        opts.md5 = True # default is md5

    return opts

def make(opts):
    hashs = HashList(md5=opts.md5, sha1=opts.sha1)
    paths = [path for path in opts.paths if os.path.isdir(path)]
    hashs.init_from_paths(paths)
    stats = hashs.init_stats()
    try:
        dirname = os.path.dirname(opts.out)
        if dirname and not os.path.exists(dirname):
            os.mkdir(dirname)
        out = codecs.open(opts.out, 'w', 'utf-8')
    except IOError:
        sys.stderr.write('Can\'t open file: %s\n' % (opts.out))
        sys.exit(1)
    hashs.make_to_lines(out)
    out.close()

def test(opts):
    hashs = HashList(md5=opts.md5, sha1=opts.sha1)
    files = []
    for path in opts.paths:
        try:
            files.append(codecs.open(path, 'r', 'utf-8'))
        except IOError:
            sys.stderr.write('Can\'t open file: %s\n' % (path))
            sys.exit(1)
    hashs.init_from_files(files)
    for path in files:
        path.close()
    stats = hashs.init_stats()
    try:
        log = FileLog(temp=False)
        log.open(opts.log)
    except IOError:
        sys.stderr.write('Can\'t open file: %s\n' % (opts.log))
        sys.exit(1)
    hashs.test_to_lines(log)
    log.close()


if __name__ == '__main__':
    opts = options(sys.argv[1:])
    if opts.make:
        make(opts)
    if opts.test:
        test(opts)
