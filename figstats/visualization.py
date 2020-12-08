from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as m_dates


def matplotlib_date_format(date_list):
    """Generate list of datetime objects"""
    datetime_list = [dt.strptime(date, '%Y-%m-%d') for date in date_list]

    return datetime_list


def plot_shares(ax, timeline_dict):
    shares_dict = timeline_dict['shares']
    non_zero = [key for key in shares_dict.keys() if shares_dict[key] > 0]

    if len(non_zero) > 0:
        dates = matplotlib_date_format(non_zero)
        for date, key in zip(dates, non_zero):
            ax.axvline(x=date, color='red')
            ax.text(date, 10, f"{shares_dict[key]}", color='red')


def plot_timeline(timeline_dict, article_dict, out_pdf=None, save=False):
    """
    Purpose:
      Plot timeline showing views and downloads

    :param timeline_dict: dict containing daily and cumulative numbers.
           From stats.Figshare.get_timeline
    :param article_dict: dictionary of article details.
           From stats.Figshare.retrieve_article_details
    :param out_pdf: Output filename. Default: timeline_<article_id>.pdf
    :param save: bool to save PDF file. Otherwise return matplotlib fig object

    :return fig: If save == False, fig is returned
    """
    datetime_list = matplotlib_date_format(list(timeline_dict['views'].keys()))
    fig, [ax0, ax1] = plt.subplots(ncols=2, nrows=2,
                                   gridspec_kw={'height_ratios': [3, 1]})

    counters = ['views', 'downloads']

    for ii, counter in zip(range(len(counters)), counters):

        # Bottom panels
        y_bottom = timeline_dict[counter].values()
        ax1[ii].bar(datetime_list, y_bottom)
        locator = m_dates.AutoDateLocator(minticks=3, maxticks=7)
        formatter = m_dates.ConciseDateFormatter(locator)
        ax1[ii].xaxis.set_major_locator(locator)
        ax1[ii].xaxis.set_major_formatter(formatter)
        ax1[ii].set_ylabel(f"Daily {counter}")
        ax1[ii].tick_params(axis='y', direction='in')
        ax1[ii].tick_params(axis='x', direction='out')
        ax1[ii].annotate(f'Maximum daily {counter}: {max(y_bottom)}',
                         (0.025, 0.95), xycoords='axes fraction',
                         va='top', ha='left')

        # Top panels
        y_top = timeline_dict[counter+'-cum'].values()
        ax0[ii].bar(datetime_list, y_top)
        ax0[ii].xaxis.set_major_locator(locator)
        ax0[ii].xaxis.set_major_formatter(formatter)
        ax0[ii].set_xticklabels('')
        ax0[ii].set_ylabel(f"Cumulative {counter}")
        ax0[ii].tick_params(axis='both', direction='in')
        ax0[ii].annotate(f'Total {counter}: {max(y_top)}', (0.025, 0.975),
                         xycoords='axes fraction', va='top', ha='left')
        # ax0[ii].set_xlabel('Date')

        plot_shares(ax0[ii], timeline_dict)

    # Heading containing title, author, license, DOI
    heading = f"Title: {article_dict['title']}\n"
    author_list = [auth_dict['full_name'] for auth_dict in article_dict['authors']]
    if len(author_list) > 3:
        heading += f"Authors: {author_list[0]} et al.\n"
    else:
        heading += f"Authors: {' '.join(author_list)}\n"
    heading += f"License: {article_dict['license']['name']}  "
    heading += f"DOI: https://doi.org/{article_dict['doi']}"
    ax0[0].text(0.01, 1.15, heading, ha='left', va='top',
                transform=ax0[0].transAxes)

    fig.set_size_inches(8, 6)
    plt.subplots_adjust(left=0.09, bottom=0.1, top=0.90, right=0.985,
                        hspace=0.025)

    if save:
        if isinstance(out_pdf, type(None)):
            out_pdf = f"timeline_{article_dict['id']}.pdf"
        fig.savefig(out_pdf)
    else:
        return fig
