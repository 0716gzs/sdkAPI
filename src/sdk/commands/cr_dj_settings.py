import argparse
import os
import re
import string
from importlib.util import find_spec
from pathlib import Path
from shutil import copy2, copystat, ignore_patterns, move
from stat import S_IWUSR as OWNER_WRITE_PERMISSION
from typing import List, Tuple, Union

from src import sdk
from src.sdk.commands import SDKCommand
from src.sdk.utils.exceptions import UsageError
from src.sdk.utils.template import render_templatefile, string_camelcase

TEMPLATES_TO_RENDER: Tuple[Tuple[str, ...], ...] = (
    ("sdk_django_settings.py.tmpl", ),
    # ("${settings_name}", "sdk_django_settings.py.tmpl"),
)

IGNORE = ignore_patterns("*.pyc", "__pycache__", ".svn")


def _make_writable(path: Union[str, os.PathLike]) -> None:
    current_permissions = os.stat(path).st_mode
    os.chmod(path, current_permissions | OWNER_WRITE_PERMISSION)


class Command(SDKCommand):
    requires_project = False

    def syntax(self) -> str:
        return "<settings_name> [project_dir]"

    def short_desc(self) -> str:
        return "Create new project"

    def _copytree(self, src: Path, dst: Path) -> None:
        """
        Since the original function always creates the directory, to resolve
        the issue a new function had to be created. It's a simple copy and
        was reduced for this case.

        More info at:
        https://github.com/scrapy/scrapy/pull/2005
        """
        ignore = IGNORE
        names = [x.name for x in src.iterdir()]
        ignored_names = ignore(src, names)

        if not dst.exists():
            dst.mkdir(parents=True)

        for name in names:
            if name in ignored_names:
                continue

            srcname = src / name
            dstname = dst
            if srcname.is_dir():
                self._copytree(srcname, dstname)
            else:
                copy2(srcname, dstname)
                _make_writable(dstname)

        copystat(src, dst)
        _make_writable(dst)

    def run(self, args: List[str], opts: argparse.Namespace) -> None:
        if len(args) not in (1, 2, 3):
            raise UsageError()
        settings_name = "sdk_" + args[2] + "_settings"

        if len(args) == 3:
            project_dir = Path(args[2])
        else:
            project_dir = Path(args[0])

        if (project_dir / settings_name).exists():
            self.exitcode = 1
            print(f"Error: sdk_django_settings already exists in {project_dir.resolve()}")
            return

        project_dir = self._find_settings_in_directory(project_dir.resolve())

        if isinstance(project_dir, bool):
            return

        self._copytree(Path(self.templates_dir), project_dir.resolve())
        # On 3.8 shutil.move doesn't fully support Path args, but it supports our use case
        # See https://bugs.python.org/issue32689
        move(project_dir, project_dir)  # type: ignore[arg-type]
        for paths in TEMPLATES_TO_RENDER:
            tplfile = Path(
                project_dir,
                *(
                    string.Template(s).substitute(settings_name=settings_name)
                    for s in paths
                ),
            )
            render_templatefile(
                tplfile,
                settings_name=settings_name,
            )
        print("=================Title=================")
        print(
            f"New django settings sdk '{settings_name}', \nusing template directory "
            f"'{self.templates_dir}', "
        )
        print(f"created in: {project_dir.resolve()}")
        print(f"You can  {project_dir.resolve()}/{settings_name}.py  file "
              f"To configure the SDKS of the three parties")
        print('=================End=================')

    @property
    def templates_dir(self) -> str:
        return str(
            Path(
                 # Path(sdk.__path__[0], "templates")
                 Path(sdk.__path__[0], "templates")
            )
        )

# # 生成以上类中opts参数
#
# def get_opts():
#     parser = argparse.ArgumentParser(description='Create new settings')
#
#     # 创建子解析器
#     subparsers = parser.add_subparsers(dest='command')
#
#     # 创建 'create' 子命令的解析器
#     create_parser = subparsers.add_parser('create', help='Create a new project')
#     create_parser.add_argument('sdk', help='Name of the new project')
#     create_parser.add_argument('directory', help='Directory where to create the project')
#
#     # 创建 'django' 子命令的解析器
#     django_parser = subparsers.add_parser('django', help='Specify Django type')
#     django_parser.add_argument('type', help='Django type')
#     return parser.parse_args()
#
#
# if __name__ == '__main__':
#     c = Command()
#     c.run(['sdk', 'create', 'django'], get_opts())

