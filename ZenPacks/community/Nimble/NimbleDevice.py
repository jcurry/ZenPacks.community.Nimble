from Products.ZenModel.Device import Device
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Globals import InitializeClass
from copy import deepcopy


class NimbleDevice(Device):
    """
    Nimble device subclass. In this case the reason for creating a subclass of
    device is to add a new type of relation. We want many "NimbleVolume"
    components to be associated with each of these devices.

    If you set the zPythonClass of a device class to
    ZenPacks.community.NimbleDevice, any devices created or moved
    into that device class will become this class and be able to contain
    NimbleVolumes.
    """

    meta_type = portal_type = 'NimbleDevice'

    # This is where we extend the standard relationships of a device to add
    # our "nimbleVolume" relationship that must be filled with components
    # of our custom "NimbleVolume" class.
    _relations = Device._relations + (
        ('nimbleVolume', ToManyCont(ToOne,
            'ZenPacks.community.Nimble.NimbleVolume',
            'nimbleDevice',
            ),
        ),
    )

    factory_type_information = deepcopy(Device.factory_type_information)

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()

InitializeClass(NimbleDevice)


