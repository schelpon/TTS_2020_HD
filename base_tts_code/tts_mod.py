# A python module for obtaining the greens function and other tts related outputs 
# needs inputs: 
    # tau - lifetime in days 
    # utbl - ratios as an arrays, 'truth' values
# to get tts outputs run the following: 
    # t, exp_decay_matrix, LT = tts_mod.prep_for_tts(tau)
    # my_mustar, my_r2, my_gf, my_t, mean_age, mode_age = tts_mod.get_tts(utbl, tau, t, exp_decay_matrix, LT)
# no need to call my_greens_func explicitylly, nested in get_tts
# outputs: 
    #  my_mustar - modeled ratios 
    #  my_r2 - r^2 value of utbl to mu* fit 
    # my_gf - greens function (y)
    # my_t - x axis for greens function, in days 
    # mean_age, mode_age - mean and modal ages for the TTS, in days 

import numpy as np 
from scipy.signal import find_peaks
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt

def prep_for_tts(tau):
    LT = (tau)*86400
    time1 = LT[0]
    time2 = LT[-1]+1
    interval = 86400/4 
    t = np.arange(time1, time2, interval)
    exp_decay_matrix = np.empty((len(LT), len(t)))
    for ii, tt in enumerate(LT):
        exp_decay_matrix[ii] = np.exp(-t/tt)
    return t, exp_decay_matrix, LT

def my_greens_func(k_coef, t, exp_decay_matrix, LT):
    z = 1.3e4 
    H = 7.64e3 
    a = z/(2*np.sqrt(np.pi*k_coef*(t**3)))
    b = (z/(2*H))-((k_coef*t)/(4*(H**2)))-((z**2)/(4*k_coef*t))
    my_gf = a*np.exp(b)
    mu_star_matrix = np.empty((len(LT), len(t)))
    my_mu_star = np.empty((len(LT), 1))
    for ii, tt in enumerate(LT):
        mu_star_matrix[ii] = exp_decay_matrix[ii]*my_gf    
        my_mu_star[ii] = np.trapz(mu_star_matrix[ii], t)
    return my_gf, my_mu_star

def get_tts(utbl, tau, t, exp_decay_matrix, LT):
    k_coef = 1 
    #k_plus = 5
    k_plus = 1 
    MSE_prev = 1000
    MSE_now = 999
    while (MSE_prev > MSE_now):
        out = my_greens_func(k_coef, t, exp_decay_matrix, LT)
        this_mustar = out[1]
        MSE_prev = MSE_now
        MSE_now = mean_squared_error(utbl, this_mustar)
        k_coef = k_coef+k_plus
    best_k = k_coef-(2*k_plus)
    out = my_greens_func(best_k, t, exp_decay_matrix, LT)
    my_gf = out[0]
    my_t = t/86400
    my_mustar = out[1]
    my_r2 = r2_score(utbl, my_mustar)
    peaks, _ = find_peaks(my_gf)
    if (len(peaks) == 0):
        mode_age = -999
    else:
        mode_age = t[peaks[0]]/86400
    mean_age = np.trapz(my_gf*t, t)/86400
    #return my_mustar, my_r2, my_gf, my_t, mean_age, mode_age
    return my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k

def plot_tts(tau, my_mustar, utbl, my_r2, my_gf, my_t, mean_age, mode_age, 
             my_color, overplot, add_scatter, add_r2, add_meanmode, my_ax, width, height, title_str):
    # ----- make axes if first plot, overplot = 0 
    if (overplot == 0):
        # get axes 
        fig, my_ax = plt.subplots(figsize=(14, 4), ncols=2)
        ax0, ax1 = my_ax
        # ax 1 labels
        ax0.set_title(r'a) $\mu^* - \tau$', fontsize = 20)
        ax0.set_xlabel(r'$\tau$ [day]', fontsize = 15)
        ax0.set_ylabel(r'$\mu^*$', fontsize = 15)
        # ax 2 labels
        ax1.set_title('b) Transit Time Spectrum', fontsize = 20)
        ax1.set_ylabel('G(t)', fontsize = 15)
        ax1.set_xlabel('Transit Time [days]', fontsize = 15)
        # squeeze
        plt.tight_layout()
        # get figure pixel height
        bbox = ax0.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width, height = bbox.width, bbox.height
        height *= fig.dpi
        width *= fig.dpi
    else: 
        ax0, ax1 = my_ax
    # ----- my mu star 
    ax0.plot(tau, my_mustar, color = my_color, linewidth = 3, zorder = 1)
    if (add_scatter == 1):
        if (my_color == 'k'):
            a = 0.3
            ax0.scatter(tau, utbl, color = my_color, marker = 's', alpha = a, zorder = 2)
        else: 
            ax0.scatter(tau, utbl, color = my_color, marker = 's', alpha = 0.5, zorder = 2)
    ax0.set_xscale('log')
    ax0.grid(which = 'major')
    ax0.set_ylim([0, 1.2])
    ax0.set_xlim([10**-1, 10**5])
    ax0.tick_params(axis='both', labelsize=15)
    # add r^2 value text, position based on overplot number 
    if (overplot == 0):
        #yloc0 = height*0.5
        yloc0 = height*0.8
    else:
       #yloc0 = (height*0.5) - (overplot*height*0.1)
        yloc0 = (height*0.8) - (overplot*height*0.1)
    if (add_r2 == 1):
        rstr = title_str + r'$R^2$ = '+ str(round(my_r2, 2))
        ax0.annotate(rstr, xy=((width*1.13), yloc0), xycoords='figure pixels', 
                    horizontalalignment='right', color = my_color, size=15)
    # ----- tts  
    ax1.plot(my_t, my_gf, color = my_color, linewidth = 3)
    ax1.set_xlim([0, 30])
    ax1.set_xticks(np.arange(0, 35, step=5))
    ax1.grid(which = 'major')
    ax1.tick_params(axis='both', labelsize=15)
    # get figure pixel height
    #bbox = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    #width, height = bbox.width, bbox.height
    #height *= fig.dpi
    #width *= fig.dpi
    # add r^2 value text, position based on overplot number 
    if (overplot == 0):
        yloc1 = height*1.1
    else:
        yloc1 = (height*1.1) - (overplot*height*0.1)
    # add mean and mode 
    if (mode_age == -999):
        mmstr = 'Mean = ' + str(round(mean_age, 1))+', Mode = <1 day'
    else: 
        mmstr = 'Mean = ' + str(round(mean_age, 1))+', Mode = ' +str(round(mode_age, 1))+' days'
    if (add_meanmode == 1):   
        ax1.annotate(mmstr, xy=((width*2.27), yloc1), xycoords='figure pixels', 
                    horizontalalignment='right', color = my_color, size=15)
    plt.ticklabel_format(axis = 'y', style = 'sci', scilimits=(-2,2))
    ax1.yaxis.offsetText.set_fontsize(15)
    if (overplot == 0):
        return fig, my_ax, width, height
