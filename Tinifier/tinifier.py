import tinify
import os
import shutil
from PIL import Image
import PIL
import sys
import time

#Used just for deleting lines of text in cmd for windows
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
########################################################

PIL.Image.MAX_IMAGE_PIXELS = 933120000 #Increases the number of pixels pillow can read (Else it thinks big images are zip bombs, dumbass lib)


root=os.path.dirname(os.path.abspath(__file__))+"\\"
print("Root Dir:",root)


tinyKeys=open((root+"tinyKeys.txt"),"r").read().splitlines()
print(tinyKeys)
print("Loaded",len(tinyKeys),"API Keys")
tinyKeyVal=0
tinify.key = tinyKeys[tinyKeyVal]

compressions_this_month = tinify.compression_count


rawPath=root+"Raw\\"
resizedPath=root+"Resized\\"
compPath=root+"AutoCompressed\\"

imagesArray=[]
errorPaths=[]
sizes=[]

numSizes=int(input("Number of sizes to resize to:"))

for sizeCounter in range(0,numSizes):
    widthX=int(input("X:"))
    widthY=int(input("Y:"))
    sizes.append([widthX,widthY])

maxImgSize=100000#Max no of bits the image size can be

dirIterator=1
moved=False


def eraseLine(eraseVal):#Erases the number of lines passed to it
    for erase in range (0,eraseVal):
        erase_line = '\x1b[2K' # USed for animated text
        cursor_up = '\x1b[1A'
        sys.stdout.write(cursor_up) #goes up a line
        sys.stdout.write(erase_line) #erases the line



#main
print("\n"*50)
files=os.listdir(rawPath)
print("Files:",files)
if len(os.listdir(rawPath))==1:
    courseName=(os.listdir(rawPath)[0].split(".")[0])
    print(courseName)
else:
    courseName=input("Output folder name:")
courseName=courseName.title()#Capitalizes the first letter of each word so the user doesnt have to because im lazy
courseName=courseName.replace(" ","_")
courseName=courseName.replace("-","_")
courseName=courseName.replace("'","_")



#Gets all files in the directory
for listedItem in files:
    if "." in listedItem and listedItem!="desktop.ini": #Files will have a . dirs (likely) won't, also doesnt bring in desktop.ini idk why thats there
        imagesArray.append(listedItem)#Adds to a list of files

print("Tinify Compressions left this month:",compressions_this_month)
print("Number of images to process",len(imagesArray))

#Creates dirs if they don't curently exist (Raw is recreated at end for next use)
if not os.path.exists(resizedPath):
    os.makedirs(resizedPath)

if not os.path.exists(compPath):
    os.makedirs(compPath)


