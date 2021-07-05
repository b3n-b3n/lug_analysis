# libraries
from tkinter.constants import CENTER
import tkinter.filedialog
import tkinter
import os

# files attached
import display_img
import scheme
import report
import calc

# general appearance settings
root = tkinter.Tk()
root.title('lug_analysis')
bg = 'grey99'
root['bg'] = bg
font = [('ms sans', '10', 'bold'), ('ms sans', '10'), ('ms sans', '8')]
bd_style = 'solid'  # border style

# main path / working directory
dname = r'{}'.format(os.path.realpath(__file__).strip('main.py'))
os.chdir(dname)  # working directory

# canvas
g = tkinter.Canvas(width=450, height=500, bg=bg, highlightthickness=0)
g.grid(row=1, column=2, rowspan=2)
g.update()

# entry box to type name of the case which is tested
report_title = tkinter.Entry(width=25, justify='center', font=font[0], border=1, relief=bd_style)
report_title.grid(row=0, column=2, stick='E'+'W'+'N', padx=25, pady=(10, 0), ipady=4)

# error label for calculations
error_lab_calc = tkinter.Label(text='', bg=bg)
error_lab_calc.grid(row=0, column=2, sticky='N', pady=(50, 0))

# error label for the scheme
err_lab_scheme = tkinter.Label(text='', bg=bg)
err_lab_scheme.grid(row=0, column=2, sticky='N', pady=(80, 0))


# ----LABELFRAMES---------------------------------------------------------
inputs = tkinter.LabelFrame(root, text='inputs', relief='ridge', bg=bg)
inputs.grid(row=0, column=0, rowspan=2, sticky='n'+'e'+'w'+'s')

materials = tkinter.LabelFrame(root, text='materials', relief='ridge', bg=bg)
materials.grid(row=2, column=0, sticky='n'+'e'+'w'+'s', rowspan=2)

outputs = tkinter.LabelFrame(root, text='outputs', relief='ridge', bg=bg)
outputs.grid(row=0, column=1, rowspan=2, sticky='n'+'e'+'w'+'s')

buttons = tkinter.LabelFrame(root, text='buttons', relief='ridge', bg=bg)
buttons.grid(row=2, column=1, sticky='n'+'e'+'w'+'s')

other_material = tkinter.LabelFrame(
    root, text='specific material & grain direction', padx=20, relief='ridge', bg=bg)
other_material.grid(row=3, column=1, sticky='n'+'e'+'w'+'s')

# ----INPUTS-----------------------------------------------------------------
entry_id = ['fx_ent', 'fy_ent', 'd_ent', 't_ent', 'a_ent', 'w_ent']
d_entry = {}
lab_text = ['Fx[N]', 'Fy[N]', 'D[mm]', 't[mm]', 'a[mm]', 'W[mm]']
default_entry_values = [50, 70, 0.5, 0.1, 0.75, 1.5]

for i in range(len(entry_id)):
    tkinter.Label(inputs, text=lab_text[i], fg='blue', font=font[0], bg=bg).grid(
        row=2*i, column=0)
    d_entry[entry_id[i]] = tkinter.Entry(
        inputs, width=15, justify='center', font=font[1], relief=bd_style)
    d_entry[entry_id[i]].grid(row=2*i+1, column=0, pady=3, padx=30)
    d_entry[entry_id[i]].config(highlightbackground=bg, highlightthickness=1)
    # d_entry[entry_id[i]].insert(0, defaults[i])


# ---MATERIALS------------------------------------------------------
material_info = tkinter.StringVar()
curve_axial = tkinter.IntVar()
curve_trans = tkinter.IntVar()
material_info.set('2024')
curve_axial.set(1)
curve_trans.set(1)

f = tkinter.DoubleVar()
f.set(1)
f_values = [1, 0.8, 0.7, 0.6]

material_value = ['2024', '7075', '15 230.6', 'other_material']
material_txt = ['2024', '7075', '15 230.6', 'specific_material']

