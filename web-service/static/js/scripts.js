async function fetchData() {
    const response = await fetch('/api/message');
    const data = await response.json();
    return data;
}

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
        .text(d => `${d.data[0]}: ${(d.data[1] / data.length * 100).toFixed(1)}%`);

    const legend = svg.append("g")
        .attr("transform", `translate(${width / 2 + 20}, ${-height / 2 + 10})`);

    legend.selectAll("rect")
        .data(sentimentCounts.keys())
        .enter()
        .append("rect")
        .attr("x", 0)
        .attr("y", (d, i) => i * 20)
        .attr("width", 10)
        .attr("height", 10)
        .attr("fill", d => color(d));

    legend.selectAll("text")
        .data(sentimentCounts.keys())
        .enter()
        .append("text")
        .attr("x", 20)
        .attr("y", (d, i) => i * 20 + 9)
        .text(d => d);
}

function createLineChart(data) {
    const sentimentByDate = d3.rollup(data, v => d3.mean(v, d => d.sentiment_score), d => new Date(d.created_at));

    const margin = { top: 20, right: 30, bottom: 30, left: 40 },
        width = 600 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const x = d3.scaleTime()
        .domain(d3.extent(sentimentByDate.keys()))
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([-1, 1])
        .range([height, 0]);

    const svg = d3.select("#sentiment-line")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append("g")
        .call(d3.axisLeft(y));

    const line = d3.line()
        .x(d => x(d[0]))
        .y(d => y(d[1]));

    svg.append("path")
        .datum(Array.from(sentimentByDate))
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", line);
}

function createBarChart(data) {
    const sentimentCounts = d3.rollup(data, v => v.length, d => d.sentiment_text);

    const margin = { top: 20, right: 30, bottom: 40, left: 90 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#sentiment-bar")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear()
        .domain([0, d3.max(Array.from(sentimentCounts.values()))])
        .range([0, width]);

    const y = d3.scaleBand()
        .range([0, height])
        .domain(sentimentCounts.keys())
        .padding(.1);

    svg.append("g")
        .call(d3.axisLeft(y));

    svg.selectAll("rect")
        .data(Array.from(sentimentCounts))
        .enter()
        .append("rect")
        .attr("x", x(0))
        .attr("y", d => y(d[0]))
        .attr("width", d => x(d[1]))
        .attr("height", y.bandwidth())
        .attr("fill", d => color(d[0]));
}

function createWordCloud(data) {
    const stopWords = new Set([
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
        "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
        "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which",
        "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
        "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
        "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by",
        "for", "with", "about", "against", "between", "into", "through", "during", "before",
        "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
        "under", "again", "further", "then", "once", "here", "there", "when", "where", "why",
        "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
        "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can",
        "will", "just", "don", "should", "now"
    ]);

    const words = data.flatMap(d => d.text.split(" "))
        .map(word => word.toLowerCase().replace(/[^a-zA-Z0-9]/g, ''))
        .filter(word => word.length > 2 && !stopWords.has(word));

    const frequency = Array.from(d3.rollup(words, v => v.length, d => d))
        .sort((a, b) => b[1] - a[1])
        .slice(0, 100)
        .map(([word, freq]) => ({ text: word, size: freq }));

    const width = 600, height = 400;

    const layout = d3.layout.cloud()
        .size([width, height])
        .words(frequency)
        .padding(5)
        .rotate(() => ~~(Math.random() * 2) * 90)
        .font("Impact")
        .fontSize(d => d.size * 10)  // Adjust the size multiplier as needed
        .on("end", draw);

    layout.start();

    function draw(words) {
        d3.select("#word-cloud")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${width / 2}, ${height / 2})`)
            .selectAll("text")
            .data(words)
            .enter()
            .append("text")
            .style("font-size", d => `${d.size}px`)
            .style("font-family", "Impact")
            .attr("text-anchor", "middle")
            .attr("transform", d => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
            .text(d => d.text);
    }
}

function createScatterPlot(data) {
    const margin = { top: 20, right: 30, bottom: 40, left: 90 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#sentiment-scatter")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear()
        .domain([-1, 1])
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.sentiment_magnitude)])
        .range([height, 0]);

    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append("g")
        .call(d3.axisLeft(y));

    svg.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => x(d.sentiment_score))
        .attr("cy", d => y(d.sentiment_magnitude))
        .attr("r", 5)
        .style("fill", d => color(d.sentiment_text));
}

function createHeatmap(data) {
    const margin = { top: 20, right: 30, bottom: 40, left: 90 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#sentiment-heatmap")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const heatmapData = Array.from(d3.rollups(data, v => v.length, d => d.created_at, d => d.sentiment_text))
        .map(([date, sentiments]) => sentiments.map(([sentiment, count]) => ({
            date: new Date(date),
            sentiment: sentiment,
            intensity: count
        }))).flat();

    const x = d3.scaleBand()
        .domain(heatmapData.map(d => d.date))
        .range([0, width])
        .padding(0.01);

    const y = d3.scaleBand()
        .domain(heatmapData.map(d => d.sentiment))
        .range([height, 0])
        .padding(0.01);

    const colorScale = d3.scaleSequential()
        .interpolator(d3.interpolateBlues)
        .domain([0, d3.max(heatmapData, d => d.intensity)]);

    svg.selectAll()
        .data(heatmapData, d => d.date + ':' + d.sentiment)
        .enter()
        .append("rect")
        .attr("x", d => x(d.date))
        .attr("y", d => y(d.sentiment))
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .style("fill", d => colorScale(d.intensity));

    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%Y-%m-%d")));

    svg.append("g")
        .call(d3.axisLeft(y));
}

function displayExampleTweets(data) {
    const positiveTweets = data.filter(d => d.sentiment_text === 'positive')
        .sort((a, b) => b.sentiment_magnitude - a.sentiment_magnitude)
        .slice(0, 5);
    const negativeTweets = data.filter(d => d.sentiment_text === 'negative')
        .sort((a, b) => b.sentiment_magnitude - a.sentiment_magnitude)
        .slice(0, 5);
    const neutralTweets = data.filter(d => d.sentiment_text === 'neutral')
        .sort(() => 0.5 - Math.random())
        .slice(0, 5);

    positiveTweets.forEach(tweet => {
        d3.select("#positive-tweets").append("div").attr("class", "tweet-box").text(tweet.text);
    });

    negativeTweets.forEach(tweet => {
        d3.select("#negative-tweets").append("div").attr("class", "tweet-box").text(tweet.text);
    });

    neutralTweets.forEach(tweet => {
        d3.select("#neutral-tweets").append("div").attr("class", "tweet-box").text(tweet.text);
    });
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
