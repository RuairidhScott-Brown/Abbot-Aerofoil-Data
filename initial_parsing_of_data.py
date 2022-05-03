import pprint
import re
import matplotlib.pyplot as plt
import scipy.interpolate
import numpy as np
import copy
import typing

demo = "C:/Users/18rsc/Documents/imperial/year_3/abbott_data/data/203.ALL"



class Aerofoil:   

    def __init__(self, file_location: str) -> None:

        self.__aerofoil_name: str | None = None
        self.__page_number: str = file_location[-7:-4]

        with open(file_location, 'r') as file:
            self.__lines = file.readlines()

        self.__data: dict = {"CL_vs_alpha": {
                        "3x10^6": { 
                            "alpha": [],
                            "CL": []
                        },
                        "6x10^6": {
                            "alpha": [],
                            "CL": []
                        }, 
                        "9x10^6": {
                            "alpha": [],
                            "CL": []
                        }, 
                        "6x10^6-rough": {
                            "alpha": [],
                            "CL": []
                        }, 
                        "flap": {
                            "alpha": [],
                            "CL": []
                        }, 
                        "flap-rough": {
                            "alpha": [],
                            "CL": []
                        }
        },
        "CM_vs_alpha": {
                        "3x10^6": { 
                            "alpha": [],
                            "CM": []
                        },
                        "6x10^6": {
                            "alpha": [],
                            "CM": []
                        }, 
                        "9x10^6": {
                            "alpha": [],
                            "CM": []
                        }, 
                        "6x10^6-rough": {
                            "alpha": [],
                            "CM": []
                        }, 
                        "flap": {
                            "alpha": [],
                            "CM": []
                        }, 
                        "flap-rough": {
                            "alpha": [],
                            "CM": []
                        }

        },
        "CL_vs_CD": {
                        "3x10^6": { 
                            "CD": [],
                            "CL": []
                        },
                        "6x10^6": {
                            "CD": [],
                            "CL": []
                        }, 
                        "9x10^6": {
                            "CD": [],
                            "CL": []
                        }, 
                        "6x10^6-rough": {
                            "CD": [],
                            "CL": []
                        }, 
                        "flap": {
                            "CD": [],
                            "CL": []
                        }, 
                        "flap-rough": {
                            "CD": [],
                            "CL": []
                        }

        },
        "CL_vs_CM": {
                        "3x10^6": { 
                            "CM": [],
                            "CL": []
                        },
                        "6x10^6": {
                            "CM": [],
                            "CL": []
                        }, 
                        "9x10^6": {
                            "CM": [],
                            "CL": []
                        }, 
                        "6x10^6-rough": {
                            "CM": [],
                            "CL": []
                        }, 
                        "flap": {
                            "CM": [],
                            "CL": []
                        }, 
                        "flap-rough": {
                            "CM": [],
                            "CL": []
                        }

        }                 
    }

        self.__clean()
        self.__create_dict()

    def __clean(self):  
        flag = True
        while flag == True:
            flag = False
            for line_number, line in enumerate(self.__lines):
                if re.search("[a-zA-Z]", line):
                    flag = True
                    self.__lines.remove(line)
        self.__remove_newline()
        self.__convert_to_float()

    def __remove_newline(self):
        for line_number, line in enumerate(self.__lines):
            self.__lines[line_number] = line.replace('\n', '')

    def __convert_to_float(self):
        for line_number, line in enumerate(self.__lines):
            string_list = line.split()
            for index, string in enumerate(string_list):
                string_list[index] = float(string)
            self.__lines[line_number] = string_list

    def __create_dict(self):
        counter = 0
        counter_2 = 0
        for index, array in enumerate(self.__lines):
            if len(array) == 3:
                break  
            if len(array) == 1:
                temp = array[0]
                if counter < temp:
                    counter = array[0]
                elif counter > temp:
                    counter_2 = 1
                    counter = array[0]
                else:
                    break

                continue
            if counter == 1 and counter_2 == 0:
                self.__data["CL_vs_alpha"]["3x10^6"]["alpha"].append(array[0])
                self.__data["CL_vs_alpha"]["3x10^6"]["CL"].append(array[1])
            elif counter == 2 and counter_2 == 0:
                self.__data["CL_vs_alpha"]["6x10^6"]["alpha"].append(array[0])
                self.__data["CL_vs_alpha"]["6x10^6"]["CL"].append(array[1])
            elif counter == 3 and counter_2 == 0:
                self.__data["CL_vs_alpha"]["9x10^6"]["alpha"].append(array[0])
                self.__data["CL_vs_alpha"]["9x10^6"]["CL"].append(array[1])
            elif counter == 4 and counter_2 == 0:
                self.__data["CL_vs_alpha"]["6x10^6-rough"]["alpha"].append(array[0])
                self.__data["CL_vs_alpha"]["6x10^6-rough"]["CL"].append(array[1])
            elif counter == 5 and counter_2 == 0:
                self.__data["CL_vs_alpha"]["flap"]["alpha"].append(array[0])
                self.__data["CL_vs_alpha"]["flap"]["CL"].append(array[1])
            elif counter == 6 and counter_2 == 0:
                self.__data["CL_vs_alpha"]["flap-rough"]["alpha"].append(array[0])
                self.__data["CL_vs_alpha"]["flap-rough"]["CL"].append(array[1])
            
            elif counter == 7 and counter_2 == 0:
                self.__data["CM_vs_alpha"]["3x10^6"]["alpha"].append(array[0])
                self.__data["CM_vs_alpha"]["3x10^6"]["CM"].append(array[1])
            elif counter == 8 and counter_2 == 0:
                self.__data["CM_vs_alpha"]["6x10^6"]["alpha"].append(array[0])
                self.__data["CM_vs_alpha"]["6x10^6"]["CM"].append(array[1])
            elif counter == 9 and counter_2 == 0:
                self.__data["CM_vs_alpha"]["9x10^6"]["alpha"].append(array[0])
                self.__data["CM_vs_alpha"]["9x10^6"]["CM"].append(array[1])
            elif counter == 10 and counter_2 == 0:
                self.__data["CM_vs_alpha"]["6x10^6-rough"]["alpha"].append(array[0])
                self.__data["CM_vs_alpha"]["6x10^6-rough"]["CM"].append(array[1])
            elif counter == 11 and counter_2 == 0:
                self.__data["CM_vs_alpha"]["flap"]["alpha"].append(array[0])
                self.__data["CM_vs_alpha"]["flap"]["CM"].append(array[1])
            elif counter == 12 and counter_2 == 0:
                self.__data["CM_vs_alpha"]["flap-rough"]["alpha"].append(array[0])
                self.__data["CM_vs_alpha"]["flap-rough"]["CM"].append(array[1])

            elif counter == 1 and counter_2 == 1:
                self.__data["CL_vs_CD"]["3x10^6"]["CL"].append(array[0])
                self.__data["CL_vs_CD"]["3x10^6"]["CD"].append(array[1])
            elif counter == 2 and counter_2 == 1:
                self.__data["CL_vs_CD"]["6x10^6"]["CL"].append(array[0])
                self.__data["CL_vs_CD"]["6x10^6"]["CD"].append(array[1])
            elif counter == 3 and counter_2 == 1:
                self.__data["CL_vs_CD"]["9x10^6"]["CL"].append(array[0])
                self.__data["CL_vs_CD"]["9x10^6"]["CD"].append(array[1])
            elif counter == 4 and counter_2 == 1:
                self.__data["CL_vs_CD"]["6x10^6-rough"]["CL"].append(array[0])
                self.__data["CL_vs_CD"]["6x10^6-rough"]["CD"].append(array[1])
            elif counter == 5 and counter_2 == 1:
                self.__data["CL_vs_CD"]["flap"]["CL"].append(array[0])
                self.__data["CL_vs_CD"]["flap"]["CD"].append(array[1])
            elif counter == 6 and counter_2 == 1:
                self.__data["CL_vs_CD"]["flap-rough"]["CL"].append(array[0])
                self.__data["CL_vs_CD"]["flap-rough"]["CD"].append(array[1])

            elif counter == 7 and counter_2 == 1:
                self.__data["CL_vs_CM"]["3x10^6"]["CL"].append(array[0])
                self.__data["CL_vs_CM"]["3x10^6"]["CM"].append(array[1])
            elif counter == 8 and counter_2 == 1:
                self.__data["CL_vs_CM"]["6x10^6"]["CL"].append(array[0])
                self.__data["CL_vs_CM"]["6x10^6"]["CM"].append(array[1])
            elif counter == 9 and counter_2 == 1:
                self.__data["CL_vs_CM"]["9x10^6"]["CL"].append(array[0])
                self.__data["CL_vs_CM"]["9x10^6"]["CM"].append(array[1])
            elif counter == 10 and counter_2 == 1:
                self.__data["CL_vs_CM"]["6x10^6-rough"]["CL"].append(array[0])
                self.__data["CL_vs_CM"]["6x10^6-rough"]["CM"].append(array[1])
            elif counter == 11 and counter_2 == 1:
                self.__data["CL_vs_CM"]["flap"]["CL"].append(array[0])
                self.__data["CL_vs_CM"]["flap"]["CM"].append(array[1])
            elif counter == 12 and counter_2 == 1:
                self.__data["CL_vs_CM"]["flap-rough"]["CL"].append(array[0])
                self.__data["CL_vs_CM"]["flap-rough"]["CM"].append(array[1])
            
    def find_the_LD_max(self,x,y):
        if len(x) == 0:
            return 0
        grad = []
        for i in range(len(x)):
            grad.append((y[i] - 0) / (x[i] - 0))
        index_grad = grad.index(max(grad))
        return y[index_grad]
        fig, axes = plt.subplots(1,2)
        axes[0].plot(x, y, "o-")
        axes[0].plot([0,x[index_grad]], [0,y[index_grad]])
        axes[1].plot(self.__data["CL_vs_CD"]["3x10^6"]["CD"],self.__data["CL_vs_CD"]["3x10^6"]["CL"], "o-")
        axes[1].plot([0,x[index_grad]], [0,y[index_grad]])
        plt.show()

    def find_LD_in_range(self, Cl, Cd, min, max):             
        Cl = np.array(Cl)
        Cd = np.array(Cd)
        LD = Cl/Cd
        LD_in_range = []
        for index, i in enumerate(Cl):
            if i > min and i < max:
                LD_in_range.append(LD[index])
        return LD_in_range


    def find_LD(self, mini, maxi):
        Re3_LD = self.find_LD_in_range(self.__data["CL_vs_CD"]["3x10^6"]["CL"],self.__data["CL_vs_CD"]["3x10^6"]["CD"], mini, maxi)
        Re6_LD = self.find_LD_in_range(self.__data["CL_vs_CD"]["6x10^6"]["CL"],self.__data["CL_vs_CD"]["6x10^6"]["CD"], mini, maxi)
        Re9_LD = self.find_LD_in_range(self.__data["CL_vs_CD"]["9x10^6"]["CL"],self.__data["CL_vs_CD"]["9x10^6"]["CD"], mini, maxi)
        Re6_LD_rough = self.find_LD_in_range(self.__data["CL_vs_CD"]["6x10^6-rough"]["CL"],self.__data["CL_vs_CD"]["6x10^6-rough"]["CD"], mini, maxi)
        #flap_1 = self.find_LD_in_range(self.__data["CL_vs_CD"]["flap_1"]["CL"],self.__data["CL_vs_CD"]["flap_1"]["CD"], mini, maxi)
        #flap_2 = self.find_LD_in_range(self.__data["CL_vs_CD"]["flap_2"]["CL"],self.__data["CL_vs_CD"]["flap_2"]["CD"], mini, maxi)

        return {"3x10^6_LD": Re3_LD, "6x10^6_LD": Re6_LD, "9x10^6_LD": Re9_LD, "6x10^6_rough_LD": Re6_LD_rough}


    def print_LD(self):

        Re3_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["3x10^6"]["CD"], self.__data["CL_vs_CD"]["3x10^6"]["CL"])
        Re3_LD_CD_index = self.__data["CL_vs_CD"]["3x10^6"]["CL"].index(Re3_LD)
        Re3_LD_CD = self.__data["CL_vs_CD"]["3x10^6"]["CD"][Re3_LD_CD_index]

        Re6_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["6x10^6"]["CD"], self.__data["CL_vs_CD"]["6x10^6"]["CL"])
        Re6_LD_CD_index = self.__data["CL_vs_CD"]["6x10^6"]["CL"].index(Re6_LD)
        Re6_LD_CD = self.__data["CL_vs_CD"]["6x10^6"]["CD"][Re6_LD_CD_index]

        Re9_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["9x10^6"]["CD"], self.__data["CL_vs_CD"]["9x10^6"]["CL"])
        Re9_LD_CD_index = self.__data["CL_vs_CD"]["9x10^6"]["CL"].index(Re9_LD)
        Re9_LD_CD = self.__data["CL_vs_CD"]["9x10^6"]["CD"][Re9_LD_CD_index]

        Re6_LD_rough = self.find_the_LD_max(self.__data["CL_vs_CD"]["6x10^6-rough"]["CD"], self.__data["CL_vs_CD"]["6x10^6-rough"]["CL"])
        Re6_LD_rough_CD_index = self.__data["CL_vs_CD"]["6x10^6-rough"]["CL"].index(Re6_LD_rough)
        Re6_LD_rough_CD = self.__data["CL_vs_CD"]["6x10^6-rough"]["CD"][Re6_LD_rough_CD_index]

        #flap_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["flap"]["CD"], self.__data["CL_vs_CD"]["flap"]["CL"])
        #flap_LD_CD_index = self.__data["CL_vs_CD"]["flap"]["CL"].index(flap_LD)
        #flap_LD_CD = self.__data["CL_vs_CD"]["3x10^6"]["CD"][flap_LD_CD_index]

        #flap-rough_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["flap-rough"]["CD"], self.__data["CL_vs_CD"]["flap-rough"]["CL"])
        #flap_2_LD_CD_index = self.__data["CL_vs_CD"]["flap-rough"]["CL"].index(flap-rough_LD)
        #flap_2_LD_CD = self.__data["CL_vs_CD"]["flap-rough"]["CD"][flap_2_LD_CD_index]

        fig, axes = plt.subplots(2,2)
        axes[0,0].plot(self.__data["CL_vs_CD"]["3x10^6"]["CL"], self.__data["CL_vs_CD"]["3x10^6"]["CD"])
        axes[0,0].plot([0, Re3_LD], [0, Re3_LD_CD])
        axes[0,1].plot(self.__data["CL_vs_CD"]["6x10^6"]["CL"], self.__data["CL_vs_CD"]["6x10^6"]["CD"])
        axes[0,1].plot([0, Re6_LD], [0, Re6_LD_CD])
        axes[1,0].plot(self.__data["CL_vs_CD"]["9x10^6"]["CL"], self.__data["CL_vs_CD"]["9x10^6"]["CD"])
        axes[1,0].plot([0, Re9_LD], [0, Re9_LD_CD])
        axes[1,1].plot(self.__data["CL_vs_CD"]["6x10^6-rough"]["CL"], self.__data["CL_vs_CD"]["6x10^6-rough"]["CD"])
        #axes[2,0].plot(self.__data["CL_vs_CD"]["flap"]["CL"], self.__data["CL_vs_CD"]["flap"]["CD"])
        #axes[2,1].plot(self.__data["CL_vs_CD"]["flap-rough"]["CL"], self.__data["CL_vs_CD"]["flap-rough"]["CD"])

        #plt.show()
            
    def LD_analysis(self):

        Re3_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["3x10^6"]["CD"], self.__data["CL_vs_CD"]["3x10^6"]["CL"])
        Re6_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["6x10^6"]["CD"], self.__data["CL_vs_CD"]["6x10^6"]["CL"])
        Re9_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["9x10^6"]["CD"], self.__data["CL_vs_CD"]["9x10^6"]["CL"])
        Re6_LD_rough = self.find_the_LD_max(self.__data["CL_vs_CD"]["6x10^6-rough"]["CD"], self.__data["CL_vs_CD"]["6x10^6-rough"]["CL"])
        flap_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["flap"]["CD"], self.__data["CL_vs_CD"]["flap"]["CL"])
        flap_rough_LD = self.find_the_LD_max(self.__data["CL_vs_CD"]["flap-rough"]["CD"], self.__data["CL_vs_CD"]["flap-rough"]["CL"])        
        return {"3x10^6_LD": Re3_LD, "6x10^6_LD": Re6_LD, "9x10^6_LD": Re9_LD, "6x10^6_rough_LD": Re6_LD_rough, "flap_LD": flap_LD, "flap-rough_LD": flap_rough_LD}

        """
        lift_over_drag = list(Re3_range_y / Re3_range_x)
        max_lift_over_drag = max(lift_over_drag)
        print(max_lift_over_drag)
        index_LD_max = lift_over_drag.index(max_lift_over_drag)
        print(index_LD_max)
        print(Re3_range_y[index_LD_max])
        
        Re6 = scipy.interpolate.interp1d(self.__data["CL_vs_CD"]["6x10^6"]["CD"], self.__data["CL_vs_CD"]["6x10^6"]["CL"])
        Re9 = scipy.interpolate.interp1d(self.__data["CL_vs_CD"]["9x10^6"]["CD"], self.__data["CL_vs_CD"]["9x10^6"]["CL"])
        Re6_rough = scipy.interpolate.interp1d(self.__data["CL_vs_CD"]["6x10^6_rough"]["CD"], self.__data["CL_vs_CD"]["6x10^6_rough"]["CL"])
        flap = scipy.interpolate.interp1d(self.__data["CL_vs_CD"]["flap"]["CD"], self.__data["CL_vs_CD"]["flap"]["CL"])
        flap-rough = scipy.interpolate.interp1d(self.__data["CL_vs_CD"]["flap-rough"]["CD"], self.__data["CL_vs_CD"]["flap-rough"]["CL"])
        """

    def plot_all_data(self):
        fig, axes = plt.subplots(2,2, figsize = (25,10))
        axes[0,0].grid()
        self.__add_to_plot(axes[0,0], self.__data["CL_vs_alpha"]["3x10^6"]["alpha"], self.__data["CL_vs_alpha"]["3x10^6"]["CL"], "RE: 3x10^6")
        self.__add_to_plot(axes[0,0], self.__data["CL_vs_alpha"]["6x10^6"]["alpha"], self.__data["CL_vs_alpha"]["6x10^6"]["CL"],"RE: 6x10^6")
        self.__add_to_plot(axes[0,0], self.__data["CL_vs_alpha"]["9x10^6"]["alpha"], self.__data["CL_vs_alpha"]["9x10^6"]["CL"], "RE: 9x10^6")
        self.__add_to_plot(axes[0,0], self.__data["CL_vs_alpha"]["6x10^6-rough"]["alpha"], self.__data["CL_vs_alpha"]["6x10^6-rough"]["CL"], "RE: 6x10^6-rough")
        self.__add_to_plot(axes[0,0], self.__data["CL_vs_alpha"]["flap"]["alpha"], self.__data["CL_vs_alpha"]["flap"]["CL"], "RE: 6x10^6 flap")
        self.__add_to_plot(axes[0,0], self.__data["CL_vs_alpha"]["flap-rough"]["alpha"], self.__data["CL_vs_alpha"]["flap-rough"]["CL"], "RE: 6x10^6-rough flap")
        axes[0,0].set_xlabel(r"$AoA^\circ$", fontsize = 20)
        axes[0,0].set_ylabel(r"$C_L$", fontsize = 20)
        axes[0,0].legend(loc = 0)

        self.__add_to_plot(axes[0,1], self.__data["CM_vs_alpha"]["3x10^6"]["alpha"], self.__data["CM_vs_alpha"]["3x10^6"]["CM"], "RE: 3x10^6")
        self.__add_to_plot(axes[0,1], self.__data["CM_vs_alpha"]["6x10^6"]["alpha"], self.__data["CM_vs_alpha"]["6x10^6"]["CM"], "RE: 6x10^6")
        self.__add_to_plot(axes[0,1], self.__data["CM_vs_alpha"]["9x10^6"]["alpha"], self.__data["CM_vs_alpha"]["9x10^6"]["CM"], "RE: 9x10^6")
        self.__add_to_plot(axes[0,1], self.__data["CM_vs_alpha"]["6x10^6-rough"]["alpha"], self.__data["CM_vs_alpha"]["6x10^6-rough"]["CM"], "RE: 6x10^6-rough")
        self.__add_to_plot(axes[0,1], self.__data["CM_vs_alpha"]["flap"]["alpha"], self.__data["CM_vs_alpha"]["flap"]["CM"], "RE: 6x10^6-rough")
        self.__add_to_plot(axes[0,1], self.__data["CM_vs_alpha"]["flap-rough"]["alpha"], self.__data["CM_vs_alpha"]["flap-rough"]["CM"], "RE: 6x10^6-rough flap")
        axes[0,1].set_xlabel(r"$AoA^\circ$", fontsize = 20)
        axes[0,1].set_ylabel(r"$C_M$", fontsize = 20)
        axes[0,1].grid()
        axes[0,1].legend(loc = 0)

        self.__add_to_plot(axes[1,0],self.__data["CL_vs_CD"]["3x10^6"]["CL"], self.__data["CL_vs_CD"]["3x10^6"]["CD"], "RE: 3x10^6")
        self.__add_to_plot(axes[1,0],self.__data["CL_vs_CD"]["6x10^6"]["CL"], self.__data["CL_vs_CD"]["6x10^6"]["CD"],"RE: 6x10^6")
        self.__add_to_plot(axes[1,0],self.__data["CL_vs_CD"]["9x10^6"]["CL"], self.__data["CL_vs_CD"]["9x10^6"]["CD"], "RE: 9x10^6")
        self.__add_to_plot(axes[1,0],self.__data["CL_vs_CD"]["6x10^6-rough"]["CL"], self.__data["CL_vs_CD"]["6x10^6-rough"]["CD"], "RE: 6x10^6-rough")
        self.__add_to_plot(axes[1,0],self.__data["CL_vs_CD"]["flap"]["CL"], self.__data["CL_vs_CD"]["flap"]["CD"], "RE: 6x10^6-rough")
        self.__add_to_plot(axes[1,0],self.__data["CL_vs_CD"]["flap-rough"]["CL"], self.__data["CL_vs_CD"]["flap-rough"]["CD"], "RE: 6x10^6-rough flap")
        axes[1,0].set_xlabel(r"$C_D$", fontsize = 20)
        axes[1,0].set_ylabel(r"$C_L$", fontsize = 20)
        axes[1,0].grid()
        axes[1,0].legend(loc = 0)

        self.__add_to_plot(axes[1,1], self.__data["CL_vs_CM"]["3x10^6"]["CM"], self.__data["CL_vs_CM"]["3x10^6"]["CL"], "RE: 3x10^6")
        self.__add_to_plot(axes[1,1], self.__data["CL_vs_CM"]["6x10^6"]["CM"], self.__data["CL_vs_CM"]["6x10^6"]["CL"], "RE: 6x10^6")
        self.__add_to_plot(axes[1,1], self.__data["CL_vs_CM"]["9x10^6"]["CM"], self.__data["CL_vs_CM"]["9x10^6"]["CL"], "RE: 9x10^6")
        self.__add_to_plot(axes[1,1], self.__data["CL_vs_CM"]["6x10^6-rough"]["CM"], self.__data["CL_vs_CM"]["6x10^6-rough"]["CL"], "RE: 6x10^6-rough")
        self.__add_to_plot(axes[1,1], self.__data["CL_vs_CM"]["flap"]["CM"], self.__data["CL_vs_CM"]["flap"]["CL"], "RE: 6x10^6-rough")
        self.__add_to_plot(axes[1,1], self.__data["CL_vs_CM"]["flap-rough"]["CM"], self.__data["CL_vs_CM"]["flap-rough"]["CL"], "RE: 6x10^6-rough flap")
        axes[1,1].set_xlabel(r"$C_M$", fontsize = 20)
        axes[1,1].set_ylabel(r"$C_L$", fontsize = 20)
        axes[1,1].grid()
        axes[1,1].legend(loc = 0)

        plt.show()

    def __add_to_plot(self, axes, x: list, y: list, label: str) -> None:            
        if len(x) < 1 or len(y) < 1:
            return
        else:
            axes.plot(x, y, "x-", label = label)

    @property
    def data(self) -> dict:
        return self.__data

    def print_data(self) -> None:
        pprint.pprint(self.__data)




