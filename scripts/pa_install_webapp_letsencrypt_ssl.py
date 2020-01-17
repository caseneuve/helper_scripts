#!/usr/bin/python3.5
"""Set the HTTPS certificate and private key for a website, assuming that these have been generated by the dehydrated
script that gets them from Let's Encrypt, and that they're in the standard place.  This script should normally only
be run on PythonAnywhere.

Usage:
  pa_install_webapp_letsencrypt_ssl.py <domain> [--suppress-reload]

Options:
  <domain>              Domain name, eg www.mydomain.com
  --suppress-reload     The website will need to be reloaded in order to activate the new certificate/key combination
                        -- this happens by default, use this option to suppress it.
"""

from docopt import docopt
from os.path import expanduser
import os
import sys

from pythonanywhere.api import Webapp
from pythonanywhere.snakesay import snakesay


def main(domain_name, suppress_reload):
    homedir = expanduser("~")
    possible_paths = (
        os.path.join(homedir, 'letsencrypt', domain_name),
        os.path.join(homedir, 'letsencrypt', 'certs', domain_name),
    )
    done = False
    for path in possible_paths:
        certificate_file = os.path.join(path, 'fullchain.pem')
        private_key_file = os.path.join(path, 'privkey.pem')
        if os.path.exists(certificate_file) and os.path.exists(private_key_file):
            with open(certificate_file, "r") as f:
                certificate = f.read()
            with open(private_key_file, "r") as f:
                private_key = f.read()

            webapp = Webapp(domain_name)
            webapp.set_ssl(certificate, private_key)
            if not suppress_reload:
                webapp.reload()

            ssl_details = webapp.get_ssl_info()
            print(
                snakesay(
                    "This method of handling Let's Encrypt certs\n"
                    "**************IS DEPRECATED.**************\n\n"
                    "You can now have a Let's Encrypt certificate managed by PythonAnywhere.\n"
                    "We handle all the details of getting it, installing it,\n"
                    "and managing renewals for you. So you don't need to do\n"
                    "any of the stuff below any more.\n\n"
                    "Anyway, All is set up for now. \n"
                    "Your new certificate will expire on {expiry:%d %B %Y},\n"
                    "so shortly before then you should switch to the new system\n"
                    "(see https://help.pythonanywhere.com/pages/HTTPSSetup/)\n"
                    "".format(
                        expiry=ssl_details["not_after"]
                    )
                )
            )

            done = True
            break

    if not done:
        print("Could not find certificate or key files (looked in {possible_paths})".format(
            possible_paths=possible_paths
        ))
        sys.exit(2)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(
        arguments['<domain>'],
        suppress_reload=arguments.get('--suppress-reload')
    )
