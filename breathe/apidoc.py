"""
breathe.apidoc
~~~~~~~~~~~~~~

Parses doxygen XML tree looking for C/C++ modules and creates ReST files
appropriately to create code documentation with Sphinx. It also creates a
modules index (See TYPEDICT below.).

This is derived from the "sphinx-autopackage" script, which is:
Copyright 2008 Société des arts technologiques (SAT),
http://www.sat.qc.ca/

:copyright: Originally by Sphinx Team, C++ modifications by Tatsuyuki Ishi
:license: BSD, see LICENSE for details.
"""

from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree
from pathlib import Path

from breathe import __version__

# Reference: Doxygen XSD schema file, CompoundKind only
# Only what breathe supports are included
# Translates identifier to English
TYPEDICT = {
    "class": "Class",
    "interface": "Interface",
    "struct": "Struct",
    "union": "Union",
    "file": "File",
    "namespace": "Namespace",
    "group": "Group",
}

# Types that accept the :members: option.
MEMBERS_TYPES = ["class", "group", "interface", "namespace", "struct"]


def print_info(msg, args):
    if not args.quiet:
        print(msg)


def write_file(name, text, args):
    """Write the output file for module/package <name>."""
    fname = Path(args.destdir, f"{name}.{args.suffix}")
    if args.dryrun:
        print_info("Would create file %s." % fname, args)
        return
    if not args.force and fname.is_file():
        print_info("File %s already exists, skipping." % fname, args)
    else:
        print_info("Creating file %s." % fname, args)
        fname.parent.mkdir(parents=True, exist_ok=True)
        try:
            orig = fname.read_text(encoding="utf-8")
            if orig == text:
                print_info("File %s up to date, skipping." % fname, args)
                return
        except FileNotFoundError:
            # Don't mind if it isn't there
            pass
        fname.write_text(text, encoding="utf-8")


def format_heading(level, text):
    """Create a heading of <level> [1, 2 or 3 supported]."""
    underlining = ["=", "-", "~"][level - 1] * len(text)
    return "%s\n%s\n\n" % (text, underlining)


def format_directive(package_type, package, args):
    """Create the breathe directive and add the options."""
    directive = ".. doxygen%s:: %s\n" % (package_type, package)
    if args.project:
        directive += "   :project: %s\n" % args.project
    if args.members and package_type in MEMBERS_TYPES:
        directive += "   :members:\n"
    return directive


def create_package_file(package, package_type, package_id, args):
    """Build the text of the file and write the file."""
    # Skip over types that weren't requested
    if package_type not in args.outtypes:
        return
    text = format_heading(1, "%s %s" % (TYPEDICT[package_type], package))
    text += format_directive(package_type, package, args)

    write_file(Path(package_type, package_id), text, args)


def create_modules_toc_file(key, value, args):
    """Create the module's index."""
    if not Path(args.destdir, key).is_dir():
        return
    text = format_heading(1, "%s list" % value)
    text += ".. toctree::\n"
    text += "   :glob:\n\n"
    text += "   %s/*\n" % key

    write_file("%slist" % key, text, args)


def recurse_tree(args):
    """
    Look for every file in the directory tree and create the corresponding
    ReST files.
    """
    index = xml.etree.ElementTree.parse(Path(args.rootpath, "index.xml"))

    # Assuming this is a valid Doxygen XML
    for compound in index.getroot():
        create_package_file(
            compound.findtext("name"), compound.get("kind"), compound.get("refid"), args
        )


class TypeAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)
        self.default = TYPEDICT.keys()
        self.metavar = ",".join(TYPEDICT.keys())

    def __call__(self, parser, namespace, values, option_string=None):
        assert isinstance(values, str)
        value_list = values.split(",")
        for value in value_list:
            if value not in TYPEDICT:
                raise ValueError("%s not a valid option" % value)
        setattr(namespace, self.dest, value_list)


def main():
    """Parse and check the command line arguments."""
    parser = argparse.ArgumentParser(
        description="""\
Parse XML created by Doxygen in <rootpath> and create one reST file with
breathe generation directives per definition in the <DESTDIR>.

Note: By default this script will not overwrite already created files.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        action="store",
        dest="destdir",
        help="Directory to place all output",
        required=True,
    )
    parser.add_argument(
        "-f", "--force", action="store_true", dest="force", help="Overwrite existing files"
    )
    parser.add_argument(
        "-m",
        "--members",
        action="store_true",
        dest="members",
        help="Include members for types: %s" % MEMBERS_TYPES,
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        dest="dryrun",
        help="Run the script without creating files",
    )
    parser.add_argument(
        "-T",
        "--no-toc",
        action="store_true",
        dest="notoc",
        help="Don't create a table of contents file",
    )
    parser.add_argument(
        "-s",
        "--suffix",
        action="store",
        dest="suffix",
        help="file suffix (default: rst)",
        default="rst",
    )
    parser.add_argument(
        "-p",
        "--project",
        action="store",
        dest="project",
        help="project to add to generated directives",
    )
    parser.add_argument(
        "-g",
        "--generate",
        action=TypeAction,
        dest="outtypes",
        help="types of output to generate, comma-separated list",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", dest="quiet", help="suppress informational messages"
    )
    parser.add_argument(
        "--version", action="version", version="Breathe (breathe-apidoc) %s" % __version__
    )
    parser.add_argument("rootpath", type=str, help="The directory contains index.xml")
    args = parser.parse_args()

    args.suffix = args.suffix.removeprefix(".")
    if not os.path.isdir(args.rootpath):
        print("%s is not a directory." % args.rootpath, file=sys.stderr)
        sys.exit(1)
    if "index.xml" not in os.listdir(args.rootpath):
        print("%s does not contain a index.xml" % args.rootpath, file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.destdir):
        if not args.dryrun:
            os.makedirs(args.destdir)
    args.rootpath = os.path.abspath(args.rootpath)
    recurse_tree(args)
    if not args.notoc:
        for key in args.outtypes:
            create_modules_toc_file(key, TYPEDICT[key], args)


# So program can be started with "python -m breathe.apidoc ..."
if __name__ == "__main__":
    main()
