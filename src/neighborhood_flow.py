#!/usr/bin/env python
import sys
import os
import collections

import data
import figs

class Counter(collections.Counter):
    year_range = range(2004, 2016)

    def restrict_to_year_range(self, multiplier=1):
        output = []
        for year in self.year_range:
            output.append(multiplier * self[year])
        return output


out_dir = sys.argv[-1]

with open(sys.argv[1]) as stream:
    reader = data.RawReader(stream)
    neighborhood = None
    new_counts, old_counts = Counter(), Counter()
    for row in reader:
        year = int(row['year'])
        if neighborhood is None:
            neighborhood = row['neighborhood']
        if neighborhood != row['neighborhood']:
            if not neighborhood:
                neighborhood = "unknown"
            fig = figs.FlowOverTime(
                Counter.year_range,
                new_counts.restrict_to_year_range(),
                old_counts.restrict_to_year_range(multiplier=-1),
            )
            filename = os.path.join(
                out_dir,
                neighborhood.lower().replace(' ', '_') + '.png',
            )
            fig.save(filename)
            fig.close()
            print "saved", filename
            neighborhood = row['neighborhood']
            new_counts, old_counts = Counter(), Counter()
        new_counts[year] = int(row['new'])
        old_counts[year] = int(row['old'])
