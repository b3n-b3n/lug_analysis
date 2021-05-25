# Lug Analysis App Doumentation

### General information:
- if you have any questions/suggestions feel free to write me mail
  on e-mail adress: bencikben@gmail.com 
- do no rename/move/delete files inside directories 'data' and 'images'
- do not rename directories 'reports', 'data' and 'images'
- all of the calculations are based on the method described in book 
  Airframe Structural Design by Michael Chung-Yung Niu, you can find
  a copy of it in directory 'additional_info'
- to start the appliation you have to open the .exe file
- firts, the console will pop-up then the graphic interface (this would 
  not be in final version it is just for testing) 

### Calculaiton:
- after inputing all desired informations you have to choose matherial
  and relevant curve which could be displayed by buttons 'Curves 1' and 
  'Curves 2'
- it is also possible to input your own material properties properties in 
  the frame 'other_material' and then you have to select option 
  other_matherial inside the frame 'materials'
- redrawing the scheme is possilbe by ckicking the 'Redraw' button or 
  by hitting <return> key
- when you are done click 'Calculate' button which will display output
  inside the frame 'outputs' and console will display certain variables
  used in calculations, the names corresponds to the ones used in the book

### Generating a report:
- Report button:
	- the function triggered by this button will save report in the form
	  of screenshot and it will ask you where you want to save it

- Multiple reports button:
	- creates multiple reports based on .txt file
	- it will promtpt you to choose the file you want to process
	- the example of suitable data could be found inside the directory 
  	test_data, it was copied directly from excel 
	- structure of the data has to look like this:

	report_name | Fx[N] | Fy[N] | D[mm] | t[mm] | a[mm] | W[mm]
	----------- | ----- | ----- | ----- | ----- | ----- | -----
	_ | _ | _ | _ | _ | _ | _
	_ | _ | _ | _ | _ | _ | _
	_ | _ | _ | _ | _ | _ | _
	_ | _ | _ | _ | _ | _ | _
