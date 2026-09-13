<script setup lang="ts">
import FileTree from '../../features/file-manager/components/FileTree.vue'
import type { AutomationNode } from '../../features/file-manager/types'
import ConfigureDialog from '../../components/ConfigureDialog.vue'

defineProps<{
  uploadedTree: AutomationNode[]
  darkMode: boolean
}>()

const emit = defineEmits<{
  upload: [node: AutomationNode]
  configure: [node: AutomationNode]
  execute: [node: AutomationNode]
}>()
</script>

<template>
  <section class="session-view">
    <div class="session-heading">
      <div>
        <div class="eyebrow">WORKSPACE SESSION</div>
        <h1>File manager</h1>
        <v-btn>configure modal</v-btn>
        <br /><br />
      </div>
    </div>
    <div class="file-manager-session">
      <v-card class="panel file-manager-card" elevation="0">
        <FileTree :nodes="uploadedTree" :dark-mode="darkMode" @upload="emit('upload', $event)"
          @configure="emit('configure', $event)" @execute="emit('execute', $event)" />
      </v-card>
    </div>
    <ConfigureDialog />
  </section>
</template>
