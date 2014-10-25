__author__ = 'sharad'

import os
import geoip
import re
import ipaddress
import socket
import collections
import geoip


LOG_FILE_NAME = "access_log_Jul95"


class BadInputError(Exception):
    pass

class LogParser():
    def __init__(self, filename):
        self.filename = filename
        self.try_open_file(filename)

    def try_open_file(self, filename):
        """This tries to see if file exists and is readable or not, if yes then returns the file handle
         otherwise returns None"""
        try:
            file_hand = open(filename, 'r', encoding="ascii")
            file_hand.close()
        except:
            raise BadInputError("File {} doesn't exist".format(filename))

    def is_valid_ip(self, address):
        "return true if valid IP otherwise return false"
        try:
            val = ipaddress.ip_address(address)
            return True
        except ValueError:
            return False

    def get_ip_address(self, urlorip):
        """The parameter passed to it is either a URL or an IP address. If its a URL return the IP address
        otherwise simply return the ip address"""
        res = self.is_valid_ip(urlorip)
        if (res):
            return urlorip
        else:
            try:
                ip = socket.gethostbyname(urlorip)
                return ip
            except socket.gaierror:
                return None

    def get_geolocation(self, ipaddr):
        """from a given ip address get its longitude and latitude"""
        ipad = ipaddress.ip_address(ipaddr)
        #print(ipad)
        #match = geoip.geolite2.lookup(ipaddr)
        #print(match)



    def print_html_report(self, html_dict):
        """for the dictionary passed where key is line number and elements are url and ip address, print
        it as an html report file"""
        pass

    def main(self):
        fhand = open(self.filename, 'r', encoding="ascii", errors='replace')
        html_dict = collections.OrderedDict()
        regex1 = re.compile(r"(.*) - - .*\".*\" (\d{3}) [\d+|-]")
        for idx, line in enumerate(fhand):
            line = line.strip()
            res1 = regex1.search(line)
            if res1:
                num = int(res1.group(2))
                if num == 404:
                    #check if ip address or URL, if URL then get its IP address
                    urlorip = res1.group(1)
                    val = self.get_ip_address(urlorip)
                    if val:
                        pass
                        #gloclat, gloclon = self.get_geolocation(val)
                    html_dict[idx + 1] = [urlorip, val]
                    print("line no. {}  {}  {}".format(idx+1, urlorip, val))
            else:
                print("no matching sequence in line {}".format(line))
        fhand.close()
        self.print_html_report(html_dict)

lp = LogParser(LOG_FILE_NAME)
lp.main()