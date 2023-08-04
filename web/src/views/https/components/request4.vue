<template>
  <div>
    <el-form :model="form" :rules="rules" autoComplete="on" ref="ruleFormRef">
      <el-row :gutter="20">
        <el-col :span="2">
          <el-form-item>
            <el-select @change="checkRequest" placeholder="请求方式"
                       v-model="form.request4"
                       value="">
              <el-option :key="index+''" :label="item.label" :value="item.value"
                         style="font-size: 12px" v-for="(item,index) in request"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="16">
          <el-form-item prop="addr">
            <el-input auto-complete="" placeholder="接口路径，“/”起始"
                      v-model.trim="form.addr"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-button :loading="loadingSend"
                     @click="fastTest(ruleFormRef)"
                     type="primary" icon="Position">Send
          </el-button>
        </el-col>
      </el-row>
      <el-tabs v-model="bodyActiveName" @tab-click="handleClick">
        <el-tab-pane name="1">
          <template #label>
            <span>
              <span>Params<span class='highlight'>({{ paramsCount }})</span></span>
            </span>
          </template>
          <div>
            <el-table
                ref="multipleTableRef"
                :data="form.queryParams"
                :header-cell-style="{background:'#eef1f6',color:'#606266'}" border
                @selection-change="handleSelectionChange"
                highlight-current-row
            >
              <el-table-column label="头部" min-width="5%" type="selection"></el-table-column>
              <el-table-column label="参数名称" min-width="35%" prop="name">
                <template #default="scope">
                  <el-input :value="scope.row.name" placeholder="参数名称"
                            v-model.trim="scope.row.name"/>
                </template>
              </el-table-column>
              <el-table-column label="参数值" min-width="35%" prop="value">
                <template #default="scope">
                  <el-input :value="scope.row.value" placeholder="参数值"
                            v-model.trim="scope.row.value"/>
                </template>
              </el-table-column>
              <el-table-column label="参数描述" min-width="25%" prop="description">
                <template #default="scope">
                  <el-input :value="scope.row.description" placeholder="参数描述"
                            v-model.trim="scope.row.description"/>
                </template>
              </el-table-column>
              <el-table-column label="操作" min-width="10%">
                <template #default="scope">
                  <el-button @click="delParams(scope.$index)" icon="Delete"
                             link></el-button>
                  <el-button @click="addParams"
                             icon="Plus"
                             link
                             v-if="scope.$index===(form.queryParams.length-1)"></el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
        <el-tab-pane name="2">
          <template #label>
            <span>
              <span>Headers<span class='highlight'>({{ headerCount }})</span></span>
            </span>
          </template>
          <div>
            <el-table :data="form.head"
                      :header-cell-style="{background:'#eef1f6',color:'#606266'}" border
                      @selection-change="handleSelectionChange"
                      highlight-current-row
                      ref="multipleTableRef">
              <el-table-column label="头部" min-width="5%" type="selection">
              </el-table-column>
              <el-table-column label="参数名" min-width="20%" prop="name">
                <template #default="scope">
                  <el-select filterable placeholder="head标签"
                             v-model="scope.row.name"
                             value="">
                    <el-option :key="index+''" :label="item.label"
                               :value="item.value"
                               style="font-size: 12px"
                               v-for="(item,index) in header"></el-option>
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column label="参数值" min-width="35%" prop="value">
                <template #default="scope">
                  <el-input :value="scope.row.value" placeholder="参数值"
                            v-model.trim="scope.row.value"/>
                </template>
              </el-table-column>
              <el-table-column label="参数描述" min-width="35%" prop="description">
                <template #default="scope">
                  <el-input :value="scope.row.description" placeholder="参数描述"
                            v-model.trim="scope.row.description"/>
                </template>
              </el-table-column>
              <el-table-column label="操作" min-width="10%">
                <template #default="scope">
                  <el-button @click="delHead(scope.$index)" icon="Delete" link/>
                  <el-button @click="addHead" icon="Plus" link v-if="scope.$index===(form.head.length-1)"/>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
        <el-tab-pane name="3">
          <template #label>
            <span>
              <span>Body</span>
            </span>
          </template>
          <el-radio class="paramsType" label="none" v-model="radio">none</el-radio>
          <el-radio class="paramsType" label="form-data" v-model="radio">form-data</el-radio>
          <el-radio class="paramsType" label="raw" v-model="radio">raw</el-radio>
          <el-button link class="beautify" v-show="radio==='raw'" @click="beautify">Beautify</el-button>
          <div class="request-body-none-wrap" v-show="ParameterType === 1">
            该请求没有 Body 体
          </div>
          <div v-show="ParameterType === 2">
            <div>
              <el-table :data="form.formParams"
                        :header-cell-style="{background:'#eef1f6',color:'#606266'}" border
                        @selection-change="handleSelectionChange"
                        highlight-current-row
                        ref="multipleTableRef">
                <el-table-column label="头部" min-width="5%" type="selection">
                </el-table-column>
                <el-table-column label="参数名" min-width="35%" prop="name">
                  <template #default="scope">
                    <el-input :value="scope.row.name" placeholder="参数名" v-model.trim="scope.row.name"/>
                  </template>
                </el-table-column>
                <el-table-column label="参数值" min-width="35%" prop="value">
                  <template #default="scope">
                    <el-input :value="scope.row.value" placeholder="参数值" v-model.trim="scope.row.value"/>
                  </template>
                </el-table-column>
                <el-table-column label="参数描述" min-width="25%" prop="description">
                  <template #default="scope">
                    <el-input :value="scope.row.description" placeholder="参数描述"
                              v-model.trim="scope.row.description"/>
                  </template>
                </el-table-column>
                <el-table-column label="操作" min-width="10%">
                  <template #default="scope">
                    <el-button @click="delFormParams(scope.$index)" icon="Delete" link/>
                    <el-button @click="addFormParams"
                               icon="Plus"
                               link
                               v-if="scope.$index===(form.formParams.length-1)"/>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
          <div v-show="ParameterType === 3">
            <div>
              <!--                <code-editor :content="codeContent" :language="codeType" class="flow-detail"-->
              <!--                             v-model="form.codeContent">-->
              <!--                </code-editor>-->
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
              <!-- 接口Response返回信息 -->
      <!--        <el-tabs @tab-click="handleClick" v-model="responseActiveName">-->
      <!--          <el-tab-pane label="实时响应" name="1">-->
      <!--            <div class="responseToolBar" v-show="ResponseContent">-->
      <!--              <el-button type="text" size="mini" class="distinct" icon="el-icon-lollipop"></el-button>-->
      <!--              <el-button type="text" size="mini" class="distinct" icon="el-icon-bangzhu"></el-button>-->
      <!--              <el-button type="text" size="mini" class="distinct" icon="el-icon-key"></el-button>-->
      <!--            </div>-->
      <!--            <div class="resultMsg" v-show="statusCode&&resultTimes">-->
      <!--                                <span>Status: <span-->
      <!--                                    :class="statusCode===200? 'green': 'red'">{{ statusCode }}&nbsp&nbsp</span></span>-->
      <!--              <span>Times: <span class="green">{{ resultTimes }}s</span></span>-->
      <!--            </div>-->
      <!--            <div v-show="ResponseContent">-->
      <!--&lt;!&ndash;              <code-mirror :content="ResponseContent" :language="codeType" class="flow-detail">&ndash;&gt;-->
      <!--&lt;!&ndash;              </code-mirror>&ndash;&gt;-->
      <!--            </div>-->
      <!--            <div class="unResponse" v-show="!ResponseContent">-->
      <!--              <div class="raw">Hit Send to get a response</div>-->
      <!--              <img :src="unResponse" alt="" class="gray">-->
      <!--            </div>-->
      <!--          </el-tab-pane>-->
      <!--          <el-tab-pane name="2" v-bind:disabled="resDisable">-->
      <!--            <span slot="label">响应头<span class='highlight'>({{ resHeaderCount }})</span></span>-->
      <!--            <el-table :data="resultHead" border v-if="headerTable">-->
      <!--              <el-table-column label="Key" prop="name"></el-table-column>-->
      <!--              <el-table-column label="Value" prop="value"></el-table-column>-->
      <!--            </el-table>-->
      <!--          </el-tab-pane>-->
      <!--          <el-tab-pane name="3" v-bind:disabled="resDisable">-->
      <!--            <span slot="label">Cookie<span class='highlight'>({{ cookiesCount }})</span></span>-->
      <!--            <el-table :data="resultCookies" border v-if="cookiesTable">-->
      <!--              <el-table-column label="Key" prop="name"></el-table-column>-->
      <!--              <el-table-column label="Value" prop="value"></el-table-column>-->
      <!--            </el-table>-->
      <!--          </el-tab-pane>-->
      <!--        </el-tabs>-->
    </el-form>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive, onMounted, watch} from 'vue'
