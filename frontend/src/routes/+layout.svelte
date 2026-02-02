<script>
  import '../app.css';
</script>

<div class="min-h-screen">
  <!-- Header -->
  <header class="border-b border-viz-border bg-viz-bg/80 backdrop-blur-sm sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
      <a href="/" class="flex items-center gap-3">
        <span class="text-2xl">🎵</span>
        <span class="text-xl font-bold bg-gradient-to-r from-viz-accent to-pink-500 bg-clip-text text-transparent">
          beets-viz
        </span>
      </a>
      <nav class="flex gap-6">
        <a href="/" class="text-gray-400 hover:text-white transition-colors">Dashboard</a>
        <a href="/timeline" class="text-gray-400 hover:text-white transition-colors">Timeline</a>
        <a href="/genres" class="text-gray-400 hover:text-white transition-colors">Genres</a>
        <a href="/labels" class="text-gray-400 hover:text-white transition-colors">Labels</a>
        <a href="/browse" class="text-gray-400 hover:text-white transition-colors">Browse</a>
      </nav>
    </div>
  </header>

  <!-- Main content -->
  <main class="max-w-7xl mx-auto px-4 py-8">
    <slot />
  </main>
</div>
