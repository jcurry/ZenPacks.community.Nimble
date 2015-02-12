from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Globals import InitializeClass

class NimbleVolume(DeviceComponent, ManagedEntity):
    meta_type = portal_type = "NimbleVolume"

    VolId = None
    VolName = None
    VolSize = 0
    VolUsage = 0
    VolReserve = 0
    VolOnline = 0
    VolNumConns = 0

    _properties = ManagedEntity._properties + (
        {'id':'snmpindex', 'type':'string', 'mode':''},
        {'id': 'VolId', 'type': 'int', 'mode': ''},
        {'id': 'VolName', 'type': 'string', 'mode': ''},
        {'id': 'VolSize', 'type': 'long', 'mode': ''},
        {'id': 'VolUsage', 'type': 'long', 'mode': ''},
        {'id': 'VolReserve', 'type': 'long', 'mode': ''},
        {'id': 'VolOnline', 'type': 'int', 'mode': ''},
        {'id': 'VolNumConns', 'type': 'int', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('nimbleDevice', ToOne(ToManyCont,
            'ZenPacks.community.Nimble.NimbleDevice',
            'nimbleVolume',
            ),
        ),
    )

    # Custom components must always implement the device method. The method
    # should return the device object that contains the component.
    def device(self):
        return self.nimbleDevice()

    def viewName(self):
        """Pretty version human readable version of this object"""
        return self.id


    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName

InitializeClass(NimbleVolume)

