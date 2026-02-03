<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let countries = [];
  let loading = true;
  let mapContainer;

  const countryNames = {
    'US': 'United States', 'GB': 'United Kingdom', 'JP': 'Japan', 'DE': 'Germany',
    'NZ': 'New Zealand', 'BR': 'Brazil', 'AU': 'Australia', 'CA': 'Canada',
    'FR': 'France', 'XW': 'Worldwide', 'XE': 'Europe', 'AT': 'Austria',
    'NO': 'Norway', 'NL': 'Netherlands', 'SE': 'Sweden', 'IT': 'Italy',
    'ES': 'Spain', 'BE': 'Belgium', 'FI': 'Finland', 'DK': 'Denmark',
    'IE': 'Ireland', 'PT': 'Portugal', 'CH': 'Switzerland', 'PL': 'Poland',
    'RU': 'Russia', 'CN': 'China', 'KR': 'South Korea', 'MX': 'Mexico',
    'AR': 'Argentina', 'CL': 'Chile', 'CO': 'Colombia', 'ZA': 'South Africa',
    'IN': 'India', 'TW': 'Taiwan', 'GR': 'Greece', 'TR': 'Turkey',
    'IS': 'Iceland', 'CZ': 'Czech Republic', 'HU': 'Hungary', 'UA': 'Ukraine',
  };

  // ISO numeric codes (used by Natural Earth / world-atlas)
  const alpha2ToNumeric = {
    'US': '840', 'GB': '826', 'JP': '392', 'DE': '276', 'NZ': '554',
    'BR': '076', 'AU': '036', 'CA': '124', 'FR': '250', 'AT': '040',
    'NO': '578', 'NL': '528', 'SE': '752', 'IT': '380', 'ES': '724',
    'BE': '056', 'FI': '246', 'DK': '208', 'IE': '372', 'PT': '620',
    'CH': '756', 'PL': '616', 'RU': '643', 'CN': '156', 'KR': '410',
    'MX': '484', 'AR': '032', 'CL': '152', 'CO': '170', 'ZA': '710',
    'IN': '356', 'TW': '158', 'GR': '300', 'TR': '792', 'IS': '352',
    'CZ': '203', 'HU': '348', 'UA': '804', 'ID': '360', 'TH': '764',
    'MY': '458', 'PH': '608', 'VN': '704', 'SG': '702', 'EG': '818',
    'NG': '566', 'KE': '404', 'IL': '376', 'RO': '642', 'HR': '191',
  };

  onMount(async () => {
    const res = await fetch('/api/countries');
    countries = await res.json();
    loading = false;
    setTimeout(renderMap, 100);
  });

  async function renderMap() {
    if (!mapContainer || typeof topojson === 'undefined') return;
    
    const width = mapContainer.clientWidth;
    const height = 380;
    
    const world = await d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json');
    const land = topojson.feature(world, world.objects.countries);
    
    // Build lookup by numeric ID
    const countsByNumeric = {};
    countries.forEach(c => {
      const numId = alpha2ToNumeric[c.code];
      if (numId) countsByNumeric[numId] = c.count;
    });
    
    const maxCount = Math.max(...countries.filter(c => alpha2ToNumeric[c.code]).map(c => c.count));
    
    const projection = d3.geoNaturalEarth1().fitSize([width, height], land);
    const path = d3.geoPath(projection);
    
    const svg = d3.select(mapContainer)
      .html('')
      .append('svg')
      .attr('width', width)
      .attr('height', height);
    
    svg.selectAll('path')
      .data(land.features)
      .enter()
      .append('path')
      .attr('d', path)
      .attr('fill', d => {
        const count = countsByNumeric[d.id];
        if (!count) return '#1a1a1a';
        const intensity = Math.log(count + 1) / Math.log(maxCount + 1);
        return d3.interpolate('#2a2a2a', '#888888')(intensity);
      })
      .attr('stroke', '#333')
      .attr('stroke-width', 0.3);
  }

  function getName(code) {
    return countryNames[code] || code;
  }
</script>

<svelte:head>
  <title>Countries | pavlovsfrog-music</title>
  <script src="https://unpkg.com/topojson-client@3"></script>
</svelte:head>

<div class="space-y-6">
  <div>
    <h1 class="text-2xl font-medium mb-1">Countries</h1>
    <p class="text-gray-500 text-sm">Where your music comes from</p>
  </div>

  {#if loading}
    <div class="text-gray-500">Loading...</div>
  {:else}
    <div class="card p-4">
      <div bind:this={mapContainer} class="w-full"></div>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-2">
      {#each countries.slice(0, 30) as country}
        <a 
          href="/browse?country={encodeURIComponent(country.code)}"
          class="flex items-center justify-between p-3 rounded border border-viz-border hover:border-gray-600 transition-colors"
        >
          <span>{getName(country.code)}</span>
          <span class="text-gray-600 text-sm">{country.count}</span>
        </a>
      {/each}
    </div>

    {#if countries.length > 30}
      <details class="card">
        <summary class="cursor-pointer text-gray-500 hover:text-white text-sm">
          + {countries.length - 30} more countries
        </summary>
        <div class="grid md:grid-cols-3 lg:grid-cols-4 gap-2 mt-4">
          {#each countries.slice(30) as country}
            <div class="flex items-center justify-between text-sm py-1">
              <span class="text-gray-400">{getName(country.code)}</span>
              <span class="text-gray-600">{country.count}</span>
            </div>
          {/each}
        </div>
      </details>
    {/if}
  {/if}
</div>
