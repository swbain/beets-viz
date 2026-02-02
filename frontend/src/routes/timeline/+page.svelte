<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let timeline = [];
  let container;

  onMount(async () => {
    const res = await fetch('/api/timeline');
    timeline = await res.json();
    
    if (timeline.length && container) {
      drawChart();
    }
  });

  function drawChart() {
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Clear previous
    d3.select(container).selectAll('*').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Filter out weird years
    const data = timeline.filter(d => d.year >= 1900 && d.year <= 2030);

    // Scales
    const x = d3.scaleBand()
      .domain(data.map(d => d.year))
      .range([0, width])
      .padding(0.1);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.count)])
      .nice()
      .range([height, 0]);

    // Gradient
    const gradient = svg.append('defs')
      .append('linearGradient')
      .attr('id', 'barGradient')
      .attr('x1', '0%')
      .attr('y1', '0%')
      .attr('x2', '0%')
      .attr('y2', '100%');
    
    gradient.append('stop')
      .attr('offset', '0%')
      .attr('stop-color', '#8b5cf6');
    
    gradient.append('stop')
      .attr('offset', '100%')
      .attr('stop-color', '#6d28d9');

    // Bars
    svg.selectAll('.bar')
      .data(data)
      .join('rect')
      .attr('class', 'bar')
      .attr('x', d => x(d.year))
      .attr('y', height)
      .attr('width', x.bandwidth())
      .attr('height', 0)
      .attr('fill', 'url(#barGradient)')
      .attr('rx', 2)
      .transition()
      .duration(800)
      .delay((d, i) => i * 5)
      .attr('y', d => y(d.count))
      .attr('height', d => height - y(d.count));

    // X Axis (show every 10 years)
    const xAxis = d3.axisBottom(x)
      .tickValues(data.filter(d => d.year % 10 === 0).map(d => d.year));
    
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(xAxis)
      .attr('color', '#6b7280');

    // Y Axis
    svg.append('g')
      .call(d3.axisLeft(y).ticks(5))
      .attr('color', '#6b7280');

    // Tooltip
    const tooltip = d3.select(container)
      .append('div')
      .attr('class', 'absolute bg-viz-card border border-viz-border rounded px-3 py-2 text-sm pointer-events-none opacity-0 transition-opacity')
      .style('z-index', 100);

    svg.selectAll('.bar')
      .on('mouseover', function(event, d) {
        d3.select(this).attr('fill', '#a78bfa');
        tooltip
          .html(`<strong>${d.year}</strong><br/>${d.count} albums`)
          .style('left', (event.offsetX + 10) + 'px')
          .style('top', (event.offsetY - 10) + 'px')
          .style('opacity', 1);
      })
      .on('mouseout', function() {
        d3.select(this).attr('fill', 'url(#barGradient)');
        tooltip.style('opacity', 0);
      });
  }
</script>

<svelte:head>
  <title>Timeline | beets-viz</title>
</svelte:head>

<div class="space-y-6">
  <div>
    <h1 class="text-3xl font-bold mb-2">Release Timeline</h1>
    <p class="text-gray-400">When was your music released?</p>
  </div>

  <div class="card relative" bind:this={container} style="min-height: 450px;">
    {#if !timeline.length}
      <div class="flex items-center justify-center h-96">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-viz-accent"></div>
      </div>
    {/if}
  </div>

  <!-- Stats below chart -->
  {#if timeline.length}
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="card text-center">
        <div class="text-2xl font-bold text-viz-accent">
          {timeline.filter(d => d.year >= 1900 && d.year <= 2030).reduce((a, b) => a.count > b.count ? a : b).year}
        </div>
        <div class="text-gray-400 text-sm">Peak Year</div>
      </div>
      <div class="card text-center">
        <div class="text-2xl font-bold">
          {timeline.filter(d => d.year >= 2020 && d.year <= 2030).reduce((sum, d) => sum + d.count, 0)}
        </div>
        <div class="text-gray-400 text-sm">2020s Albums</div>
      </div>
      <div class="card text-center">
        <div class="text-2xl font-bold">
          {timeline.filter(d => d.year >= 2010 && d.year < 2020).reduce((sum, d) => sum + d.count, 0)}
        </div>
        <div class="text-gray-400 text-sm">2010s Albums</div>
      </div>
      <div class="card text-center">
        <div class="text-2xl font-bold">
          {timeline.filter(d => d.year >= 1900 && d.year < 2000).reduce((sum, d) => sum + d.count, 0)}
        </div>
        <div class="text-gray-400 text-sm">Pre-2000</div>
      </div>
    </div>
  {/if}
</div>
