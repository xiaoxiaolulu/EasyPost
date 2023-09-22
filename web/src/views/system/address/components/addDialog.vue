<template>
    <el-dialog title="新增地址" :visible.sync="addDialogVisible" center custom-class="addressWidth">
        <el-form autoComplete="on" :model="formData" :rules="resetRules" ref="formData"
                 size="small"
                 label-position="right"
                 label-width="100px">
            <el-form-item label="环境" :required="true" prop="env">
                <el-select
                        class="selectOpt" v-model="formData.env" placeholder="请选择"
                        size="small"
                        :popper-append-to-body="false"
                        style="width: 150px;"
                >
                    <el-option
                            v-for="item in envOption"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="地址名称" :required="true" prop="name">
                <el-input v-model="formData.name"></el-input>
            </el-form-item>
            <el-form-item label="服务地址" :required="true" prop="host">
                <el-input v-model="formData.host"></el-input>
            </el-form-item>
        </el-form>
        <div class="pull-right">
            <el-button :loading="loading" type="primary" @click="submitForm('formData')">确 认</el-button>
            <el-button @click="addDialogVisible = false">取 消</el-button>
        </div>
    </el-dialog>
</template>

<script>
    import {addAddress, envList} from "@/api/api";

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
                envOption: [],
                formData: {
                    name: '',
                    env: '',
                    host: '',
                },
                resetRules: {
                    name: [{required: true,  message: "请输入地址名称！"}],
                    env: [{required: true,  message: "请选择环境！"}],
                    host: [{required: true,  message: "请输入服务地址！"}],
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
            envList().then((response) => {
                this.envOption = [];
                let envList = response.data.results
                for (let i = 0; i < envList.length; i++) {
                    this.envOption.push({
                        "label": envList[i]["name"],
                        "value": envList[i]["id"]
                    })
                }
                console.log()
            }).catch((error) => {
                console.log(error.response)
                this.$message.error("获取环境列表数据失败;请重试!");
            })
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        addAddress({
                            name: this.formData.name,
                            env: this.formData.env,
                            host: this.formData.host,
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
    .addressWidth {
        width: 30%;
        height: 40%
    }

    .pull-right {
        float: right;
    }
</style>
