import requests
# BeautifulSoup module is for web crawler
from bs4 import BeautifulSoup

def get_web_list(web_base):
    web_list = []
    pages = 1
    while True:
        webAddress = web_base + str(pages)
        if requests.get(webAddress).status_code == requests.codes.ok:
            web_list.append(webAddress)
        else:
            break
        pages += 1
    return web_list

def print_each_web(web_list):
    for iii in range(len(web_list)):
        web = requests.get(web_list[iii])
        soup = BeautifulSoup(web.text, 'html.parser')

        title_tags = soup.find_all(['p', 'h3'])
        for tag in title_tags:
            print_content(tag)

def print_content(tag):
    ######
    # Only used in this case
    if not_pass_filter(tag):
        return
    ######
    for content in tag.contents:
        if isinstance(content, str):
            if not content.isspace():
                print(content)
        else:
            print_content(content)

############
# Only used in this case
def not_pass_filter(tag):
    parent = tag.parent
    labels = ['boxout', 'hot', 'read_more_on', 'whitepapers', 'sponlinks', 'reg_foot', 'newsletter_signup', 'foot_btm', 'wptl']
    if parent.name == 'div':
        if parent.has_attr('class') and any(map(lambda cls: cls in labels, parent.get('class'))):
            return True
        elif parent.has_attr('id') and parent.get('id') in labels:
            return True
    if tag.has_attr('class') and any(map(lambda cls: cls in labels, tag.get('class'))):
        return True
    return False
############

if __name__ == "__main__":
    web_list = get_web_list('https://www.theregister.co.uk/2014/08/26/top_ten_gaming_keyboard_and_mouse_combos/?page=')
    print_each_web(web_list)