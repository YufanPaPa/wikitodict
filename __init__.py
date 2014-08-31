import requests
import re

def search(title):
    box_str = _get_infobox(title)

    #Follow redirect
    if '#REDIRECT' in box_str:
        title = re.findall("\[\[(.*)\]\]", box_str)[0]
        box_str = _get_infobox(title)

    print box_str

    box_dict = _parse(box_str)
    box_dict['article_title'] = title

    return box_dict


def _get_infobox(search_term):
    URL = "http://en.wikipedia.org/w/api.php?action=query&\
            prop=revisions&rvprop=content&format=json&\
            titles={title}&rvsection=0"

    response = requests.get(URL.format(title=search_term))
    d = response.json()
    box_str = d['query']['pages'].values()[0]['revisions'][0]['*']
    return box_str




def _parse(box_str):
    boxtype = re.findall('\{\{Infobox (.*)\n', box_str)[0]
    regex = re.compile('\{\{Infobox(.*)\}\}\n', re.DOTALL)
    box = re.findall(regex, box_str)[0]

    infobox_dict = {'boxtype': boxtype}
    for line in box.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip('| ')
            value = value.replace('[', '')
            value = value.replace(']', '')
            value = value.replace('{', '')
            value = value.replace('}', '')
            value = value.replace('<br>', ', ')
            value = value.strip()
            if len(key) > 0 and len(value) > 0:
                infobox_dict[key] = value

    return infobox_dict

from pprint import pprint
