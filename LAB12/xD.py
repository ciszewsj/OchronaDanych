if __name__ == "__main__":
    a = "12345678"
    a += chr(1)
    print(a)
    f = open("file.txt", "w")
    f.write(a)
    f.close()
