# QA Component Library

This directory contains all core frontend components of the Q&A system. Built with Vue 3, Element Plus, and TailwindCSS, these components implement a complete chat interface.

## File Structure

```
fronted/src/components/qa/
├── ChatSidebar.vue          # Chat sidebar component, manages session history
├── CollapsiblePanel.vue     # Collapsible panel component
├── Input.vue                # User input component, includes model selection and messaging
├── MessageBU.vue            # Message item component, displays single user or AI message
├── MessageList.vue          # Message list component, renders the entire chat history
├── QALayout.vue             # Main layout component for the QA system
├── TypingIndicator.vue      # Typing indicator component, shows AI's thinking state
├── UI_in_QA/               # UI components subdirectory
│   ├── ImagePreview.vue     # Image preview component
│   ├── MarkdownRenderer.vue # Markdown rendering component
│   └── ThinkingChain.vue    # Thinking chain display component
```

## Component Descriptions

### 1. QALayout.vue
- **Function**: Main layout component of the Q&A system, providing the overall page structure.
- **Features**: Includes layouts for the sidebar, message content area, and bottom input box.

### 2. ChatSidebar.vue
- **Function**: Chat sidebar component, managing session history records.
- **Features**:
  - Displays user information.
  - Provides functionality to create new chats.
  - Displays chat history list.
  - Supports sidebar collapse/expand.

### 3. MessageList.vue
- **Function**: Message list container component, managing and rendering the list of chat messages.
- **Features**: Automatically scrolls to the latest message and responds to message list changes.

### 4. MessageBU.vue
- **Function**: Individual message item component, displaying user or AI messages.
- **Features**:
  - Displays different layouts based on the message role (User or AI).
  - Integrates thinking chain display.
  - Supports source information display.
  - Provides "Copy" and "Save As" functionality.
  - Supports Markdown content rendering.

### 5. Input.vue
- **Function**: User input component, providing message input and model selection functionality.
- **Features**:
  - Supports multi-line text input with automatic resizing.
  - Model selection dropdown menu.
  - Enter to send, Shift+Enter for a new line.
  - Send button.

### 6. TypingIndicator.vue
- **Function**: Typing indicator component, displaying the status of the AI generating a response.
- **Features**: Animation effect with three dynamic dots.

### 7. CollapsiblePanel.vue
- **Function**: Collapsible panel component used to save interface space.
- **Features**:
  - Supports left/right position configuration.
  - Controllable expanded/collapsed state.
  - Custom titles.

## UI_in_QA Subdirectory Components

### 1. MarkdownRenderer.vue
- **Function**: Component for safely rendering Markdown content.
- **Features**:
  - Supports code highlighting.
  - XSS protection.
  - Custom padding.

### 2. ThinkingChain.vue
- **Function**: Component for displaying the AI's thinking process.
- **Features**:
  - Expandable/collapsible thinking content.
  - Step label display.
  - Animation transition effects.

### 3. ImagePreview.vue
- **Function**: Image preview component.
- **Features**:
  - Lazy loading.
  - Click to enlarge preview.
  - Loading state display.
  - Error state display.

## Design Principles

1. **Componentization**: Splitting the UI into independent, reusable components.
2. **Responsive**: Adapting to different screen sizes.
3. **Internationalization (i18n)**: Supporting multi-language display.
4. **Accessibility**: Following accessibility best practices.
5. **Performance**: Using techniques like virtual scrolling to handle large amounts of data.

## Usage Example

These components are typically combined in the main page of the Q&A system:

```vue
<template>
  <QALayout>
    <template #messages>
      <MessageList :messages="chatMessages" />
    </template>
    <template #input>
      <Input @send-message="handleSendMessage" />
    </template>
  </QALayout>
</template>
```

Together, these components form a fully functional Q&A interface, supporting model selection, message history, thinking chain display, source citations, and more.
