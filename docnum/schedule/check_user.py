from django.contrib.auth.models import User
from officaldoc.settings import AUTH_LDAP_BIND_DN, AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_PASSWORD
import ldap
import re


def check_invalid():
    # LDAP 連線資訊
    LDAP_BASE_DN = 'DC=inaenergy,DC=com,DC=tw'
    ldapconn = ldap.initialize(AUTH_LDAP_SERVER_URI)
    ldapconn.set_option(ldap.OPT_REFERRALS, 0)
    ldapconn.simple_bind_s(AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)

    # LDAP 搜尋所有已停用的使用者
    result = ldapconn.search_s(LDAP_BASE_DN,
                               ldap.SCOPE_SUBTREE,
                               '(&(objectClass=user)(objectCategory=person)(userAccountControl:1.2.840.113556.1.4.803:=2))',
                               None)
    invalid_users = []
    for r in result:
        if r[0]:
            invalid_users.append(r[1]['sAMAccountName'][0].decode().lower())
            # mo = re.search(r'CN=(.*),OU', r[0])
            # if mo:
            #     invalid_users.append(mo.group(1).lower())
    print(invalid_users)
    users = User.objects.filter(is_staff=False)
    for user in users:
        if user.username in invalid_users:
            user.is_active = False
            user.save()
            print(f'使用者：{user}，已停用。')