import {FormInstance, ElTable} from "element-plus";
import type {TabsPaneContext} from 'element-plus'
import unResponse from  '@/assets/image/none-response.jpg'

const multipleTableRef = ref<InstanceType<typeof ElTable>>()

const multipleSelection = ref([])

const ruleFormRef = ref<FormInstance>()

const request3 = ref(true)

const loadingSend = ref(false)

const bodyActiveName = ref("1")

const paramsCount = ref(1)

const headerCount = ref(1)

const radio = ref("none")

const ParameterType = ref(1)

const codeContent = ref("")

const codeType = ref("json")

const responseActiveName = ref("1")

const ResponseContent = ref("")

const resDisable = ref(true)

const resHeaderCount = ref(0)

const resultHead = ref({})

const headerTable = ref(false)

const cookiesCount = ref(0)

const resultCookies = ref({})

const cookiesTable = ref(false)

const statusCode = ref(0)

const resultTimes = ref(0)

const header = ref([
  {value: 'Accept', label: 'Accept'},
  {value: 'Accept-Charset', label: 'Accept-Charset'},
  {value: 'Accept-Encoding', label: 'Accept-Encoding'},
  {value: 'Accept-Language', label: 'Accept-Language'},
  {value: 'Accept-Ranges', label: 'Accept-Ranges'},
  {value: 'Authorization', label: 'Authorization'},
  {value: 'Cache-Control', label: 'Cache-Control'},
  {value: 'Connection', label: 'Connection'},
  {value: 'Cookie', label: 'Cookie'},
  {value: 'Content-Length', label: 'Content-Length'},
  {value: 'Content-Type', label: 'Content-Type'},
  {value: 'Content-MD5', label: 'Content-MD5'},
  {value: 'Date', label: 'Date'},
  {value: 'Expect', label: 'Expect'},
  {value: 'From', label: 'From'},
  {value: 'Host', label: 'Host'},
  {value: 'If-Match', label: 'If-Match'},
  {value: 'If-Modified-Since', label: 'If-Modified-Since'},
  {value: 'If-None-Match', label: 'If-None-Match'},
  {value: 'If-Range', label: 'If-Range'},
  {value: 'If-Unmodified-Since', label: 'If-Unmodified-Since'},
  {value: 'Max-Forwards', label: 'Max-Forwards'},
  {value: 'Origin', label: 'Origin'},
  {value: 'Pragma', label: 'Pragma'},
  {value: 'Proxy-Authorization', label: 'Proxy-Authorization'},
  {value: 'Range', label: 'Range'},
  {value: 'Referer', label: 'Referer'},
  {value: 'TE', label: 'TE'},
  {value: 'Upgrade', label: 'Upgrade'},
  {value: 'User-Agent', label: 'User-Agent'},
  {value: 'Via', label: 'Via'},
  {value: 'Warning', label: 'Warning'}
])