file_location = "C:/Users/18rsc/Documents/imperial/year_3/abbott_data/data/"
all_aerofoils = []
Cl_stuff_3 = []
Cl_stuff_6 = []
Cl_stuff_9 = []
counter  = 131
for page_number in range(131,264):
    file = f"{file_location}{page_number}.ALL"
    try:
        NACA = Aerofoil(file)
    except:
        continue
    Cl_stuff_3.append(NACA.find_LD(0.25, 0.4)["3x10^6_LD"])
    Cl_stuff_6.append(NACA.find_LD(0.2, 0.4)["6x10^6_LD"])
    Cl_stuff_9.append(NACA.find_LD(0.2, 0.4)["9x10^6_LD"])
    all_aerofoils.append(NACA)


# for index, value in enumerate(Cl_stuff_3):
#     three = np.average(value)
#     six = np.average(Cl_stuff_6[index])
#     nine = np.average(Cl_stuff_9[index])
#     avg = (six + nine + three) / 3
#     print(f"{index}     {three}     {six}      {nine}     {avg}")

print(len(all_aerofoils))

N = all_aerofoils[17]
N.plot_all_data()

# e = 0.9
# CL = 0.27
# AR = np.arange(5, 10, 0.1)
# induced_drag = CL / (e * np.pi *AR)
# weight = AR**(0.5)

