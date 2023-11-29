<template>
  <div class="login-wrap">
    <el-row type="flex">
      <el-col :span="16">
        <div class="left_content___3vtUv">
        </div>
      </el-col>
      <el-col :span="8">
        <div class="top">
          <div class="headerContent">
            <span class="title">天工开物</span>
          </div>
          <div class="desc">
            一站式测试质量协作平台
          </div>
        </div>
        <div class="main">
          <LoginForm/>
        </div>
        <footer class="ant-layout-footer">
          <div class="ant-pro-global-footer">
            <div class="ant-pro-global-footer-copyright">
              <span class="anticon">
                	&copy;
              </span>
              9999 不知名测试出品
            </div>
          </div>
        </footer>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
  import LoginForm from './components/LoginForm.vue'
</script>
<style lang="scss" scoped>

  .login-wrap {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: auto;
    background: #f8f8f8;
  }
  .left_content___3vtUv {
    height: 100vh;
    background-image: url('@/assets/image/login/side-logo.png');
    background-repeat: no-repeat;
    background-position: 100%;
    background-size: cover;
    box-shadow: 0 0 1px 1px #fff;
  }
  .headerContent {
    height: 44px;
    line-height: 44px
  }
  .top {
    text-align: center;
    margin: 32px 0;
  }
  .title {
    position: relative;
    top: 2px;
    color: rgba(0, 0, 0, .85);
    font-weight: 600;
    font-size: 50px;
    font-family: Avenir, "Helvetica Neue", Arial, Helvetica, sans-serif;
  }
  .desc {
    margin-top: 12px;
    margin-bottom: 40px;
    color: rgba(0, 0, 0, .45);
    font-size: 12px;
  }

  .main {
    width: 328px;
    margin: 0 auto;
  }
  .ant-layout-footer {
    padding: 24px 50px;
    font-size: 13px;
  }

  .ant-pro-global-footer {
    margin: 48px 0 24px;
    padding: 0 16px;
    text-align: center;
  }

  .ant-pro-global-footer-copyright {
    color: rgba(0, 0, 0, .45);
    font-size: 13px;
  }

  .anticon {
    display: inline-block;
    color: inherit;
    font-style: normal;
    line-height: 0;
    text-align: center;
    text-transform: none;
    vertical-align: -.125em;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
</style>
