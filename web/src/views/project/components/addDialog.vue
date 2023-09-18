<template>
  <el-dialog title="新增项目" :visible.sync="addDialogVisible" center custom-class="proWidth">
    <el-form autoComplete="on" :model="formData" :rules="resetRules" ref="formData"
             size="small"
             label-position="right"
             label-width="100px">
      <el-form-item label="项目名称" :required="true" prop="name">
        <el-input v-model="formData.name"></el-input>
      </el-form-item>
      <el-form-item label="项目类型" :required="true" prop="type">
        <el-select type="type" v-model="formData.type" v-loading="loading"
                   element-loading-spinner="el-icon-loading" clearable filterable>
          <el-option v-for="item in type" :value="item" :key="null" style="font-size: 12px">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="项目描述" :required="true" prop="desc">
        <el-input v-model="formData.desc"></el-input>
      </el-form-item>
    </el-form>
    <div class="pull-right">
      <el-button :loading="loading" type="primary" @click="submitForm('formData')">确 认</el-button>
      <el-button @click="addDialogVisible = false">取 消</el-button>
    </div>
  </el-dialog>
</template>

<script>
import {addProject} from "@/api/api";

export default {
  props: {
    value: {
      type: Boolean,
      default: false
    },
    dialogData: {
      default: null
    }
  },
  data() {
    return {
      type: [
        'Web',
        'App',
        'Pc',
        'MiniProgram'
      ],
      formData: {
        name: '',
        type: '',
        desc: ''
      },
      resetRules: {
        name: [{required: true, trigger: "blur", message: "请输入项目名称！"}],
        type: [{required: true, trigger: "blur", message: "请选择项目类型！"}],
        desc: [{required: true, trigger: "blur", message: "请输入项目描述！"}]
      },
      loading: false,
      title: '',
      addDialogVisible: false,
    }
  },

  watch: {
    value(val) {
      this.addDialogVisible = val;
      this.formData = {...this.dialogData}
    },
    addDialogVisible(val) {
      this.$emit('input', val)
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          addProject({
            name: this.formData.name,
            type: this.formData.type,
            desc: this.formData.desc,
          }).then((response) => {
            console.log(response.data);
            this.addDialogVisible = false;
            this.$parent.queryList()
          }).catch((err) => {
            console.log(err)
            this.$message.error("项目新增失败请重试");
          })
        } else {
          console.log('error submit!!');
          return false
        }
      })
    },
  }
}
</script>

<style lang="scss">
.proWidth {
  width: 30%;
  height: 40%
}

.pull-right {
  float: right;
}
</style>
