from tkinter.constants import TRUE, X
import tkinter.filedialog
import pyautogui
import datetime
import tkinter
import time
import math
import os

root = tkinter.Tk()
root.title('lug_analysis')
bg = 'grey99'
root['bg'] = bg

font = ('ms sans', '10', 'bold')
font2 = ('ms sans', '10')
font3 = ('ms sans', '8')

dname = r'{}'.format(os.path.realpath(__file__).strip('lug_analysis.py'))
os.chdir(dname)  # working directory

g = tkinter.Canvas(width=450, height=500, bg=bg, highlightthickness=0)  # 1000x600
g.grid(row=1, column=2, rowspan=6)
g.update()

def back_to_default():
    global output_value, output_lab
    for i in range(len(lab2_row)):
        output_value[output_lab[i]].config(text=output_lab[i], fg='black', font='15')
    output_value['BEA'].config(text='BEA', fg='black', font=font)


def format_data(data):
    data = data.readlines()
    for i in range(len(data)):
        data[i] = data[i].strip()
        data[i] = float(data[i])
    return data


def generate_report(check):
    global report_num
    xpos1 = root.winfo_x()
    xpos2 = root.winfo_width()
    ypos1 = root.winfo_y() + 25
    ypos2 = root.winfo_height()
   
    im = pyautogui.screenshot(region=(xpos1, ypos1, xpos2, ypos2))
    if check == 0:
        file_path = tkinter.filedialog.asksaveasfilename(defaultextension='.png')
        im.save(file_path)
    else:
        print(report_num)
        im.save(os.path.join(dname, r'reports/{}/{}.png'.format(name, report_num)))


def multiple_reports():
    global d_entry, entry_id, name, report_num

    time_now = datetime.datetime.now()
    name = '{}-{}-{}-{}-{}-{}'.format(time_now.year, time_now.day, time_now.month, time_now.hour, time_now.minute, time_now.second)
    os.mkdir(os.path.join(dname, r'reports/{}'.format(name)))
   
    file = tkinter.filedialog.askopenfile(mode='r')
    while True:
        line = file.readline()
        if line == '':
            break

        line = line.split('\t')
        line = [d.strip().replace(',', '.') for d in line]

        for i in range(1, len(line)):
            d_entry[entry_id[i-1]].delete(0, 'end')
            d_entry[entry_id[i-1]].insert(0, line[i])
        report_num = line[0]
        g.update()
        create_scheme()
        calculate()
        generate_report(1)
        
    
def show_output(value, id):
    id.config(text=value)
    ipadx = 35
    id.grid(ipadx=ipadx)
    if value < 1:
        id.config(fg='red')
    else:
        id.config(fg='green')


def get_material_data(material, reversed):
    out = {}
    if not reversed: dir = 'normal'
    else: dir = 'reversed'
    
    data = open(os.path.join(dname, r'data/material_info/{}/{}'.format(dir, material))).readline()
    data = data.split(", ")

    for d in data:
        d = d.split(": ")
        d[0] = d[0].strip("'")
        d[1] = d[1].strip("'")
        out[d[0]] = float(d[1])
    print(out)
    return out

    

