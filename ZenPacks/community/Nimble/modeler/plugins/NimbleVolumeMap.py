# Module-level documentation will automatically be shown as additional
# information for the modeler plugin in the web interface.
"""
NimbleVolumeMap
Models volumes for a Nimble storage device
"""


# The name of the class within this file must match the filename.

# SnmpPlugin is the base class that provides lots of help in modeling data
# that's available over SNMP.
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

# Classes we'll need for returning proper results from our modeler plugin's
# process method.
from Products.DataCollector.plugins.DataMaps import ObjectMap


class NimbleVolumeMap(SnmpPlugin):
    """ Map Volumes to Nimble Device """
    maptype = "NimbleVolumeMap"
    modname = "ZenPacks.community.Nimble.NimbleVolume"
    relname = "nimbleVolume"


    # volEntry = 1.3.6.1.4.1.37447.1.2.1
    # Note that the MIB says that volume sizes are in bytes but we believe they 
    #     are actually in MB.  Modeler will multiply these values up.

    snmpGetTableMaps = (
            GetTableMap('volEntry',
                '1.3.6.1.4.1.37447.1.2.1',
                {
                    '.2'  : 'VolId',
                    '.3'  : 'VolName',
                    '.4'  : '_VolSizeLow',
                    '.5'  : '_VolSizeHigh',
                    '.6'  : '_VolUsageLow',
                    '.7'  : '_VolUsageHigh',
                    '.8'  : '_VolReserveLow',
                    '.9'  : '_VolReserveHigh',
                    '.10' : 'VolOnline',
                    '.11' : 'VolNumConns',
                }
            ),
        )

    def process(self, device, results, log):
        log.info("Modeler %s processing data for device %s", self.name(), device.id)
        rm = self.relMap()
        getdata, tabledata = results
        # If no data supplied then simply return
        voltable = tabledata.get('volEntry')
        if not voltable:
            log.warn(' No SNMP response from %s for the %s plugin  for Volume Table' % ( device.id, self.name() ) )
            log.warn( "Data= %s", tabledata )
            return

        for oid, data in voltable.items():
            try:
                om=self.objectMap(data)
                # prepId santises names if they have odd characters....
                om.id = self.prepId(om.VolName)
                om.VolName = self.prepId(om.VolName)
                # MIB sez vol sizes are bytes.  They are actually MB. We want GB
                om.VolSize = (( data['_VolSizeHigh'] << 32 )+ data['_VolSizeLow']) / 1024
                om.VolUsage = (( data['_VolUsageHigh'] << 32 )+ data['_VolUsageLow']) / 1024
                om.VolReserve = (( data['_VolReserveHigh'] << 32 ) + data['_VolReserveLow']) / 1024
                om.snmpindex = str(om.VolId)
                #log.debug( 'om is %s \n' % (om))

            except (KeyError, IndexError, AttributeError, TypeError), errorInfo:
                log.warn( ' Error in NimbleVolumeMap modeler plugin %s', errorInfo)
                continue

            rm.append(om)
            log.debug('rm %s' % (rm) )
        return rm


