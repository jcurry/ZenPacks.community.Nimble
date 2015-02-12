/*
 * Based on the configuration in ../../configure.zcml this JavaScript will only
 * be loaded when the user is looking at NimbleDevice in the web interface.
 */

(function(){

var ZC = Ext.ns('Zenoss.component');

/*
 * Custom component grid panel. This controls the grid that gets displayed for
 * components of the type set in "componentType".
 *
 * The name of the component panel MUST be the exact name of the object component
 *    catenated with Panel - hence NimbleVolumePanel
 *
 * Any columns that use a "dataIndex", that dataIndex name must appear in the fields stanza
 *    but order is NOT important. You must include uid in the fields stanza (but need not include in columns).
 *    If you do NOT include "monitor" in the fields stanza, then there will be no Graphs
 *        option in the DISPLAY dropdown.
 * It is the order of the stanzas under "columns" that defines the order on the web page
 *
 * Use the Zenoss-provided ping status renderer to display icons for VolOnline where
 *      VolOnline=1 = running = green,   otherwise red
 */


/*
 * Custom component grid panel. This controls the grid that gets displayed for
 * components of the type set in "componenType".
 */
ZC.NimbleVolumePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'NimbleVolume',
            sortInfo: {
                field: 'name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'VolId'},
                {name: 'VolName'},
                {name: 'VolSize'},
                {name: 'VolUsage'},
                {name: 'VolReserve'},
                {name: 'VolNumConns'},
                {name: 'VolOnline'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'usesMonitorAttribute'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'VolId',
                dataIndex: 'VolId',
                header: _t('Volume Id'),
                sortable: true,
                width: 65
            },{
                id: 'VolName',
                dataIndex: 'VolName',
                header: _t('Volume Name'),
                sortable: true,
                width: 200
            },{
                id: 'VolSize',
                dataIndex: 'VolSize',
                header: _t('Volume Size (GB)'),
                sortable: true,
                width: 120
            },{
                id: 'VolUsage',
                dataIndex: 'VolUsage',
                header: _t('Volume Usage (GB)'),
                sortable: true,
                width: 120
            },{
                id: 'VolReserve',
                dataIndex: 'VolReserve',
                header: _t('Volume Reserve (GB)'),
                sortable: true,
                width: 120
            },{
                id: 'VolNumConns',
                dataIndex: 'VolNumConns',
                header: _t('Vol. Connections'),
                sortable: true,
                width: 120
            },{
                id: 'VolOnline',
                dataIndex: 'VolOnline',
                header: _t('Volume Online'),
                sortable: true,
                renderer: function(dS) {
                        if (dS==1) {
                          return Zenoss.render.pingStatus('up');
                        } else {
                          return Zenoss.render.pingStatus('down');
                        }
                },
                width: 65
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.NimbleVolumePanel.superclass.constructor.call(this, config);
    }
});
Ext.reg('NimbleVolumePanel', ZC.NimbleVolumePanel);

/*
 * Friendly names for the components. First parameter is the meta_type in your
 * custom component class. Second parameter is the singular form of the
 * friendly name to be displayed in the UI. Third parameter is the plural form.
 */
ZC.registerName('NimbleVolume', _t('Volume'), _t('Volumes'));



})();
