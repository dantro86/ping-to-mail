import base64
from email.mime.text import MIMEText

from apiclient import discovery
import oauth2client
from googleapiclient import errors
from oauth2client import client
from oauth2client import tools
import httplib2
import os


class GmailClient:
    """Wrapper for using gmail client API

    """
    flags = None

    def __init__(self, gmail_client_settings):

        self.flags = tools.argparser.parse_known_args()

        try:
            self.SCOPES = gmail_client_settings['scopes']
            self.CLIENT_SECRET_FILE = gmail_client_settings['secret_file']
            self.APPLICATION_NAME = gmail_client_settings['app_name']
            self.reach_text = gmail_client_settings['reach_text']
            self.unreach_text = gmail_client_settings['unreach_text']
            self.title = gmail_client_settings['title']
            self.sender = gmail_client_settings['sender']
            self.to = gmail_client_settings['to']

        except KeyError as error:
            print ('key %s is not found, check the settings file' % error.args[0])
            exit(1)

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'pingtomail-credentials.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:

                print ('flags = true')
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    @staticmethod
    def create_message(sender, to, subject, message_text):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

        Returns:
        An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    @staticmethod
    def send_message(service, user_id, message):
        """Send an email message.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message: Message to be sent.

        Returns:
            Sent Message.
        """
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print ('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)

    def send(self, reachable_bul, ip):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        text = ''

        if reachable_bul:
            text = self.reach_text % ip
        else:
            text = self.unreach_text % ip

        self.send_message(service, self.sender, self.create_message(self.sender,
                                                                    self.to,
                                                                    self.title,
                                                                    text))


