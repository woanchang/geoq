var leaflet_layer_control = {};

//TODO: Pull ordering from map object
//TODO: Allow drag-and-drop sorting that controls layer
//TODO: have an info control that modifies things like IA tools/icons
//TODO: Save info about layer configuration, then have a way to load that back in or save as settings for a Job
//TODO: Have a control to add new layers
//TODO: Be able to drag and drop layers onto the page
//TODO: Integrate with GeoNode to auto-build layers in GeoServer
//TODO: When adding ?request=GetCapabilities links to layers, do it smartly

//TODO: When changing order of Google Maps, always put below Features layers

leaflet_layer_control.$map = undefined;
leaflet_layer_control.$drawer = undefined;
leaflet_layer_control.$drawer_tray = undefined;
leaflet_layer_control.$tree = undefined;
leaflet_layer_control.accordion_sections = [];
leaflet_layer_control.$feature_info = undefined;
leaflet_layer_control.finish_options = [];

leaflet_layer_control.init = function(){
    leaflet_layer_control.$map = $("#map");
    return leaflet_layer_control.initDrawer();
};
leaflet_layer_control.initDrawer = function(){
    //Build the drawer with an Accordion and add it after the map
    var $drawer = $("<div>")
        .attr({id:"layer_info_drawer"});
    leaflet_layer_control.$drawer = $drawer;
    leaflet_layer_control.$map.after($drawer);

    var $accordion = $('<div>')
        .addClass("accordion")
        .attr('id','layer-control-accordion')
        .appendTo($drawer);

    //Build the first row of the accordion if workcell info exists
    leaflet_layer_control.addWorkCellInfo($accordion);

    //Build the next row of the accordion with details about a selected feature
    leaflet_layer_control.addFeatureInfo($accordion);

    //Build an accordion row to view workcell log
    leaflet_layer_control.addLogInfo($accordion);

    //The Layer Controls should also be built and added later, such as
    // var options = aoi_feature_edit.buildTreeLayers();
    // leaflet_layer_control.addLayerControl(map, options, $accordion);

    // by default, open work cell details
    $('#collapse-work-cell-details').collapse('toggle');

    return $accordion;
};
//leaflet_layer_control.drawAccordion = function($accordion){
//    $accordion.collapse();
//    _.each(leaflet_layer_control.accordion_sections,function(section,i){
//        if (i==0){
//            $(section).collapse('show');
//        } else {
//            $(section).collapse('hide');
//        }
//    });
//    $accordion.css('height','inherit');
//};

leaflet_layer_control.addFeatureInfo = function($accordion){
    //TODO: Fill this in

    var $content = leaflet_layer_control.buildAccordionPanel($accordion,"Feature Details");
    leaflet_layer_control.$feature_info = $("<div>")
        .html("Click a feature on the map to see an information associated with it")
        .appendTo($content);

};

leaflet_layer_control.addLogInfo = function($accordion) {

    var $content = leaflet_layer_control.buildAccordionPanel($accordion, "Workcell Log");
    //leaflet_layer_control.$feature_info = $("<div>")
    //    .html("View work log for this cell")
    //    .appendTo($content);
    var $messageScroll = $("<div id='message_scroll'>")
        .addClass("message-panel")
        .appendTo($content);
    var $messageTable = $("<table id='message_table'>")
        .addClass("table table-bordered header-fixed")
        .appendTo($messageScroll);
    var $header = $("<thead><tr><th>DateTime</th><th>User</th><th>Comment</th></tr></thead>")
        .appendTo($messageTable);
    var $body = $("<tbody id='messages'></tbody>")
        .appendTo($messageTable);
    var $buttonRow = $("<div id='button_row'>")
        .appendTo($content);
    $("<button>Submit a Comment</button>")
        .addClass("btn btn-primary")
        .click(leaflet_layer_control.submitComment)
        .appendTo($buttonRow);

    leaflet_layer_control.refreshLogInfo();
};
leaflet_layer_control.submitComment = function() {
    BootstrapDialog.show({
        title: 'Submit Comment',
        message: "Comment: <input type='text' maxlength='200'>",
        buttons: [{
            label: 'Submit',
            action: function(dialog) {
                var text = dialog.getModalBody().find('input').val();
                $.ajax({
                    url: document.URL + "/comment",
                    type: 'POST',
                    data: {
                        comment : text,
                        csrfmiddlewaretoken: aoi_feature_edit.csrf
                    }
                })
                .done( function (msg) {
                    leaflet_layer_control.refreshLogInfo();
                    dialog.close();
                });
            }
        }, {
            label: 'Cancel',
            action: function(dialog) {
                dialog.close();
            }
        }]
    });
};
leaflet_layer_control.refreshLogInfo = function() {
    var body = $('#messages');
    if ($('#messages tr').length > 0) {
        body.empty();
    }

    $.ajax({
            url: aoi_feature_edit.api_url_log,
            dataType: "json"
        })
        .done(function(entries) {
            body.empty();
            _.each(entries, function(entry) {
                $("<tr><td>" + entry.timestamp + "</td><td>" +
                    entry.user + "</td><td>" + entry.text + "</td></tr>")
                    .appendTo(body);
            })
        });

};

