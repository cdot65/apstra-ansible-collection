class FilterModule(object):

    def filters(self):
        return {
            'find_site_blueprint': self.find_site_blueprint,
        }
    
    def find_site_blueprint(self, nautobot_blueprints, blueprint_name):
        blueprint_information = str()

        if isinstance(nautobot_blueprints,list):
            for item in nautobot_blueprints:
                if item['name'] == blueprint_name:
                    blueprint_information = item

        return blueprint_information
