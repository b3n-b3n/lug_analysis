import math
import os

def get_material_data(material, reverse, dname):
    out = {}
    if not reverse:
        dir = 'normal'
    else:
        dir = 'reversed'

    data = open(os.path.join(
        dname, r'data/material_info/{}/{}'.format(dir, material))).readline()
    data = data.split(", ")

    for d in data:
        d = d.split(": ")
        d[0] = d[0].strip("'")
        d[1] = d[1].strip("'")
        out[d[0]] = float(d[1])
    print(out)
    return out


def show_output(value, id):
    id.config(text=value)
    ipadx = 35
    id.grid(ipadx=ipadx)
    if value < 1:
        id.config(fg='red')
    else:
        id.config(fg='green')


def back_to_default(lab2_row, output_lab, output_value, font):
    for i in range(len(lab2_row)):
        output_value[output_lab[i]].config(
            text=output_lab[i], fg='black', font='15')
    output_value['BEA'].config(text='BEA', fg='black', font=font[0])


def format_data(data):
    data = data.readlines()
    for i in range(len(data)):
        data[i] = data[i].strip()
        data[i] = float(data[i])
    return data



def calculate(d_entry, material_info, curve_axial, dname, output_value,
    curve_trans, specific_Fbry, specific_LFtu, error_lab_calc, output_lab, lab2_row,
    specific_LFty, specific_TFtu, specific_TFty, reverse, f, font):
    
    # global d_entry, material_info, curve_axial, dname, output_value
    # global curve_trans, specific_Fbry, specific_LFtu, error_lab_calc
    # global specific_LFty, specific_TFtu, specific_TFty, reversed, f

    error_lab_calc.config(text='')
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
        if not reverse:
            material = {'name': 'other_material', 'LFtu': float(specific_LFtu.get()), 'LTFtu': float(specific_TFtu.get(
            )), 'LFty': float(specific_LFty.get()), 'LTFty': float(specific_TFty.get()), 'Fbry': float(specific_Fbry.get())}
        else:
            material = {'name': 'other_material', 'LTFtu': float(specific_LFtu.get()), 'LFtu': float(specific_TFtu.get(
            )), 'LTFty': float(specific_LFty.get()), 'LFty': float(specific_TFty.get()), 'Fbry': float(specific_Fbry.get())}
    else:
        # load hard-coded data
        material = get_material_data(material, reverse, dname)


    f_load_type = f.get()
    print('f =', f_load_type)
    material['Fbry'] *= f_load_type

    if Fx == 0 and Fy == 0:
        error_lab_calc.config(
            text='At least one load has to have non-zero value', fg='red', font=font[1])
        return

    if Fx == 0:
        Fx = 1
    if Fy == 0:
        Fy = 1

    # AXIAL LOAD -------------------------------------------------------------------------------------------------------
    # shear-bearing-failure

    # finding closest value
    curves = [4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30]
    file_name = min(curves, key=lambda x: abs(x-(D/t)))

    # getting data
    data = open(os.path.join(
        dname, r'data/shear_bearing_failure/function/{}'.format(file_name)))
    data = format_data(data)
    kbr = 0
    # make polynomial function
    for i in range(len(data)):
        kbr += data[i] * (a/D)**(len(data)-1-i)
    print('kbr =', kbr)

    if a/D < 0.6 or a/D > 4:
        back_to_default(lab2_row, output_lab, output_value, font)
        error_lab_calc.config(
            text='Eq. 9.8.1 ratio of a/D must be in interval (0.6, 4)', fg='red', font=font[1])
        return
    else:
        Pbru = kbr*D*t*material['LFtu']
        FS_Pbru = round(Pbru / Fx, 2)
        show_output(FS_Pbru, output_value['Pbru'])

    # tension failure
    file_name = curve_axial.get()
    data = open(os.path.join(
        dname, r'data/tension_failure/function/{}'.format(file_name)))
    data = format_data(data)

    kt = 0
    for i in range(len(data)):
        kt += data[i] * (W/D)**(len(data)-1-i)
    print('kt =', kt)

    if W/D < 1 or W/D > 5:
        back_to_default(lab2_row, output_lab, output_value, font)
        error_lab_calc.config(
            text='Eq. 9.8.2 ration of W/D must be in interval [1, 5]', fg='red', font=font[1])
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
    if x < 1:
        C = 1.1
    elif x > 3:
        C = 0.7
    else:
        for i in range(len(data)):
            C += data[i] * x ** (len(data)-1-i)
    print('C =', C)

    if Pu / (D*t*material['LFtu']) < 0 or Pu / (D*t*material['LFtu']) > 3:
        back_to_default(lab2_row, output_lab, output_value, font)
        error_lab_calc.config(
            text='Eq. 9.8.1 ration of Pu / D*t*Fx must be in interval [0, 3]', fg='red', font=font[1])
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
    num = open(os.path.join(
        dname, r'data/transverse_ultimate_load/function/B{}'.format(file_name)))
    num = float(num.readline())
    if Aav / Abr > num:
        data = open(os.path.join(
            dname, r'data/transverse_ultimate_load/function/R{}'.format(file_name)))
    else:
        data = open(os.path.join(
            dname, r'data/transverse_ultimate_load/function/L{}'.format(file_name)))
    data = format_data(data)

    if 0 < Aav / Abr > 1.4:
        back_to_default(lab2_row, output_lab, output_value, font)
        error_lab_calc.config(
            text='Eq. 9.8.12, ratio of Aav / Abr must be in interval 0 - 1.4', fg='red', font=font[1])
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
        back_to_default(lab2_row, output_lab, output_value, font)
        error_lab_calc.config(
            text='Eq. 9.8.12, ratio of Aav / Abr must be in interval 0 - 1.4', fg='red', font=font[1])
    else:
        ktry_data = format_data(
            open(os.path.join(dname, r'data/transverse_ultimate_load/function/ktry')))
        ktry = 0
        x = Aav / Abr
        for i in range(len(ktry_data)):
            ktry += ktry_data[i] * x ** (len(ktry_data)-1-i)
        print('ktry =', ktry, '\n')
        print('----------------------------------\n')

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
