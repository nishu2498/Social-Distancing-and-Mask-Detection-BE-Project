w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# root.geometry("%dx%d+0+0" % (w, h))
# root.title("Covid Mask And Social Distancing System")

# # 43

# # ++++++++++++++++++++++++++++++++++++++++++++
# #####For background Image
# image2 = Image.open('covid.png')
# image2 = image2.resize((1530, 900), Image.ANTIALIAS)

# background_image = ImageTk.PhotoImage(image2)

# background_label = tk.Label(root, image=background_image)

# background_label.image = background_image

# background_label.place(x=0, y=0)  # , relwidth=1, relheight=1)
# #
# label_l1 = tk.Label(root, text="Covid Mask And Social Distancing System",font=("Times New Roman", 35, 'bold'),
#                     background="#152238", fg="white", width=50, height=2)
# label_l1.place(x=60, y=0)

# #T1.tag_configure("center", justify='center')
# #T1.tag_add("center", 1.0, "end")

# ################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# #def clear_img():
# #    img11 = tk.Label(root, background='bisque2')
# #    img11.place(x=0, y=0)


# #################################################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# ################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# # def cap_video():
    
# #     video1.upload()
# #     #from subprocess import call
# #     #call(['python','video_second.py'])

# def reg():
#     from subprocess import call
#     call(["python","socialdistance.py"])

# def log():
#     from subprocess import call
#     call(["python","detect_mask_video.py"])
    
# def window():
#   root.destroy()


# button1 = tk.Button(root, text="Covid Mask Detection", command=log, height=1,font=('times', 20, ' bold '), bg="#152238", fg="white")
# button1.place(x=100, y=160)

# button2 = tk.Button(root, text="Social Distancing",command=reg,width=14, height=1,font=('times', 20, ' bold '), bg="#152238", fg="white")
# button2.place(x=100, y=240)

# button3 = tk.Button(root, text="Exit",command=window,width=14, height=1,font=('times', 20, ' bold '), bg="#152238", fg="white")
# button3.place(x=100, y=330)

# root.mainloop()