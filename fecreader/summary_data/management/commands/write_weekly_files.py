# write some files 

import csv 

from datetime import datetime, date

from django.conf import settings
from django.db.models import Sum
from django.core.management.base import BaseCommand, CommandError


from formdata.models import SkedE
from summary_data.models import Committee_Overlay
from datetime import date
from summary_data.utils.weekly_update_utils import get_week_number, get_week_end, summarize_week_queryset

CHART_CSV_DOWNLOAD_DIR = settings.CHART_CSV_DOWNLOAD_DIR
CSV_FILE_NAME = 'weekly_ies.csv'


data_start = date(2013,1,1)


def make_header(start_week_number, end_week_number):
    headers = ['data_id','data_series_name']
    for week in range(start_week_number, end_week_number + 1):
        headers.append(get_week_end(week).strftime("%m/%d/%Y"))
    return headers


## some queries to help define sets
all_ies = SkedE.objects.filter(superceded_by_amendment=False)

all_outside_groups = Committee_Overlay.objects.filter(total_indy_expenditures__gt=0)
dem_id_list = [i.fec_id for i in all_outside_groups.filter(political_orientation='D')]
rep_id_list = [i.fec_id for i in all_outside_groups.filter(political_orientation='R')]


noncommittees = Committee_Overlay.objects.filter(ctype__in=['I'], total_indy_expenditures__gt=0)
noncommittee_id_list = [i.fec_id for i in noncommittees]
dem_noncommittee_id_list = [i.fec_id for i in noncommittees.filter(political_orientation='D')]
rep_noncommittee_id_list = [i.fec_id for i in noncommittees.filter(political_orientation='R')]


superpacs = Committee_Overlay.objects.filter(ctype__in=['U', 'O'], total_indy_expenditures__gt=0)
superpac_id_list = [i.fec_id for i in superpacs]
dem_superpac_id_list = [i.fec_id for i in superpacs.filter(political_orientation='D')]
rep_superpac_id_list = [i.fec_id for i in superpacs.filter(political_orientation='R')]

party_committees = Committee_Overlay.objects.filter(ctype__in=['X', 'Y', 'Z'], total_indy_expenditures__gt=0)
party_committee_id_list = [i.fec_id for i in party_committees]
dem_party_committee_id_list = [i.fec_id for i in party_committees.filter(political_orientation='D')]
rep_party_committee_id_list = [i.fec_id for i in party_committees.filter(political_orientation='R')]

