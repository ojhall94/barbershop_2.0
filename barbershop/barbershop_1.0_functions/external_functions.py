#!/bin/env python
# -*- coding: utf-8 -*-

"""
A collection of functions to work in conjunction with __init__.open(), used for
the button functions.

.. versioncreated:: 1.0

.. codeauthor:: Oliver James Hall <ojh251@student.bham.ac.uk>
"""

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

class barbicideclass:
    def __init__(self, _barber):
        self.barber = _barber

    def all(self, event):
        try:
            self.barber.a1min.reset()
            self.barber.a1max.reset()
        except AttributeError:
            pass
        try:
            self.barber.a2min.reset()
            self.barber.a2max.reset()
        except AttributeError:
            pass
        try:
            self.barber.a3min.reset()
            self.barber.a3max.reset()
        except AttributeError:
            pass
        try:
            self.barber.a4min.reset()
            self.barber.a4max.reset()
        except AttributeError:
            pass
        try:
            self.barber.a5min.reset()
            self.barber.a5max.reset()
        except AttributeError:
            pass

    def a1min(self, event):
        self.barber.a1min.reset()

    def a1max(self, event):
        self.barber.a1max.reset()

    def a2min(self, event):
        self.barber.a2min.reset()

    def a2max(self, event):
        self.barber.a2max.reset()

    def a3min(self, event):
        self.barber.a3min.reset()

    def a3max(self, event):
        self.barber.a3max.reset()

    def a4min(self, event):
        self.barber.a4min.reset()

    def a4max(self, event):
        self.barber.a4max.reset()

    def a5min(self, event):
        self.barber.a5min.reset()

    def a5max(self, event):
        self.barber.a5max.reset()

    def plots(self, event):
        plt.close('all')

class haircutclass:
    def __init__(self, _barber):
        self.barber = _barber

    def update(self, val):
        #Define cut dataframes
        lower = pd.DataFrame()
        upper = pd.DataFrame()

        #Append the slider cut values into this local dataframe
        for idx, client in enumerate(list(self.barber.lowers)):
            if (self.barber.clients >= 1) & (idx == 0):
                lower[client] = [self.barber.a1min.val]
                upper[client] = [self.barber.a1max.val]

            if (self.barber.clients >= 2) & (idx == 1):
                lower[client] = [self.barber.a2min.val]
                upper[client] = [self.barber.a2max.val]

            if (self.barber.clients >= 3) & (idx == 2):
                lower[client] = [self.barber.a3min.val]
                upper[client] = [self.barber.a3max.val]

            if (self.barber.clients >= 4) & (idx == 3):
                lower[client] = [self.barber.a4min.val]
                upper[client] = [self.barber.a4max.val]

            if (self.barber.clients == 5) & (idx == 4):
                lower[client] = [self.barber.a5min.val]
                upper[client] = [self.barber.a5max.val]

        #Get new, cut dataset
        dff = self.barber.shave(lower, upper)

        #Prep the data for update
        uu = np.vstack((dff[self.barber.namex].values, dff[self.barber.namey].values))

        #Update all the axes and colourbars
        for idx, client in enumerate(list(self.barber.lowers)):
            self.barber.axes[idx].collections[0].set_offsets(uu.T)
            self.barber.axes[idx].collections[0].set_array(dff[client])
            try:
                self.barber.axes[idx].collections[0].set_clim([np.nanmin(dff[client]),np.nanmax(dff[client])])
            except ValueError:
                pass
            self.barber.figs[idx].canvas.draw_idle()

        #Update the histograms
        get_histograms(self.barber, dff)

    def save(self, event):
        #Define cut dataframes
        lower = pd.DataFrame()
        upper = pd.DataFrame()

        #Append the slider cut values into this local dataframe
        for idx, client in enumerate(list(self.barber.lowers)):
            if (self.barber.clients >= 1) & (idx == 0):
                lower[client] = [self.barber.a1min.val]
                upper[client] = [self.barber.a1max.val]

            if (self.barber.clients >= 2) & (idx == 1):
                lower[client] = [self.barber.a2min.val]
                upper[client] = [self.barber.a2max.val]

            if (self.barber.clients >= 3) & (idx == 2):
                lower[client] = [self.barber.a3min.val]
                upper[client] = [self.barber.a3max.val]

            if (self.barber.clients >= 4) & (idx == 3):
                lower[client] = [self.barber.a4min.val]
                upper[client] = [self.barber.a4max.val]

            if (self.barber.clients == 5) & (idx == 4):
                lower[client] = [self.barber.a5min.val]
                upper[client] = [self.barber.a5max.val]

        out = self.barber.core_df[:]
        #Save out a cut verison of the original dataframe
        for client in list(self.barber.lowers):
            out = out[out[client] >= lower[client][0]]
            out = out[out[client] <= upper[client][0]]
        out.to_csv(self.barber.floc,header=True,sep=' ')

        #Save out the cuts if the user wants to apply them again
        cut = pd.concat([lower, upper])
        cut.index = ['lower','upper']
        cut.to_csv(self.barber.cloc,header=True,sep=' ')

        plt.close('all')

