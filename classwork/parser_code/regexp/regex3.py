from bs4 import BeautifulSoup
import re

print("?")

bs = BeautifulSoup("<HTML><body><title>abb</title></body><HTML>", 'html.parser')
regex = re.compile('a?bb')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("*")

bs = BeautifulSoup("<HTML><body><title>aaabbbbb</title></body><HTML>", 'html.parser')
regex = re.compile('a*b*')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("+")

bs = BeautifulSoup("<HTML><body><title>abbbbbb</title></body><HTML>", 'html.parser')
regex = re.compile('a+b+')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("[]")

bs = BeautifulSoup("<HTML><body><title>CAPITALS</title></body><HTML>", 'html.parser')
regex = re.compile('[A-Z]*')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("()")

bs = BeautifulSoup("<HTML><body><title>ababaaaaab</title></body><HTML>", 'html.parser')
regex = re.compile('(a*b)*')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("{m, n}")

bs = BeautifulSoup("<HTML><body><title>aabbb</title></body><HTML>", 'html.parser')
regex = re.compile('a{2,3}b{2,3}')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("[^]")

bs = BeautifulSoup("<HTML><body><title>lowercase</title></body><HTML>", 'html.parser')
regex = re.compile('[^A-Z]*')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("|")

bs = BeautifulSoup("<HTML><body><title>bid</title></body><HTML>", 'html.parser')
regex = re.compile('b(a|i|e)d')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print(".")

bs = BeautifulSoup("<HTML><body><title>bad</title></body><HTML>", 'html.parser')
regex = re.compile('b.d')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("\d")

bs = BeautifulSoup("<HTML><body><title>12a</title></body><HTML>", 'html.parser')
regex = re.compile('\d*a')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("\D")

bs = BeautifulSoup("<HTML><body><title>ba</title></body><HTML>", 'html.parser')
regex = re.compile('\D*a')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("\w")

bs = BeautifulSoup("<HTML><body><title>Apple</title></body><HTML>", 'html.parser')
regex = re.compile('\wp')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("\W")

bs = BeautifulSoup("<HTML><body><title>#party</title></body><HTML>", 'html.parser')
regex = re.compile('\Wp')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("\s")

bs = BeautifulSoup("<HTML><body><title>Hello World!</title></body><HTML>", 'html.parser')
regex = re.compile('\s[Ww]')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())

print("\S")

bs = BeautifulSoup("<HTML><body><title>First-World!</title></body><HTML>", 'html.parser')
regex = re.compile('\S[Ww]')

matches = bs.find_all(text=regex)
for match in matches:
    print(match.strip())