data_series = [
    {'data_id':1,'data_series_name':'All Independent Expenditures', 'q':all_ies},
    {'data_id':2,'data_series_name':'Dark Money', 'q':all_ies.filter(filer_committee_id_number__in=noncommittee_id_list)},
    {'data_id':3,'data_series_name':'Super PACs', 'q':all_ies.filter(filer_committee_id_number__in=superpac_id_list)},
    {'data_id':4,'data_series_name':'Party Committees', 'q':all_ies.filter(filer_committee_id_number__in=party_committee_id_list)},
    
    {'data_id':5,'data_series_name':'All Democratic Independent Expenditures', 'q':all_ies.filter(filer_committee_id_number__in=dem_id_list)},
    {'data_id':6,'data_series_name':'All Republican Independent Expenditures', 'q':all_ies.filter(filer_committee_id_number__in=rep_id_list)},
    
    {'data_id':7,'data_series_name':'Democratic Dark Money', 'q':all_ies.filter(filer_committee_id_number__in=dem_noncommittee_id_list)},
    {'data_id':8,'data_series_name':'Republican Dark Money', 'q':all_ies.filter(filer_committee_id_number__in=rep_noncommittee_id_list)},
    
    {'data_id':9,'data_series_name':'Democratic Super PACs', 'q':all_ies.filter(filer_committee_id_number__in=dem_superpac_id_list)},
    {'data_id':10,'data_series_name':'Republican Super PACs', 'q':all_ies.filter(filer_committee_id_number__in=rep_superpac_id_list)},

    {'data_id':11,'data_series_name':'Republican Party Committees', 'q':all_ies.filter(filer_committee_id_number__in=rep_party_committee_id_list)},
    {'data_id':12,'data_series_name':'Democratic Party Committees', 'q':all_ies.filter(filer_committee_id_number__in=dem_party_committee_id_list)},

    {'data_id':13,'data_series_name':'Democratic IE Senate', 'q':all_ies.filter(filer_committee_id_number__in=dem_id_list, candidate_office_checked='S')},
    {'data_id':14,'data_series_name':'Republican IE Senate', 'q':all_ies.filter(filer_committee_id_number__in=rep_id_list, candidate_office_checked='S')},
    {'data_id':15,'data_series_name':'Democratic IE House', 'q':all_ies.filter(filer_committee_id_number__in=dem_id_list, candidate_office_checked='H')},
    {'data_id':16,'data_series_name':'Republican IE House', 'q':all_ies.filter(filer_committee_id_number__in=rep_id_list, candidate_office_checked='H')},
    
    {'data_id':13,'data_series_name':'Democratic Super PAC Senate', 'q':all_ies.filter(filer_committee_id_number__in=dem_superpac_id_list, candidate_office_checked='S')},
    {'data_id':14,'data_series_name':'Republican Super PAC Senate', 'q':all_ies.filter(filer_committee_id_number__in=rep_superpac_id_list, candidate_office_checked='S')},
    {'data_id':15,'data_series_name':'Democratic Super PAC House', 'q':all_ies.filter(filer_committee_id_number__in=dem_superpac_id_list, candidate_office_checked='H')},
    {'data_id':16,'data_series_name':'Republican Super PAC House', 'q':all_ies.filter(filer_committee_id_number__in=rep_superpac_id_list, candidate_office_checked='H')},
    
    {'data_id':17,'data_series_name':'Democratic Dark Money Senate', 'q':all_ies.filter(filer_committee_id_number__in=dem_noncommittee_id_list, candidate_office_checked='S')},
    {'data_id':18,'data_series_name':'Republican Dark Money Senate', 'q':all_ies.filter(filer_committee_id_number__in=rep_noncommittee_id_list, candidate_office_checked='S')},
    {'data_id':19,'data_series_name':'Democratic Dark Money House', 'q':all_ies.filter(filer_committee_id_number__in=dem_noncommittee_id_list, candidate_office_checked='H')},
    {'data_id':20,'data_series_name':'Republican Dark Money House', 'q':all_ies.filter(filer_committee_id_number__in=rep_noncommittee_id_list, candidate_office_checked='H')},
    
    {'data_id':21,'data_series_name':'Democratic Party Committees Senate', 'q':all_ies.filter(filer_committee_id_number__in=dem_party_committee_id_list, candidate_office_checked='S')},
    {'data_id':22,'data_series_name':'Republican Party Committees Senate', 'q':all_ies.filter(filer_committee_id_number__in=rep_party_committee_id_list, candidate_office_checked='S')},
    {'data_id':23,'data_series_name':'Democratic Party Committees House', 'q':all_ies.filter(filer_committee_id_number__in=dem_party_committee_id_list, candidate_office_checked='H')},
    {'data_id':24,'data_series_name':'Republican Party Committees House', 'q':all_ies.filter(filer_committee_id_number__in=rep_party_committee_id_list, candidate_office_checked='H')}


]

class Command(BaseCommand):
    help = "Write some data csvs"
    requires_model_validation = False
   
    
    def handle(self, *args, **options):
        today = date.today()
        last_week = get_week_number(today) - 1
        first_week = get_week_number(data_start)
        
        outf = "%s/%s" % (CHART_CSV_DOWNLOAD_DIR, CSV_FILE_NAME)
        print "writing to %s" % outf
        outfile = open(outf, 'w')
        field_names = make_header(first_week, last_week)
        outfile.write(",".join(field_names) +"\n")

        dw = csv.writer(outfile)
        
        for data in data_series:
            this_row = [data['data_id'], data['data_series_name']]
            for week in range(first_week, last_week+1):
                print "handling %s week %s" % (data['data_series_name'], week)
                this_row.append(summarize_week_queryset(week, data['q']))
            dw.writerow(this_row)



        