def calculate():
    global d_entry, material_info, curve_axial, dname, output_value
    global curve_trans, specific_Fbry, specific_LFtu, error_lab_calc
    global specific_LFty, specific_TFtu, specific_TFty, reversed, f

    error_lab_calc.config(text='', font=font)
    # basic inputs
    Fx = float(d_entry['fx_ent'].get())
    Fy = float(d_entry['fy_ent'].get())
    D = float(d_entry['d_ent'].get())
    t = float(d_entry['t_ent'].get())
    a = float(d_entry['a_ent'].get())
    W = float(d_entry['w_ent'].get())
    F = math.sqrt(Fx**2 + Fy**2)

    material = material_info.get()
    if material == 'other_material':  
        # material information provided by the used
        if not reversed:
            material = {'name': 'other_material', 'LFtu': float(specific_LFtu.get()), 'LTFtu': float(specific_TFtu.get(
            )), 'LFty': float(specific_LFty.get()), 'LTFty': float(specific_TFty.get()), 'Fbry': float(specific_Fbry.get())}
        else:
            material = {'name': 'other_material', 'LTFtu': float(specific_LFtu.get()), 'LFtu': float(specific_TFtu.get(
            )), 'LTFty': float(specific_LFty.get()), 'LFty': float(specific_TFty.get()), 'Fbry': float(specific_Fbry.get())}
    else:  
        # load hard-coded data
        material = get_material_data(material, reversed)

    f_load_type = f.get()
    print('f =', f_load_type)
    material['Fbry'] *= f_load_type

    if Fx == 0 and Fy == 0:
        error_lab_calc.config(text='At least one load has to have non-zero value', fg='red', font=font2)
        return
    
    if Fx == 0: Fx = 1
    if Fy == 0: Fy = 1

    # AXIAL LOAD -------------------------------------------------------------------------------------------------------
    # shear-bearing-failure
    
    # finding closest value
    curves = [4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30]
    file_name = min(curves, key=lambda x: abs(x-(D/t)))
 
    # getting data
    data = open(os.path.join(dname, r'data/shear_bearing_failure/function/{}'.format(file_name)))
    data = format_data(data)
    kbr = 0
    # make polynomial function
    for i in range(len(data)):
        kbr += data[i] * (a/D)**(len(data)-1-i)
    print('kbr =', kbr)

    if a/D < 0.6 or a/D > 4:
        back_to_default()
        error_lab_calc.config(text='Eq. 9.8.1 ratio of a/D must be in interval (0.6, 4)', fg='red', font=font2)
        return
    else:
        Pbru = kbr*D*t*material['LFtu']
        FS_Pbru = round(Pbru / Fx, 2)
        show_output(FS_Pbru, output_value['Pbru'])

    # tension failure
    file_name = curve_axial.get()
    data = open(os.path.join(dname, r'data/tension_failure/function/{}'.format(file_name)))
    data = format_data(data)

    kt = 0
    for i in range(len(data)):
        kt += data[i] * (W/D)**(len(data)-1-i)
    print('kt =', kt)

    if W/D < 1 or W/D > 5:
        back_to_default()
        error_lab_calc.config(
            text='Eq. 9.8.2 ration of W/D must be in interval [1, 5]', fg='red', font=font2)
        return
    else:
        At = (W - D) * t
        Ptu = kt*At*material['LFtu']
        FS_Ptu = round(Ptu / Fx, 2)
        show_output(FS_Ptu, output_value['Ptu'])
        print('At = ', At)

    # yield tension failure
    data = open(os.path.join(dname, r'data/yield_failure/function/yield'))
    data = format_data(data)

    C = 0
    Pu = min(Pbru, Ptu)
    x = Pu / (D*t*material['LFtu'])
    if x < 1: C = 1.1
    elif x > 3: C = 0.7
    else:
        for i in range(len(data)): C += data[i] * x **(len(data)-1-i)
    print('C =', C)

    if Pu / (D*t*material['LFtu']) < 0 or Pu / (D*t*material['LFtu']) > 3:
        back_to_default()
        error_lab_calc.config(
            text='Eq. 9.8.1 ration of Pu / D*t*Fx must be in interval [0, 3]', fg='red', font=font2)
        return
    else:
        Pya = C * (material['LFty']/material['LFtu']) * Pu
        FS_Pya = round(Pya / Fx, 2)
        show_output(FS_Pya, output_value['Py-axial'])
        

    # TRANSVERSE LOAD -------------------------------------------------------------------------------------------------
    # ultimate load
    Abr = D * t
    A1 = (W/2 - D/2 * math.sqrt(2)/2) * t
    A2 = (a - D/2) * t
    A3 = A2
    A4 = A1
    
    Aav = 6 / ((3/A1) + (1/A2) + (1/A3) + (1/A1))
    
    print('')
    print('A1 = ', A1)
    print('A2 =', A2)
    print('A3 =', A3)
    print('A4 =', A4, '\n')
    print('Aav =', Aav)
    print('Abr =', Abr)

    file_name = curve_trans.get()
    num = open(os.path.join(dname, r'data/transverse_ultimate_load/function/B{}'.format(file_name)))
    num = float(num.readline())
    if Aav / Abr > num:
        data = open(os.path.join(dname, r'data/transverse_ultimate_load/function/R{}'.format(file_name)))
    else:
        data = open(os.path.join(dname, r'data/transverse_ultimate_load/function/L{}'.format(file_name)))
    data = format_data(data)

    if 0 < Aav / Abr > 1.4:
        back_to_default()
        error_lab_calc.config(text='Eq. 9.8.12, ratio of Aav / Abr must be in interval 0 - 1.4', fg='red', font=font2)
    else:
        ktru = 0
        for i in range(len(data)):
            ktru += data[i] * (Aav / Abr)**(len(data)-1-i)
    print('ktru =', ktru)

    Ptru = ktru * Abr * material['LFtu']
    FS_Ptru = round(Ptru / Fy, 2)
    show_output(FS_Ptru, output_value['Ptru'])
        

    # yield load
    if 0 < Aav / Abr > 1.4:
        back_to_default()
        error_lab_calc.config(text='Eq. 9.8.12, ratio of Aav / Abr must be in interval 0 - 1.4', fg='red', font=font2)
    else:
        ktry_data = format_data(open(os.path.join(dname, r'data/transverse_ultimate_load/function/ktry')))
        ktry=0
        x = Aav / Abr
        for i in range(len(ktry_data)):
            ktry += ktry_data[i] * x **(len(ktry_data)-1-i)
        print('ktry =', ktry)
        print('---------------------------------------------------')

    Pyt = ktry * Abr * material['LTFty']
    FS_Pyt = round(Pyt / Fy, 2)
    show_output(FS_Pyt, output_value['Py-tranverse'])
    

    # OBLIQUE LOAD ----------------------------------------------------------------------------------------------------------
    # ultimate load
    Rau = (Fx/min(Pbru, Ptu))**1.6
    Rtru = (Fy/Ptru)**1.6
    ultimate_oblique_load = 1 / (Rau + Rtru)**0.625
    ultimate_oblique_load = round(ultimate_oblique_load, 2)
    show_output(ultimate_oblique_load, output_value['FS1'])
    
    # yield load
    Ray = (Fx/Pya)**1.6
    Rtry = (Fy/Pyt)**1.6
    oblique_yield_load = 1 / (Ray + Rtry)**0.625
    oblique_yield_load = round(oblique_yield_load, 2)
    show_output(oblique_yield_load, output_value['FS2'])
    
    # SUCINITEL BEZPECNOSTI--------------------------------------------------------------------------------------------------
    delta_bea = F / (D * t)
    gamma_bea = round(material['Fbry'] / delta_bea, 2)
    show_output(gamma_bea, output_value['BEA'])


