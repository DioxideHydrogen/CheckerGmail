from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from time import sleep
from pesquisas import Pesquise
import unicodedata

def remover_acentos(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
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
               
            results = service.users().messages().list(userId='me',labelIds = ['INBOX', 'UNREAD'], maxResults=5).execute()
            messages = results.get('messages', [])
            

            if not messages:
                frase = 'Sem novas mensagens na caixa de email'
                a = Pesquise(frase)
                a.fala(frase)
            else:
                for message in messages:
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    payld = msg['payload'] # get payload of the message 
                    headr = payld['headers'] # get header of the payload
                    for one in headr: # getting the Subject
                        if one['name'] == 'Subject':
                            msg_subject = remover_acentos(one['value'])
                        else:
                            pass
                    frase = 'Hugo, novo email na caixa de entrada, ' + msg_subject
                    a = Pesquise(frase)
                    a.fala(frase)
            sleep(1800)
    except Exception as err:
        print err
if __name__ == '__main__':
    main()