# def best_fit(X, Y):

#     xbar = sum(X)/len(X)
#     ybar = sum(Y)/len(Y)
#     n = len(X) # or len(Y)

#     numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
#     denum = sum([xi**2 for xi in X]) - n * xbar**2

#     b = numer / denum
#     a = ybar - b * xbar

#     print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

#     return a, b

# CL__ = np.array(N.data["CL_vs_alpha"]["6x10^6"]["CL"])
# alpha__ = np.array(N.data["CL_vs_alpha"]["6x10^6"]["alpha"])

# alpha_ = np.array([])
# CL_ = np.array([])

# for index, value in enumerate(alpha__):
#     if value > -10 and value < 10:
#         print(value)
#         alpha_ = np.append(alpha_, value)
#         CL_ = np.append(CL_, CL__[index])

# print(CL_)
# print(alpha_)

# X = np.append(alpha_.reshape(len(alpha_), 1), np.ones((len(alpha_), 1)), axis=1)
# a__, b__ = best_fit(alpha_, CL_)

# theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(CL_)
# theta = [b__, a__]
# print(f'The parameters of the line: {theta}')
# y_line = X.dot(theta)

# Cl_ascpect_5 = CL__ / (1 + (CL__) / (e* np.pi *5))
# Cl_ascpect_6 = CL__ / (1 + (CL__) / (e* np.pi *6))
# Cl_ascpect_7 = CL__ / (1 + (CL__) / (e* np.pi *7.5))
# Cl_ascpect_8 = CL__ / (1 + (CL__) / (e* np.pi *8))
# Cl_ascpect_9 = CL__ / (1 + (CL__) / (e* np.pi *9))
# Cl_ascpect_10 = CL__ / (1 + (CL__) / (e* np.pi *10))


