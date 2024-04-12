<template>
  <el-dialog title="导入接口"
             v-model="isShow"
             :show-close="false"
             center
             class="importWidth">
    <el-space :size="10">
      <el-check-tag
          class="custom-check-tag"
          v-for="(button, index) in buttons" @change="onChange(button)"
                     :checked="button.checked" :key="index" style="width: 110px;height: 48px;margin-bottom: 10px">
        <i :class="`opblock opblock-${button.style}`"/>
        <span class="content">{{button.content}}</span>
      </el-check-tag>
    </el-space>
    <div class="upload">
      <el-upload
          drag
          ref="uploadRefs"
          action=""
          :auto-upload="false"
          :on-change="handleChange"
          :show-file-list="false"
          v-model:file-list="form.fileList"
          @clearFiles="clearFiles"
      >
        <el-icon v-show="!selectStatus" class="el-icon--upload"><upload-filled /></el-icon>
        <div v-show="!selectStatus" class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <i v-show="selectStatus" style="color: #00a854;text-align:center;margin-top: 50px;"
           class="el-icon-check"></i>
        <div v-show="selectStatus" style="text-align:center;height: 100px;" class="el-upload__text">
          已选择文件：{{selectUpload}}
        </div>
      </el-upload>
    </div>
    <div class="pull-right">
      <el-button type="primary" @click="onSureClick">确 认</el-button>
      <el-button @click="isShow = false">取 消</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import { UploadFilled } from '@element-plus/icons-vue'
import {ref, reactive, computed, watch} from 'vue'
import {ElMessage, UploadInstance} from "element-plus";
import {importApi} from "@/api/http";

const propsCxt: any = null

const emits = defineEmits(['update:modelValue', 'onChangeDialog'])

const props = defineProps({
  modelValue: {
    default: propsCxt,
    type: [Object, Boolean]
  },
  rowData: {
    type: Object,
    default: () => {
    }
  }
})

const buttons = ref([
  {id: 1,  content: 'Swagger', style: 'swagger', checked: true},
  {id: 2, content: 'Postman', style: 'postman', checked: false}
]);


const uploadRefs = ref<UploadInstance>()

const pk = ref();

const selectUpload = ref("")

const selectStatus = ref(false)

const isShow = computed({
  get() {
    return props.modelValue;
  },
  set(val) {
    emits('update:modelValue', val);
  }
});

let form = reactive<any>({
  id: '',
  file: '',
  fileList: []
})

const onChange = (button) => {

  let buttonT = buttons.value.find(item => item.id === button.id);
  let buttonF = buttons.value.filter(item => item.id !== button.id);

  if (buttonT) {
    // 选中的设置为相反值
    buttonT["checked"] = !buttonT["checked"];
  }
  // 未当次选中设置为false, 避免出现多个按钮出现选中状态
  buttonF.forEach(item => {
    item["checked"] = false;
  });
}

const onSureClick = () => {
  try {
    form["id"] = pk.value
    form.file = form.fileList[0].raw
    const ret = importApi(form)
    emits('onChangeDialog', true);
    ElMessage.success("接口导入成功!")
    clearFiles()
  }catch (e) {
    console.log(e)
    console.log('error submit!')
    ElMessage.error("接口导入失败请重试!")
  }
}

const clearFiles = () => {
  form.file = ""
  form.fileList = []
  selectUpload.value = ""
  selectStatus.value = false
  uploadRefs.value?.clearFiles()
}

const handleChange = (rawFile: any) => {
  if (rawFile.raw.type !== 'application/json') {
    ElMessage.error('File must be JSON format!')
    return false
  }
  selectUpload.value = rawFile.raw.name
  selectStatus.value = true
  return true
}


watch(() => props.rowData, () => {
  pk.value = props.rowData.pk
}, {deep: true, immediate: true})
</script>

<style lang="scss">
.importWidth {
  width: 30%;
  height: 55%
}

.pull-right {
  float: right;

}

.upload {
  margin-bottom: 20px;
}

.opblock-swagger {
  background: url('https://cdn.eolink.com/saas_10.9.301/ng14/assets/images/logo/swagger.gif') center no-repeat;
}

.opblock-postman {
  background: url('https://cdn.eolink.com/saas_11.4.35/ng14/assets/images/logo/postman.gif') center no-repeat;
}

.opblock {
  margin-right: -10px;
  border-radius: var(--border-radius);
  display: inline-block;
  background-size: contain;
  height: 30px;
  width: 30px;
  vertical-align: middle;
}

.content {
  margin-left: 15px;
  vertical-align: middle;
}

.custom-check-tag {
  background-color: #ffffff;
  border-style: solid;
  border-color: #f7f2fd;
  border-radius: 8px
}

</style>
