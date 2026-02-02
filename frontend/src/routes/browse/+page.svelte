<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';

  let albums = [];
  let loading = true;
  let searchQuery = '';
  let sortBy = 'added';
  let sortOrder = 'desc';
  let offset = 0;
  let hasMore = true;
  
  // Get filters from URL
  $: urlGenre = $page.url.searchParams.get('genre') || '';
  $: urlLabel = $page.url.searchParams.get('label') || '';
  $: activeFilter = urlGenre ? `Genre: ${urlGenre}` : urlLabel ? `Label: ${urlLabel}` : searchQuery ? `Search: ${searchQuery}` : '';

  async function loadAlbums(reset = false) {
    if (reset) {
      offset = 0;
      albums = [];
    }
    
    loading = true;
    const params = new URLSearchParams({
      limit: '48',
      offset: offset.toString(),
      sort: sortBy,
      order: sortOrder,
    });
    
    if (searchQuery) params.set('search', searchQuery);
    if (urlGenre) params.set('genre', urlGenre);
    if (urlLabel) params.set('label', urlLabel);
    
    const res = await fetch(`/api/albums?${params}`);
    const data = await res.json();
    
    if (reset) {
      albums = data.albums;
    } else {
      albums = [...albums, ...data.albums];
    }
    
    hasMore = data.albums.length === 48;
    loading = false;
  }

  function loadMore() {
    offset += 48;
    loadAlbums();
  }

  function handleSearch() {
    loadAlbums(true);
  }

  function clearFilter() {
    window.location.href = '/browse';
  }

  function handleSort(field) {
    if (sortBy === field) {
      sortOrder = sortOrder === 'desc' ? 'asc' : 'desc';
    } else {
      sortBy = field;
      sortOrder = 'desc';
    }
    loadAlbums(true);
  }

  function getArtUrl(artpath) {
    if (!artpath) return null;
    return `/api/art?path=${encodeURIComponent(artpath)}`;
  }

  onMount(() => {
    loadAlbums(true);
  });
  
  // Reload when URL params change
  $: if (urlGenre || urlLabel) {
    loadAlbums(true);
  }
</script>

<svelte:head>
  <title>Browse | beets-viz</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
    <div>
      <h1 class="text-3xl font-bold mb-2">Browse Albums</h1>
      {#if activeFilter}
        <div class="flex items-center gap-2">
          <span class="text-gray-400">Filtering by:</span>
          <span class="px-3 py-1 bg-viz-accent/20 text-viz-accent rounded-full text-sm flex items-center gap-2">
            {activeFilter}
            <button on:click={clearFilter} class="hover:text-white">✕</button>
          </span>
        </div>
      {/if}
    </div>
    
    <!-- Search & Sort -->
    <div class="flex gap-3">
      <div class="relative">
        <input
          type="text"
          bind:value={searchQuery}
          on:keydown={(e) => e.key === 'Enter' && handleSearch()}
          placeholder="Search..."
          class="bg-viz-card border border-viz-border rounded-lg px-4 py-2 w-64 focus:outline-none focus:border-viz-accent"
        />
        <button 
          class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
          on:click={handleSearch}
        >
          🔍
        </button>
      </div>
      
      <select
        bind:value={sortBy}
        on:change={() => loadAlbums(true)}
        class="bg-viz-card border border-viz-border rounded-lg px-4 py-2 focus:outline-none focus:border-viz-accent"
      >
        <option value="added">Recently Added</option>
        <option value="year">Release Year</option>
        <option value="artist">Artist</option>
        <option value="album">Album Name</option>
      </select>
    </div>
  </div>

  <!-- Album Grid -->
  <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4">
    {#each albums as album}
      <a href="/album/{album.id}" class="group">
        <div class="aspect-square bg-viz-border rounded-lg overflow-hidden mb-2">
          {#if album.artpath}
            <img 
              src={getArtUrl(album.artpath)} 
              alt={album.album}
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
            />
          {:else}
            <div class="w-full h-full flex items-center justify-center text-4xl text-gray-600">
              🎵
            </div>
          {/if}
        </div>
        <div class="truncate text-sm font-medium group-hover:text-viz-accent transition-colors">
          {album.album}
        </div>
        <div class="truncate text-xs text-gray-500">{album.artist}</div>
        <div class="text-xs text-gray-600">{album.year || '—'}</div>
      </a>
    {/each}
  </div>

  <!-- Loading / Load More -->
  {#if loading && albums.length === 0}
    <div class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-viz-accent"></div>
    </div>
  {:else if hasMore}
    <div class="flex justify-center py-8">
      <button
        on:click={loadMore}
        disabled={loading}
        class="px-6 py-3 bg-viz-card border border-viz-border rounded-lg hover:border-viz-accent transition-colors disabled:opacity-50"
      >
        {loading ? 'Loading...' : 'Load More Albums'}
      </button>
    </div>
  {:else if albums.length === 0}
    <div class="text-center py-12 text-gray-400">
      No albums found
    </div>
  {:else}
    <div class="text-center py-8 text-gray-500">
      Showing all {albums.length} albums
    </div>
  {/if}
</div>