# beta = (1-0.75**2)**0.5
# n_airf = (beta*2*np.pi)/(2*np.pi)
# F = 1.07*(1+(1.7/12.9))**2
# s = 0.82
# a_5 = (2*np.pi*5) / (2 + (4 + ((5**2*beta**2)/(n_airf**2))*(1 + ((np.tan(np.deg2rad(12))**2)/(beta**2))))**0.5)*s*F #(np.pi*5/2) * (theta[0]/(2*np.pi))#theta[0] / ((1 + 57.3*theta[0] )/(np.pi * e * 5))
# a_6 = (2*np.pi*6) / (2 + (4 + ((6**2*beta**2)/(n_airf**2))*(1 + ((np.tan(np.deg2rad(12))**2)/(beta**2))))**0.5)*s*F#(np.pi*6/2) * (theta[0]/(2*np.pi))#theta[0]  / ((1 + 57.3*theta[0] )/(np.pi * e * 6))
# a_7 = (2*np.pi*7.5) / (2 + (4 + ((7.5**2*beta**2)/(n_airf**2))*(1 + ((np.tan(np.deg2rad(12))**2)/(beta**2))))**0.5)*s*F#(np.pi*7.5/2) * (theta[0]/(2*np.pi))#theta[0]  / ((1 + 57.3*theta[0] )/(np.pi * e * 7.5))
# a_8 = (2*np.pi*8) / (2 + (4 + ((8**2*beta**2)/(n_airf**2))*(1 + ((np.tan(np.deg2rad(12))**2)/(beta**2))))**0.5)*s*F#(np.pi*8/2) * (theta[0]/(2*np.pi))#theta[0]  / ((1 + 57.3*theta[0] )/(np.pi * e * 8))
# a_9 = (2*np.pi*9) / (2 + (4 + ((9**2*beta**2)/(n_airf**2))*(1 + ((np.tan(np.deg2rad(12))**2)/(beta**2))))**0.5)*s*F#(np.pi*9/2) * (theta[0]/(2*np.pi))#theta[0]  / ((1 + 57.3*theta[0] )/(np.pi * e * 9))
# a_10 = (2*np.pi*10) / (2 + (4 + ((10**2*beta**2)/(n_airf**2))*(1 + ((np.tan(np.deg2rad(12))**2)/(beta**2))))**0.5)*s*F#(np.pi*10/2) * (theta[0]/(2*np.pi))#theta[0]  / ((1 + 57.3*theta[0] )/(np.pi * e * 10))

