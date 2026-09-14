<template>
  <Transition name="configure-dialog">
    <div
      v-if="dialog"
      class="configure-dialog-shell"
      role="dialog"
      aria-modal="true"
    >
      <div class="configure-dialog-backdrop" @click="dialog = false" />
      <v-card
        class="configure-dialog-card"
        prepend-icon="mdi-tune-variant"
        title="Test Configuration"
      >
        <v-card-text class="configure-dialog-fields">
          <div v-if="node" class="text-body-medium-emphasis">
            Configuring <strong>{{ node.name }}</strong>
            <div class="text-caption">{{ node.path }}</div>
          </div>
          <v-row density="comfortable">
            <v-col cols="12" lg="12" md="4" sm="6">
              <v-text-field
                v-model="form.networkTopology"
                hint="输入形式: .../env/*.enx"
                label="Network Topology(.enx)*"
                required
              />
            </v-col>

            <v-col cols="12" lg="12" md="4" sm="6">
              <v-text-field
                v-model="form.spirentConfig"
                hint="输入形式: .../spirent/*.xml"
                label="Spirent TestCenter配置文件(.xml)*"
                required
              />
            </v-col>

            <v-col cols="12" lg="12" md="4" sm="6">
              <v-text-field
                v-model="form.testCase"
                hint="输入形式: test_*"
                label="测试用例名称*"
                required
              />
            </v-col>

            <v-col cols="12" lg="12" md="4" sm="6">
              <v-text-field
                v-model="form.reportPath"
                hint="输入形式: .../report/*.docx"
                label="输出报告路径*"
                type="text"
                required
              />
            </v-col>

            <v-col cols="12" lg="12" md="4" sm="6">
              <v-text-field
                v-model="form.platformPath"
                hint="输入形式: /../../iats-poc/"
                label="测试平台路径*"
                type="text"
                required
              />
            </v-col>

            <v-col cols="12" lg="12" sm="6">
              <v-select
                v-model="form.projectName"
                :items="dataset"
                label="项目名称*"
                required
              />
            </v-col>

            <!--            <v-col cols="12" sm="6">-->
            <!--              <v-autocomplete-->
            <!--                :items="[-->
            <!--                  'Skiing',-->
            <!--                  'Ice hockey',-->
            <!--                  'Soccer',-->
            <!--                  'Basketball',-->
            <!--                  'Hockey',-->
            <!--                  'Reading',-->
            <!--                  'Writing',-->
            <!--                  'Coding',-->
            <!--                  'Basejump',-->
            <!--                ]"-->
            <!--                label="Interests"-->
            <!--                auto-select-first-->
            <!--                multiple-->
            <!--              />-->
            <!--            </v-col>-->
          </v-row>

          <small class="text-body-small text-medium-emphasis"
            >*indicates required field</small
          >
        </v-card-text>

        <v-divider />

        <v-card-actions>
          <v-spacer />

          <v-btn text="Close" variant="plain" @click="dialog = false" />

          <v-btn color="primary" text="Save" variant="tonal" @click="onSave" />
        </v-card-actions>
      </v-card>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { AutomationNode } from '../features/file-manager/types'

const BACKEND_URL = 'http://x.x.x.x:5000/api'
const postResponse = ref('')
const form = ref({
  networkTopology: '',
  spirentConfig: '',
  testCase: '',
  reportPath: '',
  platformPath: '',
  projectName: '',
})

const props = defineProps<{
  modelValue: boolean
  node?: AutomationNode | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const onSave = async () => {
  dialog.value = false
  console.log('hi this is saving')
  try {
    if (Object.values(form.value).some((val) => !val)) {
      alert('请填写所有必填字段！')
      return
    }

    try {
      const response = await fetch(`${BACKEND_URL}/submit/save-config`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Tells Flask to expect JSON
        },
        body: JSON.stringify(form.value), // Must stringify the body
      })

      if (!response.ok) {
        throw new Error('Network response error!')
      }

      const data = await response.json()
      postResponse.value = data.message
      console.log('message:', postResponse.value)
    } catch (error) {
      console.error('Error sending data:', error)
    }
  } catch (error) {
    console.error('保存配置失败', error)
  }
}

const dialog = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value),
})
const dataset = [
  'service_DCN_CTTL_certification',
  'service_DCN_DY',
  'service_DCN_didi2025',
  'service_DCN_bilibili2024',
  'service_DCN_wangyi2024',
]
</script>
