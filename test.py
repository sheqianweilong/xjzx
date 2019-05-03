import re

mobile = "23399999999"
check_mobile = re.compile(r"^1[2-9]\d{9}$")
a = check_mobile.match(mobile).group()
print(a)
