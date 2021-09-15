""" Get service plan for a given service plan id """

from main.inventory.models import ServicePlan


class GetServicePlan:
    """Get service plan for a given service plan id"""

    def __init__(self, service_plan_id):
        self.service_plan = ServicePlan.objects.get(id=int(service_plan_id))

    def process(self):

        return self