from random import randint

## latest master code can get found here: https://slickdeals.net/f/9549456-lowe-s-10-15-50-off-online-coupons-sharing-only-no-off-topic?p=93883968#post93883968
#September Master codes (as of 12/27):

# March
#10% off - 0601
#$10 off $50 - 0289, 0288
#$15 off $75 - 9359
#$20 off $100 - 0668, 0594
#$40 off $200 - 
#$25 off %250 - 0581
#$60 off $400 - 
#20% off select item - 0084
#master = "0601"

def code_gen():
    master_set = {'10% off': '0603', 'Get 10$ off for 50$ purchase': '0289', 'Get 20$ off for 100$ purchase': '0668'}
    code_set = {}
    for key, master in master_set.items():
        code_list = code_gen_master(master)
        code_set[key] = code_list
    return code_set

def code_gen_master(master):
    code_list = []
    for x in range (1):
        i = randint(0,50000)
        code = addcheckdigit("47000" + "%05d" % i + master)
        code_list.append(code)
    return code_list
    

def addcheckdigit(stuff):
    print(stuff)
    checkdigit = 0
    for x in range(14):
        if x % 2 == 0:
            checkdigit += int(stuff[x])
        else:
            checkdigit += int(stuff[x]) * 3
        
    code = str(stuff) + str((10 -(checkdigit % 10))%10)
    print(code)
    return code
