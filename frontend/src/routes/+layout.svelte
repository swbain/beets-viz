<script>
  import '../app.css';
</script>

<div class="min-h-screen">
  <!-- Header -->
  <header class="border-b border-viz-border sticky top-0 z-50 bg-viz-bg">
    <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="/" class="text-lg font-medium text-white hover:text-gray-300 transition-colors">
        pavlovsfrog-music
      </a>
      <nav class="flex gap-5 text-sm">
        <a href="/" class="text-gray-500 hover:text-white transition-colors">Dashboard</a>
        <a href="/timeline" class="text-gray-500 hover:text-white transition-colors">Timeline</a>
        <a href="/genres" class="text-gray-500 hover:text-white transition-colors">Genres</a>
        <a href="/labels" class="text-gray-500 hover:text-white transition-colors">Labels</a>
        <a href="/browse" class="text-gray-500 hover:text-white transition-colors">Browse</a>
      </nav>
    </div>
  </header>

  <!-- Main content -->
  <main class="max-w-6xl mx-auto px-4 py-6">
    <slot />
  </main>
</div>
