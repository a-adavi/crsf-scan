from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as bs


def get_forms(url1):
    response = requests.get(url1)
    soup = bs(response.content, 'html.parser')
    return soup.find_all('form')


def get_form_details(form):
    details = {}
    action = form.attrs.get('action')
    method = form.attrs.get('method', 'get').lower()
    inputs = []
    for input_tag in form.find_all('input'):
        input_type = input_tag.attrs.get('type', 'text')
        input_name = input_tag.attrs.get('name')
        inputs.append({'type': input_type, 'name': input_name})
    details['action'] = action
    details['method'] = method
    details['inputs'] = inputs
    return details


def submit_form(form_details, url2, data):
    target_url = urljoin(url2, form_details['action'])
    if form_details['method'] == 'post':
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)


def csrf_scan(url3):
    forms = get_forms(url3)
    print(f"[+] Detected {len(forms)} forms on {url3}.")
    for form in forms:
        form_details = get_form_details(form)
        data = {input1['name']: 'test' for input1 in form_details['inputs']}
        response = submit_form(form_details, url3, data)
        if response.status_code == 200:
            print(f"[+] Potential CSRF Vulnerability: {form_details['action']}")
            print(response.text)


url = input("enter website :ex = https://www.google.com/  ::> ")

csrf_scan(url)