# theta_5 = copy.copy(theta)
# theta_5[0] = a_5
# theta_6 = copy.copy(theta)
# theta_6[0] = a_6
# theta_7 = copy.copy(theta)
# theta_7[0] = a_7
# a_7_in_rad = a_7*(np.pi/180.0)
# print(f"This is the lift curve slope in degrees {theta[0]*(180/np.pi)}")
# theta_8 = copy.copy(theta)
# theta_8[0] = a_8
# theta_9 = copy.copy(theta)
# theta_9[0] = a_9
# theta_10 = copy.copy(theta)
# theta_10[0] = a_10

# al = np.linspace(-5,15, 10)
# CL_0 = theta[0]*(alpha_ + 1.32)
# CL_5 = a_5*(np.pi/180)*(al + 1.32)
# CL_6 = a_6*(np.pi/180)*(al + 1.32)
# CL_7 = a_7*(np.pi/180)*(al + 1.32)
# CL_8 = a_8*(np.pi/180)*(al + 1.32)
# CL_9 = a_9*(np.pi/180)*(al + 1.32)
# CL_10 = a_10*(np.pi/180)*(al + 1.32)
# print(CL_10)

# ## plot
# TE = 0.58
# LE = 0.82
# alpha_with_TE = theta[0] * (1 + (0.3*np.cos(np.deg2rad(40))) * (TE))
# alpha_with_LE = theta[0]*(1 + (1.1 - 1) * (LE))

