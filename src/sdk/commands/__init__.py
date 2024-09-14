"""
Base class for Scrapy commands
"""
import argparse
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.sdk.utils.conf import arglist_to_dict
from src.sdk.utils.exceptions import UsageError


class SDKCommand:
    requires_project = False
    exitcode = 0

    def __init__(self) -> None:
        pass

    def syntax(self):
        """
        Command syntax (preferably one-line). Do not include command name.
        """
        return ""

    def short_desc(self):
        """
        A short description of the command
        """
        return ""

    def long_desc(self):
        """A long description of the command. Return short description when not
        available. It cannot contain newlines since contents will be formatted
        by optparser which removes newlines and wraps text.
        """
        return self.short_desc()

    def help(self):
        """An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines since no post-formatting will
        be applied to its contents.
        """
        return self.long_desc()

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """
        group = parser.add_argument_group(title="Global Options")
        group.add_argument(
            "--logfile", metavar="FILE", help="log file. if omitted stderr will be used"
        )
        group.add_argument(
            "-L",
            "--loglevel",
            metavar="LEVEL",
            default=None,
            help=f"log level (default: {self.settings['LOG_LEVEL']})",
        )
        group.add_argument(
            "--nolog", action="store_true", help="disable logging completely"
        )
        group.add_argument(
            "--profile",
            metavar="FILE",
            default=None,
            help="write python cProfile stats to FILE",
        )
        group.add_argument("--pidfile", metavar="FILE", help="write process ID to FILE")
        group.add_argument(
            "-s",
            "--set",
            action="append",
            default=[],
            metavar="NAME=VALUE",
            help="set/override setting (may be repeated)",
        )

    def process_options(self, args, opts):
        try:
            self.settings.setdict(arglist_to_dict(opts.set), priority="cmdline")
        except ValueError:
            raise UsageError("Invalid -s value, use -s NAME=VALUE", print_help=False)

        if opts.logfile:
            self.settings.set("LOG_ENABLED", True, priority="cmdline")
            self.settings.set("LOG_FILE", opts.logfile, priority="cmdline")

        if opts.loglevel:
            self.settings.set("LOG_ENABLED", True, priority="cmdline")
            self.settings.set("LOG_LEVEL", opts.loglevel, priority="cmdline")

        if opts.nolog:
            self.settings.set("LOG_ENABLED", False, priority="cmdline")

        if opts.pidfile:
            Path(opts.pidfile).write_text(
                str(os.getpid()) + os.linesep, encoding="utf-8"
            )

    def _find_settings_in_directory(self, directory_path: Path) -> Optional[Path] | bool:
        directory_path = directory_path.parent
        directory = Path(directory_path)
        # 遍历目录及其子目录
        for path in directory.rglob('*'):
            if path.name == 'settings.py':
                return path.parent
            else:
                continue
        else:
            return False

    def run(self, args: List[str], opts: argparse.Namespace) -> None:
        """
        Entry point for running commands
        """
        raise NotImplementedError
