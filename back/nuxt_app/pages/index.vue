<template>
  <div class="top_wrapper">
    <div class="company_name_wrapper" v-if="company_name==''">
      <p>会社名を入力</p>
      <input type="text" v-model="inputed_name"  @keydown.enter.prevent="onEnter()">
    </div>
    <div v-else>
      <div class="select_mode_wrapper" v-if="mode==0">
        <div class="mode_item" @click="selectedMode(1)">
          <p>候補日を取得</p>
        </div>
        <div class="mode_item" @click="selectedMode(2)">
          <p>面接日を登録</p>
        </div>
      </div>
      <div v-else>
        <candidateField v-if="mode==1"
          :company-name="company_name"
        />
        <interviewField v-if="mode==2"
          :company-name="company_name"
         />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'IndexPage',
  data(){
    return {
      company_name: "",
      inputed_name: "",
      mode: 0
    }
  },
  methods: {
    selectedMode(mode_num: number){
      this.mode = mode_num
    },
    onEnter(value: string){
      this.company_name = this.inputed_name
    }
  }
})
</script>