# delta_alpha_0_TE = (-10.6)*TE
# delta_alpha_0_LE = 5
# print(f"This is the new slope for the TE {alpha_with_TE}")
# print(f"This is the new slope for the TE {alpha_with_LE}")
# print(theta[0])
# alpha_both = alpha_with_TE + (alpha_with_LE - theta[0])
# print(f"This is both {alpha_both*(180/np.pi)}")

# alpha_x = np.linspace(-15, 10, 100)

# y_slope_TE = (alpha_with_TE)*(alpha_x - delta_alpha_0_TE)
# y_slope_LE = (alpha_with_LE)*(alpha_x + 1.4)
# y_slope_both = (alpha_with_TE + (alpha_with_LE - theta[0]))*(alpha_x - delta_alpha_0_TE)
# y_slope_natural = a_7*(alpha_x - delta_alpha_0_TE)



# testing = b__*alpha_x - b__*delta_alpha_0_TE

# test_CL = []
# test_alpha = []
# a = N.data["CL_vs_alpha"]["6x10^6"]["CL"]
# for index, ele in enumerate(N.data["CL_vs_alpha"]["6x10^6"]["alpha"]):
#     if ele > 10 and ele < 18:
#         print(ele)
#         test_alpha.append(ele)
#         test_CL.append(a[index])

