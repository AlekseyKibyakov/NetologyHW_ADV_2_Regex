from pprint import pprint
import re
import csv

def open_contacts_file():
    with open("phonebook.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return(contacts_list)

def write_to_file(res):
    with open("phonebook_new.csv", 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerows(res)

def create_contacts_list(conlist, new_conlist):
    for el in conlist:
        temp = []
        for s in el:
            if s != '':
                temp.append(s)
        new_conlist.append(temp)

def create_names_dict(conlist, names):
    for el in new_contacts_list[1:]:
        if re.match(name_regex, el[2]) and re.match(name_regex, el[1]) and re.match(name_regex, el[0]) :     
            names['surnames'].append(el[2])
            names['firstnames'].append(el[1])
            names['lastnames'].append(el[0])

def edit_contact_name(contact_list):
    for el in contact_list[1:]:
        temp = []
        for s in el:
            if (re.findall(r'([А-ЯЁ][а-яё]+\s*){3}', s)):
                temp = s.split(' ')
                el.insert(0, temp[2])
                el.insert(0, temp[1])
                el.insert(0, temp[0])
                del el[3]
            elif (re.findall(r'([А-ЯЁ][а-яё]+\s*){2}', s)) and el.index(s) == 1:
                temp = s.split(' ')
                el.insert(1, temp[1])
                el.insert(1, temp[0])
                # if len(temp) <= 2:
                #     del el[0]
                #     break
                del el[3]
            elif (re.findall(r'([А-ЯЁ][а-яё]+\s*){2}', s)) and el.index(s) == 0:
                temp = s.split(' ')
                el.insert(0, temp[1])
                el.insert(0, temp[0])
                # if len(temp) <= 2:
                #     del el[0]
                #     break
                del el[2]   

def _get_duplicates_indices(contact_list):
    list_of_names = [' '.join([el[0], el[1]]) for el in contact_list]
    indices = {i: v for i, v in enumerate(list_of_names) if list_of_names.count(v) > 1}
    return indices

def edit_duplicates(contact_list):
    indices = _get_duplicates_indices(contact_list)
    list_to_edit = []
    for el in contact_list[1:]:
        for name in indices.values():
            if ' '.join([el[0], el[1]]) == name:
                list_to_edit.append(el)
                contact_list.remove(el)
                break
    
    result_list = []
    for j in range(len(list_to_edit)): 
        for i in range(len(list_to_edit)):
            if list_to_edit[i][0] == list_to_edit[j][0] and list_to_edit[i][1] == list_to_edit[j][1]:
                if i != j and sorted(list(set(list_to_edit[i] + list_to_edit[j]))) not in result_list:
                    result_list.append(sorted(list(set([*list_to_edit[i], *list_to_edit[j]]))))
                    
    contact_list += result_list

def edit_phone_number(contact_list):
    phone_regex = r'(8|\+7)\s*\(*(\w{3})\)*-*\s*(\w{3})-*\s*(\w{2})-*\s*(\w{2})'
    additional_phone = r'(8|\+7)\s*\(*(\w{3})\)*-*\s*(\w{3})-*\s*(\w{2})-*\s*(\w{2})\s*\(*доб\.*\s*(\w*)\)*\.*'
    for j, el in enumerate(contact_list):
        for i, num in enumerate(el):
            if re.match(additional_phone, num):
                contact_list[j][i] = re.sub(additional_phone, r'+7(\2)\3-\4-\5 доб.\6', num)
            elif re.match(phone_regex, num):
                contact_list[j][i] = re.sub(phone_regex, r'+7(\2)\3-\4-\5', num)    

def sort_contacts(new_contacts_list, names):
    org_list = ['Минфин', 'ФНС']
    phone_regex = r'(8|\+7)\s*\(*(\w{3})\)*-*\s*(\w{3})-*\s*(\w{2})-*\s*(\w{2})'
    result_list = []
    for i, el in enumerate(new_contacts_list):
        result_list.append(['', '', '', '', '', '', ''])
        if i == 0:
            result_list[0] = el
            continue
        for s in el:
            temp = s
            if s in names['lastnames']: 
                result_list[i][0] = temp
            elif s in names['firstnames']:
                result_list[i][1] = temp
            elif s in names['surnames']:
                result_list[i][2] = temp 
            elif s in org_list:
                result_list[i][3] = temp
            elif re.findall(phone_regex, s):
                result_list[i][5] = temp
            elif re.findall(r'\w+@\w+.\w{2,3}', s):
                result_list[i][6] = temp
            else:
                result_list[i][4] = temp    
    return result_list             
                
if __name__ == "__main__":
    name_regex = r'^[А-ЯЁ][a-яё]+$'
    org_list = ['Минфин', 'ФНС']
    names = {'lastnames':[], 'firstnames':[], 'surnames':[]}
    new_contacts_list = []
    con_list = open_contacts_file()   
    create_contacts_list(con_list, new_contacts_list)
    edit_contact_name(new_contacts_list)
    create_names_dict(new_contacts_list, names)
    edit_duplicates(new_contacts_list)
    edit_phone_number(new_contacts_list)
    write_to_file(sort_contacts(new_contacts_list, names))