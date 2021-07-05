# Lug Analysis App Doumentation

### General information:
- if you have any questions/suggestions feel free to mail me at: bencikben@gmail.com 
- all of the calculations are based on the method described in book Airframe Structural Design by Michael Chung-Yung Niu, you can finda copy of it in directory 'additional_info'
- the binary file (.exe) is independant and can function without other files bundeled to this repository
- the directory exe_file contains executable binary file for windows:
	- in addition it opens up a console to make it easier for debugging potential errors

### Calculation:
- after inputing all desired informations you have to choose matherialand relevant curve which could be displayed by buttons 'Curves 1' and 'Curves 2'
- it is also possible to input your own material properties properties in the frame 'specific material & grain direction' and then you have to select option specific_matherial inside the frame 'materials'
- it is possible to reverse grain direction inside the frame 'specific material & grain direction' the default orientation is L: X; LT: Y
- redrawing the scheme is possilbe by ckicking the 'Redraw' button or by hitting <return> key

### Generating a report:
- Report button:
	- the function triggered by this button will save report in the form of screenshot and will ask you where you want to save it

- Multiple reports button:
	- creates multiple reports based on .txt file
	- it will promtpt you to choose a directory where you want to save the output and after that you will have to choose the file you want to process 
	- the example of suitable data could be found inside the directory test_data, it was copied directly from excel 
	- structure of the data has to look like this (columns are divided by tabulator):

	report_name | Fx[N] | Fy[N] | D[mm] | t[mm] | a[mm] | W[mm]
	----------- | ----- | ----- | ----- | ----- | ----- | -----
	_ | _ | _ | _ | _ | _ | _
	_ | _ | _ | _ | _ | _ | _
	_ | _ | _ | _ | _ | _ | _
	_ | _ | _ | _ | _ | _ | _
