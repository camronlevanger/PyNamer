PyNamer
=======

A batch file renaming utility in Python
---------------------------------------

This is a simple file renaming utility written in Python that I've written (with inspiration) as a first step in a program I hope will eventually automatically rename all of my media files according to the [Plex Media Naming and Organization Guide](http://wiki.plexapp.com/index.php/Media_Naming_and_Organization_Guide).

While original intentions for the script are to rename media, this script can rename any type of file, according to any standards you choose.

Usage
-----

`Options:
  -h, --help            show this help message and exit
  -l, --list            List files that would be changed by PyNamer
  -d, --dryrun          Preview in superverbose changes (dry-run)
  -v, --verbose         Use verbose output
  -s, --superverbose    Use SUPER verbose output
  -V, --version         Print version info
  -L, --lowercase       Convert the filename to lowercase
  -U, --uppercase       Convert the filename to uppercase
  -f NUM, --trim-front=NUM
                        Trims NUM of characters from the front of the filename
  -b NUM, --trim-back=NUM
                        Trims NUM of characters from the back of the filename
  -r OLDVAL NEWVAL, --replace=OLDVAL NEWVAL
                        Replaces OLDVAL with NEWVAL in the filename`