def create_scheme(event=None):
    global d_entry

    W = float(d_entry['w_ent'].get())
    D = float(d_entry['d_ent'].get())
    a = float(d_entry['a_ent'].get())
    t = float(d_entry['t_ent'].get())
    error_check = 0

    cw = g.winfo_width()  # canvas width
    ch = g.winfo_height()  # canvas height
    sp = 25  # starting point
    l_lug = 310  # length of the lug
    W_lab_dis = 25  # distance of the W label
    thickness_dis = 40  # thickness diagram
    g.delete('all')
    t = 25

    # CONDITIONS
   
    ratio = 200 / W
    W *= ratio
    D *= ratio
    #t *= ratio
    a *= ratio

    if W > (ch - 100):  # if lug is too wide
        ratio = (ch - 100) / W
        W *= ratio
        D *= ratio
        #t *= ratio

    if D > W:  # if diameter is too big
        D = W
        error_lab_scheme.config(text='"D" is too big', fg='red', font=font2)
        error_check = 1

    if sp+l_lug-a+D/2 > sp+l_lug:  # if a is too small
        a = D/2
        error_lab_scheme.config(text='"a" is too small', fg='red', font=font2)
        error_check = 1

    if a > l_lug-D/2:  # if a is too big
        a = l_lug-D/2
        error_lab_scheme.config(text='"a" is too big', fg='red', font=font2)
        error_check = 1

    if error_check == 0: error_lab_scheme.config(text='')

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
    #g.create_line((sp+l_lug)-a, ch/2+W, (sp+l_lug)-a, ch/2-W, dash=(7,1,1,1))  # x
   

