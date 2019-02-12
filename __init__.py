import requests
import re

def search(title):
    box_str = _get_infobox(title)

    #Follow redirect
    if '#REDIRECT' in box_str:
        title = re.findall("\[\[(.*)\]\]", box_str)[0]
        box_str = _get_infobox(title)


    box_dict = _parse(box_str)
    box_dict['article_title'] = title

    return box_dict


def _get_infobox(search_term):

    url = "".join(['https://zh.wikipedia.org/w/api.php?',
              'action=query&',
              'prop=revisions&',
              'rvprop=content&',
              'rvsection=0&',
              'format=json',
              '&titles=',
              search_term,'&redirects']);
    response = requests.get(url)
    res=response.json()
    try:
        box_str = res['query']['pages'].values()[0]['revisions'][0]['*']
    except:
        box_str = ""
    return box_str




def _parse(box_str):
    regex = re.compile('\{\{Infobox(.*)\}\}\n', re.DOTALL)
    try:
        box_str = re.findall(regex, box_str)[0]
    except:
        box_str = box_str
    infobox_dict = {}
    for line in box_str.splitlines():
        line = _replace_all('<ref.*(/>|>.*</ref>)', '', line)
        line = _replace_all('\{\{refn[^\}\}]*?\}\}', '', line)
        line = _replace_all('<[^>]+>', '', line)
        line = _replace_all('<!--.*-->', '', line)
        line = _replace_all('</small>', '', line)
        line = _replace_all('<ref.*/>', '', line)
        line = _replace_all('.+colspan.+', '', line)
        if re.compile("\|*=").search(line) and line[0]=="|":
            key, value = line.split('=', 1)
            key = key.strip('| ')
            if re.compile("key*|value*").search(key):
                continue
            value = value.replace('[', '')
            value = value.replace(']', '')
            value = value.replace('{', '')
            value = value.replace('}', '')
            value = value.replace('<br>', ', ')
            value = value.strip()
            if len(key) > 0 and len(key)<10 and len(value) > 0 and len(value) < 30:
                infobox_dict[key] = value

    return infobox_dict

def _replace_all(origin_str,replace_str,value):
    result = re.compile(origin_str).search(value)
    if result:
        value = value.replace(result.group(),'')
    return value
