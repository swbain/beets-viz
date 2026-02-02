<script>
  import { onMount } from 'svelte';
  import StatCard from '$lib/components/StatCard.svelte';
  import RecentAlbums from '$lib/components/RecentAlbums.svelte';
  import DecadeChart from '$lib/components/DecadeChart.svelte';
  import TopArtists from '$lib/components/TopArtists.svelte';

  let stats = null;
  let loading = true;

  onMount(async () => {
    try {
      const res = await fetch('/api/stats');
      stats = await res.json();
    } catch (e) {
      console.error('Failed to load stats:', e);
    }
    loading = false;
  });
</script>

<svelte:head>
  <title>Dashboard | pavlovsfrog-music</title>
</svelte:head>

<div class="space-y-6">
  <div>
    <h1 class="text-2xl font-medium mb-1">Library</h1>
    <p class="text-gray-500 text-sm">Your music collection</p>
  </div>

  {#if loading}
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
      {#each Array(4) as _}
        <div class="card h-20 animate-pulse bg-viz-border"></div>
      {/each}
    </div>
  {:else if stats}
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
      <StatCard label="Albums" value={stats.total_albums.toLocaleString()} />
      <StatCard label="Tracks" value={stats.total_tracks.toLocaleString()} />
      <StatCard label="Artists" value={stats.total_artists.toLocaleString()} />
      <StatCard label="Hours" value={stats.total_duration_hours.toLocaleString()} />
    </div>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
      <StatCard label="Genres" value={stats.total_genres.toLocaleString()} size="small" />
      <StatCard label="Labels" value={stats.total_labels.toLocaleString()} size="small" />
      <StatCard label="Earliest" value={stats.year_range.min} size="small" />
      <StatCard label="Latest" value={stats.year_range.max} size="small" />
    </div>
  {/if}

  <div class="grid md:grid-cols-2 gap-4">
    <div class="card">
      <h2 class="text-sm font-medium text-gray-400 mb-4">By Decade</h2>
      <DecadeChart />
    </div>
    <div class="card">
      <h2 class="text-sm font-medium text-gray-400 mb-4">Top Artists</h2>
      <TopArtists />
    </div>
  </div>

  <div class="card">
    <h2 class="text-sm font-medium text-gray-400 mb-4">Recently Added</h2>
    <RecentAlbums />
  </div>
</div>