def show_table():
    new_window = tkinter.Tk()
    new_window.title('curves1')
    img = tkinter.PhotoImage(master=new_window, file=os.path.join(dname, r'images/tab1_2.png'))
    w = tkinter.Label(new_window, image=img)
    w.pack()
    new_window.mainloop()


def show_table2():

    new_window2 = tkinter.Tk()
    new_window2.title('curves2')
    img = tkinter.PhotoImage(master=new_window2, file=os.path.join(dname, r'images/tab2_small.png'))
    w = tkinter.Label(new_window2, image=img)
    w.pack()
    new_window2.mainloop()


def show_materials():
    new_window3 = tkinter.Tk()
    new_window3.title('materials')
    img = tkinter.PhotoImage(master=new_window3, file=os.path.join(dname, r'images/material.png'))
    w = tkinter.Label(new_window3, image=img)
    w.pack()
    new_window3.mainloop()

def show_load_types():
    new_window4 = tkinter.Tk()
    new_window4.title('load_types')
    img = tkinter.PhotoImage(master=new_window4, file=os.path.join(dname, r'images/druh_zatazenia2.png'))
    w = tkinter.Label(new_window4, image=img)
    w.pack()
    new_window4.mainloop()


inputs = tkinter.LabelFrame(root, text='inputs', relief='ridge', bg=bg)
inputs.grid(row=0, column=0, rowspan=2, sticky='n'+'e'+'w'+'s')

materials = tkinter.LabelFrame(root, text='materials', relief='ridge', bg=bg)
materials.grid(row=2, column=0, sticky='n'+'e'+'w'+'s', rowspan=2)

outputs = tkinter.LabelFrame(root, text='outputs', relief='ridge', bg=bg)
outputs.grid(row=0, column=1, rowspan=2, sticky='n'+'e'+'w'+'s')

buttons = tkinter.LabelFrame(root, text='buttons', relief='ridge', bg=bg)
buttons.grid(row=2, column=1, sticky='n'+'e'+'w'+'s')

other_material = tkinter.LabelFrame(root, text='specific material & grain direction', padx=20, relief='ridge', bg=bg)
other_material.grid(row=3, column=1, sticky='n'+'e'+'w'+'s')

# ----INPUTS-----------------------------------------------------------------
entry_id = ['fx_ent', 'fy_ent', 'd_ent', 't_ent', 'a_ent', 'w_ent']
d_entry = {}
lab_text = ['Fx[N]', 'Fy[N]', 'D[mm]', 't[mm]', 'a[mm]', 'W[mm]']
defaults = [50, 70, 0.5, 0.1, 0.75, 1.5]

for i in range(len(entry_id)):
    tkinter.Label(inputs, text=lab_text[i], fg='blue', font=font, bg=bg).grid(
        row=2*i, column=0)
    d_entry[entry_id[i]] = tkinter.Entry(
        inputs, width=15, justify='center', font=font2)
    d_entry[entry_id[i]].grid(row=2*i+1, column=0, pady=3, padx=30)
    d_entry[entry_id[i]].insert(0, defaults[i])


# ---MATERIALS------------------------------------------------------
material_info = tkinter.StringVar()
curve_axial = tkinter.IntVar()
curve_trans = tkinter.IntVar()
material_info.set('2024')
curve_axial.set(1)
curve_trans.set(1)

f = tkinter.DoubleVar()
f.set(1)
f_values = [1, 0.8, 0.6, 0.4]

material_value = ['2024', '7075', '15 230.6', 'other_material']
material_txt = ['2024', '7075', '15 230.6', 'specific_material']

