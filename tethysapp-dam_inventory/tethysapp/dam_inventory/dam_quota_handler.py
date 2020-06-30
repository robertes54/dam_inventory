from tethys_quotas.handlers.base import ResourceQuotaHandler
from .model import Dam
from .app import DamInventory as app


class DamQuotaHandler(ResourceQuotaHandler):
    """
    Defines quotas for dam storage for the persistent store.

    inherits from ResourceQuotaHandler
    """
    codename = "dam_quota"
    name = "Dam Quota"
    description = "Set quota on dam db entry storage for persistent store."
    default = 3  # number of dams that can be created per user
    units = "dam"
    help = "You have exceeded your quota on dams. Please visit the dams page and remove unneeded dams."
    applies_to = ["django.contrib.auth.models.User"]

    def get_current_use(self):
        """
        calculates/retrieves the current number of dams in the database

        Returns:
            Int: current number of dams in database
        """
        # Query database for count of dams
        Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()
        current_use = session.query(Dam).filter(Dam.user_id == self.entity.id).count()

        session.close()

        return current_use