# print(test_CL)
# print(test_alpha)
# test_alpha = np.array(test_alpha) + 2
# test_CL = np.array(test_CL)
# test_CL = np.flip(test_CL + 1.21)
# test_alpha = np.flip(test_alpha)

# alpha_x_HLD = np.append(alpha_x, test_alpha)
# y_slope_TE_HLD = np.append(y_slope_both, test_CL)

# L = 2
# fig, ax = plt.subplots(1,1)
# ax.plot(N.data["CL_vs_alpha"]["6x10^6"]["alpha"], N.data["CL_vs_alpha"]["6x10^6"]["CL"], "x-", label = r"Experimental $C_{l\alpha}$", linewidth = L)
# ax.plot(alpha_x_HLD , y_slope_TE_HLD, "k-", label = r"Theoretical $C_{l\alpha}$ HLD: $2.27\times 10^{-3}$ ($1/rad$)", linewidth = L)
# ax.plot(alpha_x, y_slope_LE, label = r"$C_{l\alpha}$ L.E. $2.09\times 10^{-3}$ ($1/rad$)", linewidth = L)
# ax.plot(alpha_x, y_slope_TE, label = r"$C_{l\alpha}$ T.E. $1.92\times 10^{-3}$ ($1/rad$)", linewidth = L)
# ax.axvline(x = 16.47, linestyle = "--", color = "k", label = r"Stall angle: 16.5$^\circ$", linewidth = L)
# ax.axhline(y = 2.60, linestyle = "-.", color = "k", label = r"$C_{lmax}: 2.60$", linewidth = L)
# #ax.plot(test_alpha, test_CL)
# ax.set_ylim([-1, 3])
# ax.set_xlabel(r"AoA ($^\circ$)", fontsize = 20)
# ax.set_ylabel(r"$C_l$", fontsize = 20)
# ax.legend(fontsize = 14, loc = 2)
# plt.yticks(fontsize = 15)
# plt.xticks(fontsize = 15)
# ax.grid()



