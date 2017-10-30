var margin = {
        top: 50,
        right: 20,
        bottom: 20,
        left: 60
    },
    width = 700 - margin.left - margin.right,
    height = 1000 - margin.top - margin.bottom,
    smallHeight = 200,
    smallWidth = 500;

var xNeg = d3.scaleLinear()
    .range([0, (width / 2) - (width / 50)]);
var xPos = d3.scaleLinear()
    .range([(width / 2) + (width / 50), width]);
var xPts = d3.scaleLinear()
    .range([15, width]);
var y = d3.scaleBand()
    .rangeRound([0, height])
    .paddingInner(0.25)
    .paddingOuter(0.1);
var y1 = d3.scaleBand()
    .paddingInner(0.05);
var xAxisNeg = d3.axisTop(xNeg)
    .ticks(5)
    .tickFormat(d3.format(".0%"));
var xAxisPos = d3.axisTop(xPos)
    .ticks(5)
    .tickFormat(d3.format(".0%"));
var xAxisPts = d3.axisTop(xPts)
    .ticks(5);
var yAxis = d3.axisLeft(y)
    .tickFormat('')
    .tickSize(0);
var colorScale = d3.scaleLinear().range(["red", "grey", "green"]);

var slotChart = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var teamChart = d3.select("#chart").insert("svg", ":first-child")
    .attr("width", smallWidth + margin.left + margin.right)
    .attr("height", smallHeight + margin.top + margin.bottom)
    .style("margin", "auto")
    .style("display", "block")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    .append("g")
    .attr("id", "teamChart");

// d3.json("https://raw.githubusercontent.com/reddigari/football/master/TheOcho2016/Visualizations/wk1.json", function(json) {
d3.json("data/teams_vs_average.json", function(data) {

    var maxPct = d3.max(data, function(d) {
        return d3.max(d.data, function(dd) {
            return Math.abs(dd.Pct);
        });
    });
    var maxPts = d3.max(data, function(d) {
        return d3.max(d.data, function(dd) {
            return dd.FFPts;
        });
    });

    data = data.sort(function(a, b) {return a.Owner > b.Owner});

    xNeg.domain([-maxPct, 0]);
    xPos.domain([0, maxPct]);
    xPts.domain([0, maxPts]);
    colorScale.domain([-maxPct, 0, maxPct]);

    var owners = data.map(function(d) {
        return d.Owner;
    });
    y.domain(owners);
    var slots = data[0].data.map(function(d) {
        return d.Slot;
    });

    y1.rangeRound([0, y.bandwidth()])
        .domain(slots);

    var totals = data.map(function(d) {
        return {
            Owner: d.Owner,
            Record: d.Record,
            Total: d3.sum(d.data, function(d) {
                return d.FFPts;
            })
        }
    });
    totals.sort(function(a, b) {
        return a.Total < b.Total
    });

    var xOrd = d3.scaleBand()
        .rangeRound([0, smallWidth])
        .paddingInner(0.4)
        .paddingOuter(0.3)
        .domain(totals.map(function(d) {
            return d.Owner;
        }));

    var y2 = d3.scaleLinear()
        .range([smallHeight, 0])
        .domain([0, d3.max(totals, function(d) {
            return d.Total;
        }) + 5]);

    var xOrdAxis = d3.axisBottom(xOrd)
        .tickSize(0)
        .tickPadding(5);
    var y2Axis = d3.axisLeft(y2)
        .ticks(4);

    slotChart.append("g")
        .attr("class", "x axis neg")
        .call(xAxisNeg);
    slotChart.append("g")
        .attr("class", "x axis pos")
        .call(xAxisPos);

    var teams = slotChart.selectAll(".team")
        .data(data)
        .enter().append("g")
        .attr("class", "team")
        .attr("transform", function(d) {
            return "translate(0," + y(d.Owner) + ")"
        });

    teams.selectAll(".rect")
        .data(function(d) {
            return d.data;
        })
        .enter().append("rect")
        .attr("class", "rect")
        .attr("y", function(d) {
            return y1(d.Slot)
        })
        .attr("height", y1.bandwidth())
        .attr("x", function(d) {
            return (d.Pct > 0) ? xPos(0) : xNeg(d.Pct);
        })
        .attr("width", function(d) {
            return (d.Pct > 0) ? (xPos(d.Pct) - xPos(0)) : (xNeg(0) - xNeg(d.Pct));
        })
        .style("fill", function(d) {
            return colorScale(d.Pct);
        })
        .on("mouseover", function(d) {
            tooltip.html(d.FFPts.toFixed(1))
                .style("opacity", 0.8)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY) + "px");
        })
        .on("mouseout", function() {
            tooltip.style("opacity", 0);
        });

    teams.selectAll(".posLabel")
        .data(slots)
        .enter().append("text")
        .attr("class", "posLabel")
        .text(function(d) {
            return d;
        })
        .attr("y", function(d) {
            return y1(d) + 0.75 * y1.bandwidth();
        })
        .attr("x", width / 2)
        .attr("font-size", width / 70)
        .attr("text-anchor", "middle");

    slotChart.selectAll(".teamLabel")
        .data(owners)
        .enter().append("text")
        .text(function(d) {
            return d
        })
        .attr("y", function(d) {
            return y(d) + 0.5 * y.bandwidth();
        })
        .attr("x", -15)
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
            return "rotate(-90, -15," + (y(d) + 0.5 * y.bandwidth()) + ")"
        });

    slotChart.selectAll(".divLine")
        .data(owners.slice(1))
        .enter().append("line")
        .attr("class", "divLine")
        .attr("x1", 0)
        .attr("x2", width)
        .attr("y1", function(d) {
            return y(d) - (0.5 * y.paddingInner() * y.bandwidth());
        })
        .attr("y2", function(d) {
            return y(d) - (0.5 * y.paddingInner() * y.bandwidth());
        })
        .style("stroke", "black");

    slotChart.append("text")
        .attr("id", "slotChartTitle")
        .attr("x", width / 2)
        .attr("y", -margin.top / 1.5)
        .text("Difference from League Average by Position")
        .attr("font-size", "12")
        .attr("text-anchor", "middle")

    teamChart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + smallHeight + ")")
        .call(xOrdAxis);
    teamChart.append("g")
        .attr("class", "y axis")
        .call(y2Axis)
        .append("text")
        .text("Average Fantasy Points")
        .attr("dx", -0.5 * smallHeight)
        .attr("dy", -0.5 * margin.left)
        .attr("transform", "rotate(-90)")
        .attr("font-size", 12)
        .style("fill", "black")
        .attr("text-anchor", "middle");
    teamChart.append("text")
        .attr("id", "lgAveLabel")
        .attr("x", smallWidth)
        .attr("y", y2(d3.mean(totals, function(d) {
            return d.Total;
        })))
        .text("League Average")
        .attr("text-anchor", "end")
        .attr("font-size", 10)
        .style("fill", "red");
    teamChart.append("line")
        .attr("x1", 0)
        .attr("x2", smallWidth - 75)
        .attr("y1", y2(d3.mean(totals, function(d) {
            return d.Total;
        })))
        .attr("y2", y2(d3.mean(totals, function(d) {
            return d.Total;
        })))
        .style("stroke", "red");
    teamChart.selectAll(".rect")
        .data(totals)
        .enter().append("rect")
        .attr("x", function(d) {
            return xOrd(d.Owner);
        })
        .attr("y", function(d) {
            return y2(d.Total);
        })
        .attr("width", xOrd.bandwidth())
        .attr("height", function(d) {
            return smallHeight - y2(d.Total)
        })
        .style("fill", "#8c8c8c");
    teamChart.selectAll(".ptsLabel")
        .data(totals)
        .enter().append("text")
        .attr("x", function(d) {
            return xOrd(d.Owner) + 0.5 * xOrd.bandwidth();
        })
        .attr("y", function(d) {
            return y2(d.Total) + 12;
        })
        .text(function(d) {
            return d.Total.toFixed(1)
        })
        .attr("fill", "white")
        .attr("font-size", 10)
        .attr("text-anchor", "middle");
    teamChart.selectAll(".recordLabel")
        .data(totals)
        .enter().append("text")
        .attr("x", function(d) {
            return xOrd(d.Owner) + 0.5 * xOrd.bandwidth();
        })
        .attr("y", y2(0) - 10)
        .text(function(d) {
            return d.Record
        })
        .attr("fill", "black")
        .attr("font-size", 10)
        .attr("font-weight", "bold")
        .attr("text-anchor", "middle");

});

