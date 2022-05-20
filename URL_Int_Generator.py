#Used for stuff like making a list of every staff profile page
phrase=input("Input phrase:")
maxInt=int(input("Max number to append to end:"))

for x in range(0,maxInt+1):
    print(phrase+str(x))