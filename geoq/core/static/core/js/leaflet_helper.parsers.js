//====================================
leaflet_helper.constructors = {};
leaflet_helper.constructors.identifyParser = function(result){
    //Use GeoJSON as the standard to try if no matches are found
    var parser = L.GeoJSON;
    var parserName = "Leaflet GeoJSON";

    if (result &&
        result.geometryType && result.geometryType == "esriGeometryPoint" &&
        result.features && result.features.length &&
        result.features[0] && result.features[0].attributes) {

        //Parser is CAP imagery Format
        parser = leaflet_helper.parsers.addDynamicCapimageData;
        parserName = "CAP GeoJSON";

    } else if (result &&
        result.stat == "ok" && result.photos && result.photos.page &&
        result.photos.photo && result.photos.perpage) {

        parser = leaflet_helper.parsers.flickrImages;
        parserName = "Flickr Photo Search";
    } else if (result &&
        result.meta && result.meta.code && result.meta.code==200 &&
        result.data && result.data.length) {

        parser = leaflet_helper.parsers.instagramImages;
        parserName = "Instagram Search";
    }
    //ADD new parser detectors here

    return {parser: parser, parserName:parserName};
};


leaflet_helper.constructors.urlTemplater =function(url, map, layer_json){
    if (url.indexOf("{") < 0) return url;

    //Turn search strings into underscore templates to make parseable text (safer than an eval statement)
    _.templateSettings.interpolate = /\{\{(.+?)\}\}/g;
    var _url_template = _.template(url);

    //Get map info that will be added into the url if needed
    var mapExtent=map.getBounds();
    var center = map.getCenter();
    var size = map.getSize();
    var mapState={
        zoom:map.getZoom(),
        lat:center.lat,
        lon:center.lng,
        lng:center.lng,
        n:mapExtent._northEast.lat,
        s:mapExtent._southWest.lat,
        e:mapExtent._northEast.lng,
        w:mapExtent._southWest.lng,
        width:size.x,
        height:size.y,
        radius:2
    };

    //Feed the generated variables into the template, and return the result
    layer_json = $.extend(layer_json,mapState);
    layer_json.tags = layer_json.tags || "disaster";

    var new_url;
    try {
        new_url = _url_template(layer_json);
    } catch (ex) {
        log.error ("Error in parsing a URL template: " + ex.message);
    }

    return new_url || url;
};


leaflet_helper.constructors.geojson = function(options, proxiedURL, map) {
    var outputLayer;

    var resultobj = $.ajax({
        type: 'GET',
        url: proxiedURL,
        dataType: 'json',
        async: false
    });
    //TODO: Switch away from async to sync and run function on success.
    if (resultobj.status == 200) {
        var result;
        try {
            result = JSON.parse(resultobj.responseText);
        } catch (ex){
            log.error("Error parsing JSON returned from server");
        }
        if (result && result.error && result.error.message){
            log.error("JSON layer error, message was:", result.error.message, "url:", proxiedURL);
        } else {
            var parserInfo = leaflet_helper.constructors.identifyParser(result, options);
            if (parserInfo && parserInfo.parser) {
                outputLayer = parserInfo.parser(result, options, map);

                var features = "NONE";
                if (result && result.features && result.features.length) features = result.features.length;
                log.info("JSON layer was created from :", proxiedURL, "features:", features, "parser type:", parserInfo.parserName);

                if (outputLayer) {
                    outputLayer.name = options.name || (options.type+ " layer");
                }
            }
        }
    } else {
        log.error ("A JSON layer was requested, but no valid response was received from the server, result:", resultobj);
    }
    return outputLayer;
};


//====================================
leaflet_helper.parsers = {};
leaflet_helper.parsers.standard_onEachFeature = function (feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
};
leaflet_helper.parsers.addDynamicCapimageData = function (result) {
    var jsonObjects = [];
    $(result.features).each(function () {
        var feature = $(this)[0];
        var popupContent = "<a href='" + feature.attributes.ImageURL + "' target='_new'><img style='width:256px' src='" + feature.attributes.ThumbnailURL + "' /></a>";

        var json = {
            type: "Feature",
            properties: {
                name: feature.attributes.ID + " - " + feature.attributes.DaysOld + " days old",
                image: feature.attributes.ImageURL,
                thumbnail: feature.attributes.ThumbnailURL,
                popupContent: popupContent
            },
            geometry: {
                type: "Point",
                coordinates: [feature.geometry.x, feature.geometry.y]
            }
        };
        jsonObjects.push(json);
    });
    log.info("A FEMA CAP layer was loaded, with", result.features.length, "features");

    return new L.geoJson(jsonObjects, {onEachFeature: leaflet_helper.parsers.standard_onEachFeature});
};
leaflet_helper.parsers.instagramImages = function (result, options, map) {
    var jsonObjects = [];
    var photos = result.data;

    _.each(photos,function(image){

        var imageURL = image.link;
        var thumbnailURL = image.images.thumbnail.url;

        var id = image.id;
        var title = "Instagram: "+id;
        var location = image.location;

        var popupContent = "<h5>Instagram Picture</h5>";
        popupContent += "Posted by: "+image.user.username+"<br/>";
        popupContent += "<a href='" + imageURL + "' target='_new'><img style='width:150px' src='" + thumbnailURL + "' /></a>";
        //TODO: Add Delete this button

        var json = {
            type: "Feature",
            properties: {
                name: title,
                image: imageURL,
                thumbnail: thumbnailURL,
                popupContent: popupContent
            },
            geometry: {
                type: "Point",
                coordinates: [location.longitude, location.latitude]
            }
        };
        jsonObjects.push(json);

    });

    log.info("An Instagram Social Photos layer was loaded, with "+ photos.length+" features");

    return new L.geoJson(jsonObjects, {onEachFeature: leaflet_helper.parsers.standard_onEachFeature});

};
leaflet_helper.parsers.flickrImages = function (result, options, map) {
    var jsonObjects = [];
    var photos = result.photos;

    $(photos.photo).each(function () {
        var feature = $(this)[0];

        var id=feature.id;
        var title=feature.title || "Flickr Photo";
        var secret=feature.secret;
        var server=feature.server;
        var farm=feature.farm;
        var owner=feature.owner;
        var base=id+'_'+secret+'_s.jpg';
        var major=id+'_'+secret+'_z.jpg';
        var imageURL= 'http://farm'+farm+'.static.flickr.com/'+server+'/'+major;
        var thumbnailURL='http://farm'+farm+'.static.flickr.com/'+server+'/'+base;

        var center = map.getCenter();
        var popupContent = "<h5>Flickr Picture</h5>";
        popupContent += "Posted by: "+owner+"<br/>";
        popupContent += "<a href='" + imageURL + "' target='_new'><img style='width:256px' src='" + thumbnailURL + "' /></a>";
        //TODO: Add Delete this button

        var json = {
            type: "Feature",
            properties: {
                name: title,
                image: imageURL,
                thumbnail: thumbnailURL,
                popupContent: popupContent
            },
            geometry: {
                type: "Point",
                coordinates: [center.lng, center.lat] //TODO: Make this either random, or show in a tray to dnd onto map
            }
        };
        jsonObjects.push(json);
    });

    log.info("A Flickr Social Photos layer was loaded, with "+ photos.photo.length+" features");

    return new L.geoJson(jsonObjects, {onEachFeature: leaflet_helper.parsers.standard_onEachFeature});
};