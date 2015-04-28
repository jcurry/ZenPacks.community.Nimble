=======================================
ZenPack to manage Nimble Storage Arrays 
=======================================

Description
===========

THIS IS CURRENTLY A BETA ZENPACK. IT SHOULD ONLY BE INSTALLED IN A TEST ENVIRONMENT!!!

This ZenPack is to manage Nimble storage arrays using the SNMP protocol.
A new nimble device type is created with a new component type to represent volumes.

The Nimble MIB (1.3.6.1.4.1.37447) provides a Volume table at 1.3.6.1.4.1.37447.1.2.1
with the following OIDs:
    * volID                     .2    (integer - to be used as index)
    * volName                   .3    ( string)
    * volSizeLow                .4    (low order byte, 32-bit unsigned integer)
    * volSizeHigh               .5    (high order byte, 32-bit unsigned integer)
    * volUsageLow               .6    (low order byte, 32-bit unsigned integer)
    * volUsageHigh              .7    (high order byte, 32-bit unsigned integer)
    * volReserveLow             .8    (low order byte, 32-bit unsigned integer)
    * volReserveHigh            .9    (high order byte, 32-bit unsigned integer)
    * volOnline                 .10   (0=offline, 1=online)
    * volNumConnections         .11   (unsigned integer)

The MIB says that volume size values are in bytes but we believe the values to
actually be in MB.

In addition, the Nimble MIB provides some global statistics.  These are all
device-wide values (SNMP scalar values).  The globalStats table is 1.3.6.1.4.1.37447.1.3
Relevant MIB values for this ZenPack are:
    * ioReads                   .2.0
    * ioSeqReads                .3.0
    * ioWrites                  .4.0
    * ioSeqWrites               .5.0
    * ioNonSeqReadHits          .16.0

The ZenPack provides a modeler plugin to discover all volumes for a Nimble device.  

It also provides device classes of /Storage and /Storage/Nimble.

A performance template is provided to gather and graph the scalar data listed above. The
ZenPack binds this template to the /Storage/Nimble device class.

A component performance template is provided to gather data for volume usage and graph that data.
Note that component templates must not be manually bound - they bind automatically to the object
type that exactly matches the name of the template.

The two Nimble MIBs are included in the ZenPack.

A new event is raised on volume performance thresholds.  This event includes a transform to 
improve the summary field of the event.

Because this ZenPack needs to perform functions on SNMP values in performance templates, 
the Zenoss Calculated Performance ZenPack is a prerequisite, which itself has a prerequisite
of the Python Collector ZenPack.

Objects
=======

A new device object class - NimbleDevice - with a relationship of nimbleVolume   (note capitalisation)
A new component object class for a NimbleDevice - NimbleVolume - with a relationship nimbleDevice


Modeler Plugins
===============
A modeler plugin - NimbleVolumeMap - which gathers id, name, various sizes, online status and
number of connections.  The three sets of size data are in 2 MIB values - high 32 bits and
low 32 bits.  The modeler combines these values to present a single value in the NimbleVolume
object.  We believe that the raw SNMP data is in MB.  The modeler divides this by 1024 to
present values as GB.

The NimbleVolumeMap plugin is assigned to the /Storage/Nimble device class by the ZenPack.

Templates
=========

Device-level template - NimbleGlobalStats - is available for device classes from /Storage/Nimble.
It is bound to this device class in the ZenPack.  It gathers and graphs ioreads/writes, ioSeqReads/Writes
and ioNonSeqReadHits.

Component template NimbleVolume (note the name exactly matches the new object class), is available for
device classes from /Storage/Nimble.  It must not be manually bound.  It gathers volUsageHigh and volUsageLow
SNMP tables.  To convert these values into a single datapoint, the Zenoss Calculated Performance ZenPack
is used to create a new datapoint of volUsage.  These values are all in MB.

Two thresholds are supplied for "30 percent used" and "90 percent used".  They access the object's value
for VolSize (ie the maximum size of the volume) and then threshold the VolUsage datapoint at the respective
percentages. The threshold value is multiplied by 1024 (as the VolSize object data delivered by the modeler
is given in GB).  They generate a /Perf/Nimble event if the threshold is breached.

Graphs are delivered of volUsageLow and volUsage.  Note that the volUsage datapoint in the VolUsage graph
has been modified with an RPN (Reverse Polish Notation) formula of 1024,*,1024,*   . This does not affect
the value stored in the rrd datafile but does ensure that graph actually shows bytes, rather than MB.  The
autoscaling of the rrdgraph utility then automatically applies appropriate M / G / T on the labels.

zProperties
===========

This ZenPack introduces no new zProperties but it does set the zPythonClass property to
ZenPacks.community.Nimble.NimbleDevice for the device class /Storage/Nimble.

MIBs
====

Two MIBs are supplied with this ZenPack:
    *   NIMBLE-TRAP-MIB
    *   NIMBLE-MIB


Events
======
The performance template has a threshold which generates an event of class /Perf/Nimble.  The
event has a transform which improves the output of the summary field.  The event is included 
in the ZenPack.


Daemons
========
There is no daemon shipped with this ZenPack.  zenpython is used to generate the
CalculatedPerformance datapoint for VolUsage.


Requirements & Dependencies
===========================

    * Zenoss Versions Supported: 4.x
    * External Dependencies: 
    * ZenPack Dependencies: 
        * ZenPacks.zenoss.PythonCollector at least 1.6 
        * ZenPacks.zenoss.CalculatedPerformance 2.0.4 or higher
    * Installation Notes: Restart zenoss after installation
    * Configuration:


Download
========

The ZenPack will be made available on github.

ZenPack installation
======================

Beware, as with any ZenPack, if you remove the ZenPack and devices exist under
classes defined in this ZenPack - /Storage and /Storage/Nimble - then these 
devices will be removed.

This is NOT the case if you reinstall the ZenPack.  I suggest you move any affected
device to another class (/Ping might be good, temporarily) if you are going
to remove the ZenPack.

This ZenPack can be installed from the .egg file using either the GUI or the
zenpack command line: 
    * zenpack --install ZenPacks.community.Nimble-1.0.0-py2.7.egg
    * Restart zenoss with "zenoss restart"

To install in development mode, download the bundle from github, unpack it
in a convenient directory, change to that directory, and use:
    * zenpack --link --install ZenPacks.community.Nimble
    * Restart zenoss with "zenoss restart"
    

Change History
==============
* 1.0.0
   * Initial Release
*1.0.1
   * Updated templates for NimbleGlobalStats to be DERVIVE not Gauge

