var twitterStream = {};
twitterStream.stream_open = false;
twitterStream.intervalId = undefined;
twitterStream.queryInterval = 1000 * 15;
twitterStream.tweets = [];
twitterStream.tweetFeatures = [];
twitterStream.tweetIndex = 0;
twitterStream.tweetLayer = undefined;


twitterStream.toggleStream = function(_button) {
    console.log("toggling stream...");

    if ( twitterStream.stream_url == undefined ||
        twitterStream.get_tweets_url == undefined ) {
            console.log("Error with ajax urls");
            return;
        }

    // Start leaflet GeoJson layer for Twitter
    if (twitterStream.tweetLayer == undefined) {
        twitterStream.tweetLayer = L.geoJson(false, {
            onEachFeature: function(feature, layer) {
                layer.bindPopup(feature.properties.popupContent);
            },
            filter: function(feature, layer) {
                return (feature.properties.lang === "en") &&
                    (feature.geometry !== null);
            },
            pointToLayer: function(feature, latlng) {
                var icon = L.icon({
                    iconSize: [32, 32],
                    iconAnchor: [13, 27],
                    iconUrl: 'http://png.findicons.com/files/icons/2823/turkuvaz_1/128/twitter.png'
                });

                return L.marker(latlng, {icon: icon});
            }
        }).addTo(aoi_feature_edit.map);
    }

    // if stream is active, close it
    if ( twitterStream.stream_open ) {
        console.log("closing stream...");
        twitterStream.$button.text("Start Stream");
        twitterStream.closeStream();
    } else {
        console.log("starting stream...");
        twitterStream.$button = _button;
        twitterStream.$button.text("Stop Stream");
        twitterStream.startStream();
    }

    twitterStream.stream_open = !this.stream_open;
}

twitterStream.startStream = function() {
    var map = aoi_feature_edit.map;
    if (map && map.getBounds().isValid()) {
        var query_bounds = map.getBounds().toBBoxString();
        twitterStream.query_bounds = query_bounds;

        setTimeout( function() {
            twitterStream.intervalId = twitterStream.getTweets();
        }, 5000 );

        twitterStream.toggleStreamAjaxFunc();

        console.log("Stream Opened");

    } else {
        console.log("Invalid map or bounds!");
    }
}

twitterStream.toggleStreamAjaxFunc = function() {
    jQuery.ajax({
        type: "GET",
        url: twitterStream.stream_url,
        data: {"bounds" : twitterStream.query_bounds},
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(res) {
            if ( res.tweets != undefined ) {
                res.tweets = JSON.parse(res.tweets);
            }
            console.log(res);
        },
        error: function(e, msg) {
            twitterStream.closeStream();
            console.log(e.status + " - " + e.statusText + " [" + msg + "]");
            console.log(e);
        }
    }); //ajax
}

twitterStream.closeStream = function() {
    clearInterval(twitterStream.intervalId);

    twitterStream.toggleStreamAjaxFunc();
    twitterStream.stream_open = false;

    this.$button.prop("disabled", true);
    setTimeout( function() {
        twitterStream.$button.text("Start Stream");
        twitterStream.$button.prop("disabled", false);
        console.log("Ready for streaming");
    }, 5 * 1000);
    console.log("Stream Closed");
}

twitterStream.getTweets = function() {
    var queryId = setInterval( function() {
        console.log("querying Twitter...");
        twitterStream.getTweetsAjaxFunc();
    }, this.queryInterval );

    return queryId;
}

twitterStream.getTweetsAjaxFunc = function() {
    jQuery.ajax({
        type: "GET",
        url: twitterStream.get_tweets_url,
        dataType: "json",
        success: function(res) {
            if (res.server_stream == undefined || !res.server_stream) {
                console.log("server closed stream!");
                twitterStream.closeStream();
            }

            if (res.tweets != undefined && res.tweets != null) {
                res.tweets = JSON.parse(res.tweets);

                if ( res.tweets instanceof Array && res.tweets.length > 0) {
                    twitterStream.tweets.push(res.tweets);
                    twitterStream.addTweetLayer();
                }
            }
            console.log(res);

        },
        error: function(e, msg) {
            twitterStream.closeStream();
            console.log(e.status + " - " + e.statusText + " [" + msg + "]");
            console.log(e);
        }
    }); //ajax
}

twitterStream.addTweetLayer = function() {
    var features = [];

    for (var t of twitterStream.tweets[twitterStream.tweetIndex]) {

        var dateStr = new Date(parseInt(t.timestamp_ms));
        var imageUrl = null;

        var popupContent = '<div class="tweet-popup"><div class="tweet-popup-header">' +
                        '<img src="' + t.user.profile_image_url_https + '"/>' +
                        '<span><h5>@' + t.user.screen_name + '</h5><h6>(' + t.user.name + ')</h6></span></div>' +
                        '<p>' + t.text + '</p><p>Posted today at ' + dateStr.toLocaleTimeString() + '</p>';

        if (t.entities.media != undefined && t.entities.media[0].media_url != undefined &&
            t.entities.media.type === "photo" ) {
                imageUrl = t.entities.media[0].media_url;
                var image = '<img style="width:150px;height:150px;" src="'+imageUrl+'"/>';
                popupContent = popupContent + '<p>' + image + '</p>';
            }

        popupContent = popupContent + '</div>';

        var feature_json = {
            type: "Feature",
            properties: {
                id: twitterStream.tweetIndex,
                text: t.text,
                source: 'Twitter',
                image: imageUrl,
                place: t.place,
                lang: t.lang,
                username: t.user.name,
                screen_name: t.user.screen_name,
                profile_pic_url: t.user.profile_image_url_https,
                twitter_verified: t.user.verified,
                tweet_id: t.id,
                timestamp: t.created_at,
                hashtags: t.entities.hashtags,
                popupContent: popupContent
            },
            // Note: coordinates field is GeoJson ready, the geo field isn't
            // Even though they share the same data (for the most part)
            geometry : t.coordinates,
        }

        features.push(feature_json);
    }
    twitterStream.tweetIndex++;

    console.log("adding data to twitter layer...");
    twitterStream.tweetLayer.addData(features);
}