for i in range(len(material_value)):
    tkinter.Radiobutton(materials, text=material_txt[i], variable=material_info, bg=bg, font=font3, highlightthickness=0,
                        value=material_value[i]).grid(row=i, column=0, columnspan=2, ipadx=40)

for i in range(8):
    tkinter.Radiobutton(materials, text="Curve 1.{}".format(i+1), bg=bg, font=font3, highlightthickness=0,
                        variable=curve_axial, value=i+1).grid(row=i+4, column=0)

for i in range(8):
    tkinter.Radiobutton(materials, text="Curve 2.{}".format(i+1), bg=bg,  font=font3, highlightthickness=0,
                        variable=curve_trans, value=i+1).grid(row=i+4, column=1)

tkinter.Label(materials, text='load type[f]', bg=bg,font=font3).grid(row=13, column=0, columnspan=2)
for i in range(4):
    tkinter.Radiobutton(materials, text="{}".format(f_values[i]), bg=bg, font=font3, highlightthickness=0,
                        variable=f, value=f_values[i]).grid(row=i//2+14, column=i%2)


# ---OUTPUTS---------------------------------------------------------------------
lab_row = [0, 4, 7, 11]
lab2_row = [1, 2, 3, 5, 6, 8, 10]
failure_lab = ['Shear bearing failure', 'Tension failure', 'Yield failure',
               'Ultimate load', 'Yield failure', 'Ultimate load', 'Yield failure']
load_lab = ['Reserve factors - Axial load', 'Reserve factors - Transverse load', 
            'Reserve factors - Oblique load', 'Reserve factor - Bearing stress']
output_lab = ['Pbru', 'Ptu', 'Py-axial',
              'Ptru', 'Py-tranverse', 'FS1', 'FS2']
output_value = {}
ipadx = 12

for i in range(len(lab_row)):
    tkinter.Label(outputs, text=load_lab[i], fg='blue', bg=bg, 
                  font=font).grid(row=lab_row[i], column=0, columnspan=2, ipadx=ipadx)

for i in range(len(lab2_row)):
    tkinter.Label(outputs, text=failure_lab[i], fg='black', bg=bg,
                  font=font2).grid(row=lab2_row[i], column=0, ipady=2, sticky='w'+'e', ipadx=ipadx)

for i in range(len(lab2_row)):
    output_value[output_lab[i]] = tkinter.Label(outputs, text=output_lab[i], bg=bg,  font=font2,
                                                fg='black')
    output_value[output_lab[i]].grid(row=lab2_row[i], column=1, ipady=2, ipadx=ipadx, sticky='e'+'w')

output_value['BEA'] = tkinter.Label(outputs, text='BEA', bg=bg, font=font2, fg='black')
output_value['BEA'].grid(row=12, column=0, columnspan=2)

# ---BUTTONS----------------------------------------------------------------------
ipady = 2
ipadx = 14
ipadx2 = 36
b1 = tkinter.Button(buttons, text='Curves 1', command=lambda: show_table(), font=font2, bg=bg)
b1.grid(row=0, column=0, sticky='w'+'e', ipadx=ipadx, ipady=ipady)

b2 = tkinter.Button(buttons, text='Curves 2', command=lambda: show_table2(), font=font2, bg=bg)
b2.grid(row=0, column=1, sticky='w'+'e', ipadx=ipadx2, ipady=ipady)

b3 = tkinter.Button(buttons, text='Show materials', command=lambda: show_materials(), font=font2, bg=bg)
b3.grid(row=1, column=0, sticky='e'+'w', ipadx=ipadx, ipady=ipady)

b8 = tkinter.Button(buttons, text='Load Types', command=lambda: show_load_types(), font=font2, bg=bg)
b8.grid(row=1, column=1, sticky='e'+'w', ipadx=ipadx, ipady=ipady)

b5 = tkinter.Button(buttons, text='Multiple reports', command=multiple_reports, font=font2, bg=bg)
b5.grid(row=2, column=0, sticky='e'+'w', ipadx=ipadx, ipady=ipady)

b6 = tkinter.Button(buttons, text='Generate report', command=lambda: generate_report(0), font=font2, bg=bg)
b6.grid(row=2, column=1, sticky='e'+'w', ipadx=ipadx, ipady=ipady)

b4 = tkinter.Button(buttons, text='Redraw', command=create_scheme, font=font2, bg=bg)
b4.grid(row=3, column=1, sticky='e'+'w', ipadx=ipadx2, ipady=ipady)

b7 = tkinter.Button(buttons, text='Calculate', command=calculate, font=font2, bg=bg)
b7.grid(row=3, column=0, sticky='e'+'w', ipadx=ipadx, ipady=ipady)



# ---SPECIFIC MATERIAL------------------------------------------------------------------
tkinter.Label(other_material, text='Ftu[MPa]', bg=bg, font=font3).grid(row=1, column=1, ipady=ipady)
tkinter.Label(other_material, text='Fty[MPa]', bg=bg, font=font3).grid(row=1, column=2, ipady=ipady)
tkinter.Label(other_material, text='Fbry[MPa]', bg=bg, font=font3).grid(row=1, column=3, ipady=ipady)
tkinter.Label(other_material, text='L', bg=bg, font=font3).grid(row=2, column=0)
tkinter.Label(other_material, text='LT', bg=bg, font=font3).grid(row=3, column=0)

reversed = tkinter.BooleanVar()
reversed.set(False)
tkinter.Label(other_material, text='Grain orientation', bg=bg, font=font3).grid(row=1, column=4, columnspan=2)

tkinter.Radiobutton(other_material, text='X', bg=bg, font=font3, highlightthickness=0,
    variable=reversed, value=False).grid(row=2, column=4)
tkinter.Radiobutton(other_material, text='Y', bg=bg, font=font3, highlightthickness=0,
    variable=reversed, value=True).grid(row=2, column=5)
tkinter.Radiobutton(other_material, text='X', bg=bg, font=font3, highlightthickness=0,
    variable=reversed, value=True).grid(row=3, column=4)
tkinter.Radiobutton(other_material, text='Y', bg=bg, font=font3, highlightthickness=0,
    variable=reversed, value=False).grid(row=3, column=5)


ipady = 3
width = 7
specific_LFtu = tkinter.Entry(other_material, justify='center', font=font3, width=width)
specific_LFtu.grid(row=2, column=1, ipady=ipady)

specific_LFty = tkinter.Entry(
    other_material, justify='center', font=font3, width=width)
specific_LFty.grid(row=2, column=2, ipady=ipady)

specific_TFtu = tkinter.Entry(
    other_material, justify='center', font=font3, width=width)
specific_TFtu.grid(row=3, column=1, ipady=ipady)

specific_TFty = tkinter.Entry(
    other_material, justify='center', font=font3, width=width)
specific_TFty.grid(row=3, column=2, ipady=ipady)

specific_Fbry = tkinter.Entry(
    other_material, justify='center', font=font3, width=width)
specific_Fbry.grid(row=2, column=3, rowspan=2, ipady=4*ipady)


#--------------------------------------------------------------------------------------

# entry box to type name of the case which is tested
tkinter.Entry(width=15, justify='center', font=font2, border=0).grid(row=0, column=2, stick='E'+'W'+'N', padx=25, pady=(10, 0))

# error label for calculations
error_lab_calc = tkinter.Label(text='', bg='red')
error_lab_calc.grid(row=0, column=2, sticky='N', pady=(40, 0))

# error label for drawing the scheme
error_lab_scheme = tkinter.Label(text='', bg='black')
error_lab_scheme.grid(row=0, column=2, sticky='N', pady=(70, 0))

d_entry['d_ent'].bind('<Return>', create_scheme)
d_entry['t_ent'].bind('<Return>', create_scheme)
d_entry['a_ent'].bind('<Return>', create_scheme)
d_entry['w_ent'].bind('<Return>', create_scheme)

create_scheme()
g.mainloop()
