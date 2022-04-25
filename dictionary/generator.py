f1 = open("words.txt", "r")
f2 = open("blackWords.txt", "w")
vowels = "а,у,о,ы,э,я,ю,ё,и,е".split(",")
vowelsBig = [x.upper() for x in vowels]
words = f1.read().split("\n")