const form = reactive({
  request4: 'POST',
  addr: "",
  queryParams: [{name: "", value: "", description: ""}],
  head: [{name: "", value: "", description: ""}],
  codeContent: "",
  formParams: [{name: "", value: "", description: ""}],
})

const rules = reactive({})

const request = ref([
  {value: 'GET', label: 'GET'},
  {value: 'POST', label: 'POST'},
  {value: 'PUT', label: 'PUT'},
  {value: 'DELETE', label: 'DELETE'}
])

const checkRequest = () => {
  let method = form.request4;
  request3.value = !(method === "GET" || method === "DELETE");
}

const fastTest = (formEl: FormInstance | undefined) => {
}

const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}

const delParams = (index: any) => {
  if (form.queryParams.length !== 1) {
    form.queryParams.splice(index, 1)
  }
  paramsCount.value = form.queryParams.length
}

const addParams = () => {
  let queryParams = {name: "", value: "", description: ""};
  form.queryParams.push(queryParams);
  let rows = [form.queryParams[form.queryParams.length - 1]];
  paramsCount.value = form.queryParams.length
  toggleSelection(rows)
}

const toggleSelection = (rows: any) => {
  rows.forEach((row: any) => {
    multipleTableRef.value!.toggleRowSelection(row, undefined)
  })
}

