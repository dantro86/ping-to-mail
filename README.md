# ping-to-mail
Python utility to ping hosts and send e-mail if host status is changed

Programm takes ip list from ip_list file. Then availability is verifying for each element in this list.
If host is down a message will be sent to configurable e-mail address.
If host was down and is available now an another message will be sent.
Both text messages are configurable.

Usage: sudo python pingtomail.py

Sudo is required due pyping requirements.

For working this application Google API is required.
See Turn on the Gmail API section https://developers.google.com/gmail/api/quickstart/python
Save your client_secret.json file and cofigure CLIENT_SECRET_FILE and APPLICATION_NAME values according your settings in config.ini file.

