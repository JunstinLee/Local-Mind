# Search Component Library

This directory contains all frontend components for the search functionality. Built with Vue 3, Element Plus, and TailwindCSS, these components provide semantic search capabilities and rich filtering options.

## File Structure

```
fronted/src/components/search/
├── ResultItem.vue          # Search result item component
├── SearchControlPanel.vue  # Search control panel component
├── SearchFilters.vue       # Search filters component
└── SearchResults.vue       # Search results container component
```

## Component Descriptions

### 1. SearchControlPanel.vue
- **Function**: Search control panel, containing the main search input field and filter toggle buttons.
- **Features**:
  - Provides a large text input area for entering search queries.
  - Includes a circular search button and supports Enter-key triggers for searching.
  - Integrates the SearchFilters component to provide filtering options.
  - Responsive design, adapting to different screen sizes.

### 2. SearchFilters.vue
- **Function**: Search filters component, providing various screening criteria.
- **Features**:
  - File type filtering (supports multi-select).
  - Time range filtering (All time, Today, This week, This month, This year).
  - Last modified filtering (Any time, Within 24 hours, Within a week, Within a month).
  - File size filtering (Any size, Less than 1MB, 1-10MB, Greater than 10MB).
  - Reset all filters functionality.

### 3. SearchResults.vue
- **Function**: Search results container component, managing and displaying search results.
- **Features**:
  - Displays search loading states and animations.
  - Shows the number of search results and time-taken information.
  - Provides user-friendly prompts for cases where filtering results in no matches.
  - Displays general "no results" states and the initial state before a search is performed.
  - Result animation effects (fade-in-up).

### 4. ResultItem.vue
- **Function**: Individual search result item component, displaying detailed information for each result.
- **Features**:
  - Displays file names and relevance scores.
  - Supports content preview, displaying up to 3 lines.
  - Highlights content matching the search query.
  - Displays document source information.
  - Responsive design and dark mode support.
  - Hover effects (shadow changes, border color shifts, slight upward movement).

## Design Principles

1. **Responsive Design**: All components adapt to different screen sizes.
2. **Dark Mode**: Supports dark themes to provide a better nighttime user experience.
3. **User Experience**: Provides friendly prompts for loading, empty, and error states.
4. **Performance Optimization**: Uses techniques like virtual scrolling to ensure smoothness for large lists.
5. **Accessibility**: Follows accessibility best practices, including appropriate labels and ARIA attributes.

## Usage

These components are typically combined in a search page:

```vue
<template>
  <div class="search-container">
    <SearchControlPanel />
    <SearchResults />
  </div>
</template>
```

SearchControlPanel contains the search input and filtering options, while SearchResults displays the results. Both components use Pinia stores for state management to ensure data synchronization and communication.

## Tech Stack

- Vue 3 Composition API
- Element Plus UI Library
- TailwindCSS Styling Framework
- Pinia State Management
- Lucide Vue Next Icons
- Vue I18n Internationalization
