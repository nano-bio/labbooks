function do_plots(data, fitteddata, substance) {
    var options = {legend: {margin : [15,15]}, crosshair: { mode: "xy" }, grid: { hoverable: true, autoHighlight: false }, selection: {mode: "xy"}};

    var plot = $.plot($("#placeholder"), [{ label: substance+"-: 00.00 eV / 00.00",  data: data, color: "blue"}, { label: "Fit",  data: fitteddata, color: "red"}], options);

    // Create the overview plot
    var  overview = $.plot($("#overview"), [{ label: substance,  data: data, color: "blue"}, { label: "Fit",  data: fitteddata, color: "red"}], {legend: {show: false}, selection: {mode: "xy"}, xaxis: {ticks: 4}, yaxis: {ticks: 4}});

    // this is for the legends of the main plot. has bugs, but not worth fixing atm.

    var legends = $("#placeholder .legendLabel");
    legends.each(function () {
        // fix the widths so they don't jump around
        $(this).css('width', $(this).width());
    });

    var updateLegendTimeout = null;
    var latestPosition = null;
    
    function updateLegend() {
        updateLegendTimeout = null;
        
        var pos = latestPosition;
        
        var axes = plot.getAxes();
        if (pos.x < axes.xaxis.min || pos.x > axes.xaxis.max ||
            pos.y < axes.yaxis.min || pos.y > axes.yaxis.max)
            return;

        var i, j, dataset = plot.getData();
        for (i = 0; i < dataset.length; ++i) {
            var series = dataset[i];

            // find the nearest points, x-wise
            for (j = 0; j < series.data.length; ++j)
                if (series.data[j][0] > pos.x)
                    break;
            
            // now interpolate
            var x, p1 = series.data[j - 1], p2 = series.data[j];
            if (p1 == null)
                x = p2[0];
            else if (p2 == null)
                x = p1[0];
            else
                x = p1[0] + (p2[0] - p1[0]) * (pos.x - p1[0]) / (p2[0] - p1[0]);

            // find the nearest points, y-wise
            for (j = 0; j < series.data.length; ++j)
                if (series.data[j][0] > pos.y)
                    break;

            // now interpolate
            var y, p1 = series.data[j - 1], p2 = series.data[j];
            if (p1 == null)
                y = p2[0];
            else if (p2 == null)
                y = p1[0];
            else
                y = p1[0] + (p2[0] - p1[0]) * (pos.y - p1[0]) / (p2[0] - p1[0]);


            legends.eq(i).text(series.label.replace(/:.*/, ": " + x.toFixed(2) + " eV / " + y.toFixed(2)));
        }
    }
    
    $("#placeholder").bind("plothover",  function (event, pos, item) {
        latestPosition = pos;
        if (!updateLegendTimeout)
            updateLegendTimeout = setTimeout(updateLegend, 50);
    });

    // now connect the main plot and the overview plot

    $("#placeholder").bind("plotselected", function (event, ranges) {
	    // clamp the zooming to prevent eternal zoom

	    if (ranges.xaxis.to - ranges.xaxis.from < 0.00001) {
	    	    ranges.xaxis.to = ranges.xaxis.from + 0.00001;
	    }

	    if (ranges.yaxis.to - ranges.yaxis.from < 0.00001) {
	    	    ranges.yaxis.to = ranges.yaxis.from + 0.00001;
	    }

	    // do the zooming

	    plot = $.plot($("#placeholder"), [{ label: substance+"-: 00.00 eV / 00.00",  data: data, color: "blue"}, { label: "Fit",  data: fitteddata, color: "red"}],
		    $.extend(true, {}, options, {
			    xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to },
			    yaxis: { min: ranges.yaxis.from, max: ranges.yaxis.to }
		    })
	    );

	    // don't fire event on the overview to prevent eternal loop

	    overview.setSelection(ranges, true);
    });

    // we simply send the event over to the main plot (function above)

    $("#overview").bind("plotselected", function (event, ranges) {
	    plot.setSelection(ranges);
    });
    
    // if an unselected event happens, we want both plots to go back to normal (hence clear selection in overview)
    
    $("#overview").bind("plotunselected", function (event, ranges) {
        plot = $.plot($("#placeholder"), [{ label: substance+"-: 00.00 eV / 00.00",  data: data, color: "blue"}, { label: "Fit",  data: fitteddata, color: "red"}], options);
    });
    $("#placeholder").bind("plotunselected", function (event, ranges) {
        plot = $.plot($("#placeholder"), [{ label: substance+"-: 00.00 eV / 00.00",  data: data, color: "blue"}, { label: "Fit",  data: fitteddata, color: "red"}], options);
        overview.clearSelection(true)
    });
};
