var margin = {
        top: 30,
        right: 20,
        bottom: 40,
        left: 60
    },
    width = 350 - margin.left - margin.right,
    height = 200 - margin.top - margin.bottom,
    widthBig = 700 - margin.left - margin.right,
    heightBig = 400 - margin.top - margin.bottom;

var y = d3.scaleLinear()
    .range([height, 0]);
var x = d3.scaleBand()
    .rangeRound([0, width])
    .paddingInner(0.55)
    .paddingOuter(0.1);

var xAxis = d3.axisBottom(x)
    .tickSize(0)
    .tickPadding(10);
var yAxis = d3.axisLeft(y)
    .ticks(5);

var xBig = d3.scaleBand()
    .rangeRound([0, widthBig])
    .paddingInner(0.3);
var yBig = d3.scaleLinear()
    .range([heightBig, 0]);
var x1 = d3.scaleBand()
    .domain([0, 1])
    // .rangeRound([0, xBig.bandwidth()])
    .paddingInner(0.05);
var xAxisBig = d3.axisBottom(xBig)
    .tickPadding(18);
var yAxisBig = d3.axisLeft(yBig)
    .ticks(5);

var colors = ["#ff7f0e", "#2ca02c", "#1f77b4", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#b8bf37", "#17becf"]
var colorScale = d3.scaleOrdinal(colors);

function setup() {

    d3.json("wk1.json", function(json) {

        json = json.slice(1).sort(function(a, b) {
            return a.owner > b.owner;
        });

        var teams = d3.select("#chart").selectAll(".teamProj")
            .data(json, function(d) {
                return d.owner;
            })
            .enter().append("svg")
            .attr("id", function(d) {
                return d.owner;
            })
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("class", "teamProj")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        teams.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
        teams.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(-10,0)")
            .call(yAxis);
        teams.append("text")
            .attr("y", 0 - (0.5 * margin.top))
            .text(function(d) {
                return d.owner;
            })
            .attr("text-anchor", "start")
            .attr("font-size", "14")
            .style("fill", function(d) {
                return colorScale(d.owner);
            });
        teams.append("text")
            .attr("class", "projTotal")
            .attr("x", width)
            .attr("y", 0 - (0.5 * margin.top));
        teams.append("text")
            .attr("class", "ptsTotal")
            .attr("x", width)
            .attr("y", 0 - (0.5 * margin.top))
            .attr("dy", 10)

        var league = d3.select("#chart").insert("svg", "svg:first-of-type")
            .attr("width", widthBig + margin.left + margin.right)
            .attr("height", heightBig + margin.top + margin.bottom)
            .append("g")
            .attr("id", "meanChart")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        league.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + heightBig + ")")
            // .attr("transform", "translate(0," + yBig(0) + ")")
            .call(xAxisBig);
        league.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(-10,0)")
            .call(yAxisBig)
            .append("text")
            .attr("y", heightBig / 2)
            .attr("x", -30)
            .attr("fill", "black")
            .style("text-anchor", "middle")
            .text("Fantasy Points")
            .attr("transform", "rotate(-90," + "-30," + heightBig / 2 + ")");
        league.selectAll(".slot")
            .data(json[0].data, function(d) {
                return d.Slot;
            })
            .enter().append("g")
            .attr("class", "slot")
            .attr("id", function(d) {
                return "bars" + d.Slot;
            })
        // .attr("transform", function(d) { return "translate(" + xBig(d.Slot) + ",0)"; });
        league.append("g")
            .attr("class", "legendOrdinal");
        updateChart();
    });
}

