<script>
  import { onMount } from 'svelte';

  let decades = [];
  let maxCount = 0;

  onMount(async () => {
    try {
      const res = await fetch('/api/decades');
      decades = await res.json();
      maxCount = Math.max(...decades.map(d => d.count));
    } catch (e) {
      console.error('Failed to load decades:', e);
    }
  });

  function getDecadeLabel(year) {
    if (!year) return '?';
    return `${year}s`;
  }
</script>

<div class="space-y-2">
  {#each decades as decade}
    <div class="flex items-center gap-3">
      <div class="w-12 text-sm text-gray-400">{getDecadeLabel(decade.decade)}</div>
      <div class="flex-1 h-8 bg-viz-border rounded-lg overflow-hidden">
        <div 
          class="h-full bg-gradient-to-r from-viz-accent to-pink-500 rounded-lg transition-all duration-500"
          style="width: {(decade.count / maxCount) * 100}%"
        >
        </div>
      </div>
      <div class="w-16 text-right text-sm text-gray-400">{decade.count.toLocaleString()}</div>
    </div>
  {/each}
</div>
