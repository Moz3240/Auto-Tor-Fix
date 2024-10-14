import os
choice = input('[+] to install press (Y) to uninstall press (N) >> ')
run = os.system
if str(choice) =='Y' or str(choice)=='y':

    run('chmod 777 torv4.py')
    run('mkdir /usr/share/mtor')
    run('cp torv4.py /usr/share/mtor/torv4.py')

    cmnd=(' #! /bin/sh \n exec python3 /usr/share/mtor/torv4.py "$@"')
    with open('/usr/bin/mtor','w')as file:
        file.write(cmnd)
    run('chmod +x /usr/bin/mtor & chmod +x /usr/share/mtor/torv4.py')
    print('''\n\ncongratulation Auto Tor Fix is installed successfully \nfrom now just type \x1b[6;30;42mmtor\x1b[0m in terminal ''')
if str(choice)=='N' or str(choice)=='n':
    run('rm -r /usr/share/mtor ')
    run('rm /usr/bin/mtor ')
    print('[!] now Auto Tor Fix has been removed successfully')
