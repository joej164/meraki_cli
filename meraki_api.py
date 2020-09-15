import meraki
import settings
import json


class meraki_api():
    def __init__(self):
        self.settings = settings.Settings()
        self.dashboard = meraki.DashboardAPI()
        self.org_id = self.find_meraki_org_id()

    def find_meraki_org_id(self):
        my_orgs = self.dashboard.organizations.getOrganizations()

        org_id = None
        for o in my_orgs:
            if o['name'] == self.settings.meraki_org_name:
                org_id = o['id']

        return org_id

    def find_meraki_network_id(self, network_name: str):
        networks = self.dashboard.organizations.getOrganizationNetworks(
            self.org_id)
        my_network = [n for n in networks if n['name'] == network_name]
        if my_network:
            return my_network[0]
        else:
            return None

    def get_meraki_network_details(self, network_id: str):
        return self.dashboard.networks.getNetwork(network_id)

    def create_meraki_network(self, network_name: str, tags: list = [''], timezone: str = 'America/Los_angeles'):
        return_obj = {
            'network_id': None,
            'added': False
        }

        network_info = self.find_meraki_network_id(network_name)

        if not network_info:
            network_info = self.dashboard.organizations.createOrganizationNetwork(
                self.org_id,
                network_name,
                productTypes=['appliance'],
                tags=tags,
            )
            return_obj['added'] = True

        return_obj['network_id'] = network_info['id']
        return json.dumps(return_obj)

    def delete_meraki_network(self, network_id: str = None):
        response = self.dashboard.networks.deleteNetwork(network_id)
        return response

    def set_meraki_network_appliance_site_to_site_vpn_mode(self, network_id, mode):
        vpn_status = self.dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
            network_id, mode=mode)
        return vpn_status
