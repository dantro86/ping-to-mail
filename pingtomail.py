from __future__ import print_function
from ping_source import PingSource
from mail_client import GmailClient
import time
import configparser
import argparse
from mail_client import tools


def get_sources(args):

    config = configparser.RawConfigParser()
    config.read(args[0].config)

    iplist_file = config.get('pingtomail.common', 'ip_list_file')

    with open(iplist_file, 'r') as f:
        ips = [line.strip() for line in f]

    print (ips)

    gmail_client_settings = {'scopes': config.get('pingtomail.gmail.settings', 'SCOPES'),
                             'secret_file': config.get('pingtomail.gmail.settings', 'CLIENT_SECRET_FILE'),
                             'app_name': config.get('pingtomail.gmail.settings', 'APPLICATION_NAME'),
                             'reach_text': config.get('pingtomail.gmail.settings', 'reach_text'),
                             'unreach_text': config.get('pingtomail.gmail.settings', 'unreach_text'),
                             'title': config.get('pingtomail.gmail.settings', 'title'),
                             'sender': config.get('pingtomail.gmail.settings', 'sender'),
                             'to': config.get('pingtomail.gmail.settings', 'to')}

    gmail_client = GmailClient(gmail_client_settings)

    return [PingSource(ip, True, gmail_client) for ip in ips]


def check_list(c_list):

    for source in c_list:
        response = source.ping()

        if response.ret_code == 0:
            print(source.ip + ' - reachable')
            if not source.reachable_bul:
                source.send_mail()
                source.reachable_bul = True
        else:
            print(source.ip + ' - unreachable')
            if source.reachable_bul:
                source.send_mail()
                source.reachable_bul = False


def create_arg_parser():
    parser = argparse.ArgumentParser(description='Program settings.', parents=[tools.argparser])
    parser.add_argument('-s', '--sleep', type=int, help='sleep time for ping running in sec. Default - 15', default=15)
    parser.add_argument('-c', '--config', help='path to configuration file. Default - config.ini', default='config.ini')

    args = parser.parse_known_args()
    return args


def main():
    args = create_arg_parser()
    sleep_time = args[0].sleep
    src_list = get_sources(args)

    while True:
        if src_list:
            print ('working')
            check_list(src_list)

        time.sleep(sleep_time)

if __name__ == '__main__':
    main()


