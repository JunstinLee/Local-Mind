# Common Component Library

This directory contains the application's common components. Built with Vue 3, Element Plus, and TailwindCSS, these components provide a set of reusable UI elements.

## File Structure

```
fronted/src/components/common/
├── APPSetting.vue              # Application settings modal
├── choosefolder.vue            # Folder selection component
├── CompactHeader.vue           # Compact header component
├── FileExport.vue              # File export component
├── FileUploadModal.vue         # File upload modal
├── GlobalNotification.vue      # Global notification component
├── KnowledgeBuildModal.vue     # Knowledge base construction modal
└── LoadingProgressModal.vue    # Loading progress modal
```

## Component Descriptions

### 1. APPSetting.vue
- **Function**: Application settings modal for managing language settings and model management.
- **Features**:
  - Language selection functionality.
  - Displays available models and their details.
  - Supports downloading, activating, and managing models.
  - Shows Hugging Face cache path.
  - Model status management (Active, Downloading, Downloaded, etc.).

### 2. CompactHeader.vue
- **Function**: Compact header component containing navigation tabs and action buttons.
- **Features**:
  - Title and navigation tabs integrated into a single row.
  - Includes buttons for file upload, knowledge base construction, theme switching, and settings.
  - Responsive design.
  - Integrated with the routing system.

### 3. FileUploadModal.vue
- **Function**: File upload modal supporting both file and folder uploads.
- **Features**:
  - Drag-and-drop support.
  - Folder upload support.
  - File list preview.
  - File information display (name, size).
  - Upload progress display.

### 4. KnowledgeBuildModal.vue
- **Function**: Knowledge base construction modal displaying file processing progress.
- **Features**:
  - Overall progress bar display.
  - Individual file processing status.
  - Processing state management (Pending, Processing, Completed, Error).
  - File details and error message display.

### 5. GlobalNotification.vue
- **Function**: Global notification component providing a unified notification display.
- **Features**:
  - Supports Success and Error notification types.
  - Animation transition effects.
  - Automatic centered positioning.
  - Configurable notification duration.

### 6. LoadingProgressModal.vue
- **Function**: Loading progress modal displaying backend initialization status.
- **Features**:
  - Displays model loading status.
  - Displays ChromaDB initialization status.
  - Displays search service initialization status.
  - Overall progress calculation.
  - Automatic backend status checking.

### 7. FileExport.vue
- **Function**: File export component supporting batch file exports.
- **Features**:
  - File and folder selection.
  - Export statistics (file count, total size).
  - Selected file list display.
  - Export format selection.
  - Export option configuration.

### 8. choosefolder.vue
- **Function**: Folder selection component providing a folder picker interface.
- **Features**:
  - Folder selection dialog.
  - Folder information display (name, file count, total size).
  - Folder size calculation.
  - Folder selection event triggers.

## Design Principles

1. **Reusability**: All components are designed to be reused throughout the application.
2. **Responsive Design**: All components adapt to different screen sizes.
3. **Dark Mode**: All components support dark theme.
4. **User Experience**: Provides clear visual feedback and status indicators.
5. **Accessibility**: Follows accessibility best practices.

## Usage

These common components are reused across various parts of the application:

```vue
<template>
  <div class="app-container">
    <CompactHeader />
    <FileUploadModal />
    <KnowledgeBuildModal />
    <GlobalNotification />
    <APPSetting />
    <LoadingProgressModal />
  </div>
</template>
```

Each component uses Pinia stores for state management, ensuring communication and data synchronization between components.

## Tech Stack

- Vue 3 Composition API
- Element Plus UI Library
- TailwindCSS Framework
- Pinia State Management
- Lucide Vue Next Icons
- Vue I18n Internationalization
