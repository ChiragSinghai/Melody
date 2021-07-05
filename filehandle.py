from tkinter import *
import os
fpath=''

class fileHandle:
    def __init__(self):
        pass
    @classmethod
    def save(cls,name):
        if(os.path.isdir(fpath+"//Melody//Music")):
                albumname=fpath+"//Melody//Music/"+name+".txt"
        
                if(os.path.isfile(albumname)):
                   return False
                else:
                    file=open(albumname,'a+')
                    file.close()
                    return True
        else:
            os.chdir('C:')
            os.makedirs(fpath+"//Melody//Music")
            cls.save(name)
            return True

    @classmethod
    def PlaylistData(cls):
        files=[]
        if os.path.isdir(fpath+"//Melody//Music"):
            for a,b,files in os.walk(fpath+"//Melody//Music",topdown=False):
                pass
            
            if files!=[]:
                i=0
                for filename in files:
                    file=os.path.splitext(os.path.basename(filename))
                    files[i]=file[0]
                    i+=1
        return files
    @classmethod    
    def dataInPlaylist(cls,name):
        #print(os.path.isfile("playlist/"+name+".txt"))
        if(os.path.isfile(fpath+"//Melody//Music//"+name+".txt")):
            file=open(fpath+"//Melody//Music//"+name+".txt","r")
            songs=file.readlines()
            i=0
            for song in songs:
                songs[i]=(song.strip())
                i+=1
            file.close()
            return songs
        else:
            return False
    @classmethod
    def addSongInPlaylist(cls,filelocation,currentplaylist):
        file=open(fpath+"//Melody//Music//"+currentplaylist+".txt","a+")
        file.write(filelocation+'\n')
        file.close()

    @classmethod
    def deleteSong(cls,songPath,currentplaylist):
        songNames=cls.dataInPlaylist(currentplaylist)
        if songNames or songNames==[]:
            file=open(fpath+"//Melody//Music//"+currentplaylist+".txt",'w')
            counter=0
            for name in songNames:
                if name==songPath and counter==0:
                    counter=1
                else:
                    file.write(name+'\n')
            file.close()
        else:
            print("dont exists")
    @classmethod
    def saveplaylist(cls,songs,name):
        file=open(fpath+"//Melody//Music//"+name+".txt",'w')
        for song in songs:
            file.write(song+'\n')
        file.close()
        

if __name__=='__main__':      
    obj=fileHandle()
    print(obj.save('chi'))
    print(fileHandle.PlaylistData())
    


