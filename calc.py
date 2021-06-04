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

    material_name = data[0].split(": ")
    material_name = material_name[1].strip("'")
    out['name'] = material_name
    
    for i in range(1, len(data)):
        data[i] = data[i].split(": ")
        data[i][0] = data[i][0].strip("'")
        data[i][1] = data[i][1].strip("'")
        out[data[i][0]] = float(data[i][1])
    return out


def show_output(value, id, label_map):
    label_map[id].config(text=value)
    if id != 'BEA': 
        label_map[id].grid(padx=(45, 1), stick='E')

    # highlight the results
    if value < 1: label_map[id].config(fg='red')
    else: label_map[id].config(fg='green')


def back_to_default(lab2_row, output_lab, output_value, font):
    # if there is an occurence of error the output labels
    # are returned to the default value
    for i in range(len(lab2_row)):
        output_value[output_lab[i]].config(
            text=output_lab[i], fg='black', font=font[1])
    output_value['BEA'].config(text='BEA', fg='black', font=font[1])


def format_data(data):
    data = data.readlines()
    for i in range(len(data)):
        data[i] = data[i].strip()
        data[i] = float(data[i])
    return data

def load_from_entries(d_entry, name, error_lab_calc, bg, font, cont):
    try:
        d_entry[name].config(highlightbackground=bg)
        out = float(d_entry[name].get())
        if cont: return (out, True)
        else: return (out, False)
    except:
        d_entry[name].config(highlightbackground='red')
        error_lab_calc.config(text='entries accept only float or interger vlaues', fg='red', font=font[1])
        return (-1, False)


def calculate(d_entry, material_info, curve_axial, dname, output_value,
    curve_trans, specific_Fbry, specific_LFtu, error_lab_calc, output_lab, lab2_row,
    specific_LFty, specific_TFtu, specific_TFty, reverse, f, font):
    
    bg = 'grey99'
    error_lab_calc.config(text='')
    cont = True  # continue if values are correct
    
    Fx, cont = load_from_entries(d_entry, 'fx_ent', error_lab_calc, bg, font, cont)
    Fy, cont = load_from_entries(d_entry, 'fy_ent', error_lab_calc, bg, font, cont)
    D, cont = load_from_entries(d_entry, 'd_ent', error_lab_calc, bg, font, cont)
    t, cont = load_from_entries(d_entry, 't_ent', error_lab_calc, bg, font, cont)
    a, cont = load_from_entries(d_entry, 'a_ent', error_lab_calc, bg, font, cont)
    W, cont = load_from_entries(d_entry, 'w_ent', error_lab_calc, bg, font, cont)

    # do not continue in calculaiton if an entry is missing or invalid
    if not cont: return

    F = math.sqrt(Fx**2 + Fy**2)
    material = material_info.get()
    reverse = reverse.get()
    print("reversed grain direction =", reverse)
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

    # print material data
    for mat in list(material.keys()):
        print('{}:'.format(mat), material[mat])
    print('')   

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
        show_output(FS_Pbru, 'Pbru', output_value)

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
            text='Eq. 9.8.2 ration of W/D must be in interval (1, 5)', fg='red', font=font[1])
        return
    else:
        At = (W - D) * t
        Ptu = kt*At*material['LFtu']
        FS_Ptu = round(Ptu / Fx, 2)
        show_output(FS_Ptu, 'Ptu', output_value)
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
            text='Eq. 9.8.1 ration of Pu / D*t*Fx must be in interval (0, 3)', fg='red', font=font[1])
        return
    else:
        Pya = C * (material['LFty']/material['LFtu']) * Pu
        FS_Pya = round(Pya / Fx, 2)
        show_output(FS_Pya, 'Py-axial', output_value)

    # TRANSVERSE LOAD -------------------------------------------------------------------------------------------------
    # ultimate load
    Abr = D * t
    A1 = (W/2 - D/2 * math.sqrt(2)/2) * t
    A2 = (a - D/2) * t
    A3 = A2
    A4 = A1

    Aav = 6 / ((3/A1) + (1/A2) + (1/A3) + (1/A1))

    print('')
    print('A1 =', A1)
    print('A2 =', A2)
    print('A3 =', A3)
    print('A4 =', A4, '\n')
    print('Aav =', Aav)
    print('Abr =', Abr)

    file_name = curve_trans.get()
    num = open(os.path.join(
        dname, r'data/transverse_ultimate_load/function/B{}'.format(file_name)))
    num = float(num.readline())
    if Aav / Abr > num and file_name != 6:
        data = open(os.path.join(
            dname, r'data/transverse_ultimate_load/function/R{}'.format(file_name)))
    else:
        data = open(os.path.join(
            dname, r'data/transverse_ultimate_load/function/L{}'.format(file_name)))
    data = format_data(data)

    if 0 < Aav / Abr > 1.4:
        back_to_default(lab2_row, output_lab, output_value, font)
        error_lab_calc.config(
            text='Eq. 9.8.12, ratio of Aav / Abr must be in interval (0, 1.4)', fg='red', font=font[1])
        return
    else:
        ktru = 0
        for i in range(len(data)):
            ktru += data[i] * (Aav / Abr)**(len(data)-1-i)
    print('ktru =', ktru)

    Ptru = ktru * Abr * material['LTFtu']
    FS_Ptru = round(Ptru / Fy, 2)
    show_output(FS_Ptru, 'Ptru', output_value)

    # yield load
    if 0 < Aav / Abr > 1.4:
        back_to_default(lab2_row, output_lab, output_value, font)
        error_lab_calc.config(
            text='Eq. 9.8.12, ratio of Aav / Abr must be in interval (0, 1.4)', fg='red', font=font[1])
        return
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
    show_output(FS_Pyt, 'Py-tranverse', output_value)

    # OBLIQUE LOAD ----------------------------------------------------------------------------------------------------------
    # ultimate load
    Rau = (Fx/min(Pbru, Ptu))**1.6
    Rtru = (Fy/Ptru)**1.6
    ultimate_oblique_load = 1 / (Rau + Rtru)**0.625
    ultimate_oblique_load = round(ultimate_oblique_load, 2)
    show_output(ultimate_oblique_load, 'FS1', output_value)

    # yield load
    Ray = (Fx/Pya)**1.6
    Rtry = (Fy/Pyt)**1.6
    oblique_yield_load = 1 / (Ray + Rtry)**0.625
    oblique_yield_load = round(oblique_yield_load, 2)
    show_output(oblique_yield_load, 'FS2', output_value)

    # SUCINITEL BEZPECNOSTI--------------------------------------------------------------------------------------------------
    delta_bea = F / (D * t)
    gamma_bea = round(material['Fbry'] / delta_bea, 2)
    show_output(gamma_bea, 'BEA', output_value)
