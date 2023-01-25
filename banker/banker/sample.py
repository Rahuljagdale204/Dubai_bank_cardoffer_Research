import yaml
from yaml.loader import SafeLoader

def solve():
    path = '/home/rahul/Downloads/Intership/Dubai_bank_cardoffer_Research/banker/data/testy.yaml'
    
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=SafeLoader)
        print(len(data.items()))
        for key, obj in data.items():
            print("Bankname->",key)
            print("Url->",obj['baseUrl'])
            print("[---------------------]")

    

if __name__=="__main__":
    solve()