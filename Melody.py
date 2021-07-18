try:
    from sys import argv
    from pygame import mixer
    from tkinter import filedialog,messagebox
    from tkinter import *
    import os.path
    from math import ceil
    from mutagen.mp3 import MP3
    from time import strftime,gmtime
    from filehandle import fileHandle
    from tkscrolledframe import ScrolledFrame
    fpath=''

    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    mixer.init()
    root = Tk()
    root.iconbitmap((fpath+'images//Melody.ico'))
    root.title("Melody")
    root.configure(bg='black')
    root.geometry("463x360+0+0")

    #s.map('Horizontal.TScale',slidercolor=[('active', 'white'),('!focus','white'),('focus','orange red')])
    #s.configure('TButton', background='black', foreground='black', stipple='')
    # ===================global-variable=========
    mutevolume = count = mute = init_time = var = repeat_var = 0
    oldindex = movingscale = name = currentplaylist = None
    scalemoved = closing = False
    songs = []
    saved = False
    helpobj = None


    # ==================================classes==============
    class help:
        def __init__(self, root):
            self.root = root
            self.top = Toplevel(self.root)
            self.top.title('Melody/Help')
            self.top.iconbitmap((fpath + 'images//Melody.ico'))
            self.getSize()
            self.top.geometry(f'{self.top_width}x{self.top_height}+{self.X}+{self.Y}')
            self.top.transient(self.root)
            self.top.resizable(False, False)
            self.top.grab_set()
            self.design()
            self.top.protocol("WM_DELETE_WINDOW", self.cancel)
            self.top.bind('<Escape>', self.cancel)

        def design(self):
            self.vertical_scroll = Scrollbar(self.top)
            self.vertical_scroll.pack(side=RIGHT, fill=Y)
            self.txtobj = Text(self.top,yscrollcommand=self.vertical_scroll.set,wrap='word')
            self.txtobj.pack(fill=BOTH,expand=True)
            self.vertical_scroll.config(command=self.txtobj.yview)
            self.insertText()

        def insertText(self):
            file = open(fpath+'Help.txt','r')
            s = file.read()
            self.txtobj.insert('1.0',s)
            file.close()


        def cancel(self, event=None):
            global helpobj
            self.top.destroy()
            del helpobj

        def getSize(self):
            root_width = self.root.winfo_width()
            root_height = self.root.winfo_height()
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            if root_width <= 500 and root_height <= 400:
                self.top_width = 420
                self.top_height = 330
                self.X = (root_width // 2) - (self.top_width // 2) + x
                self.Y = (root_height // 2) - (self.top_height // 2) + y

            elif root_width <= 800 and root_height <= 550:
                self.top_width = 440
                self.top_height = 350
                if root_width <= 500:
                    self.top_width = 420
                if root_height <= 400:
                    self.top_height = 330
                self.X = (root_width // 2) - (self.top_width // 2) + x
                self.Y = (root_height // 2) - (self.top_height // 2) + y

            else:
                self.top_width = 570
                self.top_height = 480
                if root_width <= 800:
                    self.top_width = 440
                if root_height <= 550:
                    self.top_height = 350
                if root_width <= 500:
                    self.top_width = 420
                if root_height <= 400:
                    self.top_height = 330

                self.X = (root_width // 2) - (self.top_width // 2) + x
                self.Y = (root_height // 2) - (self.top_height // 2) + y


    class newplaylist:
        def __init__(self, root):
            self.root = root
            self.top = Toplevel(self.root)
            self.top.title('Melody/New-playlist')
            self.top.iconbitmap((fpath+'images//Melody.ico'))
            self.getSize()
            self.top.geometry(f'{self.top_width}x{self.top_height}+{self.X}+{self.Y}')
            self.top.transient(self.root)
            self.top.resizable(False, False)
            self.top.grab_set()
            self.design()
            # self.root.bind('<Configure>',self.getSize)
            self.top.bind('<Return>', self.ok)
            self.top.protocol("WM_DELETE_WINDOW", self.cancel)
            self.top.bind('<Escape>',self.cancel)

        def design(self):
            frame = Frame(self.top)
            frame.pack(fill=BOTH, expand=True)
            labelframe = Frame(frame)
            labelframe.pack(expand=True)
            centerframe = Frame(frame)
            centerframe.pack(expand=True)
            buttonframe = Frame(frame)
            buttonframe.pack(expand=True)

            self.name = StringVar()
            playlistimage = PhotoImage(file=(fpath+"images//playlist.png"))
            pencilimage = PhotoImage(file=(fpath+"images//pencil.png"))

            imagelabel = Label(labelframe, image=playlistimage)
            imagelabel.image = playlistimage  # keep a reference!
            imagelabel.pack(pady=10)
            playlistname = Entry(centerframe, width=20, textvariable=self.name, font=('Arial', 16, 'bold'))
            playlistname.pack(pady=10, side=LEFT)
            playlistname.focus_set()
            pencillabel = Label(centerframe, image=pencilimage)
            pencillabel.image = pencilimage
            save = Button(buttonframe, text="Save", width=10, command=self.ok, font=('Arial', 16, 'bold'))
            save.pack(pady=10)
            cancel = Button(buttonframe, text="Cancel", width=10, command=self.cancel, font=('Arial', 16, 'bold'))
            cancel.pack(pady=10)
            pencillabel.pack(side=LEFT)

        def cancel(self,event=None):
            global obj, closing, saved
            saved = False
            self.top.destroy()
            closing = False
            del obj

        def ok(self, event=None):
            global currentplaylist, closing, chill
            if self.name.get() != '':
                created = fileHandle.save(self.name.get())
                if not created:
                    messagebox.showerror('Error', f'{self.name.get()} already exists', parent=self.top)
                    self.name.set('')
                else:
                    if filemenu.entrycget(1, "state") == "disabled":
                        currentplaylist = self.name.get()
                        songlist.delete(0, END)
                        songs.clear()
                        chill.cancel()

                    elif closing:
                        currentplaylist = self.name.get()
                        saveplaylist()

                    else:
                        currentplaylist = self.name.get()
                        songlist.delete(0, END)
                        songs.clear()

                    title_change()
                    global obj
                    self.top.destroy()
                    closing = False
                    del obj

        def getSize(self):
            root_width = self.root.winfo_width()
            root_height = self.root.winfo_height()
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            if root_width <= 500 and root_height <= 400:
                self.top_width = 420
                self.top_height = 330
                self.X = (root_width // 2) - (self.top_width // 2) + x
                self.Y = (root_height // 2) - (self.top_height // 2) + y

            elif root_width <= 800 and root_height <= 550:
                self.top_width = 440
                self.top_height = 350
                if root_width <= 500:
                    self.top_width = 420
                if root_height <= 400:
                    self.top_height = 330
                self.X = (root_width // 2) - (self.top_width // 2) + x
                self.Y = (root_height // 2) - (self.top_height // 2) + y

            else:
                self.top_width = 570
                self.top_height = 480
                if root_width <= 800:
                    self.top_width = 440
                if root_height <= 550:
                    self.top_height = 350
                if root_width <= 500:
                    self.top_width = 420
                if root_height <= 400:
                    self.top_height = 330

                self.X = (root_width // 2) - (self.top_width // 2) + x
                self.Y = (root_height // 2) - (self.top_height // 2) + y


    # ===========================================================
    class SaveAs:
        def __init__(self, root):
            self.root = root
            self.top = Toplevel(self.root)
            self.top.title('Melody/New-playlist')
            self.top.configure(bg='black')
            self.top.iconbitmap((fpath+'images//Melody.ico'))
            self.getSize()
            self.top.geometry(f'{self.top_width}x{self.top_height}+{self.X}+{self.Y}')
            self.top.transient(self.root)
            self.top.resizable(False, False)
            self.top.grab_set()
            self.design()
            self.top.bind('<Return>', self.ok)
            self.top.protocol("WM_DELETE_WINDOW", self.cancel)
            self.top.bind('<Escape>',self.cancel)

        def design(self):
            frame = Frame(self.top)
            frame.pack(fill=BOTH, expand=True)
            labelframe = Frame(frame)
            labelframe.pack(expand=True)
            centerframe = Frame(frame)
            centerframe.pack(expand=True)
            buttonframe = Frame(frame)
            buttonframe.pack(expand=True)

            self.name = StringVar()
            playlistimage = PhotoImage(file=(fpath+"images//playlist.png"))
            pencilimage = PhotoImage(file=(fpath+"images//pencil.png"))

            imagelabel = Label(labelframe, image=playlistimage)
            imagelabel.image = playlistimage  # keep a reference!
            imagelabel.pack(pady=10)
            playlistname = Entry(centerframe, width=20, textvariable=self.name, font=('Arial', 16, 'bold'))
            playlistname.pack(pady=10, side=LEFT)
            playlistname.insert(END, currentplaylist)
            playlistname.select_range(0, END)
            playlistname.focus_set()
            pencillabel = Label(centerframe, image=pencilimage)
            pencillabel.image = pencilimage
            save = Button(buttonframe, text="Save", width=10, command=self.ok, font=('Arial', 16, 'bold'))
            save.pack(pady=10)
            cancel = Button(buttonframe, text="Cancel", width=10, command=self.cancel, font=('Arial', 16, 'bold'))
            cancel.pack(pady=10)
            pencillabel.pack(side=LEFT)

        def cancel(self,event=None):
            global obj2
            self.top.destroy()
            del obj2

        def ok(self, event=None):
            global currentplaylist
            # noinspection PyShadowingNames
            name = self.name.get()
            os.rename(r'Melody\Music\%s.txt' % (currentplaylist), r'Melody\Music\%s.txt' % name)
            currentplaylist = self.name.get()
            saveplaylist()
            title_change()
            self.cancel()

        def getSize(self):
            root_width = self.root.winfo_width()
            root_height = self.root.winfo_height()
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            if root_width <= 500 and root_height <= 400:
                self.top_width = 420
                self.top_height = 330
                self.X = (root_width // 2) - (self.top_width // 2) + x
                self.Y = (root_height // 2) - (self.top_height // 2) + y

            elif root_width <= 800 and root_height <= 550:
                self.top_width = 440
                self.top_height = 350
                if root_width <= 500:
                    self.top_width = 420
                if root_height <= 400:
                    self.top_height = 330
                self.X = (root_width // 2) - (self.top_width // 2) + x
                self.Y = (root_height // 2) - (self.top_height // 2) + y

            else:
                self.top_width = 570
                self.top_height = 480
                if root_width <= 800:
                    self.top_width = 440
                if root_height <= 550:
                    self.top_height = 350
                if root_width <= 500:
                    self.top_width = 420
                if root_height <= 400:
                    self.top_height = 330

                self.X = (root_width // 2) - (self.top_width // 2) + x
                self.Y = (root_height // 2) - (self.top_height // 2) + y


    # ==============================================================
    class AlbumsWindow:
        def __init__(self, root):

            global saved
            self.currentsaver = saved
            saved = True
            self.root = root
            self.frame = Frame(self.root)
            self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.window = ScrolledFrame(self.frame, relief=FLAT)
            self.window.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.window.bind_arrow_keys(self.frame)
            self.window.bind_scroll_wheel(self.frame)
            self.inner_frame = self.window.display_widget(Frame, fit_width=True)
            self.Albums()

        def Albums(self):
            row = 0
            column = 0
            playlistName = fileHandle.PlaylistData()
            self.root.bind('<Escape>', self.cancel)
            for name in playlistName:
                if column == 4:
                    column = 0
                    row += 1

                label = Label(self.inner_frame, text=name, width=30, height=10, relief=SOLID,
                              font=("Helvetica", 10, "bold"))
                label.grid(row=row, column=column, padx=20, pady=10)
                column += 1
            self.inner_frame.bind_class('Label', '<Button>', self.Buttonpress)

        def Buttonpress(self, event):
            global saved, chill
            playlistname = fileHandle.PlaylistData()
            for name in playlistname:
                if (name == event.widget['text']):
                    saved = True
                    playlist = fileHandle.dataInPlaylist(name)
                    SetPlaylist(playlist, name)
                    self.cancel()
                    break

        def cancel(self, event=None):
            global chill, saved
            if event != None:
                saved = self.currentsaver
            toggle()
            self.root.unbind('<Escape>')
            self.inner_frame.unbind_class('Label', '<Button>')
            self.inner_frame.destroy()
            self.window.destroy()
            self.frame.destroy()
            del chill, self

        # ========================function==============


    def title_change():
        if currentplaylist != None:
            root.title(f'Melody-{currentplaylist}')
        else:
            root.title('Melody')


    def SetPlaylist(playlist, name):
        global currentplaylist, songs
        stop_music()
        songlist.delete(0, END)
        songs.clear()
        songs = playlist
        for song in songs:
            file = os.path.splitext(os.path.basename(song))
            songlist.insert(END, (file[0]))
            songlist.yview(END)

        currentplaylist = name
        title_change()


    def add_file(system_arg=None):
        global saved
        if system_arg == None:
            filename = filedialog.askopenfilename(title="select a file",
                                                  filetypes=(("MP3 file", "*.mp3"),
                                                             ("WAV file", "*.wav"),
                                                             ("All files", "*.*")))
            if filename != '':
                file = os.path.splitext(os.path.basename(filename))
                songlist.insert(END, (file[0]))
                songlist.yview(END)
                songs.append(filename)
                saved = False
        else:
            filename = system_arg
            file = os.path.splitext(os.path.basename(filename))
            songlist.insert(END, (file[0]))
            songlist.yview(END)
            songs.append(filename)
            saved = False


    def delete():
        global currentplaylist
        selected = songlist.curselection()
        statusbar['text'] = f'Can\'t play {songlist.get(ACTIVE)}'
        songlist.delete(ACTIVE)
        if currentplaylist != None:
            fileHandle.deleteSong(songs[selected[0]], currentplaylist)
        songs.pop(selected[0])
        #stop_music()


    def add_multiple_files():
        global saved
        filenames = filedialog.askopenfilenames(title="select a file",
                                                filetypes=(("MP3 file", "*.mp3"),
                                                           ("WAV file", "*.wav"),
                                                           ("All files", "*.*")))
        if filenames != '':
            for filename in filenames:
                file = os.path.splitext(os.path.basename(filename))
                songlist.insert(END, (file[0]))
                songlist.yview(END)
                songs.append(filename)
            saved = False


    def delete_multiple_songs():
        answer = messagebox.askquestion('Melody', 'Do you want to delete every song?', parent=root)

        if answer == 'yes':
            if mixer.music.get_busy():
                stop_music()
            songlist.delete(0, END)
            songs.clear()
            if currentplaylist != None:
                saveplaylist()
            statusbar['text'] = 'Play some music'


    def song_length(filename):
        global total_length, songs
        file = os.path.splitext(os.path.basename(filename))
        try:
            if (file[1] == '.mp3'):
                audio = MP3(filename)
                total_length = audio.info.length
            else:
                audio = mixer.Sound(filename)
                total_length = audio.get_length()
            total_time = strftime('%M:%S', gmtime(total_length))
            final_time['text'] = total_time
            Time['to'] = (total_length)
        except:
            print('hey')


    def initial_time_change():
        global count, total_length, oldindex, scalemoved, movingscale, var , repeat_var
        selected = songlist.curselection()
        if selected == ():
            pass
        else:
            try:
                if oldindex == None or oldindex != selected[0] or scalemoved:
                    if scalemoved:
                        movingscale = int(Time.get())
                        mixer.music.stop()
                        mixer.music.load(songs[selected[0]])
                        mixer.music.play(start=Time.get())
                        Time.set(movingscale)
                        scalemoved = False
                        var = 0

                    else:
                        mixer.music.load(songs[selected[0]])
                        mixer.music.play()
                        Time.set(0)
                        playbutton['image'] = playimage
                        count = 0
                    oldindex = selected[0]
                    song_length(songs[selected[0]])

                if mixer.music.get_busy():
                    current_time = (mixer.music.get_pos() / 1000)
                    if movingscale != None:
                        var += movingscale + 1
                        movingscale = None
                    current_time += var
                else:
                    current_time = int(total_length)
                converted_current_time = strftime('%M:%S', gmtime(current_time))
                playbutton['state'] = 'normal'
                if count == 0:
                    playbutton['image'] = pauseimage
                    statusbar['text'] = f'{songlist.get(selected[0])}' + ' Playing'
                    if current_time == int(total_length):
                        if repeat_var==0:
                            stop_music()
                        elif repeat_var==1:
                            selected = songlist.curselection()
                            next_song_index=selected[0]
                            stop_music()
                            songlist.activate(next_song_index)
                            songlist.selection_set(next_song_index, last=None)
                        else:
                            forward_music()


                    elif Time.get() == int(current_time) == 0:
                        Time.set(int(current_time))
                        initial_time['text'] = converted_current_time

                    elif Time.get() == int(current_time - 1):
                        Time.set(int(current_time))
                        initial_time['text'] = converted_current_time

                    elif int(current_time) == (Time.get()) + 2:
                        Time.set(int(current_time))
                        initial_time['text'] = converted_current_time

                    elif int(current_time) == (Time.get()):
                        Time.set(int(current_time))

                    else:
                        scalemoved = True

                else:
                    playbutton['image'] = playimage
                    statusbar['text'] = f'{songlist.get(selected[0])}' + ' Paused'
            except Exception as e:
                #print('error',e)
                delete()
        initial_time.after(300, initial_time_change)


    def play_music():
        global count
        if (count == 0):
            mixer.music.pause()
            playbutton['image'] = (pauseimage)
            count = 1
        else:
            mixer.music.unpause()
            playbutton['image'] = (playimage)
            count = 0


    def stop_music():
        global count, oldindex
        mixer.music.stop()
        if songlist.curselection() != ():
            statusbar['text'] = f'{songlist.get(ANCHOR)}' + ' Stopped'
        songlist.selection_clear(0, END)
        count = 1
        oldindex = None
        play_music()
        Time.set(0)
        initial_time['text'] = '--:--'
        final_time['text'] = '--:--'
        playbutton['state'] = 'disable'


    def rewind_music():
        global count, flag
        selected = songlist.curselection()
        if selected != ():
            if songlist.size() == 1:
                next_song_index = selected[0]

            elif selected[0] == 0:
                next_song_index = songlist.size() - 1

            else:
                next_song_index = selected[0] - 1
            stop_music()
            songlist.activate(next_song_index)
            songlist.selection_set(next_song_index, last=None)


    def forward_music():
        global count
        selected = songlist.curselection()
        if selected != ():
            if songlist.size() == 1:
                next_song_index = selected[0]

            elif selected[0] == songlist.size() - 1:
                next_song_index = selected[0] - selected[0]

            else:
                next_song_index = selected[0] + 1
            stop_music()
            songlist.activate(next_song_index)
            songlist.selection_set(next_song_index, last=None)


    def set_volume(value):
        global mute, mutevolume
        value = int(value)
        if (mute == 0 and value <= 0):
            mutebutton['image'] = (speakerimage0)

        elif (mute == 1 and value <= 0):
            mutebutton['image'] = (muteimage)

        elif (value > 0 and value <= 50):
            mutevolume = value
            mutebutton['image'] = (speakerimage1)
            mute = 0
        elif (value > 50 and value <= 75):
            mutevolume = value
            mutebutton['image'] = (speakerimage2)
            mute = 0
        else:
            mutevolume = value
            mutebutton['image'] = (speakerimage3)
            mute = 0
        value = value / 100
        mixer.music.set_volume(value)


    def volume_down():
        current_volume = float(volume.get())
        volume.set(current_volume - 1)
        set_volume(current_volume - 1)


    def volume_up():
        current_volume = float(volume.get())
        volume.set(current_volume + 1)

    def repeat():
        global  repeat_var
        if repeat_var==0:
            repeat_var+=1
            loop_btn.config(image=repeatone)
        elif repeat_var==1:
            repeat_var+=1
            loop_btn.config(image=repeatall)
        else:
            repeat_var=0
            loop_btn.config(image=repeatnone)
    def mute_unmute():
        global mute, mutevolume
        if (mute == 1):
            if (mutevolume * 100 <= 0):
                mute = 0
                mutebutton['image'] = (speakerimage0)

            else:
                mutevolume1 = ceil(mutevolume * 100)
                volume.set(mutevolume1)
                mute = 0
        else:
            mutevolume = mixer.music.get_volume()
            volume.set(0)
            mutebutton['image'] = (muteimage)
            mute = 1


    # ==========================
    def saveplaylist():
        global saved, closing, obj
        if not saved:
            saved = True
            if currentplaylist == None:
                closing = True
                obj = newplaylist(root)
            else:
                fileHandle.saveplaylist(songs, currentplaylist)


    def deletesongs():
        global saved
        saved = False
        selected = songlist.curselection()
        if selected != ():
            stop_music()
            songlist.delete(selected[0])
            songs.pop(selected[0])


    def callSaveAs():
        if currentplaylist is not None:
            global obj2
            obj2 = SaveAs(root)
        else:
            saveplaylist()


    def createplaylist():
        global obj, closing
        if not saved:
            if currentplaylist is not None:
                answer = messagebox.askyesnocancel('Melody', f'Do yo want to save {currentplaylist}', parent=root)
                if answer:
                    saveplaylist()
                    obj = newplaylist(root)
                elif answer is None:
                    pass
                else:
                    obj = newplaylist(root)
            else:
                obj = newplaylist(root)
        else:
            obj = newplaylist(root)


    def call_album_window_internal():
        global chill
        toggle()
        chill = AlbumsWindow(root)

    def call_help():
        global helpobj
        helpobj = help(root)

    def callalbumwindow():
        global chill, saved
        if not saved:
            if currentplaylist != None:
                answer = messagebox.askyesnocancel('Melody', f'Do you want to save changes in {currentplaylist} playlist?',
                                                   parent=root)
                if answer:
                    saveplaylist()
                    call_album_window_internal()
                elif answer is None:
                    pass
                else:
                    call_album_window_internal()
            else:
                call_album_window_internal()
        else:
            call_album_window_internal()


    def closeplaylist():
        global currentplaylist, saved, songs
        if currentplaylist != None:
            if not saved:
                answer = messagebox.askyesnocancel('Melody', f'Do you want to save changes in {currentplaylist} playlist?',
                                                   parent=root)
                if answer:
                    saveplaylist()
                elif answer is None:
                    pass
                else:
                    saved = False
                    currentplaylist = None
                    songs.clear()
                    songlist.delete(0, END)
                    stop_music()
            else:
                saved = False
                currentplaylist = None
                songs.clear()
                songlist.delete(0, END)
                stop_music()
            title_change()


    # ==========================================
    def shortcut_save(event):
        saveplaylist()


    def shortcut_open(event):
        callalbumwindow()


    def shortcut_new(event):
        createplaylist()


    def shortcut_saveas(event):
        callSaveAs()


    def bind_m(event):
        mute_unmute()


    def bind_down_key(event):
        volume_down()


    def bind_up_key(event):
        volume_up()


    def remove(event):
        if playbutton['state'] == 'normal':
            play_music()
        return 'break'


    def close_internal():
        mixer.music.stop()
        root.destroy()


    def close():
        global closing, obj
        if not saved:
            if currentplaylist != None:
                answer = messagebox.askyesnocancel('Melody', f'Do you want to save changes in {currentplaylist} playlist?',
                                                   parent=root)
                if answer:
                    saveplaylist()
                    close_internal()
                elif answer is None:
                    pass
                else:
                    close_internal()
            else:
                close_internal()
        else:
            close_internal()


    def toggle():
        if filemenu.entrycget(1, "state") == "normal":
            filemenu.entryconfig(1, state=DISABLED)
            filemenu.entryconfig(2, state=DISABLED)
            filemenu.entryconfig(3, state=DISABLED)
            filemenu.entryconfig(4, state=DISABLED)
            root.unbind('<Control-o>')

        else:
            filemenu.entryconfig(1, state=NORMAL)
            filemenu.entryconfig(2, state=NORMAL)
            filemenu.entryconfig(3, state=NORMAL)
            filemenu.entryconfig(4, state=NORMAL)
            root.bind('<Control-o>', shortcut_open)


    def editmenu_check():
        if songs == []:
            editmenu.entryconfig(2, state=DISABLED)
        else:
            editmenu.entryconfig(2, state=NORMAL)


    def optionmenu_check():
        global count
        if mixer.music.get_busy():
            optionmenu.entryconfig(1, state=NORMAL)
            if count == 0:
                optionmenu.entryconfig(0, state=NORMAL, image=pause_option, label='Pause')
            else:
                optionmenu.entryconfig(0, state=NORMAL, image=play_option, label='Play')

        else:
            optionmenu.entryconfig(0, state=DISABLED)
            optionmenu.entryconfig(1, state=DISABLED)


    def animate_button(event):
        if str(event.type)=='Enter':
            if event.widget['state']!='disabled':
                event.widget.pack(pady=5)
                event.widget.config(bg='orange red')
        else:
            if event.widget['state'] != 'disabled':
                event.widget.pack(pady=0)
                event.widget.config(bg='white')

    def delete_animate(event):
        if str(event.type)=='Enter':
            selected = songlist.curselection()
            event.widget.config(bg='orange red')
            if selected:
                delete_btn.config(image=trash2)
        else:
            event.widget.config(bg='white')
            delete_btn.config(image=trash1)

    def button_enter(event):
        event.widget.config(bg='orange red')

    def button_leave(event):
        event.widget.config(bg='white')


    def play_button(event):
        if str(event.type)=='Enter':
            if event.widget['state']!='disabled':
                event.widget.pack(pady=3)
                event.widget.config(bg='orange red')
        else:
            if event.widget['state'] != 'disabled':
                event.widget.pack(pady=0, padx=0)
                event.widget.config(bg='white')


    try:
        # ====================================images========================
        play_option = PhotoImage(file=(fpath+"images//play-button.png"))
        pause_option = PhotoImage(file=(fpath+"images//pause3.png"))
        stop_option = PhotoImage(file=(fpath+"images//stop-button.png"))

        trash2 = PhotoImage(file=(fpath+"images//trash2.png"))
        trash1 = PhotoImage(file=(fpath+"images//trash1.png"))
        songadd = PhotoImage(file=(fpath+"images//songadd.png"))

        repeatall = PhotoImage(file=(fpath+"images//repeatall.png"))
        repeatnone = PhotoImage(file=(fpath+"images//repeatnone.png"))
        repeatone = PhotoImage(file=(fpath+"images//repeat-once.png"))
        playimage = PhotoImage(file=(fpath+"images//play4.png"))
        pauseimage = PhotoImage(file=(fpath+"images//pause4.png"))
        forwardimage = PhotoImage(file=(fpath+"images//nextmusic.png"))
        stopimage = PhotoImage(file=(fpath+"images//stop1.png"))
        rewindimage = PhotoImage(file=(fpath+"images//rewind1.png"))
        minusimage = PhotoImage(file=(fpath+"images//minus.png"))
        plusimage = PhotoImage(file=(fpath+"images//plus.png"))
        speakerimage0 = PhotoImage(file=(fpath+"images//speaker.png"))
        speakerimage1 = PhotoImage(file=(fpath+"images//speaker50.png"))
        speakerimage2 = PhotoImage(file=(fpath+"images//speaker100.png"))
        speakerimage3 = PhotoImage(file=(fpath+"images//speaker3.png"))
        muteimage = PhotoImage(file=(fpath+"images//mute.png"))
        #loadimage = PhotoImage(file=("images//loader.png"))
    except Exception as e:
        print(e)
    # =========================================frame========================
    topframe = Frame(root, bg='black')
    topframe.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.1)
    centerframe0 = Frame(root, bg='black')
    centerframe0.place(relx=0.1, rely=0.65, relwidth=0.35, relheight=0.2)
    centerframe1 = Frame(root, bg='black')
    centerframe1.place(relx=0.55, rely=0.65, relwidth=0.4, relheight=0.2)
    bottomframe = Frame(root, bg='black')
    bottomframe.place(relx=0.3, rely=0.575, relwidth=0.4, relheight=0.1)
    #insider=Frame(bottomframe,bg='white')
    #insider.pack()
    button_frame=Frame(bottomframe,bg='white')
    button_frame.pack()
    add_button=Frame(button_frame)
    add_button.pack(side=LEFT)
    del_button=Frame(button_frame)
    del_button.pack(side=LEFT)
    loop_button=Frame(button_frame)
    loop_button.pack(side=LEFT)
    forward_frame = Frame(centerframe0)
    forward_frame.pack(side=RIGHT)
    stop_frame = Frame(centerframe0)
    stop_frame.pack(side=RIGHT)
    previous_frame = Frame(centerframe0)
    previous_frame.pack(side=RIGHT)
    mute_frame = Frame(centerframe1)
    mute_frame.pack(side=LEFT)
    minus_frame = Frame(centerframe1)
    minus_frame.pack(side=LEFT)
    volume_frame = Frame(centerframe1)
    volume_frame.pack(side=LEFT)
    plus_frame = Frame(centerframe1)
    plus_frame.pack(side=LEFT)
    play_frame=Frame(topframe)
    play_frame.pack(side=RIGHT)

    # ======================status bar======================
    statusbar = Label(root, text="Welcome",relief=SOLID,font=("arial", 10, "italic"),fg='white',bg='gray12',height=2)
    statusbar.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

    # ============================topframe==========================
    initial_time = Label(topframe, text="--:--", font=("arial", 10, "bold"), anchor=E, bg='Black', fg='white')
    initial_time.place(relx=0.0, relwidth=0.1, relheight=1)
    Time = Scale(topframe, from_=0.0, to=0.0, orient=HORIZONTAL, cursor="dot",relief=FLAT,
                     length=200,troughcolor='white',activebackground='orange red',width=5,showvalue=0,bg='black',sliderrelief='raised',bd=0)
    Time.place(relx=0.1,rely=0.45, relwidth=0.7)

    final_time = Label(topframe, text="--:--", font=("arial", 10, "bold"), anchor=W, bg='Black', fg='white')
    final_time.place(relx=0.8, relwidth=0.1, relheight=1)
    playbutton = Button(play_frame, image=playimage, command=play_music, state='disabled')
    playbutton.pack()
    playbutton.bind('<Enter>',play_button)
    playbutton.bind('<Leave>',play_button)
    # =================================bottomframe=================
    add_btn = Button(add_button, image=songadd, command=add_file,bd=0,bg='white')
    add_btn.pack(padx=2)
    delete_btn = Button(del_button, image=trash1, command=deletesongs,bd=0,bg='white')
    delete_btn.pack(padx=2)
    loop_btn=Button(loop_button,image=repeatnone,bd=0,bg='white',command=repeat)
    loop_btn.pack(padx=2)
    add_btn.bind('<Enter>',button_enter)
    add_btn.bind('<Leave>',button_leave)
    delete_btn.bind('<Enter>',delete_animate)
    delete_btn.bind('<Leave>',delete_animate)
    loop_btn.bind('<Enter>',button_enter)
    loop_btn.bind('<Leave>',button_leave)


    # ==================================listbox=====================
    sb = Scrollbar(root,bg='white')
    sb.place(relx=0.7, rely=0.2, relheight=0.35)
    songlist = Listbox(root, font=("Helvetica", 14, "bold"), activestyle='none'
                       , bg="white", fg="black"
                       , selectbackground="orange red", selectforeground="black"
                       , yscrollcommand=sb.set
                       , exportselection=False, takefocus=0)
    songlist.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.35)
    sb.config(command=songlist.yview)
    songlist.bind('<space>', remove)
    # ===================================centerframe0=====================
    mutebutton = Button(mute_frame, image=speakerimage0, command=mute_unmute, takefocus=0,bd=0,bg='white')
    mutebutton.pack()
    minusbutton = Button(minus_frame, image=minusimage, command=volume_down, takefocus=0,bd=0,bg='white')
    minusbutton.pack()
    volume = Scale(volume_frame, from_=0, to=100, showvalue=0, orient=HORIZONTAL,
                   command=set_volume, width=8,troughcolor='white',bg='white',sliderlength='20',relief='flat',cursor='dot',
                   activebackground='orange red',highlightbackground='black',bd=1,sliderrelief='solid')
    volume.set(75)
    # pygame.mixer.music.set_volume(0.75)
    volume.pack(side=LEFT, anchor=CENTER)
    plusbutton = Button(plus_frame, image=plusimage, command=volume_up, takefocus=0,bd=0,bg='white')
    plusbutton.pack()
    mutebutton.bind('<Enter>',animate_button)
    minusbutton.bind('<Enter>',animate_button)
    plusbutton.bind('<Enter>',animate_button)
    mutebutton.bind('<Leave>',animate_button)
    minusbutton.bind('<Leave>',animate_button)
    plusbutton.bind('<Leave>',animate_button)

    # ===============================centerframe1==================
    rewindbutton = Button(previous_frame, image=rewindimage, command=rewind_music, takefocus=0,bd=0
                          ,width=50,bg='white')
    rewindbutton.pack()
    stopbutton = Button(stop_frame, image=stopimage, command=stop_music, takefocus=0,bd=0,width=50,bg='white')
    stopbutton.pack()
    forwardbutton = Button(forward_frame, image=forwardimage, command=forward_music, takefocus=0,bd=0,width=50,bg='white')
    forwardbutton.pack()
    rewindbutton.bind('<Enter>',animate_button)
    forwardbutton.bind('<Enter>',animate_button)
    stopbutton.bind('<Enter>',animate_button)
    rewindbutton.bind('<Leave>',animate_button)
    forwardbutton.bind('<Leave>',animate_button)
    stopbutton.bind('<Leave>',animate_button)

    # ===========================menubar=================================
    menubar = Menu(root)
    root.config(menu=menubar)
    # filemenu
    filemenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New playlist", accelerator="Ctrl+N", command=createplaylist)
    filemenu.add_command(label="Open playlist", accelerator='Ctrl+O', command=callalbumwindow)
    filemenu.add_command(label="Save", accelerator='Ctrl+S', command=saveplaylist)
    filemenu.add_command(label="Save as...", accelerator='Ctrl+Shift+S', command=callSaveAs)
    filemenu.add_command(label="Close", command=closeplaylist)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=close)

    # editmenu
    editmenu = Menu(menubar, tearoff=0, postcommand=editmenu_check)
    menubar.add_cascade(label="Edit", menu=editmenu)
    editmenu.add_command(label="Add song", command=add_file)
    editmenu.add_command(label="add multiple songs", command=add_multiple_files)
    editmenu.add_command(label="Delete All", command=delete_multiple_songs)
    # editmenu.add_command(label="Paste")

    # optionmenu
    optionmenu = Menu(menubar, tearoff=0, postcommand=optionmenu_check)
    menubar.add_cascade(label="Option", menu=optionmenu)
    optionmenu.add_command(label="Play", image=play_option, compound=LEFT, command=play_music)
    # optionmenu.add_command(label="Pause",image=pause_option,compound=LEFT)
    optionmenu.add_command(label="Stop", image=stop_option, compound=LEFT, command=stop_music)

    # Help
    helpmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About us", command=call_help)

    # =====================================
    if len(argv) >= 2:
        add_file(argv[1])

    root.protocol("WM_DELETE_WINDOW", close)
    root.bind("m", bind_m)
    root.bind("-", bind_down_key)
    root.bind("=", bind_up_key)
    root.bind("<Control-n>", shortcut_new)
    root.bind("<Control-s>", shortcut_save)
    root.bind("<Control-o>", shortcut_open)
    root.bind("<Control-Shift-S>", shortcut_saveas)
    root.geometry("463x360+0+0")
    root.minsize(width=463, height=360)
    initial_time_change()
    root.mainloop()
except Exception as e:
    with open('Error.txt','w') as f:
        f.write(str(e))


