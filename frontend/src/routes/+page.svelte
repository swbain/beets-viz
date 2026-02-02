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

<div class="space-y-8">
  <!-- Header -->
  <div>
    <h1 class="text-3xl font-bold mb-2">Your Music Library</h1>
    <p class="text-gray-400">Explore your beets collection</p>
  </div>

  <!-- Stats Grid -->
  {#if loading}
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      {#each Array(4) as _}
        <div class="card animate-pulse h-32"></div>
      {/each}
    </div>
  {:else if stats}
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard 
        label="Albums" 
        value={stats.total_albums.toLocaleString()} 
        icon="💿"
      />
      <StatCard 
        label="Tracks" 
        value={stats.total_tracks.toLocaleString()} 
        icon="🎵"
      />
      <StatCard 
        label="Artists" 
        value={stats.total_artists.toLocaleString()} 
        icon="🎤"
      />
      <StatCard 
        label="Hours" 
        value={stats.total_duration_hours.toLocaleString()} 
        icon="⏱️"
      />
    </div>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard 
        label="Genres" 
        value={stats.total_genres.toLocaleString()} 
        icon="🎸"
        size="small"
      />
      <StatCard 
        label="Labels" 
        value={stats.total_labels.toLocaleString()} 
        icon="🏷️"
        size="small"
      />
      <StatCard 
        label="Earliest" 
        value={stats.year_range.min} 
        icon="📅"
        size="small"
      />
      <StatCard 
        label="Latest" 
        value={stats.year_range.max} 
        icon="✨"
        size="small"
      />
    </div>
  {/if}

  <!-- Charts Row -->
  <div class="grid md:grid-cols-2 gap-6">
    <div class="card">
      <h2 class="text-xl font-semibold mb-4">By Decade</h2>
      <DecadeChart />
    </div>
    <div class="card">
      <h2 class="text-xl font-semibold mb-4">Top Artists</h2>
      <TopArtists />
    </div>
  </div>

  <!-- Recent Albums -->
  <div class="card">
    <h2 class="text-xl font-semibold mb-4">Recently Added</h2>
    <RecentAlbums />
  </div>
</div>
