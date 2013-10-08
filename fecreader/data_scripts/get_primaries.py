# How many incumbents have credible challengers? 
import sys, os

from django.core.management import setup_environ
sys.path.append('../fecreader/')
sys.path.append('../')

import settings
setup_environ(settings)

from summary_data.models import District, Candidate_Overlay

fundraising_threshold = 50000

for office in ['H', 'S']:
    # Ignore open seats
    races = District.objects.filter(office=office, open_seat=False)

    for race in races:
        incumbent_party = race.incumbent_party
        primary_challengers = Candidate_Overlay.objects.filter(district=race, is_incumbent=False, party=incumbent_party, total_receipts__gte=fundraising_threshold).exclude(not_seeking_reelection=True)
        if primary_challengers:
            print "\n\nFound credible challenger to %s %s - %s %s %s" % (race.incumbent_name, race.incumbent_party, race.state, race.office, race.office_district)
            for challenger in primary_challengers:
                print "\tchallenger: %s (%s) %s" % (challenger.name, challenger.party, challenger.total_receipts)