leaflet_layer_control.buildAccordionPanel = function($accordion,title){
    var sectionName = _.str.dasherize(_.str.stripTags(title));

    var $drawerHolder = $("<div>")
        .addClass("accordion-group")
        .appendTo($accordion);
    var $drawerInner = $("<div>")
        .addClass("accordion-heading gray-header")
        .appendTo($drawerHolder);
//    var $header = $('<h4>')
//        .addClass("panel-title")
//        .appendTo($drawerInner);
    $('<a class="accordion-collapse" data-toggle="collapse" data-parent="#layer-control-accordion" href="#collapse'+sectionName+'">')
        .text(title)
        .appendTo($drawerInner);

    var $contentHolder = $('<div id="collapse'+sectionName+'" class="accordion-body collapse">')
        .appendTo($drawerHolder);
    var $content = $("<div>")
        .addClass('accordion-inner')
        .appendTo($contentHolder);

    leaflet_layer_control.accordion_sections.push('#collapse'+sectionName)

    return $content;
};

leaflet_layer_control.addWorkCellInfo = function($accordion) {

    if (!_.isObject(aoi_feature_edit.aoi_properties)){
        log.error("No Workcell Properties set for building side menu");
        return;
    }

    var editableUrl = '/geoq/api/job/update/'+aoi_feature_edit.aoi_id;

    var $content = leaflet_layer_control.buildAccordionPanel($accordion,"Work Cell Details");
    $content.attr({id:"drawer_tray_top"});

    var workcell_note = 'Click here to add a note';
    $.each(aoi_feature_edit.aoi_properties, function(index, value) {

        var skipIt = false;
        if (index == 'workcell_note') {
            workcell_note = value;
            skipIt = true;
        }
        if (index == 'status') {
            skipIt = true;
            var $status = $('<div>')
                .addClass('status_block')
                .html('<b>Status</b>: ')
                .appendTo($content);
            $('<span class="editable" id="status" style="display: inline">'+_.str.capitalize(value)+'</span>')
                .appendTo($status)
                .editable(editableUrl, {
                    data   : " {'Unassigned':'Unassigned','In work':'In work', 'In review':'In review', 'Completed':'Completed'}",
                    type   : 'select',
                    submit : 'OK',
                    style  : 'inherit',
                    tooltip: 'Click to change the status of this cell'
                });

        }
        if (index == 'priority') {
            skipIt = true;
            var $status = $('<div>')
                .addClass('status_block')
                .html('<b>Priority</b>: ')
                .appendTo($content);
            $('<span class="editable tight" id="priority" style="display: inline">'+_.str.capitalize(aoi_feature_edit.priority)+'</span>')
                .appendTo($status)
                .editable(editableUrl, {
                    data   : " {'1':'1','2':'2','3':'3','4':'4','5':'5'}",
                    type   : 'select',
                    submit : 'OK',
                    style  : 'inherit',
                    tooltip: 'Click to change the priority of this cell'
                });

        }
        if (!skipIt){
            var html = '<b>'+_.str.capitalize(index)+'</b>: '+_.str.capitalize(value);
            $('<div>')
                .addClass('status_block')
                .html(html)
                .appendTo($content);
        }
    });

    //Add the note editing piece at the end
    $('<div>')
        .addClass('editable')
        .attr('id','workcell_note')
        .html(workcell_note)
        .appendTo($content)
        .editable(editableUrl, {select:true});

    // add function buttons
    var $submitDiv = $('<div>')
        .addClass("dropdown")
        .appendTo($content);

    var $ul2 = $('<ul>');

    var $exportButton = $("<a>")
        .addClass("btn dropdown-toggle")
        .attr({id:'export-button-dropdown', 'data-toggle':"dropdown", type:"button", href:'#'})
        .css({textAlign: "left"})
        .click(function(){
            $ul2.dropdown('toggle');
            return false;
        })
        .append($('<span>Export</span>'))
        .append($('<b class="caret"></b>'))
        .appendTo($submitDiv);

    $ul2
        .addClass("dropdown-menu")
        .css({textAlign: "left", left: '30px'})
        .attr("role", "menu")
        .appendTo($submitDiv);

    var $li21 = $('<li>')
        .attr({role:"presentation"})
        .appendTo($ul2);
    $("<a>")
        .attr({role:"menuitem", tabindex:"-1", href:"#"})
        .text("Job as KML")
        .on("click",function(ev){
            window.open(aoi_feature_edit.api_url_job_kml, "_blank");
            $ul2.dropdown("toggle");
            return false;
        })
        .appendTo($li21);

    var $li22 = $('<li>')
        .attr({role:"presentation"})
        .appendTo($ul2);
    $("<a>")
        .attr({role:"menuitem", tabindex:"-1", href:"#"})
        .text("Job as Networked KML")
        .on("click",function(ev){
            window.open(aoi_feature_edit.api_url_job_kml_networked, "_blank");
            $ul2.dropdown("toggle");
            return false;
        })
        .appendTo($li22);

    var $li23 = $('<li>')
        .attr({role:"presentation"})
        .appendTo($ul2);
    $("<a>")
        .attr({role:"menuitem", tabindex:"-1", href:"#"})
        .text("Job as GeoRSS")
        .on("click",function(ev){
            window.open(aoi_feature_edit.api_url_job_georss, "_blank");
            $ul2.dropdown("toggle");
            return false;
        })
        .appendTo($li23);

    var $li24 = $('<li>')
        .attr({role:"presentation"})
        .appendTo($ul2);
    $("<a>")
        .attr({role:"menuitem", tabindex:"-1", href:"#"})
        .text("This Cell's bounds as GeoRSS")
        .on("click",function(ev){
            window.open(aoi_feature_edit.api_url_aoi_georss, "_blank");
            $ul2.dropdown("toggle");
            return false;
        })
        .appendTo($li24);

};
leaflet_layer_control.show_feature_info = function (feature) {

    var $content = leaflet_layer_control.$feature_info;
    if (!feature || !feature.properties || !$content || jQuery.isEmptyObject($content)) {
        return;
    }
    $content.empty();

    var editableUrl = '/geoq/api/feature/update/'+feature.properties.id;

    var feature_note_original = "Click here to add a note to this feature";
    var feature_note = feature_note_original;
    $.each(feature.properties, function(index, value) {

        var skipIt = false;
        if (index == 'feature_note') {
            feature_note = value;
            skipIt = true;
        } else if (index == 'linked_items') {
            skipIt = true;
            if (_.isArray(value) && value.length) {
                var $status = $('<div>')
                    .appendTo($content);
                $('<div>')
                    .html('<b>Linked Items:</b>')
                    .addClass('status-block')
                    .appendTo($status);

                _.each(value,function(linked_item){
                    var properties = linked_item.properties;
                    if (!_.isObject(properties)) properties = {};

                    var html = "";
                    if (linked_item.user) {
                        html += "Posted by "+linked_item.user+"</br>";
                    }
                    if (linked_item.created_at) {
                        if (moment(linked_item.created_at).isValid()){
                            html += "Linked "+moment(linked_item.created_at).calendar()+"</br>";
                        } else {
                            html += "Linked "+linked_item.created_at+"</br>";
                        }
                    }
                    if (properties && properties.source) {
                        html += "From "+properties.source+"</br>";
                    }
                    if (properties && properties.id) {
                        html += "Source ID: "+ _.str.truncate(properties.id,9)+"</br>";
                    }
                    if (properties && properties.thumbnail) {
                        html += "<img src='"+properties.thumbnail+"' width='100'><br/>";
                    }
                    if (properties && properties.image) {
                        html += "<a href='"+properties.image+"' target='_blank'>Linked Image</a>";
                    }
                    var img = $('<div>')
                        .addClass('linked-item status_block')
                        .popover({
                            title:'Linked ' + properties.source + ' Item',
                            content:JSON.stringify(properties)||"No properties",
                            trigger:'click',
                            placement:'right'
                        })
                        .html(html)
                        .appendTo($status);
                });
            }
        }

        if (!skipIt && _.isString(value)){
            var html = '<b>'+_.str.capitalize(index)+'</b>: '+_.str.capitalize(value);
            $('<div>')
                .html(html)
                .appendTo($content);
        }
    });

    //Add the note editing piece at the end
    $('<div>')
        .addClass('editable')
        .attr('id','feature_note')
        .html(feature_note)
        .appendTo($content)
        .editable(editableUrl, {select : true});

};
leaflet_layer_control.show_info = function (objToShow, node) {
    var html_objects = [];

    if (typeof objToShow == "string"){
        html_objects.push(objToShow);
    } else {
        if (objToShow.options && objToShow._leaflet_id) {
            //Probably a Leaflet layer
            html_objects.push(leaflet_layer_control.parsers.infoFromLayer(objToShow));
            html_objects.push(leaflet_layer_control.parsers.opacityControls(objToShow));

            if (leaflet_layer_control.likelyHasFeatures(objToShow)) {
                var $btn = $('<a href="#" class="btn">Refresh based on current map</a>')
                    .on('click',function(){
                        leaflet_helper.constructors.geojson(objToShow.config, aoi_feature_edit.map, objToShow);
                    });
                html_objects.push($btn);
            }
        } else if (objToShow.name && objToShow.url && objToShow.type) {
            //Probably a map info object
            html_objects.push(leaflet_layer_control.parsers.infoFromInfoObj(objToShow));
        } else {

            if (typeof objToShow == "object"){
                var obj_size = _.toArray(objToShow).length;
                if (obj_size > 1) {
                    //Show all items from the object
                    html_objects.push(leaflet_layer_control.parsers.infoFromObject(objToShow));
                } else {
                    //Likely a title/folder of the tree
                    html_objects.push(leaflet_layer_control.parsers.infoFromFolder(node));
                }
            }
        }
    }

    //Clear the tray and add each html object generated from above
    leaflet_layer_control.$drawer_tray.empty();
    _.each(html_objects,function(html){
        leaflet_layer_control.$drawer_tray.append(html);
    });
};
//=========================================

