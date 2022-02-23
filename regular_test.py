import re

text = """
begin
something 1
begin
something 2
/s/
something 3
/s/
"""

print(re.search(r'begin((?!begin).)*?/s/', text, re.DOTALL).group(0))

# inp = """step into
# 1
# 2
# step into
# 3
# 4
# step out"""
# matches = re.search(r'\bstep into(?:(?!step into).)*?\bstep out\b', inp, flags=re.DOTALL).group()
# print(matches)