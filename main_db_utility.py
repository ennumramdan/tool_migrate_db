import argparse
from controller.database.utility import Utility

__author__ = 'ennumramdaramdan'

if __name__ == '__main__':
    modes = ['parser']
    parser = argparse.ArgumentParser(description="Migrate DB Engine")
    parser.add_argument('-c', dest='config', help='engine configuration file', default="config.conf")
    parser.add_argument('-m', dest='mode', help="engine mode ({})".format(','.join(modes)))
    parser.add_argument('-t', dest='table', help="table name", default="all")
    parser.add_argument('-l', dest='last_day', help="last days", default=None)
    parser.add_argument('-id', dest='id', help="id", default=None)

    args = parser.parse_args()
    config_file = args.config

    if args.mode == "server_to_client":
        utility = Utility(config_file)
        utility.server_to_client(args.table, args.id, args.last_day)
    if args.mode == "client_to_server":
        utility = Utility(config_file)
        utility.client_to_server(args.table, args.id, args.last_day)