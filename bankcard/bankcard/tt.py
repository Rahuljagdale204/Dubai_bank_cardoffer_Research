import yaml
from yaml.loader import SafeLoader


def extract_html_links(nxtpath):
    print(nxtpath)

def extract_current_page(url):
    print(url)


def tt():
    path = '/home/rahul/Downloads/Intership/Dubai_bank_cardoffer_Research/bankcard/bankcard/Data/testfile.yaml'

    with open(path, 'r') as f:
        data = yaml.load(f,Loader=SafeLoader)
        
        for key, val in data.items():
            pass

            

if __name__ =="__main__":
    tt()
   