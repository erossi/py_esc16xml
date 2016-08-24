#/bin/env python3

import json
import xml.etree.ElementTree as ET

class Day(object):
    """ A single day
    """

    def __init__(self, xmlobj, index, date):
        """
        """
        self.idx = index
        self.date = date
        self.xml = ET.SubElement(xmlobj, 'day', {'index':index, \
                'date':date})
        self.room1 = ET.SubElement(self.xml, 'room', \
                {'name':'Casetta'})
        self.room2 = ET.SubElement(self.xml, 'room', \
                {'name':'Tendone Mickey Mouse'})


class Events(object):
    """ A single event
    <event id="3682">
     <start>09:30</start>
     <duration>00:25</duration>
     <room>Janson</room>
     <slug>keynotes_welcome</slug>
     <title>Welcome to FOSDEM 2016</title>
     <subtitle/>
     <track>Keynotes</track>
     <type>keynote</type>
     <language/>
     <abstract><p>FOSDEM welcome and opening talk.</p></abstract>
     <description><p>Welcome to FOSDEM 2016!</p></description>
     <persons>
      <person id="6">FOSDEM Staff</person>
     </persons>
     <links>
      <link href="6.mp4">FOSDEM 2016 Video (mp4)</link>
      <link href="2.webm">FOSDEM 2016 Video (webm)</link>
     </links>
    </event>
    """

    def __init__(self, day, event):
        """
        """
        self._id = event['uid'][1:]

        if (event['linea'] == '1'):
            self._subxml = ET.SubElement(day.room1, 'event', {'id':self._id})
            self._room = 'Casetta'
        else:
            self._subxml = ET.SubElement(day.room2, 'event', {'id':self._id})
            self._room = 'Tendone Mickey Mouse'

        self._start = event['orario'][:5]
        ET.SubElement(self._subxml, 'start').text = self._start

        self._duration = "00:" + event['durata']
        ET.SubElement(self._subxml, 'duration').text = self._duration

        ET.SubElement(self._subxml, 'room').text = self._room

        self._slug = None
        ET.SubElement(self._subxml, 'slug')

        self._title = event['titolo']
        ET.SubElement(self._subxml, 'title').text = self._title

        self._subtitle = None
        ET.SubElement(self._subxml, 'subtitle')
        self._track = None
        ET.SubElement(self._subxml, 'track')
        self._type = None
        ET.SubElement(self._subxml, 'type')

        self._language = event['lingua']
        ET.SubElement(self._subxml, 'language').text = self._language

        self._abstract = event['abstract']
        ET.SubElement(self._subxml, 'abstract').text = self._abstract
        
        self._description = None
        ET.SubElement(self._subxml, 'description')

        self._subpersons = ET.SubElement(self._subxml, 'persons')
        # Person requires an id
        self._person = event['autore']
        ET.SubElement(self._subpersons, 'person', {'id':self._id}).text = self._person

        ET.SubElement(self._subxml, 'links')


def main():
    # Start the XML
    myxml = ET.Element('schedule')
    # Complete the conference part
    conference = ET.SubElement(myxml, 'conference')
    ET.SubElement(conference, 'title').text = 'ESC 2016'
    ET.SubElement(conference, 'subtitle')
    ET.SubElement(conference, 'venue')
    ET.SubElement(conference, 'city').text = 'FORTE BAZZERA (VE)'
    ET.SubElement(conference, 'start').text = '2016-09-01'
    ET.SubElement(conference, 'end').text = '2016-09-04'
    ET.SubElement(conference, 'days').text = '4'
    ET.SubElement(conference, 'day_change').text = '09:00:00'
    ET.SubElement(conference, 'timeslot_duration').text = '00:05:00'

    # Read the Json file
    with open('esc16.json', 'r') as jsonfile:
        jsonobj = json.load(jsonfile)

    # jsonobj is a list of dict
    for i in jsonobj:
        for k, v in i.items():
            print (k, ":", v)

        print ('---')

    # Print the rooms
    rooms = {d['linea'] for d in jsonobj}
    print('rooms:', rooms)

    # scan for the available days
    days = {(d['giorno'], d['data'][:10]) for d in jsonobj}
    #days = dict((k, v) for k, v in days)
    print ('days:', days)

    # days
    day = dict()

    for k, v in days:
        day[k] = Day(myxml, k, v)

    # jsonobj is a list of dict
    for i in jsonobj:
        Events(day[i['giorno']], i)

    ET.dump(myxml)
    ET.ElementTree(myxml).write('output.xml', encoding='utf-8')

# Main
if __name__ == "__main__":
    main()
