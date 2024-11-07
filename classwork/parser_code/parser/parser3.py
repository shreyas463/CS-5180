from bs4 import BeautifulSoup

bs = BeautifulSoup("<HTML><body><p>Some text</p></body><HTML>", 'html.parser')

print(bs.body)
print("")

print(bs.body.prettify())