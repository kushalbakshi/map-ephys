
import numpy as np

import matplotlib.pyplot as plt
from pipeline import psth, experiment, ephys
from pipeline.plot.util import _get_trial_event_times

# from pipeline.psth import TrialCondition
# from pipeline.psth import UnitPsth

_plt_xlim = [-3, 2]


def _plot_spike_raster(ipsi, contra, vlines=[], shade_bar=None, ax=None, title='', xlim=_plt_xlim):
    if not ax:
        fig, ax = plt.subplots(1, 1)

    ipsi_tr = ipsi['raster'][1]
    for i, tr in enumerate(set(ipsi['raster'][1])):
        ipsi_tr = np.where(ipsi['raster'][1] == tr, i, ipsi_tr)

    contra_tr = contra['raster'][1]
    for i, tr in enumerate(set(contra['raster'][1])):
        contra_tr = np.where(contra['raster'][1] == tr, i, contra_tr)

    ax.plot(ipsi['raster'][0], ipsi_tr, 'r.', markersize=1)
    ax.plot(contra['raster'][0], contra_tr + ipsi_tr.max() + 1, 'b.', markersize=1)

    for x in vlines:
        ax.axvline(x=x, linestyle='--', color='k')
    if shade_bar is not None:
        ax.axvspan(shade_bar[0], shade_bar[0] + shade_bar[1], alpha=0.3, color='royalblue')

    ax.set_axis_off()
    ax.set_xlim(xlim)
    ax.set_title(title)


def _plot_psth(ipsi, contra, vlines=[], shade_bar=None, ax=None, title='', xlim=_plt_xlim):
    if not ax:
        fig, ax = plt.subplots(1, 1)

    ax.plot(contra['psth'][1], contra['psth'][0], 'b')
    ax.plot(ipsi['psth'][1], ipsi['psth'][0], 'r')

    for x in vlines:
        ax.axvline(x=x, linestyle='--', color='k')
    if shade_bar is not None:
        ax.axvspan(shade_bar[0], shade_bar[0] + shade_bar[1], alpha=0.3, color='royalblue')

    ax.set_ylabel('spikes/s')
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_xlim(xlim)
    ax.set_xlabel('Time (s)')
    ax.set_title(title)

#
# def unit_psth_ll(ipsi_hit, contra_hit, ipsi_err, contra_err):
#     max_trial_off = 500
#
#     plt_xmin = -3
#     plt_xmax = 3
#     plt_ymin = 0
#     plt_ymax = None  # dynamic per unit
#
#     plt_ymax = np.max([contra_hit['psth'][0],
#                        ipsi_hit['psth'][0],
#                        contra_err['psth'][0],
#                        ipsi_err['psth'][0]])
#
#     plt.figure()
#
#     # raster plot
#     ax = plt.subplot(411)
#     plt.plot(contra_hit['raster'][0], contra_hit['raster'][1] + max_trial_off,
#              'b.', markersize=1)
#     plt.plot(ipsi_hit['raster'][0], ipsi_hit['raster'][1], 'r.', markersize=1)
#     ax.set_axis_off()
#     ax.set_xlim([plt_xmin, plt_xmax])
#     ax.axvline(0, 0, 1, ls='--')
#     ax.axvline(-1.2, 0, 1, ls='--')
#     ax.axvline(-2.4, 0, 1, ls='--')
#
#     # histogram of hits
#     ax = plt.subplot(412)
#     plt.plot(contra_hit['psth'][1][1:], contra_hit['psth'][0], 'b')
#     plt.plot(ipsi_hit['psth'][1][1:], ipsi_hit['psth'][0], 'r')
#
#     plt.ylabel('spikes/s')
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     ax.set_xlim([plt_xmin, plt_xmax])
#     ax.set_ylim([plt_ymin, plt_ymax])
#     ax.set_xticklabels([])
#     ax.axvline(0, 0, 1, ls='--')
#     ax.axvline(-1.2, 0, 1, ls='--')
#     ax.axvline(-2.4, 0, 1, ls='--')
#     plt.title('Correct trials')
#
#     # histogram of errors
#     ax = plt.subplot(413)
#     plt.plot(contra_err['psth'][1][1:], contra_err['psth'][0], 'b')
#     plt.plot(ipsi_err['psth'][1][1:], ipsi_err['psth'][0], 'r')
#
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     ax.set_xlim([plt_xmin, plt_xmax])
#     ax.set_ylim([plt_ymin, plt_ymax])
#     ax.axvline(0, 0, 1, ls='--')
#     ax.axvline(-1.2, 0, 1, ls='--')
#     ax.axvline(-2.4, 0, 1, ls='--')
#
#     plt.title('Error trials')
#     plt.xlabel('Time to go cue (s)')
#     plt.show()


