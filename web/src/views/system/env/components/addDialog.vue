<template>
  <el-dialog title="新增环境" :visible.sync="addDialogVisible" center custom-class="envWidth">
    <el-form autoComplete="on" :model="formData" :rules="resetRules" ref="formData"
             size="small"
             label-position="right"
             label-width="100px">
      <el-form-item label="环境名称" :required="true" prop="name">
        <el-input v-model="formData.name"></el-input>
      </el-form-item>
      <el-form-item label="环境描述" :required="true" prop="desc">
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
import {addEnv} from "@/api/api";

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
      formData: {
        name: '',
        desc: ''
      },
      resetRules: {
        name: [{required: true, trigger: "blur", message: "请输入环境名称！"}],
        desc: [{required: true, trigger: "blur", message: "请输入环境描述！"}],
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
  created() {
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          addEnv({
            name: this.formData.name,
            desc: this.formData.desc,
          }).then((response) => {
            console.log(response.data);
            this.addDialogVisible = false;
            this.$parent.queryList()
          }).catch((err) => {
            this.$message({message: err.data.non_field_errors[0], type: 'error'})
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
.envWidth {
  width: 30%;
  height: 35%
}

.pull-right {
  float: right;

}
</style>