// d3.json("https://raw.githubusercontent.com/reddigari/football/master/TheOcho2016/Visualizations/wk3.json", function(json) {
function updateChart() {

    var week = d3.select("#wkSelect").property("value");
    d3.select("#chart h2")
        .html("The Ocho: Week " + week);

    d3.json("wk" + week + ".json", function(json) {

        var timeString = "Projections as of " + json[0].projTime + "<br>Scores as of " + json[0].scoreTime;
        if (json[0].rosterTime != null) timeString = "Rosters as of " + json[0].rosterTime + "<br>" + timeString;
        d3.select("#timeP")
            .html(timeString);
        json = json.slice(1).sort(function(a, b) {
            return a.owner > b.owner;
        });

        json.forEach(function(d) {
            d.data.forEach(function(dd) {
                dd.proj = parseFloat(dd.proj);
                dd.pts = parseFloat(dd.pts);
            });
        });

        var max = d3.max(json, function(d) {
            return d3.max(d.data, function(dd) {
                return d3.max([dd.proj, dd.pts]);
            });
        });
        // var min = d3.min(json, function(d) {
        //     return d3.min(d.data, function(dd) {
        //         return d3.min([dd.proj, dd.pts]);
        //     });
        // });
        // if (min > 0) min = 0;
        // y.domain([min, max]);
        y.domain([0, max]);

        var owners = json.map(function(d) {
            return d.owner;
        });
        colorScale.domain(owners)

        var aveProj = {},
            avePts = {},
            slots = json[0].data.map(function(d) {
                aveProj[d.Slot] = [];
                avePts[d.Slot] = [];
                return d.Slot;
            });

        x.domain(slots)

        var t = d3.transition();

        var teams = d3.select("#chart").selectAll(".teamProj")
            .data(json, function(d) {
                return d.owner;
            });

        teams.selectAll(".x.axis").transition(t).call(xAxis);
        teams.selectAll(".y.axis").transition(t).call(yAxis);

        json.forEach(function(t) {
            t.data.forEach(function(s) {
                aveProj[s.Slot].push(s.proj);
                avePts[s.Slot].push(s.pts);
            });
        });

        var ptsRects = teams.selectAll(".ptsRect")
            .data(function(d) {
                return d.data;
            }, function(d) {
                return d.Slot
            });
        ptsRects.enter().append("rect")
            .attr("class", "ptsRect")
            //   .style("fill", colorScale(d.owner))
            .merge(ptsRects)
            .on("mouseover", function(d) {
                tooltip.html(d.player)
                    .style("opacity", 0.8)
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY) + "px");
            })
            .on("mouseout", function() {
                tooltip.style("opacity", 0);
            })
            .transition(t)
            .attr("x", function(d) {
                return x(d.Slot);
            })
            .attr("width", x.bandwidth())
            .attr("y", function(d) {
                return (isNaN(d.pts)) ? null : y(d.pts);
            })
            .attr("height", function(d) {
                return (isNaN(d.pts)) ? null : height - y(d.pts);
            });



        var projLines = teams.selectAll(".projLine")
            .data(function(d) {
                return d.data;
            }, function(d) {
                return d.Slot;
            });
        projLines.enter().append("line")
            .attr("class", "projLine")
            .merge(projLines)
            .transition(t)
            .style("stroke", "black")
            .attr("x1", function(d) {
                return x(d.Slot);
            })
            .attr("x2", function(d) {
                return x(d.Slot) + x.bandwidth();
            })
            .attr("y1", function(d) {
                return y(d.proj);
            })
            .attr("y2", function(d) {
                return y(d.proj);
            });

        var projLabels = teams.selectAll(".projLabel")
            .data(function(d) {
                return d.data;
            }, function(d) {
                return d.Slot;
            });
        projLabels.enter().append("text")
            .attr("class", "projLabel")
            .merge(projLabels)
            .transition(t)
            .attr("x", function(d) {
                return x(d.Slot) + x.bandwidth() + 2;
            })
            .attr("y", function(d) {
                return y(d.proj) + 3;
            })
            .text(function(d) {
                return d.proj.toFixed(1);
            })
            .attr("text-anchor", "start");

        var ptsLabels = teams.selectAll(".ptsLabel")
            .data(function(d) {
                return d.data;
            }, function(d) {
                return d.Slot;
            });
        ptsLabels.enter().append("text")
            .attr("class", "ptsLabel")
            .merge(ptsLabels)
            // .transition(t)
            .attr("x", function(d) {
                return x(d.Slot) + 0.5 * x.bandwidth();
            })
            .attr("y", function(d) {
                if (d.pts < 0) return y(0);
                else
                    return ((d.pts >= d.proj) || (d.pts <= 2.0)) ? y(d.pts) - 2 : y(d.pts) + 8;
            })
            .text(function(d) {
                return (isNaN(d.pts)) ? null : d.pts.toFixed(1);
            })
            .attr("text-anchor", "middle");

        teams.select(".projTotal")
            .text(function(d) {
                return "Projected: " + d3.sum(d.data, function(d) {
                    return d.proj;
                }).toFixed(1)
            });
        teams.select(".ptsTotal")
            .text(function(d) {
                return "Actual: " + d3.sum(d.data, function(d) {
                    return d.pts;
                }).toFixed(1)
            });

        // transform average data into list and make chart of means
        aveData = slots.map(function(s) {
            var obj = {};
            obj['Slot'] = s;
            obj['proj'] = aveProj[s];
            obj['pts'] = avePts[s];
            // obj['pts'] = avePts[s].filter(function(a) {return !(a==0);});
            return obj;
        });

        xBig.domain(x.domain());
        yBig.domain(y.domain());
        x1.rangeRound([0, xBig.bandwidth()])


        var league = d3.select("#meanChart");
        league.select(".x.axis")
            .call(xAxisBig);
        league.select(".y.axis").transition(t).call(yAxisBig);
        var slotGroups = league.selectAll(".slot")
            .data(aveData, function(d) {
                return d.Slot;
            })
            .attr("transform", function(d) {
                return "translate(" + xBig(d.Slot) + ",0)";
            });

        var meanRects = slotGroups.selectAll(".rect")
            .data(function(d) {
                return [d.proj, d.pts.filter(function(a) {
                    return (!(isNaN(a)));
                })];
            });
        meanRects.enter().append("rect")
            .attr("class", "rect")
            .merge(meanRects)
            .transition(t)
            .attr("x", function(d, i) {
                return x1(i);
            })
            .attr("y", function(d) {
                return (d.length > 0) ? yBig(d3.mean(d)) : null;
            })
            .attr("height", function(d) {
                return (d.length > 0) ? heightBig - yBig(d3.mean(d)) : null;
            })
            .attr("width", x1.bandwidth())
            .style("fill", function(d, i) {
                return ["#bdbdbd", "#9f9f9f"][i]
            });

        var valLabels = slotGroups.selectAll(".valLabel")
            .data(function(d) {
                return [d.proj, d.pts.filter(function(a) {
                    return (!(isNaN(a)));
                })];
            });
        valLabels.enter().append("text")
            .attr("class", "valLabel")
            .merge(valLabels)
            .transition(t)
            .attr("x", function(d, i) {
                return x1(i) + 0.5 * x1.bandwidth();
            })
            .attr("y", yBig(1))
            .text(function(d) {
                return (d.length > 0) ? d3.mean(d).toFixed(1) : null;
            })

        slotGroups.selectAll(".colLabel")
            .data(['Proj.', 'Real'])
            .enter().append("text")
            .attr("class", "colLabel")
            .attr("x", function(d, i) {
                return x1(i) + 0.5 * x1.bandwidth();
            })
            .attr("y", heightBig + 13)
            .text(function(d) {
                return d;
            })

        var markerWidth = 10;
        var projDots = slotGroups.selectAll(".projDot")
            .data(function(d) {
                return d.proj;
            }, function(d, i) {
                return owners[i]
            });
        projDots.enter().append("rect")
            .attr("class", "projDot")
            .merge(projDots)
            .style("fill", function(d, i) {
                return colorScale(owners[i]);
            })
            .style("stroke-width", 0)
            .attr("x", x1(0) + 0.5 * x1.bandwidth() - 0.5 * markerWidth)
            .attr("width", markerWidth)
            .attr("height", 2)
            .transition(t)
            .attr("y", function(d) {
                return yBig(d);
            });
        var ptsDots = slotGroups.selectAll(".ptsDot")
            .data(function(d) {
                return d.pts;
            }, function(d, i) {
                return owners[i]
            });
        ptsDots.enter().append("rect")
            .attr("class", "ptsDot")
            .merge(ptsDots)
            .style("fill", function(d, i) {
                return colorScale(owners[i]);
            })
            .style("stroke-width", 0)
            .attr("x", x1(1) + 0.5 * x1.bandwidth() - 0.5 * markerWidth)
            .attr("width", function(d) {
                return (isNaN(d)) ? 0 : markerWidth
            })
            .attr("height", 2)
            .transition(t)
            .attr("y", function(d) {
                return (isNaN(d)) ? 0 : yBig(d);
            });

        d3.selectAll("#meanChart .x.axis text").attr("font-weight", "bold");
        d3.selectAll(".ptsRect")
            .style("fill", function(d) {
                return colorScale(this.parentNode.parentNode.id);
            });

        var legendOrdinal = d3.legendColor()
            .shape("path", d3.symbol().type(d3.symbolCircle).size(60)())
            .shapePadding(5)
            .scale(colorScale);

        league.select(".legendOrdinal")
            .attr("transform", "translate(" + xBig('K') + ",0)")
            .call(legendOrdinal);

    });

}
var q = window.location.search,
    qWk = q.match(/wk=(\d+)/i);
if (qWk) {
    qWk = qWk[1];
    d3.select("#wk" + qWk).attr("selected", "selected");
};

d3.select("#wkSelect")
    .on("change", updateChart);
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);
setup();
updateChart();