# def unit_psth(unit_key):
#     """
#     Plot a per-unit PSTH diagram
#     """
#
#     ipsi_hit_cond_key = (TrialCondition
#                          & {'trial_condition_name':
#                             'good_noearlylick_left_hit'}).fetch1('KEY')
#
#     contra_hit_cond_key = (TrialCondition
#                            & {'trial_condition_name':
#                               'good_noearlylick_right_hit'}).fetch1('KEY')
#
#     ipsi_miss_cond_key = (TrialCondition
#                           & {'trial_condition_name':
#                              'good_noearlylick_left_miss'}).fetch1('KEY')
#
#     contra_miss_cond_key = (TrialCondition
#                             & {'trial_condition_name':
#                                'good_noearlylick_right_miss'}).fetch1('KEY')
#
#     ipsi_hit_unit_psth = UnitPsth.get_plotting_data(
#         unit_key, ipsi_hit_cond_key)
#
#     contra_hit_unit_psth = UnitPsth.get_plotting_data(
#         unit_key, contra_hit_cond_key)
#
#     ipsi_miss_unit_psth = UnitPsth.get_plotting_data(
#         unit_key, ipsi_miss_cond_key)
#
#     contra_miss_unit_psth = UnitPsth.get_plotting_data(
#         unit_key, contra_miss_cond_key)
#
#     unit_psth_ll(ipsi_hit_unit_psth, contra_hit_unit_psth,
#                  ipsi_miss_unit_psth, contra_miss_unit_psth)


def plot_unit_psth(unit_key, axs=None, title='', xlim=_plt_xlim):
    """
    Default raster and PSTH plot for a specified unit - only {good, no early lick, correct trials} selected
    condition_name_kw: list of keywords to match for the TrialCondition name
    """

    hemi = (ephys.ProbeInsertion.InsertionLocation
            * experiment.BrainLocation & unit_key).fetch1('hemisphere')

    ipsi_hit_unit_psth = psth.UnitPsth.get_plotting_data(
        unit_key, {'trial_condition_name': f'good_noearlylick_{"left" if hemi == "left" else "right"}_hit'})

    contra_hit_unit_psth = psth.UnitPsth.get_plotting_data(
        unit_key, {'trial_condition_name':  f'good_noearlylick_{"right" if hemi == "left" else "left"}_hit'})

    ipsi_miss_unit_psth = psth.UnitPsth.get_plotting_data(
        unit_key, {'trial_condition_name': f'good_noearlylick_{"left" if hemi == "left" else "right"}_miss'})

    contra_miss_unit_psth = psth.UnitPsth.get_plotting_data(
        unit_key, {'trial_condition_name':  f'good_noearlylick_{"right" if hemi == "left" else "left"}_miss'})


    # get event start times: sample, delay, response
    periods, period_starts = _get_trial_event_times(['sample', 'delay', 'go'], unit_key, 'good_noearlylick_hit')

    fig = None
    if axs is None:
        fig, axs = plt.subplots(2, 2)

    # correct response
    _plot_spike_raster(ipsi_hit_unit_psth, contra_hit_unit_psth, ax=axs[0, 0],
                       vlines=period_starts,
                       title=title if title else f'Unit #: {unit_key["unit"]}\nCorrect Response', xlim=xlim)
    _plot_psth(ipsi_hit_unit_psth, contra_hit_unit_psth,
               vlines=period_starts, ax=axs[1, 0], xlim=xlim)

    # incorrect response
    _plot_spike_raster(ipsi_miss_unit_psth, contra_miss_unit_psth, ax=axs[0, 1],
                       vlines=period_starts,
                       title=title if title else f'Unit #: {unit_key["unit"]}\nIncorrect Response', xlim=xlim)
    _plot_psth(ipsi_miss_unit_psth, contra_miss_unit_psth,
               vlines=period_starts, ax=axs[1, 1], xlim=xlim)

    return fig
