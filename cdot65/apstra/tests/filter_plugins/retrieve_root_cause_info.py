class FilterModule(object):

    def filters(self):
        return {
            'retrieve_root_cause_info': self.retrieve_root_cause_info,
        }

    def retrieve_root_cause_info(self, root_cause_information):
        root_causes = list()

        if isinstance(root_cause_information,list):
            for each in root_cause_information:
                root_causes.append(each['description'])

        return root_causes
