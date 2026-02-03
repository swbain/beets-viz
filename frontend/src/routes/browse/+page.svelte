<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';

  let albums = [];
  let total = 0;
  let loading = true;
  let searchQuery = '';
  let sortBy = 'added';
  let sortOrder = 'desc';
  let offset = 0;
  let limit = 48;
  
  $: urlGenre = $page.url.searchParams.get('genre') || '';
  $: urlLabel = $page.url.searchParams.get('label') || '';
  $: urlCountry = $page.url.searchParams.get('country') || '';
  $: activeFilter = urlGenre || urlLabel || urlCountry || '';
  $: totalPages = Math.ceil(total / limit);
  $: currentPage = Math.floor(offset / limit) + 1;

  async function loadAlbums(reset = false) {
    if (reset) offset = 0;
    loading = true;
    
    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString(),
      sort: sortBy,
      order: sortOrder,
    });
    
    if (searchQuery) params.set('search', searchQuery);
    if (urlGenre) params.set('genre', urlGenre);
    if (urlLabel) params.set('label', urlLabel);
    if (urlCountry) params.set('country', urlCountry);
    
    const res = await fetch(`/api/albums?${params}`);
    const data = await res.json();
    
    albums = data.albums;
    total = data.total;
    loading = false;
  }

  function handleSearch() {
    loadAlbums(true);
  }

  function clearFilter() {
    window.location.href = '/browse';
  }

  function goToPage(p) {
    offset = (p - 1) * limit;
    loadAlbums();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function getArtUrl(artpath) {
    if (!artpath) return null;
    return `/api/art?path=${encodeURIComponent(artpath)}`;
  }

  onMount(() => loadAlbums(true));
  $: if (urlGenre || urlLabel || urlCountry) loadAlbums(true);
</script>

<svelte:head>
  <title>Browse | pavlovsfrog-music</title>
</svelte:head>

<div class="space-y-5">
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
    <div>
      <h1 class="text-2xl font-medium mb-1">Browse</h1>
      <p class="text-gray-500 text-sm">
        {#if activeFilter}
          Filtering: {urlGenre || urlLabel || urlCountry}
          <button on:click={clearFilter} class="text-gray-400 hover:text-white ml-2">clear</button>
        {:else}
          {total.toLocaleString()} albums
        {/if}
      </p>
    </div>
    
    <div class="flex gap-2">
      <input
        type="text"
        bind:value={searchQuery}
        on:keydown={(e) => e.key === 'Enter' && handleSearch()}
        placeholder="Search..."
        class="bg-viz-card border border-viz-border rounded px-3 py-1.5 text-sm w-48 focus:outline-none focus:border-gray-500"
      />
      <select
        bind:value={sortBy}
        on:change={() => loadAlbums(true)}
        class="bg-viz-card border border-viz-border rounded px-3 py-1.5 text-sm focus:outline-none focus:border-gray-500"
      >
        <option value="added">Recently Added</option>
        <option value="year">Year</option>
        <option value="artist">Artist</option>
        <option value="album">Title</option>
      </select>
    </div>
  </div>

  {#if loading && albums.length === 0}
    <div class="text-center py-12 text-gray-500">Loading...</div>
  {:else if albums.length === 0}
    <div class="text-center py-12 text-gray-500">No albums found</div>
  {:else}
    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 xl:grid-cols-8 gap-3">
      {#each albums as album}
        <a href="/album/{album.id}" class="group">
          <div class="aspect-square bg-viz-border rounded overflow-hidden mb-1.5">
            {#if album.artpath}
              <img 
                src={getArtUrl(album.artpath)} 
                alt={album.album}
                class="w-full h-full object-cover"
                loading="lazy"
              />
            {:else}
              <div class="w-full h-full flex items-center justify-center text-gray-700 text-2xl">♪</div>
            {/if}
          </div>
          <div class="truncate text-sm group-hover:text-white transition-colors">{album.album}</div>
          <div class="truncate text-xs text-gray-600">{album.artist}</div>
        </a>
      {/each}
    </div>

    {#if totalPages > 1}
      <div class="flex items-center justify-center gap-1 pt-4">
        <button 
          on:click={() => goToPage(currentPage - 1)}
          disabled={currentPage === 1}
          class="px-2 py-1 text-sm text-gray-500 hover:text-white disabled:opacity-30"
        >←</button>
        
        <span class="px-3 py-1 text-sm text-gray-500">
          {currentPage} / {totalPages}
        </span>
        
        <button 
          on:click={() => goToPage(currentPage + 1)}
          disabled={currentPage === totalPages}
          class="px-2 py-1 text-sm text-gray-500 hover:text-white disabled:opacity-30"
        >→</button>
      </div>
    {/if}
  {/if}
</div>
