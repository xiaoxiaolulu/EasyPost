<template>
  <el-dialog title="修改环境" :visible.sync="editDialogVisible" center custom-class="envWidth">
    <el-form autoComplete="on" :model="formData" :rules="resetRules" ref="formData"
             class="lk-form"
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
      <el-button @click="editDialogVisible = false">取 消</el-button>
    </div>
  </el-dialog>
</template>

<script>
import {updateEnv} from "@/api/api";

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
      editDialogVisible: false,
    }
  },
  watch: {
    value(val) {
      this.editDialogVisible = val;
      this.formData = {
        name: this.$parent.rowData.name,
        desc: this.$parent.rowData.desc
      }
    },
    editDialogVisible(val) {
      this.$emit('input', val)
    }
  },
  created() {
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          updateEnv({
            id: this.$parent.rowData.id,
            name: this.formData.name,
            desc: this.formData.desc,
          }).then((response) => {
            console.log(response.data);
            this.editDialogVisible = false;
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