const handleSelectionChange = (val: any) => {
  console.log("想")
  console.log(val)
  multipleSelection.value = val
}

const delHead = (index: number) => {
  if (form.head.length !== 1) {
    form.head.splice(index, 1)
  }
  headerCount.value = form.head.length
}

const addHead = () => {
  let headers = {name: "", value: "", description: ""};
  form.head.push(headers);
  let rows = [form.head[form.head.length - 1]];
  headerCount.value = form.head.length
  toggleSelection(rows)
}

const beautify = () => {
  form.codeContent = JSON.stringify(eval("(" + form.codeContent + ")"), null, 4)
}

const delFormParams = (index: number) => {
  if (form.formParams.length !== 1) {
    form.formParams.splice(index, 1)
  }
}

const addFormParams = () => {
  let formParams = {name: "", value: "", description: ""};
  form.formParams.push(formParams);
  let rows = [form.formParams[form.formParams.length - 1]];
  toggleSelection(rows)
}

const changeParameterType = () => {
  if (radio.value === 'none') {
     ParameterType.value = 1
  }
  if (radio.value === 'form-data') {
    ParameterType.value = 2
  }
  if (radio.value === 'raw') {
    ParameterType.value = 3
  }
}

onMounted(()=>{
  // toggleSelection(form.head);
  // toggleSelection(form.formParams);
  // toggleSelection(form.queryParams)
})

watch(radio, (newName, oldName) => {
  changeParameterType()
});
</script>

<style scoped lang="scss">
.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}

.parameter-a {
  display: block;
  color: #85ce61;
}

.parameter-b {
  display: none;
}

.code-a {
  float: right;
  display: inline-block;
}

.resultMsg {
  color: #7a8b9a;
  margin-top: 10px;
  margin-right: 20px;
  font-size: 12px;
  position: relative;
  left: 55%;
  margin-bottom: 20px;
}

.unResponse {
  text-align: center;
}

.red {
  color: red;
}

.green {
  color: lightgreen;
}

.el-collapse-item__header {
  flex: 1 0 auto;
  order: -1;
}

.raw {
  color: #C0C0C0 !important;
  font-size: 12px;
}

.gray {
  width: 15%;
  height: 15%;
  filter: Alpha(opacity=10);
  -moz-opacity: .1;
  opacity: 0.1;
}

.beautify {
  float: right;
}

.paramsType {
  color: #C0C0C0;
  margin-bottom: 10px !important;
}

.box-card {
  margin-top: 35px;
}

.el-tabs__item {
  font-size: 12px !important;
}

.request-body-none-wrap {
  padding: 24px;
  text-align: center;
  font-size: 12px;
  color: #C0C0C0;
  border: 1px solid #e6e6e6
}

.highlight {
  color: #34f10a;
}

.flow-detail {
  height: 500px;
}

.responseToolBar {
  background: rgb(238, 241, 246);
  border-radius: 5px;
  width: 130px;
  text-align: center;
  float: left;
}

.documentUrl {
  margin-left: 30px;
  float: left;
  font-size: 12px;
  text-align: center;
  padding-top: 5px;
  font-weight: bold;
  color: #ff4500;
  cursor: pointer;
}

.distinct {
  margin-right: 10px;
}
</style>