leaflet_layer_control.parsers = {};
leaflet_layer_control.parsers.infoFromLayer = function (obj){
    var html = "";
    obj = obj || {};

    var capabilitiesLink = "";
    if (obj.type == "WMS" || obj.type == "WMTS") {
        capabilitiesLink = "?request=GetCapabilities";
    }
    html+=leaflet_layer_control.parsers.textIfExists({name: obj.name, title:"Layer", header:true, linkit:obj._url, linkSuffix:capabilitiesLink});

    if (obj._layers) {
        var features = obj.getLayers();
        var count = features.length;
        html+=leaflet_layer_control.parsers.textIfExists({name: count, title:"Features in this job"});

        var number_by_analyst = 0;
        _.each (features,function(feature){
            var properties = feature.feature.properties || {};
            if (properties.analyst == aoi_feature_edit.analyst_name) {
                number_by_analyst++;
            }
        });

        if (number_by_analyst){
            html+=leaflet_layer_control.parsers.textIfExists({name: number_by_analyst, title:"Features you entered"});
        }
        //TODO: Some way to highlight these or show more info?
    }
    if (obj.options) {
        html+=leaflet_layer_control.parsers.textIfExists({name: obj.options.attribution});
        html+=leaflet_layer_control.parsers.textIfExists({name: obj.options.layers, title:"Layers"});
    }

    return html;
};
leaflet_layer_control.parsers.infoFromInfoObj = function (obj){
    var html = "";
    obj = obj || {};

    html+=leaflet_layer_control.parsers.textIfExists({name: obj.name, title:"Layer", header:true, linkit:obj.url, linkSuffix:"?request=GetCapabilities"});
    html+=leaflet_layer_control.parsers.textIfExists({name: obj.type, title:"Type"});
    html+=leaflet_layer_control.parsers.textIfExists({name: obj.layer, title:"Layers"});
//    html+=leaflet_layer_control.parsers.textIfExists({name: obj.description, style_class:'scroll-link'});
    return html;
};
leaflet_layer_control.parsers.infoFromObject = function (obj){
    var html = "";
    for(var k in obj) {
        html+=leaflet_layer_control.parsers.textIfExists({name: obj[k], title:k});
    }
    return html;
};
leaflet_layer_control.parsers.infoFromFolder = function (obj){
    var html = "";
    obj = obj || {};
    html+=leaflet_layer_control.parsers.textIfExists({name: obj.title, title:"Group", header:true});
    if (obj.children) {
        var children = _.pluck(obj.children,'title').join(", ");
        html+=leaflet_layer_control.parsers.textIfExists({name: children, title:"Sub-layers"});
    }
    html+=leaflet_layer_control.parsers.textIfExists({name: obj.selected, title:"Selected"});

    return html;
};
leaflet_layer_control.parsers.textIfExists = function(options) {
    options = options || {};
    var obj = options.name || "";
    var title = options.title || "";
    var noBold = options.noBold;
    var noBreak = options.noBreak;
    var header = options.header;
    if (header) noBreak = true;
    var linkit = options.linkit;
    var linkify = options.linkify;
    var linkSuffix = options.linkSuffix;
    var style = options.style;
    var style_class = options.style_class;

    var html = "";
    if (typeof obj != "undefined" && obj !== "") {
        if (header) {
            html+="<h5>";
        }
        if (title){
            if (noBold){
                html+= title +": ";
            } else {
                html+= "<b>"+title+":</b> ";
            }
        }
        if (obj.toString) {
            var text = obj.toString();
            if (linkify || linkit) {
                html += "<a target='_new' href='"+ (linkit || text);
                if (linkSuffix){
                    html += linkSuffix;
                }
                html += "'>" + text + "</a>";
            } else {
                html += text;
            }
        } else {
            log.error("Something was sent to a layer info area that wasn't valid text");
            html += obj || "";
        }
        if (header) {
            html+="</h5>";
        }
        if ((style || style_class) && html){
            var style_input = "";
            if (style) {
                style = style.replace(/'/g, '"');
                style_input += " style='"+style+"'";
            }
            if (style_class) {
                style_input += " class='"+style_class+"'";
            }
            html = "<span "+style_input+">"+html+"</span>";
        }
        if (!noBreak && html){
            html += "<br/>";
        }
    }

    return html;
};

leaflet_layer_control.parsers.opacityControls = function(layer) {
    //TODO: Replace this with a slider
    if (!layer || !layer.options || typeof layer.options.opacity=="undefined") {
        return undefined;
    }
    var opacity = Math.round(layer.options.opacity * 100)+"%";
    var $opacity = $('<div>');
    var $opacity_title = $("<span>")
        .html("Opacity: <b>"+opacity+"</b> (")
        .appendTo($opacity);
    _.each([100,75,50,25,0],function(num){
        $("<span>")
            .text(num+"% ")
            .css({color:'#39c',cursor:'pointer'})
            .bind('click mouseup',function(){
                leaflet_layer_control.setLayerOpacity(layer,num/100);
                $opacity_title
                    .html("Opacity: <b>"+(num)+"%</b> (");
            })
            .appendTo($opacity);
    });
    $("<span>")
        .html(")")
        .appendTo($opacity);
    return $opacity;
};

//=========================================
leaflet_layer_control.layerDataList = function (options) {

    var treeData = [];

    var layerGroups = options.layers;

    //For each layer group
    _.each(layerGroups,function(layerGroup,groupNum){
        var layerName = options.titles[groupNum] || "Layers";
        var folderName = "folder."+ groupNum;
        treeData.push({title: layerName, folder: true, key: folderName, children: [], expanded:true });


        var inUSBounds = true;
        if (typeof maptools != "undefined" && aoi_feature_edit.map && aoi_feature_edit.map.getCenter) {
            var center = aoi_feature_edit.map.getCenter();
            inUSBounds = maptools.inUSBounds(center.lat, center.lng);
        }

        //For each layer
        _.each(layerGroup, function (layer, i) {
            var name = layer.name || layer.options.name;
            var layer_obj = {title: name, key: folderName+"."+i, data:layer};

            if (!layer.skipThis) {
                //If there are any later layers with same name/settings, mark them to skip
                leaflet_layer_control.removeDuplicateLayers(layerGroups,layer);

                //Figure out if it is visible and should be "checked"
                var showEvenIfNotInUS = true;
                if (layer.options && layer.options.us_only && !inUSBounds) {
                    showEvenIfNotInUS = false;
                }

                if (showEvenIfNotInUS) {
                    if (layer.getLayers && layer.getLayers() && layer.getLayers()[0]) {
                        var layerItem = layer.getLayers()[0];
                        var options = layerItem._options || layerItem.options;
                        if (options && options.style) {
                            if (options.style.opacity == 1 || options.style.fillOpacity == 1){
                                layer_obj.selected = true;
                            }
                        }
                        if (options && options.opacity && options.opacity == 1) {
                            layer_obj.selected = true;
                        }
                    } else if (layer.options && layer.options.opacity){
                        layer_obj.selected = true;
                    } else if (layer.options && layer.options.is_geoq_feature) {
                        layer_obj.selected = true;
                    }
                }
                if (!layer_obj.selected) {
                    leaflet_layer_control.setLayerOpacity(layer,0);
                }

                //Add this to the json to build the treeview
                treeData[groupNum].children.push(layer_obj);
            }
        },layerGroups);

    },layerGroups);

    //Mark the parent groups as selected or not if all children are
    _.each(treeData,function(treeGroup){
        var anyLayerUnselected = false;
        _.each(treeGroup.children, function (treeItem) {
            if (!treeItem.selected) anyLayerUnselected = true;
        });
        treeGroup.selected = !anyLayerUnselected;
    });


    return treeData;
};
leaflet_layer_control.removeDuplicateLayers = function(layerList, layer){
    var layerSearchStart = false;

    _.each(layerList,function(layerGroup){
        _.each(layerGroup, function (layer_orig, layer_num) {
            if (layerSearchStart) {
                //It's been found previously, so only look at next layers
                var layerLookingAt = layerGroup[layer_num];
                //Check if names exist and are the same
                if (layer.name && layerLookingAt.name) {
                    if (layer.name == layerLookingAt.name) {
                        layerLookingAt.skipThis = true;
                    }
                //Check if the URL and Layer exist and are the same
                } else if (layer.url && layerLookingAt.url && layer.layer && layerLookingAt.layer) {
                    if ((layer.url == layerLookingAt.url) && (layer.layer == layerLookingAt.layer)) {
                        layerLookingAt.skipThis = true;
                    }
                }
            } else {
                if (layer_orig == layer) layerSearchStart = true;
            }
        });
    });
};


leaflet_layer_control.zIndexesOfHighest = 2;
leaflet_layer_control.setLayerOpacity = function (layer, amount){

    if (!layer.options) layer.options={};
    layer.options.opacity = amount;

    if (amount > 0) {
        layer.options.oldOpacity = amount;
    }

    if (layer.setStyle){
        layer.setStyle({opacity:amount, fillOpacity:amount});
    } else if (layer.setOpacity){
        layer.setOpacity(amount);
    }

    if (amount==0){
        if (layer._layers) {
            _.each(layer._layers,function(f){
                $(f._icon).hide();
                if (f._shadow){
                    $(f._shadow).hide();
                }
            });
        }
        if (layer.getContainer) {
            var $lc = $(layer.getContainer());
            $lc.zIndex(1);
            $lc.hide();
        } else if (layer._container) {
            $(layer._container).css('opacity',amount);
        }
    } else {
        if (layer._layers) {
            _.each(layer._layers,function(f){
                $(f._icon).show().css({opacity:amount});
                if (f._shadow){
                    $(f._shadow).show().css({opacity:amount});
                }
            });
        }
        if (layer.getContainer) {
            var $lc = $(layer.getContainer());
            leaflet_layer_control.zIndexesOfHighest++;
            $lc.zIndex(leaflet_layer_control.zIndexesOfHighest);
            $lc.show();
        } else if (layer._container) {
            var $lc = $(layer._container);
            leaflet_layer_control.zIndexesOfHighest++;
            $lc.zIndex(leaflet_layer_control.zIndexesOfHighest);
            $lc.css('opacity',amount);
        }
    }
};

leaflet_layer_control.addLayerControlInfoPanel = function($content){
    var $drawer_inner = $("<div>")
        .addClass("inner-padding")
        .appendTo($content);
    var $drawer_tray = $("<div>")
        .attr({id:"drawer_tray_bottom"})
        .addClass('drawer_tray')
        .appendTo($drawer_inner);

    leaflet_layer_control.$drawer_tray = $drawer_tray;
    $drawer_tray.html("Click a layer above to see more information.");
};

leaflet_layer_control.addLayerControl = function (map, options, $accordion) {

    //Hide the existing layer control
    $('.leaflet-control-layers.leaflet-control').css({display: 'none'});

    var $layerButton = $('<a id="toggle-drawer" href="#" class="btn">Tools <i id="layer-status"> </i><i id="layer-error"> </i></a>');
    var layerButtonOptions = {
        'html': $layerButton,
        'onClick': leaflet_layer_control.toggleDrawer,  // callback function
        'hideText': false,  // bool
        position: 'bottomright',
        'maxWidth': 60,  // number
        'doToggle': true,  // bool
        'toggleStatus': false  // bool
    };
    var layerButton = new L.Control.Button(layerButtonOptions).addTo(map);

    //Build the tree
    var $tree = $("<div>")
        .attr({name: 'layers_tree_control', id:'layers_tree_control'});

    //Build the layer schema
    var treeData = leaflet_layer_control.layerDataList(options);

    $tree.fancytree({
        checkbox: true,
        autoScroll: true,
        selectMode: 2,
        source: treeData,
        activate: function (event, data) {
            //Clicked on a treenode title
            var node = data.node;
            if (node && node.data) {
                leaflet_layer_control.show_info(node.data, node);
            }
        },
        deactivate: function (event, data) {},
        select: function (event, data) {
            // A checkbox has been checked or unchecked
            leaflet_layer_control.drawEachLayer(data,map);
            leaflet_layer_control.lastSelectedNodes = data.tree.getSelectedNodes();
        },
        focus: function (event, data) {},
        blur: function (event, data) {}
    });

    leaflet_layer_control.$tree = $tree;
    leaflet_layer_control.lastSelectedNodes = $tree.fancytree("getTree").getSelectedNodes();

    var $content = leaflet_layer_control.buildAccordionPanel($accordion,"Geo Layers for Map");

    $tree.appendTo($content);

    //TODO: Replace this with a form later to allow user to quick-add layers
    $('<a id="add_layer_button" href="/maps/layers/create" target="_new" class="btn">Add A Layer</a>')
        .appendTo($content);

    leaflet_layer_control.addLayerControlInfoPanel($content)
};
leaflet_layer_control.drawEachLayer=function(data,map){

    var selectedLayers = data.tree.getSelectedNodes();
    var layersUnClicked = _.difference(leaflet_layer_control.lastSelectedNodes, selectedLayers);
    var layersClicked = _.difference(selectedLayers, leaflet_layer_control.lastSelectedNodes);

    _.each(layersUnClicked,function(layer_obj){
        if (layer_obj && layer_obj.data && _.toArray(layer_obj.data).length) {
            var layer = layer_obj.data;
            leaflet_layer_control.setLayerOpacity(layer,0);
        } else if (layer_obj.children && layer_obj.children.length) {
            //A category was clicked
            _.each(layer_obj.children, function(layer_obj_item){
                layer_obj_item.setSelected(false);
            });
        }
    });

    _.each(layersClicked,function(layer_obj){
        if (layer_obj && layer_obj.data && _.toArray(layer_obj.data).length) {
            var layer = layer_obj.data;

            if (layer._map && layer._initHooksCalled) {
                //It's a layer that's been already built
                var oldOpacity = layer.options? layer.options.opacity||layer.options.oldOpacity||1 : 1;
                leaflet_layer_control.setLayerOpacity(layer,oldOpacity);

                if (leaflet_layer_control.likelyHasFeatures(layer)) {
                    leaflet_helper.constructors.geojson(layer.config, map);
                }
            } else {
                //It's an object with layer info, not yet built - build the layer from the config data
                var name = layer.name;
                if (!name && layer.options) name = layer.options.name;
                log.info("Creating a map layer " + name+ " URL: " + layer.url);

                var newLayer = leaflet_helper.layer_conversion(layer, map);
                if (newLayer) {
                    aoi_feature_edit.map.addLayer(newLayer);
                    leaflet_layer_control.setLayerOpacity(newLayer,1);
                    //TODO: Rethink if this should become a sub-item of the object
                    layer_obj.data = newLayer;

                    //Replace the old object list with the new layer
                    _.each(aoi_feature_edit.layers,function(layerGroup,l_i){
                        _.each(layerGroup,function(layerGroupItem,l_l){
                            if (layerGroupItem.id == layer.id) {
                                layerGroup[l_l] = newLayer;
                            }

                        });
                    });

                    //TODO: This should be consolidated into one move event
                    //TODO: The 'refresh layer json' should be a function added to the layer
                    if (layer.type == "Social Networking Link") {
                        leaflet_filter_bar.showInputTags();
                        map.on('moveend viewreset', function (e) {
                            var currentOpacity = 1;
                            if (newLayer.options) {
                                currentOpacity = newLayer.options.opacity;
                            }
                            if (currentOpacity > 0) {
                                leaflet_helper.constructors.geojson(layer, map, newLayer);
                            }
                        });
                    }
                }
            }
            if (layersClicked.length==1){
                layer_obj.setActive();
            }

        } else if (layer_obj.children && layer_obj.children.length) {
            //A category was clicked
            _.each(layer_obj.children, function(layer_obj_item){
                layer_obj_item.setSelected(true);
            });
        } else {
            log.error("A layer with no data was clicked");
        }
    });

};

leaflet_layer_control.toggleZooming=function($control){
    $control.on('mouseover',function(){
        var map=aoi_feature_edit.map;
        map.dragging.disable();
        map.touchZoom.disable();
        map.doubleClickZoom.disable();
        map.scrollWheelZoom.disable();
        if (map.tap) map.tap.disable();}
    ).on('mouseout',function(){
        var map=aoi_feature_edit.map;
        map.dragging.enable();
        map.touchZoom.enable();
        map.doubleClickZoom.enable();
        map.scrollWheelZoom.enable();
        if (map.tap) map.tap.enable();}
    );
};
leaflet_layer_control.likelyHasFeatures = function(layer){
    return ((layer.config && layer.config.type &&
            (layer.config.type=="GeoJSON" || layer.config.type=="Social Networking Link")) ||
            (layer.config && layer.config.format && layer.config.format=="json"));
};

//TODO: Abstract these
leaflet_layer_control.drawerIsOpen = false;
leaflet_layer_control.openDrawer = function() {
    leaflet_layer_control.$map.animate({marginLeft: "300px"}, 300);
    leaflet_layer_control.$map.css("overflow", "hidden");
    leaflet_layer_control.$drawer.animate({marginLeft: "0px"}, 300);
};
leaflet_layer_control.closeDrawer = function() {
    leaflet_layer_control.$map.animate({marginLeft: "0px"}, 300);
    leaflet_layer_control.$map.css("overflow", "auto");
    leaflet_layer_control.$drawer.animate({marginLeft: "-300px"}, 300);
};
leaflet_layer_control.toggleDrawer = function() {
    if(leaflet_layer_control.drawerIsOpen) {
        leaflet_layer_control.closeDrawer();
        leaflet_layer_control.drawerIsOpen = false;
    } else {
        leaflet_layer_control.openDrawer();
        leaflet_layer_control.drawerIsOpen = true;
    }
    setTimeout(aoi_feature_edit.mapResize, 400);
};