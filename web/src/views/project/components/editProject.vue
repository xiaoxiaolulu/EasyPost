<template>
    <div class="app-container">
        <div class="header-container">
            <div class="card-head-title">
                <div class="card-description">
                    <span class="page-header-back-button el-icon-back" @click=""></span>
                    <span class="page-header-heading-title">{{projectName}}</span>
                </div>
            </div>
        </div>
        <div class="container">
            <el-tabs v-model="activeName" @tab-click="">
                <el-tab-pane label="项目设置" name="1">
                    <div style="text-align: center; margin-bottom: 24px; row-gap: 0px;">
                                <span class="avatar project-avatar-image">
<!--                                    <myUpload-->
<!--                                            v-model="show"-->
<!--                                            @crop-success="cropSuccess"-->
<!--                                            @crop-upload-success="cropUploadSuccess"-->
<!--                                            @crop-upload-fail="cropUploadFail"-->
<!--                                            :headers="headers"-->
<!--                                            field="avatar"-->
<!--                                            :url="imgUrl"-->
<!--                                            method="PUT"-->
<!--                                            langType='zh'-->
<!--                                            :noRotate='false'-->
<!--                                    />-->
<!--                                <img v-if="AvatarType" :src="formData.avatar != null ? formData.avatar : Avatar"-->
<!--                                     title="点击上传头像"-->
<!--                                     class="avatar" @click="toggleShow" alt="">-->
<!--                                <img v-if="!AvatarType" :src="imgDataUrl != null ? imgDataUrl : Avatar" class="avatar"-->
<!--                                     @click="toggleShow" alt="">-->
                                </span>
                    </div>
                    <div style="padding-left: 400px">
                        <el-form autoComplete="on" :model="formData" :rules="resetRules" ref="formData"
                                 class="lk-form"
                                 label-position="right"
                                 label-width="100px"
                        >
                            <el-form-item label="项目名称" :required="true" prop="name">
                                <el-input v-model="formData.name" style="width: 350px;"></el-input>
                            </el-form-item>
                            <el-form-item label="项目类型" :required="true" prop="type">
                                <el-select type="type" v-model="formData.type" v-loading="loading"
                                           element-loading-spinner="el-icon-loading" clearable filterable>
                                    <el-option v-for="item in type" :value="item" :key="null" style="font-size: 12px">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="项目描述" :required="true" prop="desc">
                                <el-input v-model="formData.desc" style="width: 350px;"></el-input>
                            </el-form-item>
                        </el-form>
                        <div class="pull-right">
                            <el-button :loading="loading" class="el-icon-receiving" type="primary" @click="submitForm('formData')">确 认</el-button>
                        </div>
                    </div>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script>
    // import {updateProject, projectDetail} from "@/api/api";
    // import myUpload from 'vue-image-crop-upload'
    // import Avatar from '@/assets/images/avatar.png'

    export default {
        // components: {myUpload},
        data() {
            return {
                show: false,
                AvatarType: true,
                imgUrl: null,
                imgDataUrl: null,
                // Avatar: Avatar,
                headers: {
                    // 'Authorization': `JWT ${this.$store.state.userInfo.token}`
                },
                activeName: "1",
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
                projectName: "",
                resetRules: {
                    name: [{required: true, trigger: "blur", message: "请输入项目名称！"}],
                    type: [{required: true, trigger: "blur", message: "请选择项目类型！"}],
                    desc: [{required: true, trigger: "blur", message: "请输入项目描述！"}]
                },
                loading: false,
            }
        },
        mounted() {
            // const pk = this.$route.query.id;
            // projectDetail({id: pk}).then(res => {
            //     const response = res.data;
            //     this.projectName = response.name;
            //     this.formData = {
            //         avatar: response.avatar,
            //         name: response.name,
            //         type: response.type,
            //         desc: response.desc
            //     }
            //     this.imgUrl = process.env.VUE_APP_URL + "/api/project/" + pk + "/";
            // }).catch(res => {
            //     console.log(res);
            // });
        },
        watch: {
            value(val) {
                this.editDialogVisible = val;
                // this.formData = {...this.$parent.rowData}
            },
            editDialogVisible(val) {
                this.$emit('input', val)
            }
        },
        methods: {
            toggleShow() {
                this.show = !this.show
            },
            // cropSuccess(imgDataUrl, field) {
            //     console.log('-------- crop success --------', imgDataUrl, field);
            // },
            // cropUploadSuccess(jsonData, field) {
            //     console.log('-------- upload success --------');
            //     this.imgDataUrl = jsonData.avatar;
            //     this.show = false;
            //     this.AvatarType = false;
            //     console.log('field: ' + field);
            // },
            // cropUploadFail(status, field) {
            //     console.log('-------- upload fail --------');
            //     console.log('field: ' + field);
            // },
            // handleClick(tab, event) {
            //     console.log(tab, event);
            // },
            // goProjectList() {
            //     this.$router.push({
            //         name: "project"
            //     });
            // },
            submitForm(formName) {
                // this.$refs[formName].validate((valid) => {
                //     if (valid) {
                //         updateProject({
                //             id: this.$route.query.id,
                //             name: this.formData.name,
                //             type: this.formData.type,
                //             desc: this.formData.desc,
                //         }).then((response) => {
                //             this.projectName = response.data.name;
                //             console.log(response.data);
                //             this.$message.success("项目编辑成功!");
                //         }).catch((err) => {
                //             console.log(err)
                //             this.$message.error("项目编辑失败请重试!");
                //         })
                //     } else {
                //         console.log('error submit!!');
                //         return false
                //     }
                // })
            },
        }
    }
</script>

<style lang="scss">

    .pull-right {
        float: right;
    }

    .card-head-title {
        border-radius: 4px 4px 0 0;
        min-height: 48px;
    }

    .card-description {
        float: left;
    }

    .page-header-heading-title {
        margin-right: 12px;
        margin-bottom: 0;
        color: rgba(0, 0, 0, .85);
        font-weight: 600;
        font-size: 19px;
        line-height: 32px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis
    }

    .page-header-back-button {
        text-decoration: none;
        outline: none;
        transition: color .3s;
        color: #000;
        cursor: pointer;
        margin-right: 16px;
        font-size: 16px;
        line-height: 1;
    }

    .project-avatar-image {
        background: transparent;
        width: 96px !important;
        height: 96px !important;
        line-height: 48px;
        font-size: 18px;

        img {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }

    .avatar {
        margin: 0;
        padding: 0;
        color: rgba(0, 0, 0, .85);
        font-size: 13px;
        font-variant: tabular-nums;
        line-height: 1.5715;
        list-style: none;
        font-feature-settings: "tnum", "tnum";
        position: relative;
        display: inline-block;
        overflow: hidden;
        color: #fff;
        white-space: nowrap;
        text-align: center;
        vertical-align: middle;
        background: #ccc;
        width: 32px;
        height: 32px;
        line-height: 32px;
        border-radius: 50%
    }
</style>
