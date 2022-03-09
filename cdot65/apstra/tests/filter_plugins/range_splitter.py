class FilterModule(object):

    def filters(self):
        return {
            'range_splitter': self.range_splitter,
        }

    def range_splitter(self, asn_range):
        range_split = dict()
        range_split['first'] = ""
        range_split['last'] = ""

        if isinstance(asn_range,str):
            asn_range = asn_range.split('-')
            range_split['first'] = asn_range[0]
            range_split['last'] = asn_range[1]

        return range_split