# x_alpha = np.linspace(-20,60,1000)

# fig, axs = plt.subplots(1, 1)
# print(f'The parameters of the line: {theta_10}')
# axs.plot(AR, weight)
# axs.set_xlabel(r'$AR$', fontsize=20)
# axs.set_ylabel(r'$W^\prime~(N)$', fontsize=20)
# axs.axvspan(7, 8, facecolor='#2ca02c', alpha=0.5)
# axs.axvline(x=7.5, color='black', linestyle='--', label = "Chosen AR = 7.5")
# axs.legend(loc = 3,fontsize = 20)
# axs.grid()
# plt.yticks(fontsize = 15)
# plt.xticks(fontsize = 15)
# fig, axs = plt.subplots(1, 1)
# axs.plot(AR,induced_drag)
# axs.set_xlabel(r'$AR$', fontsize=20)
# axs.set_ylabel(r'$C_{Di}$', fontsize=20)
# axs.axvspan(7, 8, facecolor='#2ca02c', alpha=0.5)
# axs.axvline(x=7.5, color='black', linestyle='--', label = "Chosen AR = 7.5")
# #axs.axvline(x=9, color='purple', linestyle='-.', label = "AR with winglets = 7.5")
# axs.legend(loc = 3,fontsize = 20)
# axs.grid()
# plt.yticks(fontsize = 15)
# plt.xticks(fontsize = 15)
# #axs[2].plot(N.data["CL_vs_alpha"]["6x10^6"]["alpha"], N.data["CL_vs_alpha"]["6x10^6"]["CL"], "x--", color = "k")
# #axs[2].plot(alpha_, CL_)
# #axs[2].plot(alpha_, y_line)
# fig, axs = plt.subplots(1, 1)
# axs.plot(al, CL_5, '-', label="AR = 5")
# #axs[2].plot(al, CL_6, '-', label="AR = 6")
# axs.plot(al, CL_7,'-', label="AR = 7.5")
# #axs[2].plot(al, CL_8, '-', label="AR = 8")
# axs.plot(al, CL_9, '-', label="AR = 9")
# #axs[2].plot(al, CL_10, label="AR = 10")
# #axs[2].plot(al, CL_0, label="AR = test")

# axs.set_xlabel(r'$AoA ~(^\circ)$', fontsize=20)
# axs.set_ylabel(r'$C_L$', fontsize=20)
# axs.grid()
# axs.legend(loc=4, fontsize = 20)
# plt.yticks(fontsize = 15)
# plt.xticks(fontsize = 15)


#axs[2].plot(N.data["CL_vs_alpha"]["6x10^6"]["alpha"], Cl_ascpect_6)
#axs[2].plot(N.data["CL_vs_alpha"]["6x10^6"]["alpha"], Cl_ascpect_7)
#axs[2].plot(N.data["CL_vs_alpha"]["6x10^6"]["alpha"], Cl_ascpect_8)
#axs[2].plot(N.data["CL_vs_alpha"]["6x10^6"]["alpha"], Cl_ascpect_9)
#axs[2].plot(N.data["CL_vs_alpha"]["6x10^6"]["alpha"], Cl_ascpect_10)

#plt.show()
#N.print_LD()