<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  let album = null;
  let loading = true;

  $: albumId = $page.params.id;

  onMount(async () => {
    const res = await fetch(`/api/album/${albumId}`);
    album = await res.json();
    loading = false;
  });

  function formatDuration(seconds) {
    if (!seconds) return '—';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  function getArtUrl(artpath) {
    if (!artpath) return null;
    return `/api/art?path=${encodeURIComponent(artpath)}`;
  }
</script>

<svelte:head>
  <title>{album ? `${album.album} - ${album.albumartist}` : 'Album'} | beets-viz</title>
</svelte:head>

{#if loading}
  <div class="flex items-center justify-center h-96">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-viz-accent"></div>
  </div>
{:else if album?.error}
  <div class="text-center py-12">
    <p class="text-2xl text-gray-400">Album not found</p>
    <a href="/browse" class="text-viz-accent hover:underline mt-4 inline-block">← Back to browse</a>
  </div>
{:else if album}
  <div class="space-y-8">
    <!-- Header with album art -->
    <div class="flex flex-col md:flex-row gap-8">
      <div class="w-64 h-64 flex-shrink-0">
        {#if album.artpath}
          <img 
            src={getArtUrl(album.artpath)} 
            alt={album.album}
            class="w-full h-full object-cover rounded-xl shadow-2xl"
          />
        {:else}
          <div class="w-full h-full bg-viz-border rounded-xl flex items-center justify-center text-6xl">
            🎵
          </div>
        {/if}
      </div>
      
      <div class="flex-1">
        <h1 class="text-4xl font-bold mb-2">{album.album}</h1>
        <p class="text-xl text-gray-400 mb-4">{album.albumartist}</p>
        
        <div class="flex flex-wrap gap-4 text-sm">
          {#if album.year}
            <div class="px-3 py-1 bg-viz-card rounded-full border border-viz-border">
              📅 {album.year}
            </div>
          {/if}
          {#if album.genre}
            <div class="px-3 py-1 bg-viz-card rounded-full border border-viz-border">
              🎸 {album.genre}
            </div>
          {/if}
          {#if album.label}
            <a 
              href="/browse?label={encodeURIComponent(album.label)}"
              class="px-3 py-1 bg-viz-card rounded-full border border-viz-border hover:border-viz-accent"
            >
              🏷️ {album.label}
            </a>
          {/if}
          {#if album.country}
            <div class="px-3 py-1 bg-viz-card rounded-full border border-viz-border">
              🌍 {album.country}
            </div>
          {/if}
        </div>
      </div>
    </div>

    <!-- Track list -->
    {#if album.tracks?.length}
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">Tracks ({album.tracks.length})</h2>
        <div class="space-y-1">
          {#each album.tracks as track}
            <div class="flex items-center gap-4 p-2 rounded-lg hover:bg-viz-border/50">
              <div class="w-8 text-center text-gray-500">{track.track || '—'}</div>
              <div class="flex-1 truncate">{track.title}</div>
              <div class="text-gray-500 text-sm">{formatDuration(track.length)}</div>
              {#if track.format}
                <div class="text-xs text-gray-600 uppercase">{track.format}</div>
              {/if}
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Back link -->
    <div>
      <a href="/browse" class="text-viz-accent hover:underline">← Back to browse</a>
    </div>
  </div>
{/if}
