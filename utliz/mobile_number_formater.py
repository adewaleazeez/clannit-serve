def mobile_number(number):
    a = []
    for i in number:
        a.append(i)
    if a[0] == '0':
        a[0] = '234'
    elif a[0] != '0':
        a.insert(0,'234')
        
    return int(''.join(a))