function switchValues() {
    var vals = d3.select("input[name='values']:checked").property("value");
    var t = d3.transition();

    if (vals == "pts") {
        slotChart.selectAll(".x.axis.neg *")
            .transition(t).remove();
        slotChart.select(".x.axis.pos")
            .transition(t)
            .call(xAxisPts);
        slotChart.selectAll(".posLabel")
            .transition(t)
            .attr("x", 0);
        slotChart.selectAll(".rect")
            .transition(t)
            .attr("x", xPts(0))
            .attr("width", function(d) {
                return xPts(d.FFPts);
            });
        d3.select("#slotChartTitle")
            .text("Average Fantasy Points by Position");
    } else {
        slotChart.select(".x.axis.neg")
            .transition(t)
            .call(xAxisNeg);
        slotChart.select(".x.axis.pos")
            .transition(t)
            .call(xAxisPos);
        slotChart.selectAll(".posLabel")
            .transition(t)
            .attr("x", (width / 2));
        slotChart.selectAll(".rect")
            .transition(t)
            .attr("x", function(d) {
                return (d.Pct > 0) ? xPos(0) : xNeg(d.Pct);
            })
            .attr("width", function(d) {
                return (d.Pct > 0) ? (xPos(d.Pct) - xPos(0)) : (xNeg(0) - xNeg(d.Pct));
            });
        d3.select("#slotChartTitle")
            .text("Difference from League Average by Position");
    };
}

d3.select("input[value='pct']").property("checked", "checked");
d3.select("#chart").insert("hr", "fieldset:first-of-type");

var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

d3.selectAll("#ptsSelect input")
    .on("change", switchValues);