imageCounter=1
for image in imagesArray:#Every file within the dir

    print("\n---------------------------------------")
    print("Image",imageCounter,"/",len(imagesArray))
    imageCounter+=1

    imgExtension=(image.split("."))[1]#Gets the part following the .
    if imgExtension !="jpg":#Also converts .jpeg for the sake of the filenames being consistent
        #Converts image to jpg because tinify only uses jpgs
        print("Converting",image,"from",imgExtension," to .jpg")
        im = Image.open(os.path.join(rawPath, image))
        filename=image.replace(("."+imgExtension),".jpg")#Replaces the extension with .jpg
        JpgPath=rawPath+filename
        im=im.convert('RGB')#Converts to RGB (.png is RGBA so A channel needs to be killed off)
        im.save(JpgPath, "JPEG", quality=100, optimize=True)#Saves the image at maximum quality as it will be lowered later on
        print("Finished converting image")

    else:#I cant be arsed to rename/rejig things so this is here (I also dont understand it but know things will break if i remove it)
        filename=image
        JpgPath=rawPath+filename
        print("path:",JpgPath)

    #Resizes the image if it's too large to upload to tinify
    im = Image.open(JpgPath)
    w,h=im.size
    if w>15000 or h>10000:
        print("Current size:",im.size)
        print("Image too large, resizing via PILLOW")
        im.thumbnail((15000,10000))
        print("New size:",im.size)
    else:
        im.thumbnail(im.size)
    im.save(JpgPath, "JPEG", quality=100, optimize=True)#Saves the image at maximum quality as it will be lowered later on

    
    
    #Resizes the image smartly using tinify
    print("Resizing",filename,"via tinify")
    for size in sizes:#loops through all given sizes
        widthX=size[0]
        widthY=size[1]
        print("Resolution:",widthX,"x",widthY)
        retryCount=0
        isResized=False
        resizedFilename=str(widthX)+"x"+str(widthY)+"_"+filename
        while isResized==False:
            try:
                source = tinify.from_file(JpgPath)
                resized = source.resize(method="cover",width=widthX,height=widthY)
                resized.to_file(resizedPath+resizedFilename)
                print("Resized image successfully")
                isResized=True
            except tinify.errors.AccountError:
                print("RUN OUT OF COMPRESSIONS THIS MONTH, CHANGING KEY")
                tinyKeyVal+=1
                print("Key Value:",tinyKeyVal)
                tinify.key = tinyKeys[tinyKeyVal]
            except tinify.errors.ClientError as e:
                print("!!!!!!!!!!!!!!")
                print("Broke somehow")
                print("How it broke:",e)
                print("File:",resizedPath+resizedFilename)
                retryCount+=1
                if retryCount>5:
                    isResized=True
                    errorPaths.append([(resizedPath+resizedFilename),e])
                print("Skipping this one because it won't work")
                
        print("\n"*3)

        #Changes the image JPG quality value until it is below 100kb
        correctSize=False
        qualityValue=100#Starts at 100% quality in case the size is already good
        im = Image.open(os.path.join(resizedPath+resizedFilename))
        while correctSize==False:#loops until finds good size
            eraseLine(2)
            im.thumbnail(im.size)
            im.save((resizedPath+resizedFilename), "JPEG", quality=qualityValue, optimize=True)#Changes quality value then saves
            if os.path.getsize(resizedPath+resizedFilename) < maxImgSize: #If image is smaller than max size
                correctSize=True#Break loop
                print("Below",maxImgSize,"bytes at",qualityValue,"% quality")
                print("Size:",os.path.getsize(resizedPath+resizedFilename),"bytes")
            else:
                qualityValue=qualityValue-1#Lowers quality
                if qualityValue<1:#Makes sure the quality doesn't go below 1 because idk what will happen
                    qualityValue=1
                print("Size is",os.path.getsize(resizedPath+resizedFilename))
                print("Quality:"+str(qualityValue)+"%")
                time.sleep(0.05)


            #Compresses the image even further using tinify
        print("Compressing image via tinify")
        retryCount=0
        isCompressed=False
        while isCompressed==False:
            try:
                source = tinify.from_file(resizedPath+resizedFilename)
                originalSize=os.path.getsize(resizedPath+resizedFilename)
                source.to_file(compPath+resizedFilename)
                print("Compressed image successfully")
                print("Kilobytes saved after Tinifying:",(originalSize-os.path.getsize(compPath+resizedFilename))/1000,"kb")
                isCompressed=True
            except tinify.errors.AccountError:
                print("RUN OUT OF COMPRESSIONS THIS MONTH, CHANGING KEY")
                tinyKeyVal+=1
                print("Key Value:",tinyKeyVal)
                tinify.key = tinyKeys[tinyKeyVal]
            except tinify.errors.ClientError as e:
                print("!!!!!!!!!!!!!!")
                print("Broke somehow")
                print("How it broke:",e)
                print("File:",resizedPath+resizedFilename)
                retryCount+=1
                if retryCount>5:
                    isCompressed=True
                    errorPaths.append([(resizedPath+resizedFilename),e])
                    print("Skipping this one because it won't work")
        
            
#Moves all dirs to the 'organized' folder
courseDir=root+courseName
while moved==False:
    try:
        print("\nMoving dirs to",courseName)
        shutil.move(rawPath,courseDir)
        shutil.move(resizedPath,courseDir)
        shutil.move(compPath,courseDir)
        print("Moved all dirs")
        os.makedirs(rawPath)
        print("Recreated Raw folder for next use")
        moved=True
    except shutil.Error:
        courseDir=courseDir+"_"+str(dirIterator)
        dirIterator+=1



print("Done!")

if len(errorPaths)>0:
    print("Errored files:")
    for errorVal in errorPaths:
        print(errorVal[0])
        print(errorVal[1])

os.startfile(courseDir+r"\\AutoCompressed")
