import tkinter


def check_input(entry, name, font, err_lab_scheme, error_check):
    if error_check: return (0, True)

    try:
        out = float(entry[name].get())
        return (out, False)
    except:
        err_lab_scheme.config(text='{} must be a number'.format(name[0]), fg='red', font=font[1])
        return (0, True)


def create(event, d_entry, g, font, bg, err_lab_scheme, initial, defaults):

    error_check = False
    
    if initial:
        # initialize the scheme of a lug with some fake dimensions
        # to give is some form of reasonable shape
        D = defaults[2]
        t = defaults[3]
        a = defaults[4]
        W = defaults[5]
    else:
        W, error_check = check_input(d_entry, 'w_ent', font[1], err_lab_scheme, error_check)
        D, error_check = check_input(d_entry, 'd_ent', font[1], err_lab_scheme, error_check)
        a, error_check = check_input(d_entry, 'a_ent', font[1], err_lab_scheme, error_check)
        t, error_check = check_input(d_entry, 't_ent', font[1], err_lab_scheme, error_check)


    if not error_check:
        g.delete('all')
        cw = g.winfo_width()  # canvas width
        ch = g.winfo_height()  # canvas height
        sp = 25  # starting point
        l_lug = 310  # length of the lug
        W_lab_dis = 25  # distance of the W label
        thickness_dis = 40  # thickness diagram
        t = 25

        # CONDITIONS
    
        ratio = 200 / W
        W *= ratio
        D *= ratio
        # t *= ratio
        a *= ratio

        if W > (ch - 100):  # if lug is too wide
            ratio = (ch - 100) / W
            W *= ratio
            D *= ratio
            # t *= ratio

        if D > W:  # if diameter is too big
            D = W
            err_lab_scheme.config(text='"D" is too big', fg='red', font=font[1])
            error_check = True

        if sp+l_lug-a+D/2 > sp+l_lug:  # if a is too small
            a = D/2
            err_lab_scheme.config(text='"a" is too small', fg='red', font=font[1])
            error_check = True

        if a > l_lug-D/2:  # if a is too big
            a = l_lug-D/2
            err_lab_scheme.config(text='"a" is too big', fg='red', font=font[1])
            error_check = True

        if not error_check: err_lab_scheme.config(text='')

        # if (sp+l_lug+thickness_dis+t+W_lab_dis) > cw-25:  # if thickness is too big
        #     x = (sp+l_lug+thickness_dis+t+W_lab_dis) - (cw-25)
        #     ratio = (l_lug-x) / l_lug
        #     W *= ratio
        #     D *= ratio
        #     a *= ratio
        #     l_lug *= ratio
        #     if t > cw/2:  # stop expansion of t
        #         ratio = (cw/2) / t
        #         t *= ratio
        #         x = (cw-25) - (sp+l_lug+thickness_dis+t+W_lab_dis)
        #         thickness_dis += x
        #         if l_lug <= 1:  # if t is way too big
        #             x = (50+thickness_dis+t+W_lab_dis) - cw
        #             thickness_dis -= x
        #             l_lug = 0
        #             D = 0
        #             W = 0
        #             a = 0

        # BODY OF LUG
        width = 3
        g.create_oval((sp+l_lug)-W, ch/2-W/2, (sp+l_lug), ch/2+W/2, width=width)
        g.create_rectangle((sp+l_lug)-W, ch/2-W/2, (sp+l_lug) -W/2, ch/2+W/2+1, fill=bg, outline=bg, width=width)
        
        # hatch
        shift = 5
        for i in range(2):
            shiftx1 = 0 
            shifty1 = 0 
            while True:
                if shiftx1 >= t and shifty1 >= W/1.4:
                    break
                if i == 1:
                    g.create_line(sp+l_lug+thickness_dis, ch/2+shifty1+D/2, sp+l_lug+thickness_dis+shiftx1, ch/2+D/2)
                else:
                    g.create_line(sp+l_lug+thickness_dis, ch/2-W/2+shifty1, sp+l_lug+thickness_dis+shiftx1, ch/2-W/2)
                shiftx1 += shift 
                shifty1 += shift 
            if i == 0:
                g.create_rectangle((sp+l_lug)+thickness_dis, ch/2-D/2, (sp+l_lug)+thickness_dis+t, ch/2+500, fill=bg, outline=bg)

        # cover of overlaying hatch
        g.create_rectangle((sp+l_lug)+thickness_dis+t, ch/2-W/2, (sp+l_lug)+thickness_dis*4+t, ch/2+W, fill=bg, outline=bg)
        g.create_rectangle((sp+l_lug)+thickness_dis, ch/2+W/2, (sp+l_lug)+thickness_dis+t, ch/2+W/2+t*8, fill=bg, outline=bg)

        g.create_line(sp, ch/2-W/2, (sp+l_lug)-W/2, ch/2-W/2, width=width)
        g.create_line(sp, ch/2+W/2, (sp+l_lug)-W/2, ch/2+W/2, width=width)
        g.create_line(sp, ch/2-W/2, sp, ch/2+W/2, width=width)

        g.create_oval((sp+l_lug)-a-D/2, ch/2-D/2, (sp+l_lug)-a+D/2,
                    ch/2+D/2, fill='', width='3')  # hole
        g.create_rectangle((sp+l_lug)+thickness_dis, ch/2-W/2, (sp+l_lug)+thickness_dis+t, ch/2+W/2)  # thickness
        # if D <= W:  # srafovanie
        #     g.create_rectangle((sp+l_lug)+thickness_dis, ch/2-W/2,(sp+l_lug)+thickness_dis+t, ch/2-W/2+(W-D)/2)
        #     g.create_rectangle((sp+l_lug)+thickness_dis, ch/2+W/2,
        #                        (sp+l_lug)+thickness_dis+t, ch/2+W/2-(W-D)/2)

        # LABELS
        offset = 25
        offset2 = 10
        arrowshape = (10, 15, 3)
        # Fx
        g.create_line((sp+l_lug)-a, ch/2, sp+l_lug, ch/2, arrow=tkinter.LAST, arrowshape=arrowshape, fill='blue', width=3)
        g.create_text((sp+l_lug)-(a/2), ch/2 + offset, text='Fx', fill='blue', font=('ms sans', '11', 'bold'))
        # Fy
        g.create_line((sp+l_lug)-a, ch/2, (sp+l_lug) - a, ch/2 - W/2, arrow=tkinter.LAST, arrowshape=arrowshape, fill='blue', width=3)
        g.create_text((sp+l_lug) - a + offset, ch/2 - W/4, text='Fy', fill='blue', font=('ms sans', '11', 'bold'))
        # D
        g.create_line((sp+l_lug)-a-D/2, ch/2, (sp+l_lug) - a-D/2, ch/2-W/2-offset)
        g.create_line((sp+l_lug)-a+D/2, ch/2, (sp+l_lug) - a+D/2, ch/2-W/2-offset)
        g.create_line((sp+l_lug)-a-D/2, ch/2-W/2-25, (sp+l_lug) - a+D/2, ch/2-W/2-offset, arrow=tkinter.BOTH, arrowshape=arrowshape,)
        g.create_text((sp+l_lug)-a, ch/2-W/2-offset-offset2, text='D')
        # a
        g.create_line((sp+l_lug)-a, ch/2, (sp+l_lug)-a, ch/2+W/2+offset)
        g.create_line((sp+l_lug), ch/2, (sp+l_lug), ch/2+W/2+offset)
        g.create_line((sp+l_lug)-a, ch/2+W/2+offset, (sp+l_lug), ch/2+W/2+offset, arrow=tkinter.BOTH, arrowshape=arrowshape,)
        g.create_text((sp+l_lug)-a/2, ch/2+W/2+offset-offset2, text='a')
        # W
        g.create_line(sp+l_lug+thickness_dis+t+W_lab_dis, ch/2+20, sp + l_lug+thickness_dis+t+W_lab_dis, ch/2+W/2, arrow=tkinter.LAST, arrowshape=arrowshape)
        g.create_line(sp+l_lug+thickness_dis+t+W_lab_dis, ch/2-20, sp + l_lug+thickness_dis+t+W_lab_dis, ch/2-W/2, arrow=tkinter.LAST, arrowshape=arrowshape)
        g.create_text(sp+l_lug+thickness_dis+t+W_lab_dis, ch/2, text='W')
        # t
        g.create_line((sp+l_lug)+thickness_dis, ch/2-W/2, (sp+l_lug)+thickness_dis, ch/2-W/2-offset-offset2)
        g.create_line((sp+l_lug)+thickness_dis+t, ch/2-W/2, (sp+l_lug)+thickness_dis+t, ch/2-W/2-offset-offset2)
        g.create_line((sp+l_lug)+thickness_dis/4, ch/2-W/2-offset-offset2, (sp+l_lug)+thickness_dis, ch/2-W/2-offset-offset2, arrow=tkinter.LAST, arrowshape=arrowshape)
        g.create_line((sp+l_lug)+thickness_dis+t, ch/2-W/2-offset-offset2, (sp+l_lug)+thickness_dis*1.75+t, ch/2-W/2-offset-offset2, arrow=tkinter.FIRST, arrowshape=arrowshape)
        g.create_text(sp+l_lug+thickness_dis+t/2, ch/2-W/2-offset-offset2, text='t')
        # axis
        g.create_line(sp, ch/2, (sp+l_lug + thickness_dis + t), ch/2, dash=(7,1,1,1))  # y
        g.create_line((sp+l_lug)-a, ch/2+W, (sp+l_lug)-a, ch/2-W, dash=(7,1,1,1))  # x
    