for i in range(len(material_value)):
    tkinter.Radiobutton(materials, text=material_txt[i], variable=material_info, bg=bg, font=font[2], highlightthickness=0,
                        value=material_value[i]).grid(row=i, column=0, columnspan=2, ipadx=40)

for i in range(8):
    tkinter.Radiobutton(materials, text="Curve 1.{}".format(i+1), bg=bg, font=font[2], highlightthickness=0,
                        variable=curve_axial, value=i+1).grid(row=i+4, column=0)

for i in range(11):
    tkinter.Radiobutton(materials, text="Curve 2.{}".format(i+1), bg=bg,  font=font[2], highlightthickness=0,
                        variable=curve_trans, value=i+1).grid(row=i+4, column=1)

tkinter.Label(materials, text='load type[f]', bg=bg, font=font[2]).grid(
    row=16, column=0, columnspan=2)
for i in range(4):
    tkinter.Radiobutton(materials, text="{}".format(f_values[i]), bg=bg, font=font[2], highlightthickness=0,
                        variable=f, value=f_values[i]).grid(row=i//2+17, column=i % 2)


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
    tkinter.Label(outputs, text=load_lab[i], fg='blue', bg=bg, justify='center',
                  font=font[0]).grid(row=lab_row[i], column=0, columnspan=2, sticky='e'+'w', ipadx=40)

for i in range(len(lab2_row)):
    tkinter.Label(outputs, text=failure_lab[i], fg='black', bg=bg,
                  font=font[1]).grid(row=lab2_row[i], column=0, ipady=2, sticky='w', ipadx=ipadx)

for i in range(len(lab2_row)):
    output_value[output_lab[i]] = tkinter.Label(outputs, text=output_lab[i], bg=bg,  font=font[1],
                                                fg='black')
    output_value[output_lab[i]].grid(
        row=lab2_row[i], column=1, ipady=2, ipadx=ipadx, sticky='e')

output_value['BEA'] = tkinter.Label(
    outputs, text='BEA', bg=bg, font=font[1], fg='black')
output_value['BEA'].grid(row=12, column=0, columnspan=2, ipadx=40)


# ---SPECIFIC MATERIAL------------------------------------------------------------------
ipady = 2
tkinter.Label(other_material, text='Ftu[MPa]', bg=bg, font=font[2]).grid(
    row=1, column=1, ipady=ipady)
tkinter.Label(other_material, text='Fty[MPa]', bg=bg, font=font[2]).grid(
    row=1, column=2, ipady=ipady)
tkinter.Label(other_material, text='Fbry[MPa]', bg=bg, font=font[2]).grid(
    row=1, column=3, ipady=ipady)
tkinter.Label(other_material, text='L', bg=bg,
              font=font[2]).grid(row=2, column=0)
tkinter.Label(other_material, text='LT', bg=bg,
              font=font[2]).grid(row=3, column=0)

reverse = tkinter.BooleanVar()
reverse.set(False)
tkinter.Label(other_material, text='Grain orientation', bg=bg,
              font=font[2]).grid(row=1, column=4, columnspan=2)

tkinter.Radiobutton(other_material, text='X', bg=bg, font=font[2], highlightthickness=0,
                    variable=reverse, value=False).grid(row=2, column=4)
tkinter.Radiobutton(other_material, text='Y', bg=bg, font=font[2], highlightthickness=0,
                    variable=reverse, value=True).grid(row=2, column=5)
tkinter.Radiobutton(other_material, text='X', bg=bg, font=font[2], highlightthickness=0,
                    variable=reverse, value=True).grid(row=3, column=4)
tkinter.Radiobutton(other_material, text='Y', bg=bg, font=font[2], highlightthickness=0,
                    variable=reverse, value=False).grid(row=3, column=5)


ipady = 3
width = 7
specific_LFtu = tkinter.Entry(
    other_material, justify='center', font=font[2], width=width, relief=bd_style)
specific_LFtu.grid(row=2, column=1, ipady=ipady, pady=(0, 5))

specific_LFty = tkinter.Entry(
    other_material, justify='center', font=font[2], width=width, relief=bd_style)
specific_LFty.grid(row=2, column=2, ipady=ipady, pady=(0, 5))

specific_TFtu = tkinter.Entry(
    other_material, justify='center', font=font[2], width=width, relief=bd_style)
specific_TFtu.grid(row=3, column=1, ipady=ipady)

specific_TFty = tkinter.Entry(
    other_material, justify='center', font=font[2], width=width, relief=bd_style)
specific_TFty.grid(row=3, column=2, ipady=ipady)

specific_Fbry = tkinter.Entry(
    other_material, justify='center', font=font[2], width=width, relief=bd_style)
specific_Fbry.grid(row=2, column=3, rowspan=2, ipady=6*ipady)

# ---BUTTONS----------------------------------------------------------------------
ipady = 19
ipadx = 25
ipadx2 = 36
padx = 5
pady = 5
bd_style2 = 'groove'
calc_args = (d_entry, material_info, curve_axial, dname, output_value,
    curve_trans, specific_Fbry, specific_LFtu, error_lab_calc, output_lab, lab2_row,
    specific_LFty, specific_TFtu, specific_TFty, reverse, f, font)

b1 = tkinter.Button(buttons, text='Curves 1',
                    command=lambda: display_img.show_table(dname), font=font[1], bg=bg, relief=bd_style2)
b1.grid(row=0, column=0, sticky='w'+'e', ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)

b2 = tkinter.Button(buttons, text='Curves 2',
                    command=lambda: display_img.show_table2(dname), font=font[1], bg=bg, relief=bd_style2)
b2.grid(row=0, column=1, sticky='w'+'e', ipadx=ipadx2, ipady=ipady, padx=padx, pady=pady)

b3 = tkinter.Button(buttons, text='Show materials',
                    command=lambda: display_img.show_materials(dname), font=font[1], bg=bg, relief=bd_style2)
b3.grid(row=1, column=0, sticky='e'+'w', ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)

b4 = tkinter.Button(buttons, text='Redraw', command=lambda:
                    scheme.create(None, d_entry, g, font, bg, err_lab_scheme, False, []), font=font[1], bg=bg, relief=bd_style2)
b4.grid(row=3, column=1, sticky='e'+'w', ipadx=ipadx2, ipady=ipady, padx=padx, pady=pady)

b5 = tkinter.Button(buttons, text='Multiple reports', relief=bd_style2,
                    command=lambda: report.multiple_reports(dname, entry_id, d_entry, g, font, bg, err_lab_scheme, root, calc_args, report_title), font=font[1], bg=bg)
b5.grid(row=2, column=0, sticky='e'+'w', ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)

b6 = tkinter.Button(buttons, text='Generate report',
                    command=lambda: report.generate_report(True, root, None, None), font=font[1], bg=bg, relief=bd_style2)
b6.grid(row=2, column=1, sticky='e'+'w', ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)

b7 = tkinter.Button(buttons, text='Calculate', relief=bd_style2,
    command=lambda: calc.calculate(*calc_args), font=font[1], bg=bg)
b7.grid(row=3, column=0, sticky='e'+'w', ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)

b8 = tkinter.Button(buttons, text='Load Types', relief=bd_style2,
                    command=lambda: display_img.show_load_types(dname), font=font[1], bg=bg)
b8.grid(row=1, column=1, sticky='e'+'w', ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)


# --------------------------------------------------------------------------------------

d_entry['d_ent'].bind('<Return>', lambda x: scheme.create(
    x, d_entry, g, font, bg, err_lab_scheme, False, []))
d_entry['t_ent'].bind('<Return>', lambda x: scheme.create(
    x, d_entry, g, font, bg, err_lab_scheme, False, []))
d_entry['a_ent'].bind('<Return>', lambda x: scheme.create(
    x, d_entry, g, font, bg, err_lab_scheme, False, []))
d_entry['w_ent'].bind('<Return>', lambda x: scheme.create(
    x, d_entry, g, font, bg, err_lab_scheme, False, []))

scheme.create(None, d_entry, g, font, bg, err_lab_scheme, True, default_entry_values)
g.mainloop()
