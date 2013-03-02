#!/usr/bin/env python

import os
import sys
import platform
import fnmatch
from optparse import OptionParser


def print_version():
    print 'PyNamer v1.0'
    print 'Camron Levanger'
    print 'https://github.com/camronlevanger/PyNamer'


def print_filenames(filenames):
    total = 0
    for filename in filenames:
        print filename
        total += 1

    return total


def RenameFile(options, filepath):
    """
    Renames a file with the given options
    """

    # split the filepath and the filename apart, this ensures that we dont
    # rename the directory in addtion to the filename
    pathname = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    if options.superverbose:
        print '==========================================='
        print filename

    # trim the beginning of filename by supplied number
    if options.trimfront:
        filename = filename[options.trimfront:]
        if options.superverbose:
            print '...front trimmed %s' % filename

    # trim ending of filename by supplied number
    if options.trimback:
        filename = filename[:len(filename) - options.trimback]
        if options.superverbose:
            print '...back trimmed %s' % filename

    # replace matches in filename with supplied value
    if options.replace:
        for vals in options.replace:
            filename = filename.replace(vals[0], vals[1])
        if options.superverbose:
            print '...replaced vals %s' % filename

    # convert filename to all lowercase letters
    if options.lowercase:
        filename = filename.lower()
        if options.superverbose:
            print '...lowercased %s' % filename

     # convert filename to all uppercase letters
    if options.uppercase:
        filename = filename.upper()
        if options.superverbose:
            print '...uppercased %s' % filename

    # rejoin the filename and filepath
    new_filepath = os.path.join(pathname, filename)

    # finally, we actually rename the file on the filesystem
    try:

        print "%s -> %s" % (filepath, new_filepath)

        # if this is not a dry-run, then rename the files on disk
        if not options.dryrun:
            os.rename(filepath, new_filepath)

    except OSError, ex:
        print >>sys.stderr, "Error renaming '%s': %s" % (filepath, ex.strerror)

if __name__ == "__main__":

    # define (allthethings)
    usage = "usage: %prog [options] directory fnmatch"
    optParser = OptionParser(usage=usage)

    optParser.add_option("-l",
                         "--list",
                         action="store_true",
                         dest="list",
                         default=False,
                         help="List files that would be changed by PyNamer")

    optParser.add_option("-d",
                         "--dryrun",
                         action="store_true",
                         dest="dryrun",
                         default=False,
                         help="Preview in superverbose changes (dry-run)")

    optParser.add_option("-v",
                         "--verbose",
                         action="store_true",
                         dest="verbose",
                         default=False,
                         help="Use verbose output")

    optParser.add_option("-s",
                         "--superverbose",
                         action="store_true",
                         dest="superverbose",
                         default=False,
                         help="Use SUPER verbose output")

    optParser.add_option("-V",
                         "--version",
                         action="store_true",
                         dest="version",
                         default=False,
                         help="Print version info")

    optParser.add_option("-L",
                         "--lowercase",
                         action="store_true",
                         dest="lowercase",
                         default=False,
                         help="Convert the filename to lowercase")

    optParser.add_option("-U",
                         "--uppercase",
                         action="store_true",
                         dest="uppercase",
                         default=False,
                         help="Convert the filename to uppercase")

    optParser.add_option("-f",
                         "--trim-front",
                         type="int",
                         dest="trimfront",
                         metavar="NUM",
                         help="Trims NUM of characters "
                              "from the front of the filename")

    optParser.add_option("-b",
                         "--trim-back",
                         type="int",
                         dest="trimback",
                         metavar="NUM",
                         help="Trims NUM of characters from "
                              "the back of the filename")

    optParser.add_option("-r",
                         "--replace",
                         action="append",
                         type="string",
                         nargs=2,
                         dest="replace",
                         help="Replaces OLDVAL with NEWVAL in the filename",
                         metavar="OLDVAL NEWVAL")

    (options, args) = optParser.parse_args()

    # if version flag, just print the version info and quit
    if options.version:
        print_version()
        sys.exit(0)

    if options.dryrun:
        options.superverbose = True

    # set the default file separator
    separator = '/'

    # detect user OS, set Windows separator id needed
    system = platform.system()
    if system is 'Windows':
        separator = "\\"

    if options.verbose or options.superverbose:
        print 'PyNamer v1.1'
        print '...detected %s platform separator is %s' % (system, separator)

    # supply a default fnmatch value in case none privided in args
    match = '*'

    # if there isn't at least 1 arg this script can't do anything
    if len(args) < 1:
        optParser.error("You must supply directory of files to rename...")

    # first argument in the args list should be the directory
    directory = args[0]

    # the second argument should be the fnmatch value, but if it isn't there
    # we use the match default already set
    try:
        match = args[1]
    except:
        if options.verbose or options.superverbose:
            print '...No fnmatch arg provided, using %s by default' % match

    # if the user didn't add the directory separator in the args, we add it
    # for them so that the rename class can find the file
    if not directory.endswith(separator):
        directory = ''.join([directory, separator])
        if options.verbose or options.superverbose:
            print '...adding separator to directory...%s' % directory

    if options.verbose:
        print 'Gathering list of matching files in %s' % (args[0])

    # loop through the provided directory and add any matching files to the list
    filenames = []
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename, match):
            thisfile = ''.join([directory, filename])
            filenames.append(thisfile)
            if options.verbose:
                print '...%s' % thisfile

    if options.list:
        print 'List of files matching %s' % match
        print '=================================='
        total = print_filenames(filenames)
        print '%s matches' % total
        sys.exit(0)

    if options.superverbose:
        print 'List of files matching %s' % match
        print '=================================='
        total = print_filenames(filenames)
        print '%s files will be renamed' % total

    # send the list of filenames through the renamer
    for filename in filenames:
        RenameFile(options, filename)

    # all finished!
    sys.exit(0)
