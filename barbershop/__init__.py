#!/bin/env python
# -*- coding: utf-8 -*-

"""
A Python package that aids the user in making dynamic cuts to data in various
parameter spaces, using a simple GUI.

.. versioncreated:: 0.1
.. versionchanged:: 1.0

.. codeauthor:: Oliver James Hall <ojh251@student.bham.ac.uk>
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.widgets import Slider, Button
import glob as glob
import pandas as pd

from .external_functions import *

class open:
    def __init__(self, _core_df, _namex, _namey):
        '''
        A class that initialises the barbershop class which all other content is
        appended to.

        Parameters:
            _core_df (pandas.core.frame.DataFrame): A dataframe containing all
                        data the user wishes to call in this module.
            _namex (str): The name of the X values in _core_df
            _namey (str): The name of the Y values in _core_df
        '''
        #Check contents is a dataframe
        if not isinstance(_core_df, pd.core.frame.DataFrame):
            print('Please enter in a pandas DataFrame containing the data.')
            self.close_shop()
            return None

        self.core_df = _core_df
        self.namex = _namex
        self.namey = _namey
        self.X = self.core_df[self.namex]
        self.Y = self.core_df[self.namey]

        #Premeptively turn both histograms off
        self.hist_x_on = False
        self.hist_y_on = False

        #Initializing other metadata
        self.clients = 0
        self.seating = pd.DataFrame({self.namex: self.X, self.namey : self.Y})
        self.lowers = pd.DataFrame()
        self.uppers = pd.DataFrame()
        self.floc = 'dataframe_cut.csv'
        self.cloc = 'cuts.csv'

        #Check X and Y are of equal length
        if len(self.X) != len(self.Y):
            print('X and Y are not of equal length.')
            self.close_shop()
            return None

        if any(type(word) != str for word in [self.namex, self.namey]):
            print('Please enter "name" as a string.')
            self.close_shop()
            return None

    def histograms_on(self,x=False,y=False):
        '''Turn on optional histograms for x and y parameter spaces.
        Parameters:
            x (bool): Default False. Set True to display histogram in x.
            y (bool): Default False. Set True to display histogram in y.
        '''
        self.hist_x_on = x
        self.hist_y_on = y

    def add_client(self, name, lower=-np.inf, upper=np.inf):
        '''
        A function that allows the user to add a parameter to make cuts in, up to
        a maximum of five. The user has the option of setting lower and upper
        limits on the cuts in this parameter space. If values are given for either
        'lower', 'upper', or 'both', these are used to make initial cuts to the
        data.

        Parameters:
            client (ndarray): an array as the same length as self.X and self.Y,
                arranged identically, with parameter values for each data point.

            name (str): a string containing the name of the dataframe column to
                make cuts in, which will be referred to in other functions and
                printed on the GUI.

            lower (float): Default -Inf. The lowest possible value of the cut
                in this parameter space. If no value is given, it takes the
                minimum value in the 'client' ndarray.

            upper (float): Default Inf. The highest possible value of the cut
                in this parameter space. If no value is given, it takes the
                highest value in the 'client' ndarray.
        '''
        #Call the data from the core dataframe
        try:
            client = self.core_df[name]
        except KeyError:
            print('The handle "'+str(name)+'" is not affiliated with a dataframe column.')
            print('Please enter a correct handle, or re-open the barbershop with a different dataframe.')
            print('Client leaving the barbershop.')
            print('Number of seats in use : '+str(self.clients)+'/5.')
            return None

        #Check that the list of clients isn't already full
        if self.clients == 5:
            print('The barbershop is full, please proceed to plot the GUI, or remove clients using the evict_client(name) command.')
            return None

        #Check length of the client is in agreement with X and Y
        if len(client) != len(self.X):
            print('Client is not of equal length with X and Y.')
            print('Client leaving the barbershop.')
            print('Number of seats in use : '+str(self.clients)+'/5.')
            return None

        #Check that name is a string
        if type(name) != str:
            print('Please enter "name" as a string.')
            print('Client leaving the barbershop.')
            print('Number of seats in use : '+str(self.clients)+'/5.')
            return None

        #Adding the data to the existing class dataframe 'self.seating'
        self.seating[name] = client

        #Save the lower and upper values
        if not np.isfinite(lower):
            self.lowers[name] = [np.nanmin(client)]
        else:
            self.lowers[name] = [lower]
        if not np.isfinite(upper):
            self.uppers[name] = [np.nanmax(client)]
        else:
            self.uppers[name] = [upper]

        self.clients += 1
        print('Number of seats in use : '+str(self.clients)+'/5.')

        if self.clients == 5:
            print('The barbershop is now full (5 parameter spaces)')
            print('Please evict a client if you wish to add another.')

    def evict_client(self, name):
        '''
        Simple function that allows the user to remove a set of data in a given
        parameter space by passing the name it was given when added to the
        'add_client' function.

        Parameters:
            name (str): a string containing the name of the ndarray client,
                which will be referred to in other functions and printed on the
                GUI.
        '''
        #Check that name is a string
        if type(name) != str:
            print('Please enter "name" as a string.')
            return None

        #Check this name is actually included in the list of clients
        if not any(word == name for word in list(self.seating)):
            print('There is no set of parameters in the list of clients with this name.')
            return None

        #Remove client of title 'name' from the list of parameters
        del self.seating[name]
        del self.lowers[name]
        del self.uppers[name]
        self.clients -= 1
        print('Client '+str(name)+' has been evicted.')
        print('Number of seats in use : '+str(self.clients)+'/5.')

    def close_shop(self):
        '''
        Simple function that allows the user to reset the barbershop class
        completely by deleting all existing metadata.
        '''
        del self.X
        del self.Y
        del self.hist_x_on
        del self.hist_y_on
        del self.clients
        del self.seating
        del self.lowers
        del self.uppers
        del self.namex
        del self.namey

        print('All array and cuts metadata have been deleted from memory.')
        print('Please re-initialize the module.')
        print('\n\n')

    def get_regular(self, sfile):
        '''
        A function that allows the user to apply identical cuts to the same parameter
        spaces for a new dataframe saved from a previous set of cuts.

        NOTE: This class overwrites all loaded clients.

        Parameters:
            sfile (str): The location of the .csv file containing the cuts to be
            applied to the self.core_df dataframe.
        '''
        try:
            reg = pd.DataFrame.from_csv(sfile,sep=' ')
        except IOError:
            print('This file does not exist. Please fill in a correct file path.')
            return None
        try:
            l = reg.loc['lower']
            u = reg.loc['upper']
            self.lowers = pd.DataFrame()
            self.uppers = pd.DataFrame()
            for client in l.index:
                self.lowers[client] = [l[client]]
                self.uppers[client] = [u[client]]

        except KeyError:
            print('Please make sure you fill in a path to the correct file.')
            return None

        #Check all the regular names are in the loaded core_df
        for client in list(self.lowers):
            if all(word != client for word in list(self.core_df)):
                print('The label '+client+' is not in the loaded dataframe.')
                print('Please either make new cuts or reload barbershop after updating the labels in your dataframe.')
                return None

        print('All read-in labels correspond to columns in the loaded dataframe.')
        if self.clients > 0:
            print('Overwriting current clients...')
            self.seating = pd.DataFrame({self.namex: self.X, self.namey : self.Y})
            self.clients = 0

        for client in list(self.lowers):
            self.seating[client] = self.core_df[client]
            self.clients += 1
            print('Number of seats in use : '+str(self.clients)+'/5.')

        self.show_mirror()

    def show_mirror(self):
        '''
        A function that plots the data, sliders for cuts, and buttons.
        It plots:
            -For each client: a plot of X vs Y coloured according to the client
                data with corresponding colourbar.
            -A plot of X vs Y
            -(Optional): A histogram in X and/or Y
            -A plot containing up to 10 sliders (two for each client), buttons to
                reset the cuts on each slider, to save out the data, and to close
                all plots.
        '''
        #Make initial cuts
        dff = self.shave(self.lowers, self.uppers)

        '''
        INITIATING HISTOGRAMS
        '''
        #Initialise initial histograms axes if requested
        if any([self.hist_x_on, self.hist_y_on]):
            self.bins = int(np.sqrt(len(dff)))      #Save out number of bins for histograms
            if not all([self.hist_x_on, self.hist_y_on]):
                self.Hfig, self.Hax = plt.subplots()              #Create the figure
            else:
                #If both histograms are turned on
                self.Hfig, self.Hax = plt.subplots(2)         #Create the figure

            #Populated histograms
            get_histograms(self, dff)


        '''
        INITIATING PLOTS
        '''
        #Initialise all display parameter plots
        cmaps = ['viridis','winter','plasma','GnBu','cool']
        self.figs, self.axes = self.get_shells()
        #Create first build of plots
        for idx, client in enumerate(list(self.lowers)):
            ctemp = self.axes[idx].scatter(dff[self.namex],dff[self.namey],\
                        cmap = cmaps[idx], c=dff[client], s=20)
            self.figs[idx].colorbar(ctemp, label=client)
            self.axes[idx].grid()
            self.axes[idx].set_axisbelow(True)
            self.axes[idx].set_xlabel(self.namex)
            self.axes[idx].set_ylabel(self.namey)
            self.axes[idx].set_xlim(np.nanmin(self.seating[self.namex]),\
                                    np.nanmax(self.seating[self.namex]))
            self.axes[idx].set_ylim(np.nanmin(self.seating[self.namey]),\
                                    np.nanmax(self.seating[self.namey]))

        '''
        INITIATING SLIDERS
        '''
        #Initialise barbercide class for button functions
        barbicide = barbicideclass(self)
        #Initialise haircut class for slider functions
        haircut = haircutclass(self)
        axcolor = 'white'   #Defining button colours

        Sfig, Sax = plt.subplots(2*self.clients, figsize=(6,self.clients))
        #Adjusting the figure for buttons
        Sfig.subplots_adjust(bottom=(1./(2*self.clients+0.8)), right=0.70)

        #Note: This section can not be iterative, and is hardcoded
        for idx, client in enumerate(list(self.lowers)):
            if (self.clients >= 1) & (idx == 0):
                #Minimum value in parameter space 'client'
                self.a1min = Slider(Sax[int(2*idx)], 'Min '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.lowers[client][0])
                #Maximum value in parameter space 'client'
                self.a1max = Slider(Sax[int(2*idx)+1], 'Max '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.uppers[client][0])
                #Reset button for minimum slider
                l = Sax[int(2*idx)].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a1minres = Button(tax, 'Reset '+client+' Min', color=axcolor, hovercolor='0.7')
                #Reset button for maximum slider
                l = Sax[int(2*idx)+1].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a1maxres = Button(tax, 'Reset '+client+' Max', color=axcolor, hovercolor='0.7')

                #Update commands for the widgets
                self.a1min.on_changed(haircut.update)
                self.a1max.on_changed(haircut.update)
                self.a1minres.on_clicked(barbicide.a1min)
                self.a1maxres.on_clicked(barbicide.a1max)

            if (self.clients >= 2) & (idx == 1):
                #Minimum value in parameter space 'client'
                self.a2min = Slider(Sax[int(2*idx)], 'Min '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.lowers[client][0])
                #Maximum value in parameter space 'client'
                self.a2max = Slider(Sax[int(2*idx)+1], 'Max '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.uppers[client][0])

                #Reset button for minimum slider
                l = Sax[int(2*idx)].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a2minres = Button(tax, 'Reset '+client+' Min', color=axcolor, hovercolor='0.7')
                #Reset button for maximum slider
                l = Sax[int(2*idx)+1].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a2maxres = Button(tax, 'Reset '+client+' Max', color=axcolor, hovercolor='0.7')

                #Update commands for the widgets
                self.a2min.on_changed(haircut.update)
                self.a2max.on_changed(haircut.update)
                self.a2minres.on_clicked(barbicide.a2min)
                self.a2maxres.on_clicked(barbicide.a2max)

            if (self.clients >= 3) & (idx == 2):
                #Maximum value in parameter space 'client'
                self.a3min = Slider(Sax[int(2*idx)], 'Min '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.lowers[client][0])
                #Minimum value in parameter space 'client'
                self.a3max = Slider(Sax[int(2*idx)+1], 'Max '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.uppers[client][0])

                #Reset button for minimum slider
                l = Sax[int(2*idx)].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a3minres = Button(tax, 'Reset '+client+' Min', color=axcolor, hovercolor='0.7')
                #Reset button for maximum slider
                l = Sax[int(2*idx)+1].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a3maxres = Button(tax, 'Reset '+client+' Max', color=axcolor, hovercolor='0.7')

                #Update commands for the widgets
                self.a3min.on_changed(haircut.update)
                self.a3max.on_changed(haircut.update)
                self.a3minres.on_clicked(barbicide.a3min)
                self.a3maxres.on_clicked(barbicide.a3max)

            if (self.clients >= 4) & (idx == 3):
                #Maximum value in parameter space 'client'
                self.a4min = Slider(Sax[int(2*idx)], 'Min '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.lowers[client][0])
                #Minimum value in parameter space 'client'
                self.a4max = Slider(Sax[int(2*idx)+1], 'Max '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.uppers[client][0])

                #Reset button for minimum slider
                l = Sax[int(2*idx)].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a4minres = Button(tax, 'Reset '+client+' Min', color=axcolor, hovercolor='0.7')
                #Reset button for maximum slider
                l = Sax[int(2*idx)+1].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a4maxres = Button(tax, 'Reset '+client+' Max', color=axcolor, hovercolor='0.7')

                #Update commands for the widgets
                self.a4min.on_changed(haircut.update)
                self.a4max.on_changed(haircut.update)
                self.a4minres.on_clicked(barbicide.a4min)
                self.a4maxres.on_clicked(barbicide.a4max)

            if (self.clients == 5) & (idx == 4):
                #Maximum value in parameter space 'client'
                self.a5min = Slider(Sax[int(2*idx)], 'Min '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.lowers[client][0])
                #Minimum value in parameter space 'client'
                self.a5max = Slider(Sax[int(2*idx)+1], 'Max '+client,\
                                np.nanmin(self.seating[client]),\
                                np.nanmax(self.seating[client]),\
                                valinit = self.uppers[client][0])

                #Reset button for minimum slider
                l = Sax[int(2*idx)].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a5minres = Button(tax, 'Reset '+client+' Min', color=axcolor, hovercolor='0.7')
                #Reset button for maximum slider
                l = Sax[int(2*idx)+1].get_position()
                tax = plt.axes([l.x0+l.width+0.08, l.y0, 0.18, l.height])
                self.a5maxres = Button(tax, 'Reset '+client+' Max', color=axcolor, hovercolor='0.7')

                #Update commands for the widgets
                self.a5min.on_changed(haircut.update)
                self.a5max.on_changed(haircut.update)
                self.a5minres.on_clicked(barbicide.a5min)
                self.a5maxres.on_clicked(barbicide.a5max)

        #Build the Save, Close Plots, Reset All commands
        y0 = (Sax[-1].get_position().y0) - (Sax[0].get_position().y0 - Sax[1].get_position().y0)
        tax = plt.axes([l.x0, y0, (l.width-0.05)/2, l.height])
        self.savebut = Button(tax, 'Save Cuts', color=axcolor, hovercolor='green')
        self.savebut.on_clicked(haircut.save)

        tax = plt.axes([l.x0+(l.width-0.05)/2+0.05, y0, (l.width-0.05)/2, l.height])
        self.closebut = Button(tax, 'Close Plots', color=axcolor, hovercolor='red')
        self.closebut.on_clicked(barbicide.plots)

        tax = plt.axes([l.x0+l.width+0.08, y0, 0.18, l.height])
        self.resetbut = Button(tax, 'Reset All', color=axcolor, hovercolor='orange')
        self.resetbut.on_clicked(barbicide.all)

        plt.show()

    def get_shells(self):
        '''
        Simple class that returns N empty figures where N is the number of
        variables added using the add_client() function.
        '''
        if self.clients == 0:
            print('Please add at least one client variable.')
            return None

        if self.clients == 1:
            f1, a1 = plt.subplots()
            return [f1], [a1]

        if self.clients == 2:
            f1, a1 = plt.subplots()
            f2, a2 = plt.subplots()
            return (f1, f2), (a1, a2)

        if self.clients == 3:
            f1, a1 = plt.subplots()
            f2, a2 = plt.subplots()
            f3, a3 = plt.subplots()
            return (f1, f2, f3), (a1, a2, a3)

        if self.clients == 4:
            f1, a1 = plt.subplots()
            f2, a2 = plt.subplots()
            f3, a3 = plt.subplots()
            f4, a4 = plt.subplots()
            return (f1, f2, f3, f4), (a1, a2, a3, a4)

        if self.clients == 5:
            f1, a1 = plt.subplots()
            f2, a2 = plt.subplots()
            f3, a3 = plt.subplots()
            f4, a4 = plt.subplots()
            f5, a5 = plt.subplots()
            return (f1, f2, f3, f4, f5), (a1, a2, a3, a4, a5)

    def shave(self, lower, upper):
        '''
        A function that takes the full data array 'self.odf' and applies cuts
        according to the values fed in.

        Parameters:
            lower (pandas.core.frame.DataFrame): A pandas Dataframe containing
                the lower boundary of the cut in each parameter space.

            upper (pandas.core.frame.DataFrame): A pandas Dataframe containing
                the upper boundary of the cut in each parameter space.

        Returns:
            pandas.core.frame.DataFrame: A pandas Dataframe containing the now
                cut data for all parameter spaces.

        '''
        dff = self.seating[:]
        #Apply cuts cyclicly for every client
        for client in list(self.lowers):
            dff = dff[dff[client] >= lower[client][0]]
            dff = dff[dff[client] <= upper[client][0]]
        return dff

    def check_seating(self):
        print('Number of seats in use : '+str(self.clients)+'/5:')
        print(list(self.lowers))

    def give_savelocs(self, floc='dataframe_cut.csv', cloc='cuts.csv'):
        '''
        A function to be called by the user to feed in custom locations to save
        the output of the module.

        Parameters:
            floc (str): Default 'dataframe_cut.csv'. The output location of the
                cut version of the DataFrame fed into barbershop.open().

            cloc (str): Default 'cuts.csv'. The output location of the list of
                cuts made to the data.
        '''
        self.floc = floc
        self.cloc = cloc
