async function fetchData() {
    const response = await fetch('/api/message');
    const data = await response.json();
    return data;
}

fetchData().then(data => {
    if (data && Array.isArray(data)) {
        createPieChart(data);
        createLineChart(data);
        createBarChart(data);
        createWordCloud(data);
        createScatterPlot(data);
        createHeatmap(data);
        displayExampleTweets(data);
    } else {
        console.error("Invalid data format:", data);
    }
});

const color = d3.scaleOrdinal()
    .domain(['positive', 'negative', 'neutral'])
    .range(['#8FB339', '#E94B3C', '#6E7E85']); // Muted colors

function createPieChart(data) {
    const sentimentCounts = d3.rollup(data, v => v.length, d => d.sentiment_text);

    const width = 400, height = 400, radius = Math.min(width, height) / 2;

    const svg = d3.select("#sentiment-pie")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    const pie = d3.pie().value(d => d[1]);
    const arc = d3.arc().innerRadius(0).outerRadius(radius);

    svg.selectAll('path')
        .data(pie(Array.from(sentimentCounts)))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', d => color(d.data[0]));

    svg.selectAll('text')
        .data(pie(Array.from(sentimentCounts)))
        .enter()
        .append('text')
        .attr('transform', d => `translate(${arc.centroid(d)})`)
        .attr('dy', '0.35em')
        .style('text-anchor', 'middle')
        .text(d => d.data[0]);

    const legend = svg.append("g")
        .attr("transform", `translate(${-width / 2}, ${-height / 2})`);

    legend.selectAll("rect")
        .data(sentimentCounts.keys())
        .enter()
        .append("rect")
        .attr("x", 10)
        .attr("y", (d, i) => 10 + i * 20)
        .attr("width", 10)
        .attr("height", 10)
        .attr("fill", d => color(d));

    legend.selectAll("text")
        .data(sentimentCounts.keys())
        .enter()
        .append("text")
        .attr("
