# Traditional Component Library

This directory contains all frontend components for traditional file management functionality. Built with Vue 3, Element Plus, and TailwindCSS, these components provide traditional file browsing, filtering, and management features.

## File Structure

```
fronted/src/components/traditional/
├── DocItem.vue           # Document item display component
├── FileTree.vue          # File tree structure display component
└── TraditionalFilter.vue # Traditional filter component
```

## Component Descriptions

### 1. DocItem.vue
- **Function**: Document list item component, displaying detailed information for a single document.
- **Features**:
  - Displays document name, modification date, size, and path.
  - Formatted date and file size display.
  - Provides document detail viewing and deletion actions.
  - Responsive design, adapting to different screen sizes.
  - Dark mode support.

### 2. FileTree.vue
- **Function**: File tree structure display component, showing files and folders in a hierarchical tree.
- **Features**:
  - Recursive rendering of file tree structures.
  - Supports folder expansion/collapsing.
  - Different file types use color-coded icons.
  - Displays file count statistics.
  - Responsive design and dark mode support.

### 3. TraditionalFilter.vue
- **Function**: Traditional filter component, providing keyword and file type filtering capabilities.
- **Features**:
  - Modal-based filter settings interface.
  - Supports keyword search.
  - Multi-select for file types (PDF, DOCX, TXT, MD, etc.).
  - Visual representation of selected filter criteria.
  - Filter reset and apply functionality.
  - Integrated with file storage state.

## Design Principles

1. **Responsive Design**: All components adapt to different screen sizes.
2. **Dark Mode**: Supports dark themes to provide a better nighttime user experience.
3. **User Experience**: Provides friendly prompts for loading, empty, and error states.
4. **Performance Optimization**: Uses techniques like virtual scrolling to ensure smoothness for large lists.
5. **Accessibility**: Follows accessibility best practices, including appropriate labels and ARIA attributes.

## Usage

These components are typically combined in a traditional file management page:

```vue
<template>
  <div class="traditional-container">
    <TraditionalFilter @filters-changed="handleFiltersChange" />
    <FileTree :treeData="fileTreeData" :isLoading="isLoading" />
    <DocItem :documents="filteredDocuments" :isLoading="isLoading" />
  </div>
</template>
```

Components communicate and manage state through Pinia stores to ensure data synchronization.

## Tech Stack

- Vue 3 Composition API
- Element Plus UI Library
- TailwindCSS Styling Framework
- Pinia State Management
- Lucide Vue Next Icons
- Vue i18n Internationalization

## Component Relationships

- The `TraditionalFilter` component is responsible for setting and managing filter criteria.
- The `FileTree` component displays the file system hierarchy in a tree structure.
- The `DocItem` component displays detailed document information in a list format.
- All components synchronize state through Pinia stores.
