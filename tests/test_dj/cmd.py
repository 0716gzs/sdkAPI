# 生成以上类中opts参数
import argparse
from src.sdk.commands.cr_dj_settings import Command


def get_opts():
    parser = argparse.ArgumentParser(description='Create new settings')

    # 创建子解析器
    subparsers = parser.add_subparsers(dest='command')

    # 创建 'create' 子命令的解析器
    create_parser = subparsers.add_parser('create', help='Create a new project')
    create_parser.add_argument('sdk', help='Name of the new project')
    create_parser.add_argument('directory', help='Directory where to create the project')

    # 创建 'django' 子命令的解析器
    django_parser = subparsers.add_parser('django', help='Specify Django type')
    django_parser.add_argument('type', help='Django type')
    return parser.parse_args()


if __name__ == '__main__':
    c = Command()
    c.run(['sdk', 'create', 'django'], get_opts())
