<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Chat Input</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Inter', sans-serif;
      background-color: #212121;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
  </style>
</head>
<body>

<div class="w-full max-w-4xl p-4">
  <div class="bg-zinc-800 rounded-2xl p-4 flex flex-col space-y-4 shadow-2xl">
    <!-- Top section for the input placeholder -->
    <div class="flex-grow">
      <span class="text-zinc-400 text-lg">Send a message</span>
    </div>

    <!-- Bottom section for all the buttons -->
    <div class="flex items-center justify-end space-x-2">
      <!-- Global icon button -->
      <button class="flex-shrink-0 w-10 h-10 rounded-full bg-zinc-700 flex items-center justify-center text-zinc-400 hover:bg-zinc-600 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.23.23-1.82l4.89 4.89-2.73 2.73zM19.79 16c-.22-.64-.49-1.3-.79-2H15l4.13-4.13c.1.91.17 1.83.17 2.78 0 2.21-1.03 4.19-2.63 5.53l.92.92c.62-.62 1.14-1.32 1.55-2.07zM12 4.07c3.95.49 7 3.85 7 7.93 0 .62-.08 1.23-.23 1.82l-4.89-4.89 2.73-2.73zm-8.83 8.83L7 16h5.83l-3.23-3.23L4.17 12.9zM15 17.58l-2.73-2.73L15 12.07l2.73 2.73-2.73 2.73zm2.73-2.73l-2.73 2.73-2.73-2.73 2.73-2.73 2.73 2.73zM12 21.93c-4.9-1.2-8-6-8-10s3.1-8.8 8-10c4.9 1.2 8 6 8 10s-3.1 8.8-8 10zM17.58 15L15 17.58l2.73-2.73-2.73-2.73 2.73 2.73zm-2.73 2.73l-2.73 2.73L12 19.93l2.73-2.73-2.73 2.73z"/>
        </svg>
      </button>

      <!-- Turbo button -->
      <button class="flex items-center px-3 py-2 rounded-full bg-zinc-700 text-zinc-400 hover:bg-zinc-600 transition-colors space-x-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
          <path d="M13 14h-2V9h2v5zm4.29-6.29l-1.41-1.41-2.83 2.83-1.41-1.41L12 6.71l2.83 2.83 1.41-1.41zm-6.58 0L7 9.59l1.41 1.41-2.83 2.83-1.41-1.41L4.71 12 7.54 9.17zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-2-12h4v8h-4v-8z"/>
        </svg>
        <span class="text-sm">Turbo</span>
      </button>

      <!-- Dropdown button -->
      <button class="flex items-center px-3 py-2 rounded-full bg-zinc-700 text-zinc-300 hover:bg-zinc-600 transition-colors space-x-1">
        <span class="text-sm">gpt-oss:20b</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      <!-- Upload button -->
      <button class="flex-shrink-0 w-10 h-10 rounded-full bg-zinc-700 flex items-center justify-center text-zinc-400 hover:bg-zinc-600 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
      </button>
    </div>

  </div>
</div>

</body>
</html>
