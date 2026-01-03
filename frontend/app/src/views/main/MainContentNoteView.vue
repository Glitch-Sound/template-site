<script setup lang="ts"></script>

<template>
  <v-row class="note-row" no-gutters justify="center">
    <v-col cols="10" md="3" class="note-col">
      <v-card elevation="3" prepend-icon="mdi-apps">
        <template v-slot:title>
          <span class="font-weight-black">Rule!!</span>
        </template>
        <v-card-text class="mx-5">
          月 ： 棚卸<br />
          水 ： 指摘一次回答<br />
          金 ： 最新化<br />
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="10" md="4" class="note-col">
      <v-card elevation="3" prepend-icon="mdi-apps">
        <template v-slot:title>
          <span class="font-weight-black">Workflow</span>
        </template>
        <v-card-text class="mx-5">
          1.　Setting：顧客情報追加<br />
          2.　Setting：プロジェクトグループ追加<br />
          3.　Project：プロジェクト追加<br />
          4.　Project：Threadより状況報告<br />
          5.　Project：プロジェクト最新化<br /><br />

          <p class="ml-6">※Thread：Importtant ... MNG専用</p>
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="10" md="3" class="note-col">
      <v-card elevation="3" prepend-icon="mdi-apps">
        <template v-slot:title>
          <span class="font-weight-black">Rank</span>
        </template>
        <v-card-text class="mx-5">
          A ： 作業確定 + 正式番号発行<br />
          B ： 作業確定 + 正式番号未発行<br />
          C ： 作業内容調整中<br />
          D ： 継続予定<br />
          E ： 新規<br />
          X ： ドロップ
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped>
@import '@/assets/main.css';
@import '@/views/main/main.css';
</style>