def get_histograms(barber, dff):
    uu = np.vstack((dff[barber.namex].values, dff[barber.namey].values))

    # #Update histograms, if they exist
    if any([barber.hist_x_on, barber.hist_y_on]):
        if not all([barber.hist_x_on, barber.hist_y_on]):
            #If only one histogram is turned on
            barber.Hax.cla()
            if barber.hist_x_on:
                #Plot original line in red
                barber.Hax.hist(\
                    barber.shave(barber.lowers, barber.uppers)[barber.namex],\
                    histtype='step', color='r', bins='sqrt', label='Initial Cut')
                barber.Hax.set_ylabel('Counts')
                barber.Hax.set_xlabel(barber.namex)
                #Plot updated histogram with same bins
                barber.Hax.hist(uu[0], histtype='step', color='k', bins=barber.bins, label='Post-Cuts')
            else:
                #Plot original line in red
                barber.Hax.hist(\
                    barber.shave(barber.lowers, barber.uppers)[barber.namey],\
                    histtype='step', color='r', bins='sqrt', label='Initial Cut')
                barber.Hax.set_ylabel('Counts')
                barber.Hax.set_xlabel(barber.namey)
                #Plot updated histogram with same bins
                barber.Hax.hist(uu[1], histtype='step', color='k', bins=barber.bins, label='Post-Cuts')
            barber.Hax.legend(loc='best',fancybox=True)
        else:
            #If both histograms are turned on
            barber.Hax[0].cla()
            barber.Hax[1].cla()
            #Plot original line in red
            barber.Hax[0].hist(\
                barber.shave(barber.lowers, barber.uppers)[barber.namex],\
                histtype='step', color='r', bins='sqrt', label='Initial Cut')
            barber.Hax[1].hist(\
                barber.shave(barber.lowers, barber.uppers)[barber.namey],\
                histtype='step', color='r', bins='sqrt', label='Initial Cut')
            #Plot updated histograms with same bins
            barber.Hax[0].hist(uu[0],\
                    histtype='step', color='k', bins='sqrt')
            barber.Hax[1].hist(uu[1],\
                    histtype='step', color='k', bins='sqrt')
            barber.Hax[0].set_ylabel('Counts')
            barber.Hax[0].set_xlabel(barber.namex)
            barber.Hax[1].set_ylabel('Counts')
            barber.Hax[1].set_xlabel(barber.namey)
            barber.Hax[0].legend(loc='best', fancybox=True)
            barber.Hax[1].legend(loc='best', fancybox=True)

        barber.Hfig.suptitle('Histograms of the data. Pre-cuts shown in red.')
        barber.Hfig.tight_layout(rect=[0, 0.03, 1, 0.95])

        barber.Hfig.canvas.draw_idle()

def quartet():
    import webbrowser
    url = 'https://www.youtube.com/watch?v=VNUgsbKisp8'

    try:
        webbrowser.get(using='google-chrome').open(url, new=2)
    except:
        try:
            webbrowser.get(using='firefox').open(url, new=2)
        except:
            pass
