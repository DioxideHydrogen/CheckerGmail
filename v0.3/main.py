from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from time import sleep
import unicodedata


def remover_acentos(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

print '''\033[1m
    =======================================
            Alexa Email Checker v0.1
    =======================================\033[0;0m
'''


def main():
    try:
        while True:
            store = file.Storage('token.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
                creds = tools.run_flow(flow, store)
            service = build('gmail', 'v1', http=creds.authorize(Http()))

            # Call the Gmail API to fetch INBOX

            results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=2, q="category:primary").execute() #Atualização 0.2 -> include "CATEGORY_PERSONAL" at labelIds, but have problems with this Id, so in v0.3 -> I put q="category:primary", and now the script only get main menssages of the Inbox of the gmail.
            messages = results.get('messages', [])

            if not messages:
                frase = 'Sem novas mensagens na caixa de email'
                print frase
            else:
                for message in messages:
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    payld = msg['payload']  # get payload of the message
                    headr = payld['headers']  # get header of the payload
                    for one in headr:  # getting the Subject
                        if one['name'] == 'Subject':
                            msg_subject = remover_acentos(one['value'])
                        else:
                            pass
                    print 'Novo email na caixa de entrada, ' + msg_subject
            sleep(600) # Aguarda 10 minutos para checkar novamente
    except Exception as err:
        print err


if __name__ == '__main__':
    main()
