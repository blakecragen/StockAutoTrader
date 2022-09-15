def write(text):
    writer = open("RobinhoodData.txt","a+")
    text = str(text)
    writer.write("\n" + text)
    writer.close()
