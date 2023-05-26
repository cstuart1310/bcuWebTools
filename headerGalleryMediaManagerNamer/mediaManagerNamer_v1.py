print("\n"*10)#Clears


#inputs
noImages=int(input("Number of images with the same course:"))
course=input("Course:")
offsetVal=input("Offset:")
names=[]

try:
    imgCount=int(offsetVal)+1
except Exception as e:
    print(e)

for x in range(0,noImages):
    print("\n")
    print("-----------------------------------------")
    name=input("Name:")
    names.append(name)
    imgCount=names.count(name)#Increases the image count if the name has already been put on a piece of work (Also works if an empty name is entered)
    
    altDesc=input("Image description:")

    print("\n")
    #processed data
    print("_________________________________________")
    print("Title:")    
    if name=="":
        print(course+" Piece "+str(imgCount))
    else:
        print(name+" - "+course+" Piece "+str(imgCount))
    print("\n")
    
    print("----------------------------------------")
    print("Description:")    
    if name=="":
        print(course+" Piece "+str(imgCount)+"\n"+altDesc)
    else:
        print(name+" - "+course+" Piece "+str(imgCount)+"\n"+altDesc)
    print("\n")

    print("----------------------------------------")
    print("Alt Text:")
    print(altDesc)
    print("\n")
    
    print("----------------------------------------")
    print("Caption Title/Text")
    if name=="":
        print("Work from "+course)
    else:
        print("Work by - "+name+", "+course)
    
    print("--------------------------------------------------------------------------------")
